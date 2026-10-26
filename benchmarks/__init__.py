"""
Aeovexor.AI Benchmarking Package Initializer
Exposes detection, pose, occlusion, calibration, and privacy benchmark suites.
"""

from .detection.benchmark_detection import DetectionBenchmark, compute_3d_box_iou
from .pose.benchmark_pose import PoseBenchmark
from .occlusion.benchmark_occlusion import OcclusionBenchmark
from .calibration.benchmark_calibration import CalibrationBenchmark
from .privacy.benchmark_privacy import PrivacyBenchmark

__all__ = [
    "DetectionBenchmark",
    "compute_3d_box_iou",
    "PoseBenchmark",
    "OcclusionBenchmark",
    "CalibrationBenchmark",
    "PrivacyBenchmark",
]
