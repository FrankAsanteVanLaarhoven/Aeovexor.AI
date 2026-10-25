"""AEOVEXOR: Universal Research Testbed & Versioned Algorithm Suite.

Provides standardized input/output contracts for registering and executing
competing 3D spatial perception, registration, SLAM, and surface reconstruction
algorithms as independent modular experimental plugins.
"""
from enum import Enum
import hashlib
import time
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import numpy as np

from .contracts import SpatialFrame, FrameMetadata
from .geometry import (
    voxel_downsample,
    statistical_outlier_removal,
    estimate_normals,
    ransac_plane,
    compute_geometric_descriptors,
)
from .advanced_math import range_compensated_clustering, progressive_morphological_ground_filter
from .registration import icp_point_to_point, icp_point_to_plane, gicp_registration
from .slam import LiDAROdometry
from .benchmarks import evaluate_clustering, evaluate_trajectory


class PluginCategory(str, Enum):
    CLUSTERING = "clustering"
    REGISTRATION = "registration"
    SLAM = "slam"
    RECONSTRUCTION = "reconstruction"
    FILTERING = "filtering"
    GROUND_FILTER = "ground_filter"
    SEGMENTATION = "segmentation"


class PluginMetadata:
    def __init__(
        self,
        name: str,
        version: str,
        category: PluginCategory,
        description: str,
        author: str = "AEOVEXOR Core",
        dependencies: Optional[List[str]] = None,
        default_params: Optional[Dict[str, Any]] = None,
        aliases: Optional[List[str]] = None,
    ):
        self.name = name
        self.version = version
        self.category = category
        self.description = description
        self.author = author
        self.dependencies = dependencies or []
        self.default_params = default_params or {}
        self.aliases = aliases or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "category": self.category.value,
            "description": self.description,
            "author": self.author,
            "dependencies": self.dependencies,
            "default_params": self.default_params,
            "aliases": self.aliases,
        }


class PluginOutputContract:
    def __init__(
        self,
        plugin_name: str,
        category: PluginCategory,
        success: bool,
        latency_ms: float,
        metrics: Dict[str, Any],
        labels: Optional[np.ndarray] = None,
        transform: Optional[np.ndarray] = None,
        trajectory: Optional[np.ndarray] = None,
        filtered_frame: Optional[SpatialFrame] = None,
        mesh_vertices: Optional[np.ndarray] = None,
        mesh_faces: Optional[np.ndarray] = None,
        provenance_hash: Optional[str] = None,
    ):
        self.plugin_name = plugin_name
        self.category = category
        self.success = success
        self.latency_ms = latency_ms
        self.metrics = metrics
        self.labels = labels
        self.transform = transform
        self.trajectory = trajectory
        self.filtered_frame = filtered_frame
        self.mesh_vertices = mesh_vertices
        self.mesh_faces = mesh_faces
        self.provenance_hash = provenance_hash or ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plugin_name": self.plugin_name,
            "category": self.category.value,
            "success": self.success,
            "latency_ms": round(self.latency_ms, 2),
            "metrics": self.metrics,
            "has_labels": self.labels is not None,
            "has_transform": self.transform is not None,
            "has_trajectory": self.trajectory is not None,
            "has_mesh": self.mesh_vertices is not None,
            "provenance_hash": self.provenance_hash,
        }


class PluginInterface:
    """Base interface for all versioned AEOVEXOR algorithms."""

    metadata: PluginMetadata

    def execute(self, frame: SpatialFrame, **kwargs) -> PluginOutputContract:
        raise NotImplementedError


