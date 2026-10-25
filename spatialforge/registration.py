"""Robust Point Cloud Registration Engine for SpatialForge-3D.

Includes:
- Robust Point-to-Point ICP with outlier distance rejection
- Point-to-Plane ICP with linearized normal constraints & Huber loss
- Generalized ICP (GICP) modeling anisotropic surface covariances
- Global descriptor-based RANSAC initial alignment
"""
from typing import Dict, Optional, Tuple, Union
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation

from .geometry import compute_covariances, compute_multiscale_features, estimate_normals


def icp(
    src: np.ndarray,
    dst: np.ndarray,
    method: str = "point_to_plane",
    max_distance: float = 1.0,
    max_iterations: int = 50,
    tolerance: float = 1e-6,
    src_normals: Optional[np.ndarray] = None,
    dst_normals: Optional[np.ndarray] = None,
    src_covariances: Optional[np.ndarray] = None,
    dst_covariances: Optional[np.ndarray] = None,
    initial_transform: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, Dict[str, Union[float, int]]]:
    """Unified registration entrypoint for SpatialForge-3D.
    
    Methods:
    - 'point_to_point': Classical Besl & McKay SVD ICP
    - 'point_to_plane': Chen & Medioni linearized normal constraint with Huber loss
    - 'gicp': Generalized ICP (Segal et al.) with local surface covariance weighting
    """
    src = np.asarray(src, dtype=np.float64)
    dst = np.asarray(dst, dtype=np.float64)
    if min(len(src), len(dst)) < 3:
        raise ValueError("Both source and destination must have >= 3 points")

    if method == "point_to_point":
        return icp_point_to_point(
            src, dst, max_distance=max_distance, max_iterations=max_iterations,
            tolerance=tolerance, initial_transform=initial_transform
        )
    elif method == "point_to_plane":
        return icp_point_to_plane(
            src, dst, dst_normals=dst_normals, max_distance=max_distance,
            max_iterations=max_iterations, tolerance=tolerance, initial_transform=initial_transform
        )
    elif method == "gicp":
        return gicp_registration(
            src, dst, src_covariances=src_covariances, dst_covariances=dst_covariances,
            max_distance=max_distance, max_iterations=max_iterations, tolerance=tolerance,
            initial_transform=initial_transform
        )
    else:
        raise ValueError(f"Unknown registration method: '{method}'")


def icp_point_to_point(
    src: np.ndarray,
    dst: np.ndarray,
    max_distance: float = 1.0,
    max_iterations: int = 50,
    tolerance: float = 1e-6,
    initial_transform: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, Dict[str, Union[float, int]]]:
    """Closed-form SVD Point-to-Point ICP."""
    T = np.eye(4) if initial_transform is None else np.asarray(initial_transform, dtype=np.float64).copy()
    tree = cKDTree(dst)
    prev_rmse = float("inf")
    n_src = len(src)
    inlier_count = 0

    for it in range(max_iterations):
        moved = (src @ T[:3, :3].T) + T[:3, 3]
        dists, idx = tree.query(moved)
        mask = dists <= max_distance
        inlier_count = int(mask.sum())

        if inlier_count < 3:
            break

        p_in = moved[mask]
        q_in = dst[idx[mask]]

        p_center = p_in.mean(axis=0)
        q_center = q_in.mean(axis=0)

        # Cross-covariance
        H = (p_in - p_center).T @ (q_in - q_center)
        u, _, vt = np.linalg.svd(H)
        R_delta = vt.T @ u.T
        if np.linalg.det(R_delta) < 0:
            vt[-1] *= -1.0
            R_delta = vt.T @ u.T

        t_delta = q_center - (R_delta @ p_center)

        delta = np.eye(4)
        delta[:3, :3] = R_delta
        delta[:3, 3] = t_delta
        T = delta @ T

        curr_rmse = float(np.sqrt(np.mean(np.sum(((p_in @ R_delta.T) + t_delta - q_in) ** 2, axis=1))))
        if abs(prev_rmse - curr_rmse) < tolerance:
            prev_rmse = curr_rmse
            break
        prev_rmse = curr_rmse

    return T, {
        "inlier_rmse_m": float(prev_rmse),
        "fitness": float(inlier_count / n_src),
        "inlier_count": int(inlier_count),
        "iterations": int(it + 1),
    }


