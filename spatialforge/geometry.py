"""Advanced 3D Geometry and Feature Engine for SpatialForge-3D.

Includes:
- Centroid & feature-preserving voxel grid downsampling
- Statistical Outlier Removal (SOR) & Radius Outlier Removal (ROR)
- High-throughput VoxelHashGrid spatial index
- Robust normal estimation with viewpoint orientation
- Multi-scale PCA geometric descriptors (curvature, linearity, planarity, scattering,
  omnivariance, anisotropy, eigenentropy, surface variation)
- RANSAC 3D plane fitting & autonomous robot ground extraction
"""
from typing import Dict, List, Optional, Tuple, Union
import numpy as np
from scipy.spatial import cKDTree


def voxel_downsample(
    xyz: np.ndarray,
    step: float,
    features: Optional[np.ndarray] = None,
) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
    """Downsamples point cloud using a 3D regular voxel grid with centroid averaging.
    
    If features (N, D) are provided, computes the mean feature vector per voxel.
    """
    if step <= 0:
        raise ValueError("Voxel step must be > 0")
    xyz = np.asarray(xyz, dtype=np.float64)
    if len(xyz) == 0:
        return (np.empty((0, 3)), np.empty((0, features.shape[1]))) if features is not None else np.empty((0, 3))

    voxel_coords = np.floor(xyz / step).astype(np.int64)
    _, inv = np.unique(voxel_coords, axis=0, return_inverse=True)
    n_voxels = inv.max() + 1

    sums = np.zeros((n_voxels, 3), dtype=np.float64)
    np.add.at(sums, inv, xyz)
    counts = np.bincount(inv)[:, None]
    downsampled_xyz = sums / counts

    if features is not None:
        feat = np.asarray(features)
        f_sums = np.zeros((n_voxels, feat.shape[1]), dtype=feat.dtype)
        np.add.at(f_sums, inv, feat)
        downsampled_feat = f_sums / counts
        return downsampled_xyz, downsampled_feat

    return downsampled_xyz


def statistical_outlier_removal(
    xyz: np.ndarray,
    k: int = 16,
    std_ratio: float = 2.0,
) -> Tuple[np.ndarray, np.ndarray]:
    """Filters noisy points by analyzing average distance to k nearest neighbors.
    
    Returns (inlier_mask, mean_distances).
    """
    xyz = np.asarray(xyz, dtype=np.float64)
    if len(xyz) < k:
        return np.ones(len(xyz), dtype=bool), np.zeros(len(xyz))

    tree = cKDTree(xyz)
    distances, _ = tree.query(xyz, k=k + 1)
    mean_dist = np.mean(distances[:, 1:], axis=1)

    global_mean = np.mean(mean_dist)
    global_std = np.std(mean_dist)
    threshold = global_mean + std_ratio * global_std

    inlier_mask = mean_dist <= threshold
    return inlier_mask, mean_dist


def radius_outlier_removal(
    xyz: np.ndarray,
    radius: float = 0.5,
    min_neighbors: int = 5,
) -> np.ndarray:
    """Removes points that have fewer than min_neighbors within the given sphere radius."""
    xyz = np.asarray(xyz, dtype=np.float64)
    if len(xyz) == 0:
        return np.empty(0, dtype=bool)

    tree = cKDTree(xyz)
    counts = tree.query_ball_point(xyz, r=radius, return_length=True)
    return np.asarray(counts) >= min_neighbors


class VoxelHashGrid:
    """Spatial hash index for O(1) neighborhood and voxel queries.
    
    Ideal for real-time streaming LiDAR odometry and TSDF mapping.
    """

    def __init__(self, voxel_size: float):
        if voxel_size <= 0:
            raise ValueError("Voxel size must be > 0")
        self.voxel_size = float(voxel_size)
        self.grid: Dict[Tuple[int, int, int], List[int]] = {}

    def insert(self, xyz: np.ndarray) -> None:
        coords = np.floor(xyz / self.voxel_size).astype(np.int64)
        for i, (vx, vy, vz) in enumerate(coords):
            key = (int(vx), int(vy), int(vz))
            if key not in self.grid:
                self.grid[key] = []
            self.grid[key].append(i)

    def query_radius(self, point: np.ndarray, radius: float, xyz: np.ndarray) -> List[int]:
        r_vox = int(np.ceil(radius / self.voxel_size))
        center_vox = np.floor(point / self.voxel_size).astype(np.int64)
        cx, cy, cz = int(center_vox[0]), int(center_vox[1]), int(center_vox[2])
        r2 = radius * radius

        candidates = []
        for dx in range(-r_vox, r_vox + 1):
            for dy in range(-r_vox, r_vox + 1):
                for dz in range(-r_vox, r_vox + 1):
                    key = (cx + dx, cy + dy, cz + dz)
                    if key in self.grid:
                        candidates.extend(self.grid[key])

        if not candidates:
            return []

        cand_pts = xyz[candidates]
        d2 = np.sum((cand_pts - point) ** 2, axis=1)
        inliers = [candidates[i] for i, val in enumerate(d2) if val <= r2]
        return inliers


