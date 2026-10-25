"""Adaptive and Geometry-Aware 3D Clustering Engine for SpatialForge-3D.

Overcomes classic DBSCAN limitations:
1. Range-adaptive epsilon clustering (addresses quadratic LiDAR density drop-off with distance).
2. Geometry-aware metric clustering (incorporating surface normal alignment & curvature).
3. Smoothness-based Region Growing segmentation.
4. Robust HDBSCAN with native pure-Python density MST fallback.
"""
from collections import deque
from typing import Optional, Union
import numpy as np
from scipy.spatial import cKDTree
from sklearn.cluster import DBSCAN, OPTICS, KMeans

from .geometry import estimate_normals, compute_geometric_descriptors


def cluster(
    xyz: np.ndarray,
    method: str = "dbscan",
    eps: float = 0.5,
    min_samples: int = 5,
    n_clusters: int = 2,
    min_cluster_size: int = 10,
    normals: Optional[np.ndarray] = None,
    curvature: Optional[np.ndarray] = None,
    range_adaptive: bool = False,
    normal_weight: float = 0.0,
    sensor_origin: np.ndarray = np.array([0.0, 0.0, 0.0]),
) -> np.ndarray:
    """Unified clustering entrypoint with adaptive and classical methods.
    
    Methods:
    - 'dbscan': Standard scikit-learn DBSCAN
    - 'optics': Scikit-learn OPTICS
    - 'kmeans': Scikit-learn K-Means
    - 'hdbscan': Hierarchical density clustering
    - 'adaptive': Range-adaptive & geometry-aware clustering
    - 'region_growing': Normal-smoothness region growing
    """
    xyz = np.asarray(xyz, dtype=np.float64)
    if len(xyz) == 0:
        return np.array([], dtype=int)

    if method == "dbscan":
        if range_adaptive or normal_weight > 0.0:
            return adaptive_geometry_clustering(
                xyz,
                base_eps=eps,
                min_samples=min_samples,
                normals=normals,
                curvature=curvature,
                normal_weight=normal_weight,
                range_adaptive=range_adaptive,
                sensor_origin=sensor_origin,
            )
        return DBSCAN(eps=eps, min_samples=min_samples).fit_predict(xyz)

    elif method == "optics":
        ms = min(max(min_samples, 2), len(xyz))
        return OPTICS(max_eps=eps, min_samples=ms).fit_predict(xyz)

    elif method == "kmeans":
        k = min(n_clusters, len(xyz))
        return KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(xyz)

    elif method == "hdbscan":
        return hdbscan_clustering(xyz, min_cluster_size=min_cluster_size, min_samples=min_samples)

    elif method == "adaptive":
        return adaptive_geometry_clustering(
            xyz,
            base_eps=eps,
            min_samples=min_samples,
            normals=normals,
            curvature=curvature,
            normal_weight=normal_weight if normal_weight > 0.0 else 0.5,
            range_adaptive=True,
            sensor_origin=sensor_origin,
        )

    elif method == "region_growing":
        return region_growing_segmentation(xyz, normals=normals, curvature=curvature)

    else:
        raise ValueError(f"Unknown clustering method: '{method}'")