def icp_point_to_plane(
    src: np.ndarray,
    dst: np.ndarray,
    dst_normals: Optional[np.ndarray] = None,
    max_distance: float = 1.0,
    max_iterations: int = 50,
    tolerance: float = 1e-6,
    huber_delta: float = 0.1,
    initial_transform: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, Dict[str, Union[float, int]]]:
    """Linearized Point-to-Plane ICP with robust Huber M-estimator.
    
    Solves (p x n_q)^T alpha + n_q^T t = (q - p)^T n_q per iteration.
    Significantly faster convergence and lower drift on LiDAR scans with planes/ground/walls.
    """
    if dst_normals is None:
        dst_normals = estimate_normals(dst, k=min(16, len(dst)))

    T = np.eye(4) if initial_transform is None else np.asarray(initial_transform, dtype=np.float64).copy()
    tree = cKDTree(dst)
    prev_rmse = float("inf")
    n_src = len(src)
    inlier_count = 0

    for it in range(max_iterations):
        moved = (src @ T[:3, :3].T) + T[:3, 3]
        dists, idx = tree.query(moved)
        mask = dists <= max_distance
        inlier_count = int(mask.sum())

        if inlier_count < 6:
            # Need at least 6 points for 6-DoF linear solve
            return icp_point_to_point(src, dst, max_distance=max_distance, max_iterations=max_iterations, initial_transform=T)

        p = moved[mask]
        q = dst[idx[mask]]
        n = dst_normals[idx[mask]]

        # Residuals r_i = (q_i - p_i) . n_i
        residuals = np.sum((q - p) * n, axis=1)

        # Huber weighting
        abs_r = np.abs(residuals)
        weights = np.where(abs_r <= huber_delta, 1.0, huber_delta / np.maximum(abs_r, 1e-12))
        sqrt_w = np.sqrt(weights)[:, None]

        # Cross product p x n
        cross = np.cross(p, n)
        # J_i = [p x n | n] (6 parameters: alpha, beta, gamma, tx, ty, tz)
        J = np.hstack([cross, n]) * sqrt_w
        b = residuals * sqrt_w[:, 0]

        # Solve normal equations: (J^T J) xi = J^T b
        try:
            xi, _, _, _ = np.linalg.lstsq(J.T @ J + np.eye(6) * 1e-8, J.T @ b, rcond=None)
        except np.linalg.LinAlgError:
            break

        # Small angle rotation vector xi[:3] and translation xi[3:]
        rot_vec = xi[:3]
        trans_vec = xi[3:]
        R_delta = Rotation.from_rotvec(rot_vec).as_matrix()

        delta = np.eye(4)
        delta[:3, :3] = R_delta
        delta[:3, 3] = trans_vec
        T = delta @ T

        curr_rmse = float(np.sqrt(np.mean(residuals ** 2)))
        if abs(prev_rmse - curr_rmse) < tolerance:
            prev_rmse = curr_rmse
            break
        prev_rmse = curr_rmse

    return T, {
        "inlier_rmse_m": float(prev_rmse),
        "fitness": float(inlier_count / n_src),
        "inlier_count": int(inlier_count),
        "iterations": int(it + 1),
    }


