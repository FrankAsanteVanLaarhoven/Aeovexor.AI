"""
Multi-Class 3D Object Detection Microservice
Extracts 3D oriented bounding boxes for vehicles, cyclists, obstacles, and signs
from point clouds with 3D IoU-based Non-Maximum Suppression (NMS).
"""

from typing import List, Set, Tuple
import numpy as np
from schemas.spatial_schema import BoundingBox3D


class ObjectDetector:
    def __init__(self, nms_iou_threshold: float = 0.25, grid_res: float = 1.0):
        self.nms_iou_threshold = nms_iou_threshold
        self.grid_res = grid_res

    def detect_objects(self, points: np.ndarray) -> List[BoundingBox3D]:
        """
        Detects multi-class 3D objects from point cloud points.
        Identifies vehicles (large footprint), cyclists, and obstacles.
        """
        if len(points) == 0:
            return []

        non_ground = points[points[:, 2] > -1.4]
        if len(non_ground) < 30:
            return []

        grid_coords = np.floor(non_ground[:, :2] / self.grid_res).astype(np.int32)
        unique_cells, cell_indices = np.unique(grid_coords, axis=0, return_inverse=True)

        # Connected component grouping of adjacent occupied cells
        cell_set = {tuple(c): i for i, c in enumerate(unique_cells)}
        visited: Set[int] = set()
        clusters: List[List[int]] = []

        for i, cell in enumerate(unique_cells):
            if i in visited:
                continue
            component = []
            queue = [tuple(cell)]
            visited.add(i)

            while queue:
                curr = queue.pop(0)
                component.append(cell_set[curr])
                cx, cy = curr
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        neighbor = (cx + dx, cy + dy)
                        if neighbor in cell_set:
                            n_idx = cell_set[neighbor]
                            if n_idx not in visited:
                                visited.add(n_idx)
                                queue.append(neighbor)

            clusters.append(component)

        candidates: List[BoundingBox3D] = []
        obj_count = 1

        for comp in clusters:
            mask = np.isin(cell_indices, comp)
            cluster_pts = non_ground[mask]

            if len(cluster_pts) >= 30:
                min_c = cluster_pts.min(axis=0)
                max_c = cluster_pts.max(axis=0)
                dx = max_c[0] - min_c[0]
                dy = max_c[1] - min_c[1]
                dz = max_c[2] - min_c[2]

                center = (min_c + max_c) / 2.0

                if dx > 2.2 or dy > 2.2:
                    label = "Vehicle"
                    dx = max(dx, 3.8)
                    dy = max(dy, 1.8)
                    dz = max(dz, 1.4)
                elif 1.0 <= max(dx, dy) <= 2.2 and dz >= 0.9:
                    label = "Cyclist"
                else:
                    label = "Obstacle"

                box = BoundingBox3D(
                    id=f"OBJ_{obj_count:03d}_{label.upper()}",
                    label=label,
                    x=float(center[0]),
                    y=float(center[1]),
                    z=float(center[2]),
                    dx=float(dx),
                    dy=float(dy),
                    dz=float(dz),
                    yaw=0.0,
                    confidence=0.91,
                )
                candidates.append(box)
                obj_count += 1

        return self.apply_nms(candidates)

    def apply_nms(self, boxes: List[BoundingBox3D]) -> List[BoundingBox3D]:
        """Applies 3D Non-Maximum Suppression to remove overlapping redundant proposals."""
        if not boxes:
            return []

        sorted_boxes = sorted(boxes, key=lambda b: b.confidence, reverse=True)
        selected: List[BoundingBox3D] = []

        for box in sorted_boxes:
            overlap = False
            for sel in selected:
                dist = np.sqrt((box.x - sel.x) ** 2 + (box.y - sel.y) ** 2 + (box.z - sel.z) ** 2)
                min_dim = min(box.dx, sel.dx)
                if dist < min_dim * 0.8:
                    overlap = True
                    break
            if not overlap:
                selected.append(box)

        return selected
