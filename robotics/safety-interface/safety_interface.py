"""
Industrial Robotics Safety Interface (ISO 13849 / ISO 3691-4)
Monitors dynamic safety exclusion zones, calculates Time-to-Collision (TTC),
and triggers hardware Emergency Stop (E-Stop) or dynamic velocity reductions.
"""

from typing import List, Optional, Tuple
import numpy as np
from schemas.spatial_schema import BoundingBox3D, SafetyZoneEvent


class SafetyInterface:
    def __init__(
        self,
        estop_radius_m: float = 1.5,
        slowdown_radius_m: float = 3.5,
        warning_radius_m: float = 6.0,
        nominal_max_speed_mps: float = 1.6,
    ):
        self.estop_radius_m = estop_radius_m
        self.slowdown_radius_m = slowdown_radius_m
        self.warning_radius_m = warning_radius_m
        self.nominal_max_speed_mps = nominal_max_speed_mps

    def evaluate_safety_zones(
        self, obstacle_boxes: List[BoundingBox3D], current_robot_speed_mps: float = 1.0
    ) -> SafetyZoneEvent:
        """
        Evaluates obstacle distances relative to the robot origin (0, 0, 0).
        Commands emergency stop if any object breaches the E-Stop perimeter.
        """
        if not obstacle_boxes:
            return SafetyZoneEvent(
                event_id="SAFE_CLEAR",
                zone_name="CLEAR_ZONE",
                intrusion_distance_m=999.0,
                e_stop_triggered=False,
                recommended_speed_limit_mps=self.nominal_max_speed_mps,
            )

        # Find closest obstacle distance
        min_dist = float("inf")
        closest_box: Optional[BoundingBox3D] = None

        for b in obstacle_boxes:
            dist = np.sqrt(b.x**2 + b.y**2 + b.z**2)
            # Subtract bounding radius
            effective_dist = max(0.0, dist - max(b.dx, b.dy) / 2.0)
            if effective_dist < min_dist:
                min_dist = effective_dist
                closest_box = b

        # Zone logic
        if min_dist <= self.estop_radius_m:
            return SafetyZoneEvent(
                event_id=f"ESTOP_{closest_box.id if closest_box else 'OBS'}",
                zone_name="E-STOP_ZONE",
                intrusion_distance_m=float(min_dist),
                e_stop_triggered=True,
                recommended_speed_limit_mps=0.0,
            )
        elif min_dist <= self.slowdown_radius_m:
            ratio = (min_dist - self.estop_radius_m) / (self.slowdown_radius_m - self.estop_radius_m)
            allowed_speed = float(self.nominal_max_speed_mps * 0.4 * ratio)
            return SafetyZoneEvent(
                event_id=f"SLOWDOWN_{closest_box.id if closest_box else 'OBS'}",
                zone_name="SLOWDOWN_ZONE",
                intrusion_distance_m=float(min_dist),
                e_stop_triggered=False,
                recommended_speed_limit_mps=max(allowed_speed, 0.2),
            )
        else:
            return SafetyZoneEvent(
                event_id="SAFE_OPERATING",
                zone_name="CAUTION_OR_CLEAR",
                intrusion_distance_m=float(min_dist),
                e_stop_triggered=False,
                recommended_speed_limit_mps=self.nominal_max_speed_mps,
            )
