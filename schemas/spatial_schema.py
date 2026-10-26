"""
Aeovexor.AI Unified Spatial & Vision Intelligence Schemas
Standardized Pydantic models for sensor frames, bounding boxes, pose, tracking,
safety events, credentials, and policy rules.
"""

from typing import List, Optional, Dict, Any, Tuple
from pydantic import BaseModel, Field
import time
import hashlib
import json


class BoundingBox3D(BaseModel):
    id: str = Field(..., description="Unique bounding box identifier")
    label: str = Field(..., description="Semantic class label (e.g. Person, Vehicle, Cyclist, Obstacle)")
    x: float = Field(..., description="Center X position in meters")
    y: float = Field(..., description="Center Y position in meters")
    z: float = Field(..., description="Center Z position in meters")
    dx: float = Field(..., description="Dimension along X (length) in meters")
    dy: float = Field(..., description="Dimension along Y (width) in meters")
    dz: float = Field(..., description="Dimension along Z (height) in meters")
    yaw: float = Field(0.0, description="Heading / yaw rotation in degrees")
    confidence: float = Field(1.0, ge=0.0, le=1.0, description="Detection confidence score")
    velocity: Optional[Tuple[float, float, float]] = Field(None, description="(vx, vy, vz) velocity in m/s")


class Keypoint3D(BaseModel):
    name: str = Field(..., description="Joint name (e.g. nose, left_shoulder, right_knee)")
    x: float = Field(..., description="Joint X in meters")
    y: float = Field(..., description="Joint Y in meters")
    z: float = Field(..., description="Joint Z in meters")
    confidence: float = Field(1.0, ge=0.0, le=1.0)


class Pose3D(BaseModel):
    person_id: str = Field(..., description="Associated person/track ID")
    keypoints: List[Keypoint3D] = Field(default_factory=list, description="3D skeleton keypoints")
    mpjpe_error: Optional[float] = Field(None, description="Estimated joint position error in mm")
    activity: Optional[str] = Field(None, description="Inferred activity (e.g. Walking, Reaching, Sitting)")


class FaceDetection(BaseModel):
    face_id: str = Field(..., description="Detected face ID")
    bbox_2d: Tuple[float, float, float, float] = Field(..., description="(x_min, y_min, x_max, y_max) normalized")
    blurred: bool = Field(True, description="Whether privacy blur has been applied")
    redaction_hash: Optional[str] = Field(None, description="Cryptographic receipt of redaction")


class Tracklet3D(BaseModel):
    track_id: str = Field(..., description="Unique temporal track ID")
    label: str = Field(..., description="Tracked object category")
    current_box: BoundingBox3D = Field(..., description="Latest estimated 3D bounding box")
    history_length: int = Field(1, description="Number of consecutive frames tracked")
    state: str = Field("CONFIRMED", description="Tracking state: TENTATIVE, CONFIRMED, LOST, DELETED")
    speed_mps: float = Field(0.0, description="Magnitude of speed in meters per second")


class OcclusionProfile(BaseModel):
    object_id: str = Field(..., description="ID of the target object")
    occlusion_percentage: float = Field(0.0, ge=0.0, le=100.0, description="Estimated occlusion level")
    visible_points: int = Field(0, description="Number of unoccluded LiDAR points")
    total_expected_points: int = Field(0, description="Estimated total surface points")
    is_line_of_sight: bool = Field(True, description="Direct unobstructed line of sight to sensor")


class SafetyZoneEvent(BaseModel):
    event_id: str = Field(..., description="Unique safety event identifier")
    timestamp_ns: int = Field(default_factory=lambda: int(time.time_ns()))
    zone_name: str = Field(..., description="Safety zone name (e.g. E-STOP_ZONE, CAUTION_ZONE)")
    intrusion_distance_m: float = Field(..., description="Minimum distance from robot hazard to object")
    e_stop_triggered: bool = Field(False, description="Whether hardware emergency stop was commanded")
    recommended_speed_limit_mps: float = Field(0.0, description="Mandated robot velocity limit")


class CredentialToken(BaseModel):
    device_id: str = Field(..., description="Hardware device UUID or agent identifier")
    public_key_pem: str = Field(..., description="Public key representation")
    scopes: List[str] = Field(default_factory=list, description="Authorized scopes (e.g. sensor:read, robot:control)")
    expires_at: int = Field(..., description="Unix timestamp of token expiration")
    signature: str = Field(..., description="Cryptographic signature of payload")


class PolicyRule(BaseModel):
    rule_id: str = Field(..., description="Policy identifier")
    description: str = Field(..., description="Human-readable rule explanation")
    zone_type: str = Field("PUBLIC", description="PUBLIC, RESTRICTED, or CONFIDENTIAL")
    require_face_blur: bool = Field(True, description="Mandate automatic face redaction")
    allow_raw_sensor_export: bool = Field(False, description="Permission to download unredacted point clouds")
    max_retention_days: int = Field(30, description="Data retention limit")


class PointCloudFrame(BaseModel):
    sensor_id: str = Field(..., description="Sensor identifier (e.g. lidar_top, depth_cam_01)")
    frame_id: int = Field(..., description="Monotonically increasing sequence number")
    timestamp_ns: int = Field(default_factory=lambda: int(time.time_ns()))
    coordinate_frame: str = Field("base_link", description="Coordinate reference frame (e.g. base_link, sensor_frame)")
    num_points: int = Field(0, description="Total number of points in cloud")
    provenance_hash: Optional[str] = Field(None, description="SHA256 provenance digest")

    def compute_provenance_hash(self, point_bytes: bytes) -> str:
        h = hashlib.sha256()
        h.update(self.sensor_id.encode())
        h.update(str(self.frame_id).encode())
        h.update(str(self.timestamp_ns).encode())
        h.update(point_bytes)
        digest = h.hexdigest()
        self.provenance_hash = digest
        return digest
