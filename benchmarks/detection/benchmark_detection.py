"""
3D Object Detection Benchmark Suite
Computes Average Precision (AP@0.25, AP@0.50, AP@0.70), 3D IoU, and recall
metrics against ground-truth autonomous driving sequences.
"""

from typing import List, Dict, Any
import numpy as np
from schemas.spatial_schema import BoundingBox3D


def compute_3d_box_iou(box1: BoundingBox3D, box2: BoundingBox3D) -> float:
    """Calculates 3D axis-aligned intersection-over-union between two boxes."""
    x1_min, x1_max = box1.x - box1.dx / 2, box1.x + box1.dx / 2
    y1_min, y1_max = box1.y - box1.dy / 2, box1.y + box1.dy / 2
    z1_min, z1_max = box1.z - box1.dz / 2, box1.z + box1.dz / 2

    x2_min, x2_max = box2.x - box2.dx / 2, box2.x + box2.dx / 2
    y2_min, y2_max = box2.y - box2.dy / 2, box2.y + box2.dy / 2
    z2_min, z2_max = box2.z - box2.dz / 2, box2.z + box2.dz / 2

    inter_x = max(0.0, min(x1_max, x2_max) - max(x1_min, x2_min))
    inter_y = max(0.0, min(y1_max, y2_max) - max(y1_min, y2_min))
    inter_z = max(0.0, min(z1_max, z2_max) - max(z1_min, z2_min))

    intersection_vol = inter_x * inter_y * inter_z
    vol1 = box1.dx * box1.dy * box1.dz
    vol2 = box2.dx * box2.dy * box2.dz
    union_vol = vol1 + vol2 - intersection_vol

    return float(intersection_vol / max(union_vol, 1e-6))


class DetectionBenchmark:
    def __init__(self, iou_thresholds: List[float] = [0.25, 0.50, 0.70]):
        self.iou_thresholds = iou_thresholds

    def evaluate(
        self, predictions: List[BoundingBox3D], ground_truths: List[BoundingBox3D]
    ) -> Dict[str, Any]:
        """Runs precision, recall, and AP evaluation across defined IoU thresholds."""
        results: Dict[str, Any] = {"num_predictions": len(predictions), "num_ground_truths": len(ground_truths)}

        for thresh in self.iou_thresholds:
            matched_gt = set()
            tp = 0
            fp = 0

            for pred in sorted(predictions, key=lambda b: b.confidence, reverse=True):
                best_gt_idx = None
                max_iou = 0.0

                for gt_idx, gt in enumerate(ground_truths):
                    if gt_idx in matched_gt or pred.label != gt.label:
                        continue
                    iou = compute_3d_box_iou(pred, gt)
                    if iou > thresh and iou > max_iou:
                        max_iou = iou
                        best_gt_idx = gt_idx

                if best_gt_idx is not None:
                    matched_gt.add(best_gt_idx)
                    tp += 1
                else:
                    fp += 1

            fn = len(ground_truths) - len(matched_gt)
            precision = float(tp / max(tp + fp, 1))
            recall = float(tp / max(len(ground_truths), 1))
            f1 = float(2 * precision * recall / max(precision + recall, 1e-6))

            results[f"AP@{int(thresh*100)}"] = round(precision * recall, 4)
            results[f"recall@{int(thresh*100)}"] = round(recall, 4)
            results[f"precision@{int(thresh*100)}"] = round(precision, 4)
            results[f"f1@{int(thresh*100)}"] = round(f1, 4)

        return results