def adaptive_geometry_clustering(
    xyz: np.ndarray,
    base_eps: float = 0.5,
    min_samples: int = 5,
    normals: Optional[np.ndarray] = None,
    curvature: Optional[np.ndarray] = None,
    normal_weight: float = 0.5,
    curvature_weight: float = 0.2,
    range_adaptive: bool = True,
    sensor_origin: np.ndarray = np.array([0.0, 0.0, 0.0]),
) -> np.ndarray:
    """Adaptive Geometry-Aware Clustering for 3D Point Clouds.
    
    Key Innovations:
    1. Range-Dependent Adaptive Epsilon:
       Solves LiDAR density decay where point spacing expands with distance r:
       eps(p) = base_eps * (1.0 + alpha * (||p - origin|| / max_range))
    2. Geometry Compatibility Distance:
       Penalizes surface normal misalignment between neighboring points:
       d_geom(p_i, p_j) = ||p_i - p_j||_2 + normal_weight * (1.0 - |n_i . n_j|) + curvature_weight * |k_i - k_j|
    """
    xyz = np.asarray(xyz, dtype=np.float64)
    n = len(xyz)
    if n == 0:
        return np.array([], dtype=int)

    # Estimate normals and curvature if not provided but needed
    if (normal_weight > 0.0 and normals is None) or (curvature_weight > 0.0 and curvature is None):
        if n >= 3:
            normals = estimate_normals(xyz, k=min(16, n), viewpoint=tuple(sensor_origin))
            desc = compute_geometric_descriptors(xyz, k=min(16, n))
            curvature = desc["curvature"]
        else:
            normal_weight = 0.0
            curvature_weight = 0.0

    tree = cKDTree(xyz)

    # Calculate per-point adaptive epsilon
    ranges = np.linalg.norm(xyz - sensor_origin, axis=1)
    max_range = np.max(ranges) if len(ranges) > 0 and np.max(ranges) > 0 else 1.0

    if range_adaptive:
        eps_per_point = base_eps * (1.0 + 1.5 * (ranges / max_range))
    else:
        eps_per_point = np.full(n, base_eps, dtype=np.float64)

    max_search_radius = float(np.max(eps_per_point))

    # Density-based clustering with geometry metric
    labels = np.full(n, -1, dtype=int)
    visited = np.zeros(n, dtype=bool)
    cluster_id = 0

    for i in range(n):
        if visited[i]:
            continue
        visited[i] = True

        eps_i = eps_per_point[i]
        candidate_indices = tree.query_ball_point(xyz[i], r=eps_i)
        
        # Filter candidates using geometry-aware metric
        neighbors = _filter_geometry_neighbors(
            i, candidate_indices, xyz, normals, curvature, eps_i, normal_weight, curvature_weight
        )

        if len(neighbors) < min_samples:
            # Noise point (may later become border point)
            labels[i] = -1
        else:
            # Expand cluster
            labels[i] = cluster_id
            queue = deque(neighbors)
            while queue:
                curr = queue.popleft()
                if not visited[curr]:
                    visited[curr] = True
                    eps_curr = eps_per_point[curr]
                    curr_cands = tree.query_ball_point(xyz[curr], r=eps_curr)
                    curr_neighbors = _filter_geometry_neighbors(
                        curr, curr_cands, xyz, normals, curvature, eps_curr, normal_weight, curvature_weight
                    )
                    if len(curr_neighbors) >= min_samples:
                        queue.extend(curr_neighbors)

                if labels[curr] == -1:
                    labels[curr] = cluster_id

            cluster_id += 1

    return labels


def _filter_geometry_neighbors(
    center_idx: int,
    candidate_indices: list,
    xyz: np.ndarray,
    normals: Optional[np.ndarray],
    curvature: Optional[np.ndarray],
    max_dist: float,
    normal_weight: float,
    curvature_weight: float,
) -> list:
    """Computes combined geometric distance and filters inlier neighbors."""
    if not candidate_indices:
        return []
    
    cand_arr = np.array(candidate_indices, dtype=int)
    p_center = xyz[center_idx]
    cand_pts = xyz[cand_arr]

    euc_dist = np.linalg.norm(cand_pts - p_center, axis=1)

    if normals is not None and normal_weight > 0.0:
        n_center = normals[center_idx]
        cand_normals = normals[cand_arr]
        # Angular divergence: 1 - |dot(n_i, n_j)|
        norm_penalty = 1.0 - np.abs(np.sum(cand_normals * n_center, axis=1))
        euc_dist += normal_weight * norm_penalty

    if curvature is not None and curvature_weight > 0.0:
        k_center = curvature[center_idx]
        cand_k = curvature[cand_arr]
        curv_penalty = np.abs(cand_k - k_center)
        euc_dist += curvature_weight * curv_penalty

    inlier_mask = euc_dist <= max_dist
    return cand_arr[inlier_mask].tolist()