def compute_covariances(xyz: np.ndarray, k: int = 16) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Computes local covariance matrices and their sorted eigenvalues and eigenvectors.
    
    Returns (covariances: (N, 3, 3), eigenvalues: (N, 3), eigenvectors: (N, 3, 3))
    where eigenvalues are sorted in ascending order: lambda_0 <= lambda_1 <= lambda_2.
    """
    xyz = np.asarray(xyz, dtype=np.float64)
    n = len(xyz)
    if n < 3:
        raise ValueError("Need >= 3 points to compute covariances")

    k_eff = min(max(k, 3), n)
    tree = cKDTree(xyz)
    _, idx = tree.query(xyz, k=k_eff)

    neighbors = xyz[idx]  # (N, K, 3)
    centered = neighbors - neighbors.mean(axis=1, keepdims=True)

    # Covariance per point
    cov = np.einsum("nki,nkj->nij", centered, centered) / k_eff
    # Add tiny regularizer for numerical stability
    cov += np.eye(3)[None, :, :] * 1e-12

    evals, evecs = np.linalg.eigh(cov)
    return cov, evals, evecs


def estimate_normals(
    xyz: np.ndarray,
    k: int = 16,
    viewpoint: Tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> np.ndarray:
    """Estimates surface normals via PCA with consistent orientation towards sensor viewpoint."""
    xyz = np.asarray(xyz, dtype=np.float64)
    _, _, evecs = compute_covariances(xyz, k=k)
    # The normal corresponds to the eigenvector of the smallest eigenvalue (index 0)
    normals = evecs[:, :, 0]

    # Reorient towards sensor viewpoint: (p - viewpoint) . normal < 0
    vp = np.asarray(viewpoint, dtype=np.float64)
    dir_to_vp = vp - xyz
    dots = np.sum(normals * dir_to_vp, axis=1)
    flip_mask = dots < 0
    normals[flip_mask] *= -1.0

    return normals


def compute_geometric_descriptors(xyz: np.ndarray, k: int = 16) -> Dict[str, np.ndarray]:
    """Computes full set of 3D geometric descriptors from covariance eigenvalues.
    
    Descriptors:
    - Curvature: lambda_0 / (lambda_0 + lambda_1 + lambda_2)
    - Linearity: (lambda_2 - lambda_1) / lambda_2
    - Planarity: (lambda_1 - lambda_0) / lambda_2
    - Scattering (sphericity): lambda_0 / lambda_2
    - Omnivariance: (lambda_0 * lambda_1 * lambda_2)**(1/3)
    - Anisotropy: (lambda_2 - lambda_0) / lambda_2
    - Eigenentropy: -sum(lambda_i * ln(lambda_i))
    - Surface variation: lambda_0 / sum(lambda_i)
    """
    _, evals, _ = compute_covariances(xyz, k=k)
    l0 = evals[:, 0]
    l1 = evals[:, 1]
    l2 = evals[:, 2]

    l_sum = np.maximum(l0 + l1 + l2, 1e-12)
    l2_safe = np.maximum(l2, 1e-12)

    # Normalized eigenvalues for entropy
    p0 = l0 / l_sum
    p1 = l1 / l_sum
    p2 = l2 / l_sum
    entropy = -(p0 * np.log(np.maximum(p0, 1e-12)) + p1 * np.log(np.maximum(p1, 1e-12)) + p2 * np.log(np.maximum(p2, 1e-12)))

    return {
        "curvature": l0 / l_sum,
        "linearity": (l2 - l1) / l2_safe,
        "planarity": (l1 - l0) / l2_safe,
        "scattering": l0 / l2_safe,
        "omnivariance": np.maximum(l0 * l1 * l2, 1e-18) ** (1.0 / 3.0),
        "anisotropy": (l2 - l0) / l2_safe,
        "eigenentropy": entropy,
        "surface_variation": l0 / l_sum,
    }


def compute_multiscale_features(xyz: np.ndarray, scales: List[int] = [8, 16, 32]) -> np.ndarray:
    """Computes multi-scale geometric feature representation.
    
    Concatenates curvature, linearity, planarity, and scattering across multiple scales.
    Returns feature matrix of shape (N, len(scales) * 4).
    """
    xyz = np.asarray(xyz, dtype=np.float64)
    all_features = []
    for s in scales:
        desc = compute_geometric_descriptors(xyz, k=s)
        feat_stack = np.column_stack([desc["curvature"], desc["linearity"], desc["planarity"], desc["scattering"]])
        all_features.append(feat_stack)
    return np.hstack(all_features)


def ransac_plane(
    xyz: np.ndarray,
    distance_threshold: float = 0.05,
    max_iterations: int = 500,
    probability: float = 0.99,
) -> Tuple[np.ndarray, np.ndarray]:
    """Robust RANSAC 3D plane fitting.
    
    Returns:
    - plane_equation: (a, b, c, d) where ax + by + cz + d = 0, normalized such that ||(a, b, c)|| = 1
    - inlier_mask: boolean array (N,) indicating points belonging to the plane
    """
    xyz = np.asarray(xyz, dtype=np.float64)
    n = len(xyz)
    if n < 3:
        raise ValueError("Need >= 3 points for plane fitting")

    best_inliers = np.zeros(n, dtype=bool)
    best_plane = np.array([0.0, 0.0, 1.0, 0.0])
    max_inlier_count = 0

    rng = np.random.default_rng(42)

    for it in range(max_iterations):
        sample_idx = rng.choice(n, size=3, replace=False)
        p1, p2, p3 = xyz[sample_idx]

        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2)
        norm_len = np.linalg.norm(normal)
        if norm_len < 1e-8:
            continue

        normal /= norm_len
        d = -np.dot(normal, p1)

        # Distance of all points to plane: |ax + by + cz + d|
        distances = np.abs(np.dot(xyz, normal) + d)
        inliers = distances <= distance_threshold
        inlier_count = np.sum(inliers)

        if inlier_count > max_inlier_count:
            max_inlier_count = inlier_count
            best_inliers = inliers
            best_plane = np.append(normal, d)

            # Adaptive stopping criterion
            w = inlier_count / n
            if w > 0:
                p_no_outliers = 1.0 - (w ** 3)
                p_no_outliers = max(min(p_no_outliers, 1.0 - 1e-8), 1e-8)
                adaptive_iters = int(np.log(1.0 - probability) / np.log(p_no_outliers))
                if it >= adaptive_iters and it >= 50:
                    break

    # Refit plane on all inliers if sufficient
    if max_inlier_count >= 3:
        inlier_pts = xyz[best_inliers]
        center = inlier_pts.mean(axis=0)
        u, s, vh = np.linalg.svd(inlier_pts - center)
        refit_normal = vh[2]
        refit_d = -np.dot(refit_normal, center)
        best_plane = np.append(refit_normal, refit_d)
        best_inliers = np.abs(np.dot(xyz, refit_normal) + refit_d) <= distance_threshold

    return best_plane, best_inliers


def extract_ground_plane(
    xyz: np.ndarray,
    distance_threshold: float = 0.15,
    max_slope_deg: float = 15.0,
    expected_up: Tuple[float, float, float] = (0.0, 0.0, 1.0),
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Isolates the ground plane and separates obstacles for robotics navigation.
    
    Returns (ground_mask, obstacle_mask, plane_model).
    """
    xyz = np.asarray(xyz, dtype=np.float64)
    up = np.asarray(expected_up, dtype=np.float64)
    up /= np.linalg.norm(up)

    plane, inliers = ransac_plane(xyz, distance_threshold=distance_threshold)
    normal = plane[:3]

    # Verify normal is roughly aligned with gravity/up vector
    cos_angle = np.abs(np.dot(normal, up))
    angle_deg = np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))

    if angle_deg > max_slope_deg:
        # Not a valid horizontal ground plane
        return np.zeros(len(xyz), dtype=bool), np.ones(len(xyz), dtype=bool), plane

    ground_mask = inliers
    obstacle_mask = ~inliers
    return ground_mask, obstacle_mask, plane
