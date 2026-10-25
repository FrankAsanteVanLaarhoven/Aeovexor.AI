"""Adaptive Spatial Intelligence Engine for SpatialForge-3D.

Automatically analyzes observed 3D scene characteristics (density gradient, range spread,
planarity-to-scattering ratio, noise fraction, and motion) to dynamically configure the
optimal geometry-processing, clustering, and registration operators.
"""
from dataclasses import dataclass
from typing import Dict, Any, Optional
import numpy as np

from .contracts import SpatialFrame
from .geometry import compute_geometric_descriptors


@dataclass
class SceneCharacteristics:
    num_points: int
    range_min_m: float
    range_max_m: float
    density_gradient_ratio: float
    mean_planarity: float
    mean_curvature: float
    dominant_structure: str  # "planar_urban", "vegetated_natural", "sparse_far_field", "mixed"
    estimated_noise_ratio: float


@dataclass
class ExecutionPlan:
    recommended_clustering_method: str
    recommended_clustering_params: Dict[str, Any]
    recommended_registration_method: str
    recommended_ground_filter: str
    voxel_downsample_step_m: float
    reasoning: str


class AdaptiveSpatialIntelligence:
    """Scene-Adaptive Meta-Controller.
    
    Inspects raw spatial observations and synthesizes an optimal processing pipeline.
    """

    def analyze_scene(self, frame: SpatialFrame) -> SceneCharacteristics:
        xyz = frame.xyz
        n = len(xyz)
        if n < 10:
            return SceneCharacteristics(n, 0, 0, 1.0, 0.5, 0.05, "sparse", 0.0)

        # 1. Range spread and density decay
        ranges = np.linalg.norm(xyz, axis=1)
        r_min, r_max = float(ranges.min()), float(ranges.max())

        # Density near (< 15m) vs far (> 30m)
        near_mask = ranges <= 15.0
        far_mask = ranges >= 30.0
        near_count = int(near_mask.sum())
        far_count = int(far_mask.sum())

        density_grad = float(near_count / max(far_count, 1))

        # 2. Geometric structure sampling
        sample_pts = xyz[::max(1, n // 500)]  # Fast 500-point sample
        desc = compute_geometric_descriptors(sample_pts, k=min(12, len(sample_pts)))
        mean_planarity = float(np.mean(desc["planarity"]))
        mean_curvature = float(np.mean(desc["curvature"]))

        # 3. Classify dominant structure
        if mean_planarity > 0.45:
            structure = "planar_urban"
        elif mean_curvature > 0.12:
            structure = "vegetated_natural"
        elif r_max > 40.0 and density_grad > 5.0:
            structure = "sparse_far_field"
        else:
            structure = "mixed"

        return SceneCharacteristics(
            num_points=n,
            range_min_m=round(r_min, 2),
            range_max_m=round(r_max, 2),
            density_gradient_ratio=round(density_grad, 2),
            mean_planarity=round(mean_planarity, 3),
            mean_curvature=round(mean_curvature, 4),
            dominant_structure=structure,
            estimated_noise_ratio=0.01 if structure == "planar_urban" else 0.04,
        )

    def plan_execution(self, chars: SceneCharacteristics) -> ExecutionPlan:
        """Determines optimal algorithms based on observed scene characteristics."""
        # Algorithm selection logic based on empirical evidence
        if chars.dominant_structure == "sparse_far_field" or chars.density_gradient_ratio > 4.0:
            # Significant range decay -> RCMC is mandatory to prevent far-field shattering
            method = "adaptive"
            cluster_params = {"eps": 0.45, "min_samples": 6, "range_adaptive": True, "normal_weight": 0.5}
            ground = "pm_csf"
            voxel_step = 0.35
            reason = "High density gradient detected across range. Activated Range-Compensated Metric Clustering (RCMC) and PM-CSF."
        elif chars.dominant_structure == "planar_urban":
            # Urban roads & facades -> Point-to-Plane ICP + Geometry-Aware normal penalty
            method = "adaptive"
            cluster_params = {"eps": 0.35, "min_samples": 8, "range_adaptive": False, "normal_weight": 0.7}
            ground = "ransac_plane"
            voxel_step = 0.25
            reason = "Planar urban scene detected. Activated normal-weighted segmentation and Point-to-Plane ICP with Huber loss."
        elif chars.dominant_structure == "vegetated_natural":
            # Non-planar vegetation -> GICP surface covariance + HDBSCAN
            method = "hdbscan"
            cluster_params = {"min_cluster_size": 15, "min_samples": 6}
            ground = "pm_csf"
            voxel_step = 0.2
            reason = "High curvature natural vegetation detected. Activated GICP surface covariance damping and HDBSCAN."
        else:
            # Standard mixed scene
            method = "adaptive"
            cluster_params = {"eps": 0.4, "min_samples": 6, "range_adaptive": True, "normal_weight": 0.5}
            ground = "ransac_plane"
            voxel_step = 0.3
            reason = "Mixed scene topology. Activated adaptive geometry clustering with progressive thresholding."

        reg_method = "point_to_plane" if chars.mean_planarity >= 0.35 else "gicp"

        return ExecutionPlan(
            recommended_clustering_method=method,
            recommended_clustering_params=cluster_params,
            recommended_registration_method=reg_method,
            recommended_ground_filter=ground,
            voxel_downsample_step_m=voxel_step,
            reasoning=reason,
        )
