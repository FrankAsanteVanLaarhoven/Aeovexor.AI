"""Real-time Sequential LiDAR Odometry and Mapping Engine for SpatialForge-3D.

Inspired by KISS-ICP and FAST-LIO2 principles:
- Constant velocity motion prediction
- Adaptive voxel grid local map representation
- Point-to-plane scan-to-map registration with dynamic thresholding
- Cumulative map creation and drift-resilient trajectory tracking
"""
from typing import Dict, List, Optional, Tuple, Union
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation

from .geometry import estimate_normals, voxel_downsample
from .registration import icp_point_to_plane


class LiDAROdometry:
    """Sequential LiDAR Odometry & Local Mapping.
    
    Tracks sensor trajectory from continuous point cloud streams
    (e.g., KITTI Velodyne, Waymo, Ouster, Hesai, or ROS2 PointCloud2).
    """

    def __init__(
        self,
        voxel_size: float = 0.4,
        max_range: float = 80.0,
        min_range: float = 1.0,
        max_submap_points: int = 50000,
        max_iterations: int = 30,
    ):
        self.voxel_size = float(voxel_size)
        self.max_range = float(max_range)
        self.min_range = float(min_range)
        self.max_submap_points = int(max_submap_points)
        self.max_iterations = int(max_iterations)

        self.poses: List[np.ndarray] = []
        self.timestamps: List[int] = []
        self.submap_points: Optional[np.ndarray] = None
        self.submap_normals: Optional[np.ndarray] = None
        self.last_delta: np.eye = np.eye(4)
        self.adaptive_threshold: float = self.voxel_size * 2.0

    def step(self, xyz: np.ndarray, timestamp_ns: int = 0) -> Tuple[np.ndarray, Dict[str, float]]:
        """Processes a single LiDAR scan frame and returns (current_pose_4x4, metrics)."""
        xyz = np.asarray(xyz, dtype=np.float64)

        # Range filter
        ranges = np.linalg.norm(xyz, axis=1)
        valid = (ranges >= self.min_range) & (ranges <= self.max_range)
        filtered_xyz = xyz[valid]

        # Voxel downsample incoming scan
        scan_down = voxel_downsample(filtered_xyz, step=self.voxel_size)
        if len(scan_down) < 10:
            current_pose = self.poses[-1] if self.poses else np.eye(4)
            self.poses.append(current_pose)
            self.timestamps.append(timestamp_ns)
            return current_pose, {"rmse": 0.0, "fitness": 0.0}

        # First frame: initialize map
        if not self.poses:
            init_pose = np.eye(4)
            self.poses.append(init_pose)
            self.timestamps.append(timestamp_ns)
            self.submap_points = scan_down.copy()
            self.submap_normals = estimate_normals(self.submap_points, k=min(16, len(self.submap_points)))
            return init_pose, {"rmse": 0.0, "fitness": 1.0}

        # Predict pose using constant velocity model: T_pred = T_prev @ delta
        prev_pose = self.poses[-1]
        predicted_pose = prev_pose @ self.last_delta

        # Register scan against local submap
        # Transform scan with predicted pose into map frame
        curr_pose, info = icp_point_to_plane(
            scan_down,
            self.submap_points,
            dst_normals=self.submap_normals,
            max_distance=self.adaptive_threshold,
            max_iterations=self.max_iterations,
            initial_transform=predicted_pose,
        )

        # Update last delta
        self.last_delta = np.linalg.inv(prev_pose) @ curr_pose
        self.poses.append(curr_pose)
        self.timestamps.append(timestamp_ns)

        # Update adaptive threshold based on observed RMSE
        rmse = info.get("inlier_rmse_m", self.voxel_size)
        self.adaptive_threshold = float(np.clip(3.0 * rmse, self.voxel_size * 0.5, self.voxel_size * 4.0))

        # Add registered points to local submap
        R = curr_pose[:3, :3]
        t = curr_pose[:3, 3]
        world_scan = (scan_down @ R.T) + t

        self._update_submap(world_scan, curr_pose[:3, 3])

        return curr_pose, {
            "inlier_rmse_m": float(rmse),
            "fitness": float(info.get("fitness", 0.0)),
            "submap_size": len(self.submap_points),
            "adaptive_threshold": self.adaptive_threshold,
        }

    def _update_submap(self, new_world_points: np.ndarray, current_pos: np.ndarray) -> None:
        """Merges new points into submap, downsamples, and retains local neighborhood."""
        combined = np.vstack([self.submap_points, new_world_points])
        downsampled = voxel_downsample(combined, step=self.voxel_size)

        # Prune points far from current sensor position
        if len(downsampled) > self.max_submap_points:
            dists = np.linalg.norm(downsampled - current_pos, axis=1)
            keep_idx = np.argsort(dists)[: self.max_submap_points]
            downsampled = downsampled[keep_idx]

        self.submap_points = downsampled
        self.submap_normals = estimate_normals(self.submap_points, k=min(16, len(self.submap_points)))

    def get_trajectory(self) -> np.ndarray:
        """Returns the full estimated trajectory as (N, 4, 4) poses."""
        return np.array(self.poses, dtype=np.float64)

    def get_accumulated_map(self) -> np.ndarray:
        """Returns the current accumulated point cloud map in global frame."""
        return self.submap_points if self.submap_points is not None else np.empty((0, 3))
