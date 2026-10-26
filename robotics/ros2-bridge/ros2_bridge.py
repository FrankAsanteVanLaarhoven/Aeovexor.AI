"""
ROS 2 Humble Spatial Bridge
Provides bidirectional transformation between ROS 2 PointCloud2 / TF2 messages
and Aeovexor.AI native numpy point clouds. Includes pure-Python serialization.
"""

from typing import Dict, Any, Optional, Tuple
import numpy as np
import struct
import time
from schemas.spatial_schema import PointCloudFrame


class ROS2PointCloud2Bridge:
    def __init__(self, frame_id: str = "base_link"):
        self.frame_id = frame_id

    def numpy_to_pointcloud2_dict(
        self, points: np.ndarray, intensities: Optional[np.ndarray] = None
    ) -> Dict[str, Any]:
        """
        Serializes an (N, 3) numpy array into standard sensor_msgs/PointCloud2 binary layout:
        Fields: x (FLOAT32), y (FLOAT32), z (FLOAT32), intensity (FLOAT32).
        Step = 16 bytes per point.
        """
        if points.ndim != 2 or points.shape[1] != 3:
            raise ValueError("Points must have shape (N, 3)")

        num_points = len(points)
        if intensities is None or len(intensities) != num_points:
            intensities = np.full(num_points, 0.5, dtype=np.float32)

        # Pack into (N, 4) float32 buffer
        combined = np.empty((num_points, 4), dtype=np.float32)
        combined[:, :3] = points
        combined[:, 3] = intensities

        raw_data = combined.tobytes()

        return {
            "header": {
                "stamp": {"sec": int(time.time()), "nanosec": int(time.time_ns() % 1e9)},
                "frame_id": self.frame_id,
            },
            "height": 1,
            "width": num_points,
            "fields": [
                {"name": "x", "offset": 0, "datatype": 7, "count": 1},  # FLOAT32 = 7
                {"name": "y", "offset": 4, "datatype": 7, "count": 1},
                {"name": "z", "offset": 8, "datatype": 7, "count": 1},
                {"name": "intensity", "offset": 12, "datatype": 7, "count": 1},
            ],
            "is_bigendian": False,
            "point_step": 16,
            "row_step": 16 * num_points,
            "data": raw_data,
            "is_dense": True,
        }

    def pointcloud2_dict_to_numpy(self, msg: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
        """Deserializes a PointCloud2 message dict back into (points, intensities)."""
        data = msg["data"]
        point_step = msg.get("point_step", 16)
        arr = np.frombuffer(data, dtype=np.float32)

        # Float count per point
        floats_per_pt = point_step // 4
        reshaped = arr.reshape(-1, floats_per_pt)
        points = reshaped[:, :3]
        intensities = reshaped[:, 3] if floats_per_pt >= 4 else np.zeros(len(points), dtype=np.float32)

        return points, intensities
