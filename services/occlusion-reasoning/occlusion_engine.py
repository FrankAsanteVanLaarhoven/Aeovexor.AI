"""
Occlusion Reasoning Microservice
Computes raycasting line-of-sight visibility and occlusion percentages
between the sensor origin (0, 0, 0) and target 3D bounding boxes.
"""

from typing import List
import numpy as np
from schemas.spatial_schema import BoundingBox3D, OcclusionProfile


class OcclusionEngine:
    def __init__(self, sensor_origin: np.ndarray = np.array([0.0, 0.0, 0.0])):
        self.sensor_origin = sensor_origin

    def compute_occlusion(
        self, target_box: BoundingBox3D, point_cloud: np.ndarray, occluding_boxes: List[BoundingBox3D] = None
    ) -> OcclusionProfile:
        """
        Calculates line-of-sight occlusion percentage of target_box by analyzing
        intervening obstacle volumes between sensor origin and target center.
        """
        target_center = np.array([target_box.x, target_box.y, target_box.z])
        sensor_dist = float(np.linalg.norm(target_center - self.sensor_origin))

        # Points in target box
        x_min, x_max = target_box.x - target_box.dx / 2, target_box.x + target_box.dx / 2
        y_min, y_max = target_box.y - target_box.dy / 2, target_box.y + target_box.dy / 2
        z_min, z_max = target_box.z - target_box.dz / 2, target_box.z + target_box.dz / 2

        in_box = (
            (point_cloud[:, 0] >= x_min)
            & (point_cloud[:, 0] <= x_max)
            & (point_cloud[:, 1] >= y_min)
            & (point_cloud[:, 1] <= y_max)
            & (point_cloud[:, 2] >= z_min)
            & (point_cloud[:, 2] <= z_max)
        )
        visible_points = int(np.sum(in_box))

        # Expected points based on sensor distance (inverse square approximation)
        expected_points = max(int(1500.0 / max(sensor_dist, 1.0)), 15)

        # Check line-of-sight against other boxes closer to sensor
        occlusion_ratio = 0.0
        is_los = True

        if occluding_boxes:
            for obs in occluding_boxes:
                if obs.id == target_box.id:
                    continue
                obs_center = np.array([obs.x, obs.y, obs.z])
                obs_dist = np.linalg.norm(obs_center - self.sensor_origin)

                # If obstacle is between sensor and target
                if obs_dist < sensor_dist:
                    # Projection angle check
                    ray_vec = target_center / sensor_dist
                    obs_proj = np.dot(obs_center, ray_vec)
                    perp_dist = np.linalg.norm(obs_center - obs_proj * ray_vec)

                    if perp_dist < (obs.dx + obs.dy) / 4.0:
                        is_los = False
                        occlusion_ratio = min(occlusion_ratio + 0.45, 1.0)

        measured_ratio = max(0.0, 1.0 - (visible_points / float(expected_points)))
        final_occlusion_pct = float(min(max(occlusion_ratio, measured_ratio) * 100.0, 100.0))

        return OcclusionProfile(
            object_id=target_box.id,
            occlusion_percentage=final_occlusion_pct,
            visible_points=visible_points,
            total_expected_points=expected_points,
            is_line_of_sight=is_los and final_occlusion_pct < 65.0,
        )