class PluginRegistry:
    """Universal Plugin Registry for AEOVEXOR Research Testbed."""

    def __init__(self):
        self._plugins: Dict[str, PluginInterface] = {}
        self._aliases: Dict[str, str] = {}
        self._register_builtins()

    def register(self, plugin: PluginInterface):
        name = plugin.metadata.name
        self._plugins[name] = plugin
        for alias in getattr(plugin.metadata, "aliases", []):
            self._aliases[alias] = name

    def get(self, name: str) -> Optional[PluginInterface]:
        if name in self._plugins:
            return self._plugins[name]
        canonical = self._aliases.get(name)
        if canonical and canonical in self._plugins:
            return self._plugins[canonical]
        return None

    def list_plugins(self, category: Optional[PluginCategory] = None) -> List[Dict[str, Any]]:
        results = []
        for p in self._plugins.values():
            if category is None or p.metadata.category == category:
                results.append(p.metadata.to_dict())
        return results

    def execute(self, name: str, frame: SpatialFrame, **kwargs) -> PluginOutputContract:
        plugin = self.get(name)
        if not plugin:
            raise KeyError(f"Plugin '{name}' not found in registry")
        return plugin.execute(frame, **kwargs)

    def compare_plugins(
        self,
        plugin_names: List[str],
        frame: SpatialFrame,
        ground_truth: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Runs competing algorithms on the identical dataset side-by-side with cryptographic provenance."""
        results = {}
        comparison_matrix = []

        for name in plugin_names:
            plugin_obj = self.get(name)
            if not plugin_obj:
                continue
            out = self.execute(name, frame, **kwargs)
            results[name] = out
            entry = {
                "plugin": name,
                "version": plugin_obj.metadata.version,
                "category": plugin_obj.metadata.category.value,
                "latency_ms": out.latency_ms,
                "success": out.success,
                **out.metrics,
            }
            comparison_matrix.append(entry)

        return {
            "dataset_points": len(frame),
            "dataset_provenance": frame.metadata.provenance_hash,
            "compared_plugins": plugin_names,
            "comparison_matrix": comparison_matrix,
            "detailed_outputs": {k: v.to_dict() for k, v in results.items()},
        }

    def _register_builtins(self):
        # 1. AEOVEXOR Adaptive Range-Compensated Clustering
        self.register(RCMCPlugin())
        # 2. AEOVEXOR Euclidean Density Clustering Baseline
        self.register(DBSCANPlugin())
        # 3. AEOVEXOR Anisotropic Generalized ICP
        self.register(GICPPlugin())
        # 4. AEOVEXOR Rigid Point-to-Point ICP Baseline
        self.register(PointToPointICPPlugin())
        # 5. AEOVEXOR Progressive Morphological Terrain Filter
        self.register(PMCSFGroundPlugin())
        # 6. AEOVEXOR Geometric Planar Segmentation Baseline
        self.register(RANSACGroundPlugin())
        # 7. AEOVEXOR Scan-to-Submap LiDAR Odometry
        self.register(LiDARSLAMPlugin())
        # 8. AEOVEXOR TSDF Volumetric Reconstruction
        self.register(TSDFReconstructionPlugin())
        # 9. AEOVEXOR Statistical Outlier Filter
        self.register(SORFilterPlugin())


# --- Builtin Native Plugins ---

class RCMCPlugin(PluginInterface):
    def __init__(self):
        self.metadata = PluginMetadata(
            name="aeovexor_rcmc",
            version="0.3.0",
            category=PluginCategory.CLUSTERING,
            description="Adaptive Range-Compensated Metric Clustering solving 1/r^2 beam divergence",
            author="AEOVEXOR Perception Lab",
            dependencies=["numpy", "scipy"],
            default_params={"base_eps": 0.45, "min_samples": 6, "normal_weight": 0.5},
            aliases=["spatialforge_rcmc"],
        )

    def execute(self, frame: SpatialFrame, **kwargs) -> PluginOutputContract:
        t0 = time.perf_counter()
        eps = kwargs.get("base_eps", self.metadata.default_params["base_eps"])
        k = kwargs.get("min_samples", self.metadata.default_params["min_samples"])
        w_n = kwargs.get("normal_weight", self.metadata.default_params["normal_weight"])

        labels = range_compensated_clustering(frame.xyz, base_eps=eps, min_samples=k, normal_weight=w_n)
        latency = (time.perf_counter() - t0) * 1000.0

        num_clusters = len(set(labels) - {-1})
        noise_frac = float(np.mean(labels == -1))
        h = hashlib.sha256(labels.tobytes()).hexdigest()

        return PluginOutputContract(
            plugin_name=self.metadata.name,
            category=self.metadata.category,
            success=True,
            latency_ms=latency,
            metrics={"num_clusters": num_clusters, "noise_fraction": round(noise_frac, 4)},
            labels=labels,
            provenance_hash=h,
        )


class DBSCANPlugin(PluginInterface):
    def __init__(self):
        self.metadata = PluginMetadata(
            name="aeovexor_dbscan",
            version="0.3.0",
            category=PluginCategory.CLUSTERING,
            description="Classical Euclidean Fixed-Radius Density Clustering baseline",
            author="AEOVEXOR Perception Lab",
            dependencies=["scikit-learn"],
            default_params={"eps": 0.45, "min_samples": 6},
            aliases=["open3d_dbscan"],
        )

    def execute(self, frame: SpatialFrame, **kwargs) -> PluginOutputContract:
        from sklearn.cluster import DBSCAN

        t0 = time.perf_counter()
        eps = kwargs.get("eps", self.metadata.default_params["eps"])
        k = kwargs.get("min_samples", self.metadata.default_params["min_samples"])

        labels = DBSCAN(eps=eps, min_samples=k).fit_predict(frame.xyz)
        latency = (time.perf_counter() - t0) * 1000.0

        num_clusters = len(set(labels) - {-1})
        noise_frac = float(np.mean(labels == -1))
        h = hashlib.sha256(labels.tobytes()).hexdigest()

        return PluginOutputContract(
            plugin_name=self.metadata.name,
            category=self.metadata.category,
            success=True,
            latency_ms=latency,
            metrics={"num_clusters": num_clusters, "noise_fraction": round(noise_frac, 4)},
            labels=labels,
            provenance_hash=h,
        )


class GICPPlugin(PluginInterface):
    def __init__(self):
        self.metadata = PluginMetadata(
            name="aeovexor_gicp",
            version="0.3.0",
            category=PluginCategory.REGISTRATION,
            description="Generalized Anisotropic ICP with Huber M-estimator weighting",
            author="AEOVEXOR Perception Lab",
            dependencies=["numpy", "scipy"],
            default_params={"max_distance": 1.0, "max_iterations": 40},
            aliases=["spatialforge_gicp"],
        )

    def execute(self, frame: SpatialFrame, **kwargs) -> PluginOutputContract:
        target = kwargs.get("target_frame")
        if target is None:
            from scipy.spatial.transform import Rotation
            R_gt = Rotation.from_euler("xyz", [1.5, -2.0, 3.0], degrees=True).as_matrix()
            t_gt = np.array([0.10, -0.05, 0.02])
            dst = (frame.xyz @ R_gt.T) + t_gt
        else:
            dst = target.xyz

        t0 = time.perf_counter()
        T, info = gicp_registration(frame.xyz, dst, max_distance=kwargs.get("max_distance", 1.0))
        latency = (time.perf_counter() - t0) * 1000.0

        rmse = info.get("inlier_rmse_m", info.get("rmse", 0.0))
        return PluginOutputContract(
            plugin_name=self.metadata.name,
            category=self.metadata.category,
            success=True,
            latency_ms=latency,
            metrics={"rmse": round(float(rmse), 5), "iterations": int(info.get("iterations", 0))},
            transform=T,
            provenance_hash=hashlib.sha256(T.tobytes()).hexdigest(),
        )


class PointToPointICPPlugin(PluginInterface):
    def __init__(self):
        self.metadata = PluginMetadata(
            name="aeovexor_p2p",
            version="0.3.0",
            category=PluginCategory.REGISTRATION,
            description="Standard Rigid Point-to-Point ICP alignment baseline",
            author="AEOVEXOR Perception Lab",
            dependencies=["numpy", "scipy"],
            default_params={"max_distance": 1.0, "max_iterations": 40},
            aliases=["open3d_icp_p2p"],
        )

    def execute(self, frame: SpatialFrame, **kwargs) -> PluginOutputContract:
        target = kwargs.get("target_frame")
        if target is None:
            from scipy.spatial.transform import Rotation
            R_gt = Rotation.from_euler("xyz", [1.5, -2.0, 3.0], degrees=True).as_matrix()
            t_gt = np.array([0.10, -0.05, 0.02])
            dst = (frame.xyz @ R_gt.T) + t_gt
        else:
            dst = target.xyz

        t0 = time.perf_counter()
        T, info = icp_point_to_point(frame.xyz, dst, max_distance=kwargs.get("max_distance", 1.0))
        latency = (time.perf_counter() - t0) * 1000.0

        rmse = info.get("inlier_rmse_m", info.get("rmse", 0.0))
        return PluginOutputContract(
            plugin_name=self.metadata.name,
            category=self.metadata.category,
            success=True,
            latency_ms=latency,
            metrics={"rmse": round(float(rmse), 5), "iterations": int(info.get("iterations", 0))},
            transform=T,
            provenance_hash=hashlib.sha256(T.tobytes()).hexdigest(),
        )


class PMCSFGroundPlugin(PluginInterface):
    def __init__(self):
        self.metadata = PluginMetadata(
            name="aeovexor_pmcsf",
            version="0.3.0",
            category=PluginCategory.GROUND_FILTER,
            description="Progressive Morphological Ground Filter for complex ramps, slopes, and terrain",
            author="AEOVEXOR Perception Lab",
            dependencies=["numpy", "scipy"],
            default_params={"cell_size": 1.0, "max_window_size": 15.0},
            aliases=["spatialforge_pmcsf"],
        )

    def execute(self, frame: SpatialFrame, **kwargs) -> PluginOutputContract:
        t0 = time.perf_counter()
        ground_mask, obstacle_mask = progressive_morphological_ground_filter(frame.xyz)
        latency = (time.perf_counter() - t0) * 1000.0

        labels = np.zeros(len(frame), dtype=np.int32)
        labels[obstacle_mask] = 1

        return PluginOutputContract(
            plugin_name=self.metadata.name,
            category=self.metadata.category,
            success=True,
            latency_ms=latency,
            metrics={"ground_points": int(ground_mask.sum()), "non_ground_points": int(obstacle_mask.sum())},
            labels=labels,
            filtered_frame=frame.filter_mask(ground_mask),
            provenance_hash=hashlib.sha256(labels.tobytes()).hexdigest(),
        )


class RANSACGroundPlugin(PluginInterface):
    def __init__(self):
        self.metadata = PluginMetadata(
            name="aeovexor_ransac",
            version="0.3.0",
            category=PluginCategory.GROUND_FILTER,
            description="Geometric Planar RANSAC ground surface extraction baseline",
            author="AEOVEXOR Perception Lab",
            dependencies=["numpy"],
            default_params={"distance_threshold": 0.25, "max_iterations": 200},
            aliases=["open3d_ransac_plane"],
        )

    def execute(self, frame: SpatialFrame, **kwargs) -> PluginOutputContract:
        t0 = time.perf_counter()
        plane, inliers = ransac_plane(frame.xyz, distance_threshold=0.25, max_iterations=200)
        latency = (time.perf_counter() - t0) * 1000.0

        labels = np.zeros(len(frame), dtype=np.int32)
        labels[inliers] = 1

        return PluginOutputContract(
            plugin_name=self.metadata.name,
            category=self.metadata.category,
            success=True,
            latency_ms=latency,
            metrics={"ground_inliers": int(inliers.sum()), "plane_equation": [round(float(v), 3) for v in plane]},
            labels=labels,
            filtered_frame=frame.filter_mask(inliers),
            provenance_hash=hashlib.sha256(labels.tobytes()).hexdigest(),
        )


class LiDARSLAMPlugin(PluginInterface):
    def __init__(self):
        self.metadata = PluginMetadata(
            name="aeovexor_slam",
            version="0.3.0",
            category=PluginCategory.SLAM,
            description="Scan-to-submap LiDAR Odometry with dynamic thresholding and voxel hash map",
            author="AEOVEXOR Navigation Lab",
            dependencies=["numpy", "scipy"],
            default_params={"voxel_size": 0.35, "max_range": 50.0},
            aliases=["kiss_icp_odometry"],
        )

    def execute(self, frame: SpatialFrame, **kwargs) -> PluginOutputContract:
        slam = LiDAROdometry(voxel_size=0.35, max_range=50.0)
        t0 = time.perf_counter()
        T, metrics = slam.step(frame.xyz, timestamp_ns=frame.metadata.timestamp_ns)
        latency = (time.perf_counter() - t0) * 1000.0

        return PluginOutputContract(
            plugin_name=self.metadata.name,
            category=self.metadata.category,
            success=True,
            latency_ms=latency,
            metrics={"map_points": len(slam.get_accumulated_map()), "rmse": round(float(metrics.get("rmse", 0.0)), 4)},
            transform=T,
            trajectory=slam.get_trajectory(),
            provenance_hash=hashlib.sha256(T.tobytes()).hexdigest(),
        )


class TSDFReconstructionPlugin(PluginInterface):
    def __init__(self):
        self.metadata = PluginMetadata(
            name="aeovexor_tsdf",
            version="0.3.0",
            category=PluginCategory.RECONSTRUCTION,
            description="Truncated Signed Distance Function (TSDF) raycast volumetric surface reconstruction",
            author="AEOVEXOR Geometry Lab",
            dependencies=["numpy"],
            default_params={"voxel_size": 0.25, "truncation_m": 0.5},
            aliases=["spatialforge_tsdf"],
        )

    def execute(self, frame: SpatialFrame, **kwargs) -> PluginOutputContract:
        from .reconstruction import TSDFVolume

        t0 = time.perf_counter()
        min_b = frame.xyz.min(axis=0) - 0.5
        max_b = frame.xyz.max(axis=0) + 0.5
        tsdf = TSDFVolume(min_b, max_b, voxel_size=0.3, truncation_margin=0.6)
        tsdf.integrate_points(frame.xyz[:2000], sensor_origin=np.array([0, 0, 1.8]))
        verts, faces = tsdf.extract_mesh()
        latency = (time.perf_counter() - t0) * 1000.0

        return PluginOutputContract(
            plugin_name=self.metadata.name,
            category=self.metadata.category,
            success=True,
            latency_ms=latency,
            metrics={"mesh_vertices": len(verts), "mesh_faces": len(faces)},
            mesh_vertices=verts,
            mesh_faces=faces,
            provenance_hash=hashlib.sha256(verts.tobytes()).hexdigest(),
        )


class SORFilterPlugin(PluginInterface):
    def __init__(self):
        self.metadata = PluginMetadata(
            name="aeovexor_sor",
            version="0.3.0",
            category=PluginCategory.FILTERING,
            description="Statistical Outlier Removal (SOR) Gaussian kNN distance filter",
            author="AEOVEXOR Geometry Lab",
            dependencies=["scipy"],
            default_params={"k": 16, "std_ratio": 1.5},
            aliases=["pcl_statistical_outlier_removal"],
        )

    def execute(self, frame: SpatialFrame, **kwargs) -> PluginOutputContract:
        t0 = time.perf_counter()
        inlier_mask, mean_distances = statistical_outlier_removal(frame.xyz, k=16, std_ratio=1.5)
        latency = (time.perf_counter() - t0) * 1000.0

        return PluginOutputContract(
            plugin_name=self.metadata.name,
            category=self.metadata.category,
            success=True,
            latency_ms=latency,
            metrics={"inliers": int(inlier_mask.sum()), "outliers_removed": int((~inlier_mask).sum())},
            labels=inlier_mask.astype(np.int32),
            filtered_frame=frame.filter_mask(inlier_mask),
            provenance_hash=hashlib.sha256(inlier_mask.tobytes()).hexdigest(),
        )


# Global default registry instance
GLOBAL_REGISTRY = PluginRegistry()
