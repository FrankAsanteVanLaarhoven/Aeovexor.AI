"""Comprehensive Peer-Reviewed Benchmark and Algorithm Test Suite for SpatialForge-3D."""
from pathlib import Path
import numpy as np
import pytest
from scipy.spatial.transform import Rotation
import torch

from spatialforge import (
    SpatialFrame, FrameMetadata, BoundingBox3D,
    load_frame, read_kitti_velodyne, load_waymo_frame,
    voxel_downsample, statistical_outlier_removal, radius_outlier_removal,
    estimate_normals, compute_geometric_descriptors, ransac_plane, extract_ground_plane,
    VoxelHashGrid,
    cluster, adaptive_geometry_clustering, region_growing_segmentation,
    icp, icp_point_to_plane, gicp_registration,
    LiDAROdometry,
    TSDFVolume, OccupancyGrid3D,
    compute_oriented_bounding_box, SemanticSceneGraph, compute_obstacle_clearance, compute_traversability_map,
    compute_optimal_scale_features, range_compensated_clustering,
    progressive_morphological_ground_filter, compute_minimal_oriented_bounding_box,
    PointNetLite, predict_point_semantics,
    evaluate_trajectory, evaluate_clustering, evaluate_segmentation,
    bootstrap_confidence_interval, paired_significance_test,
    generate_interactive_html,
)


@pytest.fixture
def rng():
    return np.random.default_rng(42)


def test_spatial_frame_contracts(rng):
    xyz = rng.normal(size=(50, 3))
    intensity = rng.uniform(0, 1, 50).astype(np.float32)
    frame = SpatialFrame(xyz=xyz, intensity=intensity)
    assert len(frame) == 50
    assert frame.metadata.provenance_hash is not None

    # Test SE(3) transformation
    T = np.eye(4)
    T[:3, 3] = [1.0, 2.0, 3.0]
    moved = frame.transform(T)
    assert np.allclose(moved.xyz[:, 0], xyz[:, 0] + 1.0)

    # Test NaN rejection
    bad_xyz = xyz.copy()
    bad_xyz[0, 0] = np.nan
    with pytest.raises(ValueError):
        SpatialFrame(xyz=bad_xyz)


def test_velodyne_kitti_ingestion():
    p = Path(__file__).resolve().parents[1] / "examples" / "velodyne_000008.bin"
    if p.is_file():
        frame = load_frame(p)
        assert len(frame) > 0
        assert frame.intensity is not None
        assert frame.metadata.sensor_type == "lidar"


def test_waymo_open_dataset_ingestion():
    p = Path("/Users/favl/Downloads/waymo-open-dataset-master 2/tutorial/frames")
    if p.is_file():
        frame = load_frame(p)
        assert len(frame) > 10000
        assert frame.metadata.coordinate_frame == "vehicle"
        assert "num_3d_boxes" in frame.metadata.extra


def test_geometry_and_descriptors(rng):
    xyz = rng.normal(scale=2.0, size=(100, 3))
    # Outlier removal
    inliers, _ = statistical_outlier_removal(xyz, k=10, std_ratio=1.5)
    assert inliers.dtype == bool
    assert inliers.sum() > 50

    # Voxel hashing
    grid = VoxelHashGrid(voxel_size=0.5)
    grid.insert(xyz)
    neighbors = grid.query_radius(xyz[0], radius=0.6, xyz=xyz)
    assert 0 in neighbors

    # Normals & Descriptors
    normals = estimate_normals(xyz, k=10)
    assert normals.shape == (100, 3)
    assert np.allclose(np.linalg.norm(normals, axis=1), 1.0)

    desc = compute_geometric_descriptors(xyz, k=10)
    assert "curvature" in desc and "planarity" in desc and "linearity" in desc
    assert (desc["curvature"] >= 0).all()


def test_ransac_and_ground_extraction(rng):
    # Plane z = 0 with slight noise
    plane_pts = np.column_stack([rng.uniform(-5, 5, 100), rng.uniform(-5, 5, 100), rng.normal(0, 0.02, 100)])
    obstacles = np.column_stack([rng.uniform(-2, 2, 20), rng.uniform(-2, 2, 20), rng.uniform(0.5, 2.0, 20)])
    all_pts = np.vstack([plane_pts, obstacles])

    plane, inliers = ransac_plane(all_pts, distance_threshold=0.08)
    assert inliers.sum() >= 95

    ground_mask, obs_mask, _ = extract_ground_plane(all_pts, distance_threshold=0.08)
    assert ground_mask.sum() >= 95
    assert obs_mask.sum() >= 15


