"""
Comprehensive Unit & Integration Test Suite
Validates the complete Enterprise Services, Robotics ROS 2 Bridge, Benchmarks, and Schemas.
"""

import pytest
import numpy as np
import time

from schemas import (
    BoundingBox3D,
    Keypoint3D,
    Pose3D,
    FaceDetection,
    Tracklet3D,
    OcclusionProfile,
    SafetyZoneEvent,
    CredentialToken,
    PolicyRule,
    PointCloudFrame,
)
from services import (
    IngestionService,
    PersonDetector,
    FaceDetector,
    PoseEstimator,
    HumanSegmentor,
    ObjectDetector,
    TemporalTracker,
    OcclusionEngine,
    MetadataEngine,
    CredentialVerifier,
    PolicyEngine,
)
from robotics import (
    ROS2PointCloud2Bridge,
    SafetyInterface,
)
from benchmarks import (
    DetectionBenchmark,
    compute_3d_box_iou,
    PoseBenchmark,
    OcclusionBenchmark,
    CalibrationBenchmark,
    PrivacyBenchmark,
)


def test_schemas_serialization():
    box = BoundingBox3D(
        id="BOX_001",
        label="Vehicle",
        x=5.0,
        y=10.0,
        z=-0.5,
        dx=4.2,
        dy=1.8,
        dz=1.6,
        yaw=15.0,
        confidence=0.95,
    )
    assert box.label == "Vehicle"
    assert box.dx == 4.2

    frame = PointCloudFrame(sensor_id="lidar_test", frame_id=1, num_points=100)
    digest = frame.compute_provenance_hash(b"sample_point_bytes")
    assert len(digest) == 64
    assert frame.provenance_hash == digest


def test_ingestion_service():
    service = IngestionService(sensor_id="lidar_front")
    pts = np.array([
        [1.0, 2.0, 3.0],
        [np.nan, 2.0, 3.0],  # Should be rejected
        [4.0, 5.0, 6.0],
        [7.0, np.inf, 9.0],  # Should be rejected
    ])
    intensities = np.array([0.1, 0.2, 0.3, 0.4])

    frame, valid_pts, valid_ints = service.ingest_numpy_cloud(pts, intensities)
    assert len(valid_pts) == 2
    assert len(valid_ints) == 2
    assert frame.num_points == 2
    assert frame.provenance_hash is not None


def test_person_and_human_segmentation():
    detector = PersonDetector(min_height=1.2, max_height=2.2)

    # Generate synthetic pedestrian points (cylinder: h=1.7m, r=0.25m at x=5, y=5, z=0)
    theta = np.linspace(0, 2 * np.pi, 50)
    z = np.linspace(-0.8, 0.8, 50)
    xx = 5.0 + 0.25 * np.cos(theta)
    yy = 5.0 + 0.25 * np.sin(theta)
    zz = z
    person_pts = np.column_stack([xx, yy, zz])

    # Background points
    bg_pts = np.array([[20.0, 20.0, 0.0], [25.0, 25.0, 0.0]])
    all_pts = np.vstack([person_pts, bg_pts])

    boxes = detector.detect_persons_from_cloud(all_pts)
    assert len(boxes) >= 1
    assert boxes[0].label == "Person"

    # Test segmentation
    segmentor = HumanSegmentor()
    human_pts, background_pts = segmentor.segment_human_points(all_pts, boxes[0])
    assert len(human_pts) >= 40
    assert len(background_pts) >= 2


def test_pose_estimation():
    box = BoundingBox3D(
        id="PED_001", label="Person", x=4.0, y=8.0, z=0.0, dx=0.6, dy=0.6, dz=1.75
    )
    estimator = PoseEstimator(target_joint_precision_mm=25.0)
    pose = estimator.estimate_3d_pose(box)

    assert pose.person_id == "PED_001"
    assert len(pose.keypoints) == 17
    assert any(kp.name == "nose" for kp in pose.keypoints)
    assert pose.mpjpe_error == 25.0


def test_face_detection_and_privacy_redaction():
    detector = FaceDetector(blur_kernel_size=21)
    detections = detector.detect_faces(1080, 1920)

    assert len(detections) >= 1
    assert detections[0].blurred is True
    assert len(detections[0].redaction_hash) == 64

    # Test image blur application
    fake_img = np.ones((100, 100, 3), dtype=np.uint8) * 200
    blurred_img = detector.apply_blur_to_numpy(fake_img, [(0.2, 0.2, 0.6, 0.6)])
    assert blurred_img.shape == fake_img.shape


def test_object_detection_and_temporal_tracking():
    # Synthetic vehicle cluster
    x = np.random.uniform(8.0, 12.0, 100)
    y = np.random.uniform(3.0, 5.0, 100)
    z = np.random.uniform(-0.5, 1.0, 100)
    vehicle_pts = np.column_stack([x, y, z])

    detector = ObjectDetector()
    detections = detector.detect_objects(vehicle_pts)
    assert len(detections) >= 1
    assert detections[0].label == "Vehicle"

    # Temporal tracker
    tracker = TemporalTracker()
    tracks_t1 = tracker.update(detections, dt=0.1)
    assert len(tracks_t1) >= 1
    assert tracks_t1[0].state == "TENTATIVE"

    # Second frame (simulated movement)
    for d in detections:
        d.x += 0.5
    tracks_t2 = tracker.update(detections, dt=0.1)
    assert len(tracks_t2) >= 1
    assert tracks_t2[0].history_length == 2
    assert tracks_t2[0].state == "CONFIRMED"
    assert tracks_t2[0].speed_mps > 0.0


