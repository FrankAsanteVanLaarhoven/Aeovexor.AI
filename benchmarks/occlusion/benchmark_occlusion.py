"""
Occlusion-Stratified Benchmark Suite
Measures detection robustness and recall degradation across stratified
occlusion tiers: Light (0-20%), Moderate (20-60%), and Heavy (>60%).
"""

from typing import List, Dict, Any
from schemas.spatial_schema import BoundingBox3D, OcclusionProfile
from benchmarks.detection.benchmark_detection import compute_3d_box_iou


class OcclusionBenchmark:
    def __init__(self, match_iou_threshold: float = 0.4):
        self.match_iou_threshold = match_iou_threshold

    def evaluate_stratified_recall(
        self,
        predictions: List[BoundingBox3D],
        ground_truths: List[BoundingBox3D],
        occlusion_profiles: List[OcclusionProfile],
    ) -> Dict[str, Any]:
        """Evaluates detection recall stratified by occlusion percentage."""
        occ_map = {p.object_id: p.occlusion_percentage for p in occlusion_profiles}

        tiers = {
            "light_0_20": {"total": 0, "detected": 0},
            "moderate_20_60": {"total": 0, "detected": 0},
            "heavy_60_100": {"total": 0, "detected": 0},
        }

        for gt in ground_truths:
            occ_val = occ_map.get(gt.id, 0.0)
            if occ_val <= 20.0:
                tier = "light_0_20"
            elif occ_val <= 60.0:
                tier = "moderate_20_60"
            else:
                tier = "heavy_60_100"

            tiers[tier]["total"] += 1

            # Match prediction if same ID or 3D IoU >= match_iou_threshold
            is_matched = any(
                p.id == gt.id or compute_3d_box_iou(p, gt) >= self.match_iou_threshold
                for p in predictions
            )
            if is_matched:
                tiers[tier]["detected"] += 1

        results = {}
        for tier_name, data in tiers.items():
            tot = data["total"]
            det = data["detected"]
            recall = float(det / max(tot, 1) * 100.0) if tot > 0 else 100.0
            results[f"recall_{tier_name}"] = round(recall, 2)
            results[f"count_{tier_name}"] = tot

        return results
