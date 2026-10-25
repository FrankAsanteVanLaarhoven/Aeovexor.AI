"""Canonical Spatial Data Contracts for SpatialForge-3D.

Enforces sensor-neutral representation, coordinate frames, timestamps,
units, provenance hashes, and uncertainty covariance tracking.
"""
from dataclasses import dataclass, field
import hashlib
import json
import time
from typing import Dict, List, Optional, Tuple, Union
import numpy as np


@dataclass
class FrameMetadata:
    """Rigorous metadata contract for every spatial observation."""
    coordinate_frame: str = "sensor_lidar"  # e.g., sensor_lidar, base_link, odom, map, utm
    unit: str = "meter"
    timestamp_ns: int = 0
    sensor_id: str = "lidar_0"
    sensor_type: str = "spinning_lidar"  # spinning_lidar, solid_state, rgbd, stereo, uav
    crs: Optional[str] = None  # e.g. EPSG:4326, UTM-32N for GIS
    calibration_id: Optional[str] = None
    provenance_hash: Optional[str] = None
    extra: Dict[str, Union[str, int, float, bool]] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "coordinate_frame": self.coordinate_frame,
            "unit": self.unit,
            "timestamp_ns": self.timestamp_ns,
            "sensor_id": self.sensor_id,
            "sensor_type": self.sensor_type,
            "crs": self.crs,
            "calibration_id": self.calibration_id,
            "provenance_hash": self.provenance_hash,
            "extra": self.extra,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "FrameMetadata":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class BoundingBox3D:
    """3D Bounding Box representation (AABB or OBB)."""
    center: np.ndarray  # (3,)
    extent: np.ndarray  # (3,) length, width, height (dx, dy, dz)
    rotation: np.ndarray = field(default_factory=lambda: np.eye(3))  # (3, 3)
    class_id: int = -1
    label: str = "unknown"
    confidence: float = 1.0

    def volume(self) -> float:
        return float(np.prod(self.extent))

    def corners(self) -> np.ndarray:
        """Computes 8 corners of the 3D bounding box."""
        dx, dy, dz = self.extent / 2.0
        x_corners = np.array([dx, dx, -dx, -dx, dx, dx, -dx, -dx])
        y_corners = np.array([dy, -dy, -dy, dy, dy, -dy, -dy, dy])
        z_corners = np.array([dz, dz, dz, dz, -dz, -dz, -dz, -dz])
        local = np.vstack([x_corners, y_corners, z_corners]).T  # (8, 3)
        return (local @ self.rotation.T) + self.center