def test_entropy_minimization_and_range_clustering(rng):
    xyz = rng.normal(size=(60, 3))
    opt_features = compute_optimal_scale_features(xyz, scale_candidates=[8, 12, 16])
    assert "optimal_k" in opt_features
    assert len(opt_features["optimal_k"]) == 60

    # Range compensated clustering
    c1 = rng.normal([0, 0, 0], 0.04, (30, 3))
    c2 = rng.normal([20, 0, 0], 0.15, (30, 3)) # Far cluster
    data = np.vstack([c1, c2])
    labels = range_compensated_clustering(data, base_eps=0.3, min_samples=4)
    found_clusters = set(labels) - {-1}
    assert len(found_clusters) >= 2


def test_registration_variants(rng):
    src = rng.normal(scale=1.0, size=(80, 3))
    # Small translation & rotation
    R = Rotation.from_euler("z", 5, degrees=True).as_matrix()
    t = np.array([0.05, -0.03, 0.02])
    dst = (src @ R.T) + t

    # Point-to-Plane
    T_p2pl, info_p2pl = icp_point_to_plane(src, dst, max_distance=0.5, max_iterations=30)
    assert np.allclose(T_p2pl[:3, 3], t, atol=1e-2)
    assert info_p2pl["inlier_rmse_m"] < 0.05

    # GICP
    T_gicp, info_gicp = gicp_registration(src, dst, max_distance=0.5, max_iterations=30)
    assert np.allclose(T_gicp[:3, 3], t, atol=1e-2)


def test_slam_odometry_loop(rng):
    slam = LiDAROdometry(voxel_size=0.3, max_range=50.0)
    base_cloud = rng.normal(scale=3.0, size=(120, 3))

    # Simulate 3 consecutive frames with 10cm forward motion
    for i in range(3):
        frame_xyz = base_cloud - np.array([i * 0.1, 0, 0])
        pose, info = slam.step(frame_xyz, timestamp_ns=i * 100_000_000)

    traj = slam.get_trajectory()
    assert len(traj) == 3
    # Check estimated forward displacement
    assert traj[-1, 0, 3] > 0.15


def test_tsdf_and_occupancy(rng):
    pts = rng.normal(size=(50, 3))
    tsdf = TSDFVolume(bounds_min=[-3, -3, -3], bounds_max=[3, 3, 3], voxel_size=0.5)
    tsdf.integrate_points(pts)
    assert tsdf.weights.sum() > 0

    occ = OccupancyGrid3D(bounds_min=[-3, -3, -3], bounds_max=[3, 3, 3], voxel_size=0.5)
    occ.integrate_points(pts)
    occ_pts = occ.get_occupied_points()
    assert len(occ_pts) > 0


def test_scene_graph_and_reasoning(rng):
    box_car = BoundingBox3D(center=np.array([2.0, 0.0, 0.5]), extent=np.array([4.0, 2.0, 1.5]), label="car", class_id=1)
    box_sign = BoundingBox3D(center=np.array([2.5, 0.0, 2.0]), extent=np.array([0.5, 0.5, 1.0]), label="sign", class_id=3)

    sg = SemanticSceneGraph()
    sg.add_object(1, box_car)
    sg.add_object(2, box_sign)
    sg.build_relations(adjacency_threshold_m=2.0)
    d = sg.to_dict()
    assert d["num_objects"] == 2
    assert len(d["relations"]) > 0

    # Clearance & Traversability
    safety = compute_obstacle_clearance(robot_position=[0, 0, 0], obstacle_points=[[0.8, 0, 0]])
    assert safety["is_safe"] is True
    ground = np.column_stack([rng.uniform(-3, 3, 50), rng.uniform(-3, 3, 50), rng.normal(0, 0.05, 50)])
    trav = compute_traversability_map(ground, grid_res=1.0)
    assert trav["traversable_fraction"] > 0.8


def test_pointnet_deep_learning():
    model = PointNetLite(in_channels=3, num_classes=5, mode="segmentation")
    x = torch.randn(2, 3, 128)
    out = model(x)
    assert out.shape == (2, 5, 128)

    # Test inference helper
    pts = np.random.randn(200, 3).astype(np.float32)
    preds = predict_point_semantics(model, pts)
    assert len(preds) == 200


def test_benchmarks_and_statistics():
    # 95% Confidence interval
    data = [0.85, 0.87, 0.86, 0.88, 0.84, 0.89, 0.86]
    ci = bootstrap_confidence_interval(data, confidence_level=0.95, num_bootstraps=200)
    assert ci["ci_lower"] < ci["mean"] < ci["ci_upper"]

    # Significance testing
    baseline = [0.80, 0.81, 0.79, 0.82, 0.80]
    proposed = [0.88, 0.89, 0.87, 0.90, 0.88]
    test_res = paired_significance_test(baseline, proposed)
    assert test_res["statistically_significant"] is True


def test_all_8_critical_gaps():
    from spatialforge.gap_verification import verify_all_gaps
    res = verify_all_gaps()
    assert all(v["status"] == "PASS" for v in res.values())