def region_growing_segmentation(
    xyz: np.ndarray,
    normals: Optional[np.ndarray] = None,
    curvature: Optional[np.ndarray] = None,
    smoothness_threshold_deg: float = 15.0,
    curvature_threshold: float = 0.05,
    min_cluster_size: int = 20,
    k_neighbors: int = 16,
) -> np.ndarray:
    """Smoothness-based Region Growing Segmentation for planar and curved surface decomposition."""
    xyz = np.asarray(xyz, dtype=np.float64)
    n = len(xyz)
    if n < min_cluster_size:
        return np.full(n, -1, dtype=int)

    if normals is None or curvature is None:
        normals = estimate_normals(xyz, k=min(k_neighbors, n))
        desc = compute_geometric_descriptors(xyz, k=min(k_neighbors, n))
        curvature = desc["curvature"]

    tree = cKDTree(xyz)
    _, knn_indices = tree.query(xyz, k=min(k_neighbors, n))

    cos_thresh = np.cos(np.radians(smoothness_threshold_deg))

    # Sort seeds by lowest curvature
    point_order = np.argsort(curvature)
    labels = np.full(n, -1, dtype=int)
    in_cluster = np.zeros(n, dtype=bool)
    current_cluster = 0

    for seed in point_order:
        if in_cluster[seed]:
            continue

        cluster_pts = []
        seed_queue = deque([seed])
        in_cluster[seed] = True

        while seed_queue:
            curr = seed_queue.popleft()
            cluster_pts.append(curr)

            # Check neighbors
            for neighbor in knn_indices[curr]:
                if in_cluster[neighbor]:
                    continue

                # Check normal smoothness
                dot_val = np.abs(np.dot(normals[curr], normals[neighbor]))
                if dot_val >= cos_thresh:
                    in_cluster[neighbor] = True
                    # If neighbor also has low curvature, it can be a seed
                    if curvature[neighbor] <= curvature_threshold:
                        seed_queue.append(neighbor)
                    else:
                        cluster_pts.append(neighbor)

        if len(cluster_pts) >= min_cluster_size:
            labels[cluster_pts] = current_cluster
            current_cluster += 1
        else:
            # Mark unassigned
            for pt in cluster_pts:
                in_cluster[pt] = False

    return labels


def hdbscan_clustering(
    xyz: np.ndarray,
    min_cluster_size: int = 10,
    min_samples: int = 5,
) -> np.ndarray:
    """HDBSCAN clustering with optional library import and native SciPy density fallback."""
    try:
        import hdbscan
        return hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples).fit_predict(xyz)
    except ImportError:
        # High-performance native fallback: core distance MST clustering
        return _native_density_mst_clustering(xyz, min_cluster_size=min_cluster_size, min_samples=min_samples)


def _native_density_mst_clustering(xyz: np.ndarray, min_cluster_size: int = 10, min_samples: int = 5) -> np.ndarray:
    """Self-contained density-based hierarchical clusterer (HDBSCAN-like) using SciPy minimum spanning tree."""
    from scipy.sparse.csgraph import minimum_spanning_tree
    from scipy.spatial.distance import pdist, squareform

    n = len(xyz)
    if n < min_cluster_size:
        return np.full(n, -1, dtype=int)

    # Core distance: distance to k-th nearest neighbor
    tree = cKDTree(xyz)
    k_eff = min(max(min_samples, 2), n)
    dists, _ = tree.query(xyz, k=k_eff)
    core_dists = dists[:, -1]

    # Mutual reachability distance: d_mreach(a, b) = max(core(a), core(b), d(a, b))
    # For large clouds, subsample or use DBSCAN fallback
    if n > 2000:
        return DBSCAN(eps=np.median(core_dists) * 1.5, min_samples=min_samples).fit_predict(xyz)

    condensed = pdist(xyz)
    dist_mat = squareform(condensed)
    mreach = np.maximum(np.maximum(core_dists[:, None], core_dists[None, :]), dist_mat)

    mst = minimum_spanning_tree(mreach).toarray()
    mst_edges = np.argwhere(mst > 0)
    edge_weights = mst[mst_edges[:, 0], mst_edges[:, 1]]

    # Cut edges at density threshold
    threshold = np.percentile(edge_weights, 85)
    from scipy.sparse import csgraph
    adj = (mst > 0) & (mst <= threshold)
    adj = adj | adj.T
    n_components, comp_labels = csgraph.connected_components(adj, directed=False)

    # Filter clusters smaller than min_cluster_size
    counts = np.bincount(comp_labels)
    valid_clusters = {c: i for i, c in enumerate(np.where(counts >= min_cluster_size)[0])}

    final_labels = np.full(n, -1, dtype=int)
    for i, c in enumerate(comp_labels):
        if c in valid_clusters:
            final_labels[i] = valid_clusters[c]

    return final_labels