def gicp_registration(
    src: np.ndarray,
    dst: np.ndarray,
    src_covariances: Optional[np.ndarray] = None,
    dst_covariances: Optional[np.ndarray] = None,
    max_distance: float = 1.0,
    max_iterations: int = 40,
    tolerance: float = 1e-6,
    initial_transform: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, Dict[str, Union[float, int]]]:
    """Generalized ICP (GICP) incorporating full 3D surface covariances.
    
    Models error distribution as e_i ~ N(0, C_B + R C_A R^T).
    """
    if src_covariances is None:
        src_covariances, _, _ = compute_covariances(src, k=min(16, len(src)))
    if dst_covariances is None:
        dst_covariances, _, _ = compute_covariances(dst, k=min(16, len(dst)))

    # Regularize covariances for planar surface assumption (Segal et al.)
    # Replace smallest eigenvalue with epsilon, keep others
    def regularize_cov(cov_mats):
        evals, evecs = np.linalg.eigh(cov_mats)
        evals[:, 0] = 1e-3  # thickness along surface normal
        evals[:, 1] = 1.0
        evals[:, 2] = 1.0
        return np.einsum("nij,nj,nkj->nik", evecs, evals, evecs)

    C_A = regularize_cov(src_covariances)
    C_B = regularize_cov(dst_covariances)

    T = np.eye(4) if initial_transform is None else np.asarray(initial_transform, dtype=np.float64).copy()
    tree = cKDTree(dst)
    prev_rmse = float("inf")
    n_src = len(src)
    inlier_count = 0

    for it in range(max_iterations):
        R = T[:3, :3]
        t = T[:3, 3]
        moved = (src @ R.T) + t
        dists, idx = tree.query(moved)
        mask = dists <= max_distance
        inlier_count = int(mask.sum())

        if inlier_count < 6:
            break

        p = moved[mask]
        q = dst[idx[mask]]
        cA_in = C_A[mask]
        cB_in = C_B[idx[mask]]

        # Sigma_i = C_B_i + R C_A_i R^T
        R_cA_RT = np.einsum("ij,njk,lk->nil", R, cA_in, R)
        sigma = cB_in + R_cA_RT

        # Mahalanobis distance weights
        diff = q - p
        try:
            sigma_inv = np.linalg.inv(sigma)
        except np.linalg.LinAlgError:
            sigma_inv = np.linalg.pinv(sigma)

        # Weighted least squares update
        w_d = np.einsum("ni,nij->nj", diff, sigma_inv)
        w_norm = np.linalg.norm(w_d, axis=1, keepdims=True)
        weights = 1.0 / np.maximum(w_norm, 1e-6)

        # Solve SVD on weighted correspondences
        p_c = np.sum(p * weights, axis=0) / np.sum(weights)
        q_c = np.sum(q * weights, axis=0) / np.sum(weights)

        H = ((p - p_c) * weights).T @ (q - q_c)
        u, _, vt = np.linalg.svd(H)
        R_delta = vt.T @ u.T
        if np.linalg.det(R_delta) < 0:
            vt[-1] *= -1.0
            R_delta = vt.T @ u.T
        t_delta = q_c - (R_delta @ p_c)

        delta = np.eye(4)
        delta[:3, :3] = R_delta
        delta[:3, 3] = t_delta
        T = delta @ T

        curr_rmse = float(np.sqrt(np.mean(np.sum((p @ R_delta.T + t_delta - q) ** 2, axis=1))))
        if abs(prev_rmse - curr_rmse) < tolerance:
            prev_rmse = curr_rmse
            break
        prev_rmse = curr_rmse

    return T, {
        "inlier_rmse_m": float(prev_rmse),
        "fitness": float(inlier_count / n_src),
        "inlier_count": int(inlier_count),
        "iterations": int(it + 1),
    }


def global_registration_ransac(
    src: np.ndarray,
    dst: np.ndarray,
    distance_threshold: float = 0.5,
    max_iterations: int = 1000,
    scales: list = [8, 16, 32],
) -> Tuple[np.ndarray, Dict[str, Union[float, int]]]:
    """Coarse Global Alignment using multi-scale geometric feature matching and RANSAC."""
    src_feat = compute_multiscale_features(src, scales=scales)
    dst_feat = compute_multiscale_features(dst, scales=scales)

    feat_tree = cKDTree(dst_feat)
    _, matches = feat_tree.query(src_feat)

    n_src = len(src)
    best_T = np.eye(4)
    best_inliers = 0
    dst_tree = cKDTree(dst)
    rng = np.random.default_rng(42)

    for _ in range(max_iterations):
        sample_idx = rng.choice(n_src, size=3, replace=False)
        src_samp = src[sample_idx]
        dst_samp = dst[matches[sample_idx]]

        # Compute rigid transform from 3 points
        sc = src_samp.mean(axis=0)
        dc = dst_samp.mean(axis=0)
        u, _, vt = np.linalg.svd((src_samp - sc).T @ (dst_samp - dc))
        R = vt.T @ u.T
        if np.linalg.det(R) < 0:
            vt[-1] *= -1.0
            R = vt.T @ u.T
        t = dc - R @ sc

        moved = (src @ R.T) + t
        dists, _ = dst_tree.query(moved)
        inliers = int((dists <= distance_threshold).sum())

        if inliers > best_inliers:
            best_inliers = inliers
            best_T[:3, :3] = R
            best_T[:3, 3] = t

    return best_T, {
        "inlier_count": best_inliers,
        "fitness": float(best_inliers / n_src),
    }
