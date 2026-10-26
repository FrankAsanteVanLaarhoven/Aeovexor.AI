"""
Human Segmentation Microservice
Isolates human point cloud clusters and generates binary segmentation masks
differentiating pedestrians from static background terrain and vehicles.
"""

from typing import Tuple
import numpy as np
from schemas.spatial_schema import BoundingBox3D


class HumanSegmentor:
    def __init__(self, margin_m: float = 0.15):
        self.margin_m = margin_m

    def segment_human_points(
        self, cloud_points: np.ndarray, person_box: BoundingBox3D
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extracts indices and 3D points strictly enclosed within the person's bounding cylinder/box.
        Returns (human_points, background_points).
        """
        if len(cloud_points) == 0:
            return np.empty((0, 3)), np.empty((0, 3))

        x_min = person_box.x - (person_box.dx / 2.0 + self.margin_m)
        x_max = person_box.x + (person_box.dx / 2.0 + self.margin_m)
        y_min = person_box.y - (person_box.dy / 2.0 + self.margin_m)
        y_max = person_box.y + (person_box.dy / 2.0 + self.margin_m)
        z_min = person_box.z - (person_box.dz / 2.0 + self.margin_m)
        z_max = person_box.z + (person_box.dz / 2.0 + self.margin_m)

        in_x = (cloud_points[:, 0] >= x_min) & (cloud_points[:, 0] <= x_max)
        in_y = (cloud_points[:, 1] >= y_min) & (cloud_points[:, 1] <= y_max)
        in_z = (cloud_points[:, 2] >= z_min) & (cloud_points[:, 2] <= z_max)

        mask = in_x & in_y & in_z
        human_pts = cloud_points[mask]
        bg_pts = cloud_points[~mask]

        return human_pts, bg_pts
