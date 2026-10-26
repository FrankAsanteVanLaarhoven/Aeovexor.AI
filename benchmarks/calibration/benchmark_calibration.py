"""
Multi-Sensor Calibration Benchmark Suite
Evaluates Camera-LiDAR extrinsic calibration accuracy, reprojection RMSE (pixels),
and angular rotation errors against known checkerboard/target ground truth.
"""

from typing import Dict, Any, List
import numpy as np


class CalibrationBenchmark:
    def __init__(self, camera_matrix: np.ndarray = None):
        # Default pinhole camera intrinsics
        self.camera_matrix = camera_matrix or np.array([
            [721.5, 0.0, 609.5],
            [0.0, 721.5, 172.8],
            [0.0, 0.0, 1.0],
        ])

    def evaluate_extrinsic_reprojection(
        self,
        lidar_points_3d: np.ndarray,
        measured_2d_pixels: np.ndarray,
        extrinsic_r: np.ndarray,
        extrinsic_t: np.ndarray,
    ) -> Dict[str, Any]:
        """
        Projects 3D LiDAR points into 2D camera coordinates and calculates RMSE (pixels).
        P_cam = R * P_lidar + T
        P_img = K * P_cam
        """
        if len(lidar_points_3d) == 0 or len(measured_2d_pixels) == 0:
            return {"reprojection_rmse_px": 0.0, "max_pixel_error": 0.0}

        # Transform to camera frame
        pts_cam = (extrinsic_r @ lidar_points_3d.T).T + extrinsic_t
        # Filter points in front of camera (z > 0.1)
        valid_z = pts_cam[:, 2] > 0.1
        pts_cam = pts_cam[valid_z]
        target_pixels = measured_2d_pixels[valid_z]

        # Project to image plane
        u = (self.camera_matrix[0, 0] * pts_cam[:, 0] / pts_cam[:, 2]) + self.camera_matrix[0, 2]
        v = (self.camera_matrix[1, 1] * pts_cam[:, 1] / pts_cam[:, 2]) + self.camera_matrix[1, 2]
        projected = np.stack([u, v], axis=1)

        errors = np.linalg.norm(projected - target_pixels, axis=1)
        rmse = float(np.sqrt(np.mean(errors**2)))
        max_err = float(np.max(errors))

        return {
            "reprojection_rmse_px": round(rmse, 3),
            "max_pixel_error": round(max_err, 3),
            "valid_points_evaluated": int(np.sum(valid_z)),
        }
