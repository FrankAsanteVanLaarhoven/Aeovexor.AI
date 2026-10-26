"""
Person Detection Microservice
Extracts 3D human / pedestrian bounding boxes from spatial point clouds
based on height, density, and geometric aspect ratios.
"""

from typing import List, Optional, Set, Dict, Tuple
import numpy as np
from schemas.spatial_schema import BoundingBox3D


class PersonDetector:
    def __init__(
        self,
        min_height: float = 1.1,
        max_height: float = 2.2,
        min_width: float = 0.25,
        max_width: float = 1.1,
        min_cluster_points: int = 15,
        grid_res: float = 0.5,
    ):
        self.min_height = min_height
        self.max_height = max_height
        self.min_width = min_width
        self.max_width = max_width
        self.min_cluster_points = min_cluster_points
        self.grid_res = grid_res

    def detect_persons_from_cloud(
        self, points: np.ndarray, cluster_distance_thresh: float = 0.5
    ) -> List[BoundingBox3D]:
        """
        Detects 3D person bounding boxes from point cloud points.
        Uses connected-component spatial occupancy clustering and humanoid aspect filtering.
        """
        if len(points) == 0:
            return []

        boxes: List[BoundingBox3D] = []
        non_ground = points[points[:, 2] > -1.4]
        if len(non_ground) < self.min_cluster_points:
            return []

        # Quantize onto 2D spatial grid
        grid_coords = np.floor(non_ground[:, :2] / self.grid_res).astype(np.int32)
        unique_cells, cell_indices = np.unique(grid_coords, axis=0, return_inverse=True)

        # Build cell lookup and graph adjacency
        cell_set = {tuple(c): i for i, c in enumerate(unique_cells)}
        visited: Set[int] = set()
        clusters: List[List[int]] = []

        for i, cell in enumerate(unique_cells):
            if i in visited:
                continue
            # BFS connected component
            component = []
            queue = [tuple(cell)]
            visited.add(i)

            while queue:
                curr = queue.pop(0)
                component.append(cell_set[curr])
                cx, cy = curr
                # 8-connected neighbors
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        neighbor = (cx + dx, cy + dy)
                        if neighbor in cell_set:
                            n_idx = cell_set[neighbor]
                            if n_idx not in visited:
                                visited.add(n_idx)
                                queue.append(neighbor)

            clusters.append(component)

        idx_counter = 1
        for comp in clusters:
            # Aggregate all points in component
            mask = np.isin(cell_indices, comp)
            cluster_pts = non_ground[mask]

            if len(cluster_pts) >= self.min_cluster_points:
                min_c = cluster_pts.min(axis=0)
                max_c = cluster_pts.max(axis=0)
                dx = max_c[0] - min_c[0]
                dy = max_c[1] - min_c[1]
                dz = max_c[2] - min_c[2]

                width = max(dx, dy)
                if (
                    self.min_height <= dz <= self.max_height
                    and self.min_width <= width <= self.max_width
                ):
                    center = (min_c + max_c) / 2.0
                    box = BoundingBox3D(
                        id=f"PED_{idx_counter:03d}",
                        label="Person",
                        x=float(center[0]),
                        y=float(center[1]),
                        z=float(center[2]),
                        dx=float(max(dx, 0.45)),
                        dy=float(max(dy, 0.45)),
                        dz=float(dz),
                        yaw=0.0,
                        confidence=min(0.70 + (len(cluster_pts) / 100.0) * 0.25, 0.98),
                    )
                    boxes.append(box)
                    idx_counter += 1

        return boxes
