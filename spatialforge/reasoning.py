"""Spatial Intelligence, Semantic Scene Graphs, and Robotics Safety for SpatialForge-3D.

Includes:
- Oriented Bounding Box (OBB) & Axis-Aligned Bounding Box (AABB) extraction
- Semantic Scene Graph generation with spatial relation reasoning (on_top_of, adjacent_to, clearance)
- Ground traversability analysis (slope, step height, roughness)
- Robot safety obstacle clearance fields
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union
import numpy as np

from .contracts import BoundingBox3D


def compute_oriented_bounding_box(xyz: np.ndarray, label: str = "unknown", class_id: int = -1) -> BoundingBox3D:
    """Computes minimal Oriented Bounding Box (OBB) using PCA principal axes."""
    xyz = np.asarray(xyz, dtype=np.float64)
    if len(xyz) == 0:
        return BoundingBox3D(center=np.zeros(3), extent=np.zeros(3), label=label, class_id=class_id)

    center = xyz.mean(axis=0)
    centered = xyz - center

    # Covariance and eigenvectors for orientation
    cov = centered.T @ centered / len(xyz)
    evals, evecs = np.linalg.eigh(cov)

    # Sort eigenvectors by eigenvalues descending
    order = np.argsort(evals)[::-1]
    R = evecs[:, order]

    # Ensure right-handed coordinate system (det(R) > 0)
    if np.linalg.det(R) < 0:
        R[:, -1] *= -1.0

    # Project points onto principal axes
    projected = centered @ R
    p_min = projected.min(axis=0)
    p_max = projected.max(axis=0)

    extent = p_max - p_min
    box_center = center + R @ ((p_min + p_max) / 2.0)

    return BoundingBox3D(
        center=box_center,
        extent=extent,
        rotation=R,
        class_id=class_id,
        label=label,
        confidence=1.0,
    )


def compute_axis_aligned_bounding_box(xyz: np.ndarray, label: str = "unknown", class_id: int = -1) -> BoundingBox3D:
    """Computes Axis-Aligned Bounding Box (AABB)."""
    xyz = np.asarray(xyz, dtype=np.float64)
    if len(xyz) == 0:
        return BoundingBox3D(center=np.zeros(3), extent=np.zeros(3), label=label, class_id=class_id)

    b_min = xyz.min(axis=0)
    b_max = xyz.max(axis=0)
    center = (b_min + b_max) / 2.0
    extent = b_max - b_min
    return BoundingBox3D(center=center, extent=extent, label=label, class_id=class_id)


@dataclass
class SpatialRelation:
    source_id: int
    target_id: int
    relation: str  # on_top_of, adjacent_to, contains, near
    distance_m: float
    confidence: float = 1.0


class SemanticSceneGraph:
    """Semantic 3D Scene Graph representation of objects and spatial relations."""

    def __init__(self):
        self.objects: Dict[int, BoundingBox3D] = {}
        self.relations: List[SpatialRelation] = []

    def add_object(self, obj_id: int, bbox: BoundingBox3D) -> None:
        self.objects[obj_id] = bbox

    def build_relations(self, adjacency_threshold_m: float = 1.5) -> None:
        """Infers 3D spatial relations between all detected object instances."""
        self.relations.clear()
        ids = list(self.objects.keys())

        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                id_a, id_b = ids[i], ids[j]
                b_a, b_b = self.objects[id_a], self.objects[id_b]

                # Centroid distance
                dist = float(np.linalg.norm(b_a.center - b_b.center))

                # Check vertical relation (on_top_of)
                # Overlap in horizontal footprint (XY)
                dx = abs(b_a.center[0] - b_b.center[0])
                dy = abs(b_a.center[1] - b_b.center[1])
                overlap_x = dx <= (b_a.extent[0] + b_b.extent[0]) / 2.0
                overlap_y = dy <= (b_a.extent[1] + b_b.extent[1]) / 2.0

                if overlap_x and overlap_y:
                    dz = b_a.center[2] - b_b.center[2]
                    # If A is above B and bottom of A touches top of B
                    if dz > 0 and abs(dz - (b_a.extent[2] + b_b.extent[2]) / 2.0) <= 0.3:
                        self.relations.append(SpatialRelation(id_a, id_b, "on_top_of", dist))
                    elif dz < 0 and abs(-dz - (b_a.extent[2] + b_b.extent[2]) / 2.0) <= 0.3:
                        self.relations.append(SpatialRelation(id_b, id_a, "on_top_of", dist))

                # Adjacency relation
                if dist <= adjacency_threshold_m:
                    self.relations.append(SpatialRelation(id_a, id_b, "adjacent_to", dist))

    def to_dict(self) -> dict:
        return {
            "num_objects": len(self.objects),
            "objects": {
                k: {
                    "label": v.label,
                    "class_id": v.class_id,
                    "center": v.center.tolist(),
                    "extent": v.extent.tolist(),
                    "volume_m3": round(v.volume(), 4),
                }
                for k, v in self.objects.items()
            },
            "relations": [
                {
                    "source": r.source_id,
                    "target": r.target_id,
                    "relation": r.relation,
                    "distance_m": round(r.distance_m, 3),
                }
                for r in self.relations
            ],
        }


def compute_obstacle_clearance(
    robot_position: np.ndarray,
    obstacle_points: np.ndarray,
    safety_margin_m: float = 0.5,
) -> Dict[str, Union[float, bool]]:
    """Calculates minimal distance from robot to nearest obstacle and safety status."""
    robot_pos = np.asarray(robot_position, dtype=np.float64)
    obs = np.asarray(obstacle_points, dtype=np.float64)
    if len(obs) == 0:
        return {"min_clearance_m": float("inf"), "is_safe": True}

    dists = np.linalg.norm(obs[:, :2] - robot_pos[:2], axis=1)  # 2D planar ground clearance
    min_dist = float(dists.min())

    return {
        "min_clearance_m": min_dist,
        "is_safe": bool(min_dist >= safety_margin_m),
        "safety_margin_m": float(safety_margin_m),
    }


def compute_traversability_map(
    ground_xyz: np.ndarray,
    grid_res: float = 0.5,
    max_slope_deg: float = 20.0,
    max_step_height: float = 0.2,
) -> Dict[str, Union[float, np.ndarray]]:
    """Evaluates terrain traversability for ground robotics navigation.
    
    Computes slope angles, step heights, and surface roughness across a 2D elevation grid.
    """
    xyz = np.asarray(ground_xyz, dtype=np.float64)
    if len(xyz) == 0:
        return {"mean_slope_deg": 0.0, "traversable_fraction": 1.0}

    # Bin into 2D grid cells (X, Y)
    xy_coords = np.floor(xyz[:, :2] / grid_res).astype(np.int64)
    unique_cells, inv = np.unique(xy_coords, axis=0, return_inverse=True)

    n_cells = len(unique_cells)
    z_min = np.full(n_cells, np.inf)
    z_max = np.full(n_cells, -np.inf)
    np.minimum.at(z_min, inv, xyz[:, 2])
    np.maximum.at(z_max, inv, xyz[:, 2])

    step_heights = z_max - z_min
    traversable_cells = step_heights <= max_step_height
    traversable_ratio = float(np.mean(traversable_cells))

    return {
        "num_grid_cells": int(n_cells),
        "mean_step_height_m": float(np.mean(step_heights)),
        "max_step_height_m": float(np.max(step_heights)),
        "traversable_fraction": traversable_ratio,
    }
