"""Native C++ and Rust Acceleration Bridge for Aeovexor.AI.

Provides high-performance FFI bindings to C++ SIMD spatial routines and
Rust zero-copy binary LiDAR parsers, with seamless fallback to NumPy.
"""

from __future__ import annotations
import ctypes
import os
import subprocess
from pathlib import Path
from typing import Tuple, Optional
import numpy as np


class C_Point3D(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float),
        ("intensity", ctypes.c_float),
    ]


_CPP_LIB = None
_CPP_LOAD_ERROR = None

def _get_cpp_lib():
    global _CPP_LIB, _CPP_LOAD_ERROR
    if _CPP_LIB is not None:
        return _CPP_LIB
    if _CPP_LOAD_ERROR is not None:
        return None

    # Search paths for libspatialforge_core
    base_dir = Path(__file__).resolve().parent.parent
    candidates = [
        base_dir / "native" / "cpp" / "build" / "libspatialforge_core.dylib",
        base_dir / "native" / "cpp" / "build" / "libspatialforge_core.so",
        base_dir / "native" / "cpp" / "libspatialforge_core.dylib",
        base_dir / "native" / "cpp" / "libspatialforge_core.so",
    ]

    for p in candidates:
        if p.exists():
            try:
                lib = ctypes.CDLL(str(p))
                # Configure signatures
                lib.sf_cpp_version.restype = ctypes.c_char_p
                lib.sf_cpp_voxel_filter.argtypes = [
                    ctypes.POINTER(C_Point3D),
                    ctypes.c_int32,
                    ctypes.c_float,
                    ctypes.POINTER(C_Point3D),
                    ctypes.c_int32,
                ]
                lib.sf_cpp_voxel_filter.restype = ctypes.c_int32

                lib.sf_cpp_sor_filter.argtypes = [
                    ctypes.POINTER(C_Point3D),
                    ctypes.c_int32,
                    ctypes.c_int32,
                    ctypes.c_float,
                    ctypes.POINTER(C_Point3D),
                    ctypes.c_int32,
                ]
                lib.sf_cpp_sor_filter.restype = ctypes.c_int32

                _CPP_LIB = lib
                return _CPP_LIB
            except Exception as e:
                _CPP_LOAD_ERROR = str(e)

    _CPP_LOAD_ERROR = "Library file not found"
    return None


def get_native_status() -> dict:
    """Return operational status of C++, Rust, and Go subsystems."""
    cpp_lib = _get_cpp_lib()
    cpp_version = cpp_lib.sf_cpp_version().decode("utf-8") if cpp_lib else None

    base_dir = Path(__file__).resolve().parent.parent
    rust_cli = base_dir / "native" / "rust" / "target" / "release" / "aeovexor-spatial-cli"
    rust_available = rust_cli.exists()

    go_service = base_dir / "services" / "go-telemetry" / "aeovexor-telemetry-service"
    go_available = go_service.exists()

    return {
        "cpp_native": {
            "available": cpp_lib is not None,
            "version": cpp_version,
            "engine": "AppleClang SIMD C++17",
        },
        "rust_native": {
            "available": rust_available,
            "version": "aeovexor-rust-core-2.4.0",
            "cli_path": str(rust_cli) if rust_available else None,
        },
        "go_streaming": {
            "available": go_available,
            "version": "aeovexor-go-telemetry-2.4.0",
            "binary_path": str(go_service) if go_available else None,
        },
        "python_orchestrator": {
            "status": "FastAPI ASGI Online",
            "framework": "Python 3.11",
        },
    }


def native_cpp_voxel_filter(points: np.ndarray, leaf_size: float = 0.2) -> np.ndarray:
    """Run accelerated C++ voxel grid filter on (N, 3) or (N, 4) point cloud."""
    cpp = _get_cpp_lib()
    if cpp is None or len(points) == 0:
        # Fallback to NumPy
        from spatialforge.core import voxel_grid_sample
        return voxel_grid_sample(points, voxel_size=leaf_size)

    n = len(points)
    in_arr = (C_Point3D * n)()
    for i in range(n):
        in_arr[i].x = float(points[i, 0])
        in_arr[i].y = float(points[i, 1])
        in_arr[i].z = float(points[i, 2])
        in_arr[i].intensity = float(points[i, 3]) if points.shape[1] > 3 else 1.0

    out_arr = (C_Point3D * n)()
    out_count = cpp.sf_cpp_voxel_filter(in_arr, n, ctypes.c_float(leaf_size), out_arr, n)

    if out_count <= 0:
        return points

    result = np.zeros((out_count, points.shape[1]), dtype=np.float32)
    for i in range(out_count):
        result[i, 0] = out_arr[i].x
        result[i, 1] = out_arr[i].y
        result[i, 2] = out_arr[i].z
        if points.shape[1] > 3:
            result[i, 3] = out_arr[i].intensity
    return result


def native_cpp_sor_filter(points: np.ndarray, k: int = 10, std_ratio: float = 1.0) -> np.ndarray:
    """Run accelerated C++ Statistical Outlier Removal (SOR) on point cloud."""
    cpp = _get_cpp_lib()
    if cpp is None or len(points) == 0:
        return points

    n = len(points)
    in_arr = (C_Point3D * n)()
    for i in range(n):
        in_arr[i].x = float(points[i, 0])
        in_arr[i].y = float(points[i, 1])
        in_arr[i].z = float(points[i, 2])
        in_arr[i].intensity = float(points[i, 3]) if points.shape[1] > 3 else 1.0

    out_arr = (C_Point3D * n)()
    out_count = cpp.sf_cpp_sor_filter(in_arr, n, k, ctypes.c_float(std_ratio), out_arr, n)

    if out_count <= 0:
        return points

    result = np.zeros((out_count, points.shape[1]), dtype=np.float32)
    for i in range(out_count):
        result[i, 0] = out_arr[i].x
        result[i, 1] = out_arr[i].y
        result[i, 2] = out_arr[i].z
        if points.shape[1] > 3:
            result[i, 3] = out_arr[i].intensity
    return result


def native_rust_benchmark_kitti(bin_path: str) -> dict:
    """Execute high-speed Rust binary benchmark on KITTI LiDAR dataset."""
    base_dir = Path(__file__).resolve().parent.parent
    rust_cli = base_dir / "native" / "rust" / "target" / "release" / "aeovexor-spatial-cli"

    if not rust_cli.exists():
        return {"status": "unsupported", "message": "Rust CLI binary not yet built"}

    try:
        res = subprocess.run(
            [str(rust_cli), "--benchmark", str(bin_path)],
            capture_output=True,
            text=True,
            check=True,
        )
        return {
            "status": "success",
            "engine": "Rust Native Core v2.4.0",
            "output": res.stdout,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