class SpatialFrame:
    """Canonical Point Cloud and Spatial Data Frame.
    
    Guarantees:
    - Finite Nx3 coordinates in declared metric frame.
    - Optional attribute channels: intensity, rgb, normals, curvature, covariances, classes, instances.
    - Automatic provenance hashing (SHA256 of coordinates & attributes).
    - Immutable SE(3) transformation support.
    """

    def __init__(
        self,
        xyz: np.ndarray,
        intensity: Optional[np.ndarray] = None,
        rgb: Optional[np.ndarray] = None,
        normals: Optional[np.ndarray] = None,
        curvature: Optional[np.ndarray] = None,
        covariances: Optional[np.ndarray] = None,
        classes: Optional[np.ndarray] = None,
        instances: Optional[np.ndarray] = None,
        timestamps: Optional[np.ndarray] = None,
        metadata: Optional[FrameMetadata] = None,
    ):
        self._xyz = np.asarray(xyz, dtype=np.float64)
        if self._xyz.ndim != 2 or self._xyz.shape[1] != 3:
            raise ValueError(f"XYZ points must have shape (N, 3), got {self._xyz.shape}")
        if not np.isfinite(self._xyz).all():
            raise ValueError("Point coordinates must be finite (no NaN, inf or -inf)")

        n = len(self._xyz)

        self._intensity = self._validate_channel(intensity, n, "intensity", (n,), np.float32)
        self._rgb = self._validate_channel(rgb, n, "rgb", (n, 3), np.uint8)
        self._normals = self._validate_channel(normals, n, "normals", (n, 3), np.float64)
        self._curvature = self._validate_channel(curvature, n, "curvature", (n,), np.float64)
        self._covariances = self._validate_channel(covariances, n, "covariances", (n, 3, 3), np.float64)
        self._classes = self._validate_channel(classes, n, "classes", (n,), np.int32)
        self._instances = self._validate_channel(instances, n, "instances", (n,), np.int32)
        self._timestamps = self._validate_channel(timestamps, n, "timestamps", (n,), np.int64)

        self.metadata = metadata if metadata is not None else FrameMetadata()
        if self.metadata.provenance_hash is None and n > 0:
            self.metadata.provenance_hash = self.compute_digest()

    @staticmethod
    def _validate_channel(data, n: int, name: str, expected_shape: tuple, dtype) -> Optional[np.ndarray]:
        if data is None:
            return None
        arr = np.asarray(data)
        if len(arr) != n:
            raise ValueError(f"Channel {name} length {len(arr)} does not match point count {n}")
        if arr.shape != expected_shape:
            raise ValueError(f"Channel {name} shape {arr.shape} does not match expected {expected_shape}")
        return arr.astype(dtype, copy=False)

    @property
    def xyz(self) -> np.ndarray:
        return self._xyz

    @property
    def points(self) -> np.ndarray:
        """Convenience alias for self.xyz."""
        return self._xyz

    @property
    def intensity(self) -> Optional[np.ndarray]:
        return self._intensity

    @property
    def intensities(self) -> Optional[np.ndarray]:
        """Convenience alias for self.intensity."""
        return self._intensity

    @property
    def rgb(self) -> Optional[np.ndarray]:
        return self._rgb

    @property
    def normals(self) -> Optional[np.ndarray]:
        return self._normals

    @property
    def curvature(self) -> Optional[np.ndarray]:
        return self._curvature

    @property
    def covariances(self) -> Optional[np.ndarray]:
        return self._covariances

    @property
    def classes(self) -> Optional[np.ndarray]:
        return self._classes

    @property
    def instances(self) -> Optional[np.ndarray]:
        return self._instances

    @property
    def timestamps(self) -> Optional[np.ndarray]:
        return self._timestamps

    def __len__(self) -> int:
        return len(self._xyz)

    def bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        if len(self._xyz) == 0:
            return np.zeros(3), np.zeros(3)
        return self._xyz.min(axis=0), self._xyz.max(axis=0)

    def compute_digest(self) -> str:
        """Compute deterministic SHA-256 digest of geometry."""
        h = hashlib.sha256()
        h.update(self._xyz.tobytes())
        if self._intensity is not None:
            h.update(self._intensity.tobytes())
        if self._classes is not None:
            h.update(self._classes.tobytes())
        return h.hexdigest()

    def filter_mask(self, mask: np.ndarray) -> "SpatialFrame":
        """Returns a new SpatialFrame with points selected by boolean mask."""
        mask = np.asarray(mask, dtype=bool)
        if len(mask) != len(self._xyz):
            raise ValueError(f"Mask length {len(mask)} != {len(self._xyz)}")
        return SpatialFrame(
            xyz=self._xyz[mask],
            intensity=self._intensity[mask] if self._intensity is not None else None,
            rgb=self._rgb[mask] if self._rgb is not None else None,
            normals=self._normals[mask] if self._normals is not None else None,
            curvature=self._curvature[mask] if self._curvature is not None else None,
            covariances=self._covariances[mask] if self._covariances is not None else None,
            classes=self._classes[mask] if self._classes is not None else None,
            instances=self._instances[mask] if self._instances is not None else None,
            timestamps=self._timestamps[mask] if self._timestamps is not None else None,
            metadata=FrameMetadata(**self.metadata.to_dict()),
        )

    def transform(self, matrix_4x4: np.ndarray, target_frame: Optional[str] = None) -> "SpatialFrame":
        """Applies SE(3) transformation matrix [R | t] to coordinates, normals, and covariances."""
        T = np.asarray(matrix_4x4, dtype=np.float64)
        if T.shape != (4, 4):
            raise ValueError(f"Transformation matrix must be 4x4, got {T.shape}")
        R = T[:3, :3]
        t = T[:3, 3]

        new_xyz = (self._xyz @ R.T) + t
        new_normals = None
        if self._normals is not None:
            new_normals = self._normals @ R.T
            # Re-normalize
            norms = np.linalg.norm(new_normals, axis=1, keepdims=True)
            new_normals = np.divide(new_normals, np.maximum(norms, 1e-12))

        new_covariances = None
        if self._covariances is not None:
            new_covariances = np.einsum("ij,njk,lk->nil", R, self._covariances, R)

        meta = FrameMetadata(**self.metadata.to_dict())
        if target_frame:
            meta.coordinate_frame = target_frame
        meta.provenance_hash = None  # Recomputed on init

        return SpatialFrame(
            xyz=new_xyz,
            intensity=self._intensity.copy() if self._intensity is not None else None,
            rgb=self._rgb.copy() if self._rgb is not None else None,
            normals=new_normals,
            curvature=self._curvature.copy() if self._curvature is not None else None,
            covariances=new_covariances,
            classes=self._classes.copy() if self._classes is not None else None,
            instances=self._instances.copy() if self._instances is not None else None,
            timestamps=self._timestamps.copy() if self._timestamps is not None else None,
            metadata=meta,
        )

    def to_dict(self) -> dict:
        b_min, b_max = self.bounds()
        return {
            "num_points": len(self),
            "bounds_min": b_min.tolist(),
            "bounds_max": b_max.tolist(),
            "has_intensity": self._intensity is not None,
            "has_rgb": self._rgb is not None,
            "has_normals": self._normals is not None,
            "has_classes": self._classes is not None,
            "metadata": self.metadata.to_dict(),
        }
