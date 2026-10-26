"""
3D Human Pose Benchmark Suite
Computes Mean Per Joint Position Error (MPJPE in mm) and Percentage of Correct Keypoints (PCK).
"""

from typing import List, Dict, Any
import numpy as np
from schemas.spatial_schema import Pose3D


class PoseBenchmark:
    def __init__(self, pck_threshold_mm: float = 150.0):
        self.pck_threshold_mm = pck_threshold_mm

    def evaluate_poses(self, estimated_poses: List[Pose3D], ground_truth_poses: List[Pose3D]) -> Dict[str, Any]:
        """Calculates MPJPE (mm) and PCK across paired 3D human pose skeletons."""
        if not estimated_poses or not ground_truth_poses:
            return {"mpjpe_mm": 0.0, "pck_pct": 100.0, "evaluated_joints": 0}

        errors_mm = []
        pck_correct = 0
        total_joints = 0

        gt_map = {p.person_id: p for p in ground_truth_poses}

        for est in estimated_poses:
            if est.person_id not in gt_map:
                continue
            gt = gt_map[est.person_id]
            gt_kp_map = {kp.name: kp for kp in gt.keypoints}

            for kp in est.keypoints:
                if kp.name in gt_kp_map:
                    gt_kp = gt_kp_map[kp.name]
                    dist_m = np.sqrt(
                        (kp.x - gt_kp.x) ** 2 + (kp.y - gt_kp.y) ** 2 + (kp.z - gt_kp.z) ** 2
                    )
                    dist_mm = dist_m * 1000.0
                    errors_mm.append(dist_mm)
                    total_joints += 1
                    if dist_mm <= self.pck_threshold_mm:
                        pck_correct += 1

        mpjpe = float(np.mean(errors_mm)) if errors_mm else 0.0
        pck = float((pck_correct / max(total_joints, 1)) * 100.0)

        return {
            "mpjpe_mm": round(mpjpe, 2),
            "pck_pct": round(pck, 2),
            "total_evaluated_joints": total_joints,
            "threshold_mm": self.pck_threshold_mm,
        }
