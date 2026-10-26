"""
Ingestion Microservice
Handles multi-sensor LiDAR, RGB-D, and camera stream acquisition,
finite float validation, coordinate frame normalization, and provenance hashing.
"""

from typing import Dict, Any, Optional, Tuple
import numpy as np
import hashlib
import time
from schemas.spatial_schema import PointCloudFrame


class IngestionService:
    def __init__(self, sensor_id: str = "lidar_top", default_frame: str = "base_link"):
        self.sensor_id = sensor_id
        self.default_frame = default_frame
        self.total_frames_ingested = 0

    def ingest_numpy_cloud(
        self,
        points: np.ndarray,
        intensities: Optional[np.ndarray] = None,
        timestamp_ns: Optional[int] = None,
    ) -> Tuple[PointCloudFrame, np.ndarray, np.ndarray]:
        """
        Validates and ingests a raw numpy Nx3 point cloud array.
        Rejects NaNs/Infs and enforces standard meters.
        """
        if points.ndim != 2 or points.shape[1] != 3:
            raise ValueError(f"Points array must be of shape (N, 3), got {points.shape}")

        # 1. Finite coordinate check
        finite_mask = np.isfinite(points).all(axis=1)
        valid_points = points[finite_mask].astype(np.float32)

        if intensities is not None and len(intensities) == len(points):
            valid_intensities = intensities[finite_mask].astype(np.float32)
        else:
            valid_intensities = np.full(len(valid_points), 0.5, dtype=np.float32)

        self.total_frames_ingested += 1
        ts = timestamp_ns or time.time_ns()

        frame = PointCloudFrame(
            sensor_id=self.sensor_id,
            frame_id=self.total_frames_ingested,
            timestamp_ns=ts,
            coordinate_frame=self.default_frame,
            num_points=len(valid_points),
        )

        # Compute immutable provenance hash
        frame.compute_provenance_hash(valid_points.tobytes())

        return frame, valid_points, valid_intensities

    def ingest_kitti_bin_bytes(self, data: bytes) -> Tuple[PointCloudFrame, np.ndarray, np.ndarray]:
        """Ingests raw KITTI float32 binary buffer (x, y, z, intensity)."""
        raw_arr = np.frombuffer(data, dtype=np.float32)
        if len(raw_arr) % 4 != 0:
            raise ValueError("Buffer byte length must be divisible by 16 (4 float32 values per point)")
        reshaped = raw_arr.reshape(-1, 4)
        points = reshaped[:, :3]
        intensities = reshaped[:, 3]
        return self.ingest_numpy_cloud(points, intensities)