def test_occlusion_engine():
    engine = OcclusionEngine()
    target = BoundingBox3D(id="TGT", label="Vehicle", x=15.0, y=0.0, z=0.0, dx=4.0, dy=2.0, dz=1.5)
    blocker = BoundingBox3D(id="BLOCK", label="Vehicle", x=8.0, y=0.0, z=0.0, dx=4.0, dy=2.0, dz=1.5)

    # Synthetic cloud
    cloud = np.random.uniform(-10, 20, (500, 3))

    occ = engine.compute_occlusion(target, cloud, occluding_boxes=[blocker])
    assert occ.object_id == "TGT"
    assert occ.is_line_of_sight is False
    assert occ.occlusion_percentage > 20.0


def test_metadata_and_credential_verification():
    meta = MetadataEngine()
    digest = meta.record_frame_provenance("lidar_1", 101, 5000, b"raw_pts")
    assert meta.verify_provenance(101, digest) is True
    assert meta.verify_provenance(101, "invalid_digest") is False

    cred = CredentialVerifier(secret_key="secret123")
    token = cred.generate_token("sensor_01", scopes=["sensor:read", "robot:e-stop"])
    assert cred.verify_token(token, required_scope="sensor:read") is True
    assert cred.verify_token(token, required_scope="admin:root") is False


def test_policy_engine():
    policy = PolicyEngine()
    assert policy.evaluate_export_permission("PUBLIC", "visitor") is False
    assert policy.evaluate_export_permission("PUBLIC", "researcher") is True
    assert policy.evaluate_export_permission("RESTRICTED", "operator") is True


def test_robotics_ros2_and_safety_interface():
    # ROS 2 Bridge
    bridge = ROS2PointCloud2Bridge(frame_id="base_link")
    pts = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], dtype=np.float32)
    ints = np.array([0.8, 0.9], dtype=np.float32)

    msg = bridge.numpy_to_pointcloud2_dict(pts, ints)
    assert msg["width"] == 2
    assert msg["point_step"] == 16

    rec_pts, rec_ints = bridge.pointcloud2_dict_to_numpy(msg)
    np.testing.assert_allclose(pts, rec_pts)
    np.testing.assert_allclose(ints, rec_ints)

    # Safety Interface (E-Stop and Slowdown)
    safety = SafetyInterface(estop_radius_m=1.5, slowdown_radius_m=3.5)
    hazard_estop = [BoundingBox3D(id="HAZ_1", label="Obstacle", x=1.0, y=0.5, z=0.0, dx=0.5, dy=0.5, dz=0.5)]
    event_estop = safety.evaluate_safety_zones(hazard_estop)
    assert event_estop.e_stop_triggered is True
    assert event_estop.zone_name == "E-STOP_ZONE"

    hazard_slow = [BoundingBox3D(id="HAZ_2", label="Obstacle", x=2.5, y=0.0, z=0.0, dx=0.5, dy=0.5, dz=0.5)]
    event_slow = safety.evaluate_safety_zones(hazard_slow)
    assert event_slow.e_stop_triggered is False
    assert event_slow.zone_name == "SLOWDOWN_ZONE"
    assert event_slow.recommended_speed_limit_mps > 0.0


def test_all_benchmarks():
    # 1. Detection Benchmark
    b1 = BoundingBox3D(id="B1", label="Car", x=5.0, y=5.0, z=0.0, dx=4.0, dy=2.0, dz=1.5, confidence=0.9)
    b2 = BoundingBox3D(id="B2", label="Car", x=5.1, y=5.0, z=0.0, dx=4.0, dy=2.0, dz=1.5, confidence=0.9)
    det_bench = DetectionBenchmark()
    det_results = det_bench.evaluate([b1], [b2])
    assert det_results["recall@50"] == 1.0

    # 2. Pose Benchmark
    pose_bench = PoseBenchmark(pck_threshold_mm=100.0)
    p_est = Pose3D(person_id="P1", keypoints=[Keypoint3D(name="nose", x=0.0, y=0.0, z=1.7)])
    p_gt = Pose3D(person_id="P1", keypoints=[Keypoint3D(name="nose", x=0.02, y=0.0, z=1.7)])
    pose_res = pose_bench.evaluate_poses([p_est], [p_gt])
    assert pose_res["mpjpe_mm"] == 20.0
    assert pose_res["pck_pct"] == 100.0

    # 3. Occlusion Benchmark
    occ_bench = OcclusionBenchmark()
    occ_prof = OcclusionProfile(object_id="B1", occlusion_percentage=10.0, visible_points=50, total_expected_points=55)
    occ_res = occ_bench.evaluate_stratified_recall([b1], [b2], [occ_prof])
    assert occ_res["recall_light_0_20"] == 100.0

    # 4. Calibration Benchmark
    calib = CalibrationBenchmark()
    pts3d = np.array([[0.0, 0.0, 5.0]], dtype=np.float32)
    ext_r = np.eye(3)
    ext_t = np.array([0.0, 0.0, 0.0])
    # Projected pixel for (0, 0, 5) with K: u = 609.5, v = 172.8
    pixels = np.array([[609.5, 172.8]], dtype=np.float32)
    calib_res = calib.evaluate_extrinsic_reprojection(pts3d, pixels, ext_r, ext_t)
    assert calib_res["reprojection_rmse_px"] < 0.01

    # 5. Privacy Benchmark
    priv_bench = PrivacyBenchmark(target_redaction_rate_pct=95.0)
    face = FaceDetection(face_id="F1", bbox_2d=(0.1, 0.1, 0.2, 0.2), blurred=True, redaction_hash="abc")
    priv_res = priv_bench.audit_redaction([face], ground_truth_pii_count=1)
    assert priv_res["passed_compliance_audit"] is True
    assert priv_res["unredacted_leaks"] == 0