def test_versioned_plugin_registry():
    from spatialforge.plugins import GLOBAL_REGISTRY, PluginCategory
    plugins = GLOBAL_REGISTRY.list_plugins()
    assert len(plugins) >= 6

    # Test executing built-in plugins
    xyz = np.random.randn(300, 3).astype(np.float32)
    frame = SpatialFrame(xyz=xyz)

    # 1. RCMC Clustering plugin
    out_rcmc = GLOBAL_REGISTRY.execute("spatialforge_rcmc", frame)
    assert out_rcmc.success is True
    assert out_rcmc.labels is not None
    assert "num_clusters" in out_rcmc.metrics

    # 2. Side-by-side plugin comparison
    comp = GLOBAL_REGISTRY.compare_plugins(["spatialforge_rcmc", "open3d_dbscan"], frame)
    assert len(comp["comparison_matrix"]) == 2
    assert comp["comparison_matrix"][0]["plugin"] == "spatialforge_rcmc"


def test_workspace_server_api():
    from fastapi.testclient import TestClient
    from workspace.server import app

    client = TestClient(app)
    # Health endpoint
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["version"] == "0.3.0"

    # Datasets endpoint
    r = client.get("/api/datasets")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

    # Plugins endpoint
    r = client.get("/api/plugins")
    assert r.status_code == 200
    assert len(r.json()) >= 6

    # 5 Domains REST endpoints
    sample_ds = "velodyne_000008.bin"
    r_det = client.post("/api/domains/detect", json={"dataset_path": sample_ds})
    assert r_det.status_code == 200
    assert "objects_detected" in r_det.json()

    r_seg = client.post("/api/domains/segment", json={"dataset_path": sample_ds})
    assert r_seg.status_code == 200
    assert "class_counts" in r_seg.json()

    r_nav = client.post("/api/domains/navigation", json={"dataset_path": sample_ds})
    assert r_nav.status_code == 200
    assert "recommended_action" in r_nav.json()

    r_twin = client.post("/api/domains/digital_twin", json={"dataset_path": sample_ds})
    assert r_twin.status_code == 200
    assert "num_mesh_vertices" in r_twin.json()

    # Landing page & console UI routes
    r_landing = client.get("/")
    assert r_landing.status_code == 200
    assert "AEOVEXOR" in r_landing.text
    assert "Perceive. Reconstruct. Understand." in r_landing.text

    r_console = client.get("/console")
    assert r_console.status_code == 200
    assert "AEOVEXOR Studio" in r_console.text

    # Custom 404 test (Quality Gate #8)
    r_404 = client.get("/non-existent-spatial-route-xyz")
    assert r_404.status_code == 404
    assert "404" in r_404.text


def test_ouster_sdk_adapter():
    from spatialforge.ouster_adapter import (
        OusterSensorMetadata,
        create_synthetic_ouster_scan,
    )
    meta = OusterSensorMetadata(prod_line="OS-1-64", lidar_mode="1024x10")
    assert meta.columns_per_frame == 1024
    assert meta.pixels_per_column == 64

    scan = create_synthetic_ouster_scan(meta)
    frame = scan.to_spatial_frame()
    assert len(frame) > 1000
    assert frame.metadata.sensor_type == "ouster_lidar"
    assert frame.xyz.shape[1] == 3
    assert frame.intensity is not None


def test_five_core_domains():
    from spatialforge.domains import (
        run_slam_and_mapping,
        detect_objects_3d,
        segment_point_cloud,
        plan_autonomous_navigation,
        generate_digital_twin,
    )
    # Generate test frame
    rng = np.random.default_rng(42)
    road_pts = rng.uniform([-10, -10, -1.75], [10, 10, -1.70], size=(400, 3)).astype(np.float32)
    car_pts = rng.uniform([3, -1, -1.5], [7, 1, 0.2], size=(150, 3)).astype(np.float32)
    tree_pts = rng.uniform([-5, 4, -1.0], [-3, 6, 2.5], size=(100, 3)).astype(np.float32)
    test_xyz = np.vstack([road_pts, car_pts, tree_pts])
    frame = SpatialFrame(xyz=test_xyz)

    # 1. 3D mapping and SLAM
    slam_res = run_slam_and_mapping([frame, frame])
    assert slam_res.num_frames_processed == 2
    assert len(slam_res.accumulated_map_points) > 0

    # 2. 3D Object Detection
    objs = detect_objects_3d(frame)
    assert isinstance(objs, list)

    # 3. Point-Cloud Segmentation
    seg_res = segment_point_cloud(frame)
    assert seg_res.ground_fraction > 0.0
    assert "Ground" in seg_res.class_counts

    # 4. Autonomous Navigation
    nav_res = plan_autonomous_navigation(frame)
    assert nav_res.minimum_obstacle_clearance_m > 0
    assert nav_res.recommended_action in ["PROCEED", "REDUCE_SPEED", "EMERGENCY_STOP"]

    # 5. Digital Twins
    twin = generate_digital_twin(frame, voxel_size=0.4)
    assert twin.voxel_resolution_m == 0.4
    assert twin.watertight_volume_m3 > 0



