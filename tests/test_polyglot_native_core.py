import numpy as np
import pytest
from fastapi.testclient import TestClient
from workspace.server import app
from spatialforge.native_bridge import (
    get_native_status,
    native_cpp_voxel_filter,
    native_cpp_sor_filter,
    native_rust_benchmark_kitti,
)

client = TestClient(app)


def test_native_subsystems_status():
    status = get_native_status()
    assert "cpp_native" in status
    assert "rust_native" in status
    assert "go_streaming" in status
    assert "python_orchestrator" in status

    # Verify C++ engine is available and active
    assert status["cpp_native"]["available"] is True
    assert "spatialforge-native-cpp" in status["cpp_native"]["version"]

    # Verify Rust engine is built
    assert status["rust_native"]["available"] is True
    assert status["rust_native"]["version"] == "aeovexor-rust-core-2.4.0"

    # Verify Go binary exists
    assert status["go_streaming"]["available"] is True


def test_native_cpp_voxel_filter():
    # 50 points tightly placed in a cube
    pts = np.random.uniform(0.0, 0.2, (50, 4)).astype(np.float32)
    filtered = native_cpp_voxel_filter(pts, leaf_size=0.5)
    assert len(filtered) > 0
    assert len(filtered) < len(pts)


def test_native_cpp_sor_filter():
    pts = np.array([
        [0.0, 0.0, 0.0, 1.0],
        [0.1, 0.0, 0.0, 1.0],
        [0.0, 0.1, 0.0, 1.0],
        [50.0, 50.0, 50.0, 1.0], # Outlier
    ], dtype=np.float32)
    inliers = native_cpp_sor_filter(pts, k=2, std_ratio=1.0)
    assert len(inliers) == 3
    assert not any(p[0] > 10.0 for p in inliers)


def test_native_rust_benchmark_kitti():
    res = native_rust_benchmark_kitti("examples/velodyne_000008.bin")
    assert res["status"] == "success"
    assert "Zero-Copy Parse" in res["output"]
    assert "Voxel Grid Time" in res["output"]


def test_api_native_endpoints():
    # 1. Status
    resp = client.get("/api/native/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["cpp_native"]["available"] is True

    # 2. Voxel API
    voxel_payload = {
        "points": [
            [0.1, 0.1, 0.1, 1.0],
            [0.2, 0.2, 0.2, 1.0],
            [5.0, 5.0, 5.0, 1.0],
        ],
        "leaf_size": 1.0,
    }
    resp = client.post("/api/native/voxel", json=voxel_payload)
    assert resp.status_code == 200
    res_data = resp.json()
    assert res_data["status"] == "success"
    assert res_data["filtered_count"] == 2

    # 3. Rust benchmark API
    bench_payload = {"dataset": "examples/velodyne_000008.bin"}
    resp = client.post("/api/native/rust/benchmark", json=bench_payload)
    assert resp.status_code == 200
    assert resp.json()["status"] == "success"
