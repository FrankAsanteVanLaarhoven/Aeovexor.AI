"""
Aeovexor.AI Robotics Package Initializer
Exposes ROS 2 Bridge and Industrial Safety Interface.
"""

import importlib.util
import sys
from pathlib import Path

_ROBOTICS_DIR = Path(__file__).parent


def _import_from_subpath(module_name: str, rel_path: str):
    file_path = _ROBOTICS_DIR / rel_path
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {file_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


ros2_mod = _import_from_subpath("robotics.ros2_bridge", "ros2-bridge/ros2_bridge.py")
safety_mod = _import_from_subpath("robotics.safety_interface", "safety-interface/safety_interface.py")

ROS2PointCloud2Bridge = ros2_mod.ROS2PointCloud2Bridge
SafetyInterface = safety_mod.SafetyInterface

__all__ = [
    "ROS2PointCloud2Bridge",
    "SafetyInterface",
]
