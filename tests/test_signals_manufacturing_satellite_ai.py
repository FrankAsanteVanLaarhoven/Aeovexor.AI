"""
Test Suite for Signal Processing, Manufacturing Quality, Satellite 3D Earth Mapping & OpenRouter AI Copilot
"""

import os
import pytest
import numpy as np

from spatialforge.contracts import SpatialFrame
from spatialforge.signal_processing import (
    kaufman_adaptive_filter_1d,
    apply_kaufman_filter_to_point_cloud,
    evaluate_emergency_hazard_alerts,
    fuse_wifi_slam_with_lidar,
)
from spatialforge.manufacturing import (
    evaluate_surface_degradation,
    classify_material_spectral_grading,
    automated_curvature_adaptive_sampling,
    manual_roi_box_sampling,
)
from spatialforge.satellite_elevation import (
    generate_satellite_3d_point_cloud,
    PRESET_LOCATIONS,
)
from spatialforge.ai_copilot import (
    resolve_openrouter_api_key,
    query_openrouter_spatial_copilot,
    AVAILABLE_MODELS,
)


def test_kaufman_adaptive_filter_smoothing():
    # Step signal with Gaussian noise
    clean_signal = np.concatenate([np.ones(50) * 10.0, np.ones(50) * 20.0])
    noisy_signal = clean_signal + np.random.normal(0, 0.5, size=100)

    filtered = kaufman_adaptive_filter_1d(noisy_signal, period=10, fast_period=2, slow_period=30)
    assert len(filtered) == 100
    # Variance of flat portion should be reduced
    assert np.var(filtered[:40]) < np.var(noisy_signal[:40])
    # Step edge from 10 to 20 should be preserved
    assert filtered[-1] > 18.0


def test_kaufman_point_cloud_filter():
    pts = np.random.uniform(5.0, 25.0, size=(120, 3))
    intensities = np.random.uniform(0.1, 0.9, size=120)
    frame = SpatialFrame(xyz=pts, intensity=intensities)

    filtered_frame = apply_kaufman_filter_to_point_cloud(frame, period=6)
    assert len(filtered_frame) == 120
    assert filtered_frame.intensity is not None
    assert len(filtered_frame.intensity) == 120


def test_emergency_hazard_alerts():
    # Create obstacle 2 meters ahead
    obstacle_pts = np.array([
        [2.0, 0.0, 0.0],
        [2.1, 0.1, 0.1],
        [2.2, -0.1, 0.0],
    ])
    frame = SpatialFrame(xyz=obstacle_pts)

    alerts = evaluate_emergency_hazard_alerts(frame, ego_speed_ms=10.0)
    assert len(alerts) > 0
    primary = alerts[0]
    assert primary.distance_m <= 2.2
    assert primary.alert_level == "CRITICAL_BRAKE"
    assert primary.time_to_impact_s < 1.0


def test_wifi_slam_manifold_fusion():
    lidar_pose = np.eye(4)
    lidar_pose[:3, 3] = [8.0, 4.0, 0.0]

    result = fuse_wifi_slam_with_lidar(lidar_pose)
    assert len(result.fused_pose_xyz) == 3
    assert result.covariance_uncertainty_m > 0.0
    assert len(result.observed_access_points) >= 4
    assert result.signal_fingerprint_confidence >= 0.90


def test_manufacturing_surface_degradation():
    # Create planar surface with small perturbations (within 1mm)
    x = np.linspace(-1, 1, 30)
    y = np.linspace(-1, 1, 30)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X) + np.random.normal(0, 0.0003, size=X.shape)  # ~0.3mm noise
    pts = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))

    rep = evaluate_surface_degradation(pts, tolerance_threshold_mm=2.0)
    assert rep.total_surface_points == 900
    assert rep.passes_iso_tolerance is True
    assert rep.surface_degradation_index < 0.25
    assert "Grade" in rep.wear_classification


def test_material_spectral_grading():
    metallic = np.ones(50) * 0.88
    res_metal = classify_material_spectral_grading(metallic)
    assert "Metallic" in res_metal.material_class
    assert res_metal.confidence >= 0.90

    asphalt = np.ones(50) * 0.32
    res_asphalt = classify_material_spectral_grading(asphalt)
    assert "Asphalt" in res_asphalt.material_class


def test_automated_and_manual_sampling():
    pts = np.random.uniform(-10, 10, size=(1000, 3))

    sampled_auto, res_auto = automated_curvature_adaptive_sampling(pts, target_reduction=0.5)
    assert len(sampled_auto) == 500
    assert res_auto.reduction_ratio == 0.50

    sampled_roi, res_roi = manual_roi_box_sampling(pts, [-2, -2, -2], [2, 2, 2])
    assert len(sampled_roi) < len(pts)
    assert res_roi.sampling_method == "Manual_ROI_Box"


def test_satellite_3d_point_cloud_elevation():
    sf = PRESET_LOCATIONS["san_francisco"]
    res = generate_satellite_3d_point_cloud(lat=sf["lat"], lon=sf["lon"], zoom=14, grid_size=32)

    assert res.total_points == 32 * 32
    assert len(res.points_flat) == 32 * 32 * 3
    assert len(res.colors_flat) == 32 * 32 * 3
    assert len(res.semantic_labels) == 32 * 32
    assert res.instant_mesh_triangles == (31 * 31 * 2)
    assert res.elevation_max_m > res.elevation_min_m
    assert "Water_Hydrology" in res.summary_by_class


def test_ai_copilot_openrouter_resolution_and_chat():
    key, src = resolve_openrouter_api_key()
    assert ".env.local" in src or "os.environ" in src or "Not configured" in src

    assert len(AVAILABLE_MODELS) >= 6
    claude = next((m for m in AVAILABLE_MODELS if "claude" in m["id"]), None)
    assert claude is not None

    chat_res = query_openrouter_spatial_copilot(
        prompt="Analyze surface degradation and emergency collision risk",
        model="anthropic/claude-3.5-sonnet",
        telemetry_context={"surface_degradation_index": 0.05, "time_to_impact_s": 1.8},
    )
    assert chat_res["status"] == "success"
    assert "response" in chat_res
    assert len(chat_res["response"]) > 50
