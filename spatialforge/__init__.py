"""SpatialForge-3D: Production Spatial Intelligence, LiDAR, and Point-Cloud Engineering Engine."""

from .contracts import BoundingBox3D, FrameMetadata, SpatialFrame
from .io import (
    load_frame,
    save_frame,
    read_kitti_velodyne,
    load_waymo_frame,
    iter_waymo_frames,
    read_ply,
    write_ply,
    read_pcd,
    write_pcd,
    read_las,
    load_poses,
    save_poses,
)
from .geometry import (
    voxel_downsample,
    statistical_outlier_removal,
    radius_outlier_removal,
    VoxelHashGrid,
    estimate_normals,
    compute_covariances,
    compute_geometric_descriptors,
    compute_multiscale_features,
    ransac_plane,
    extract_ground_plane,
)
from .clustering import (
    cluster,
    adaptive_geometry_clustering,
    region_growing_segmentation,
    hdbscan_clustering,
)
from .registration import (
    icp,
    icp_point_to_point,
    icp_point_to_plane,
    gicp_registration,
    global_registration_ransac,
)
from .slam import LiDAROdometry
from .reconstruction import TSDFVolume, OccupancyGrid3D, save_mesh_obj
from .reasoning import (
    compute_oriented_bounding_box,
    compute_axis_aligned_bounding_box,
    SemanticSceneGraph,
    compute_obstacle_clearance,
    compute_traversability_map,
)
from .learning import PointNetLite, predict_point_semantics
from .benchmarks import (
    evaluate_trajectory,
    evaluate_clustering,
    evaluate_segmentation,
    evaluate_registration,
    bootstrap_confidence_interval,
    paired_significance_test,
    BenchmarkProfiler,
)
from .advanced_math import (
    compute_optimal_scale_features,
    range_compensated_clustering,
    progressive_morphological_ground_filter,
    compute_minimal_oriented_bounding_box,
)
from .viz import generate_interactive_html

__version__ = "1.0.0"

__all__ = [
    "SpatialFrame",
    "FrameMetadata",
    "BoundingBox3D",
    "load_frame",
    "save_frame",
    "read_kitti_velodyne",
    "load_waymo_frame",
    "iter_waymo_frames",
    "read_ply",
    "write_ply",
    "read_pcd",
    "write_pcd",
    "read_las",
    "load_poses",
    "save_poses",
    "voxel_downsample",
    "statistical_outlier_removal",
    "radius_outlier_removal",
    "VoxelHashGrid",
    "estimate_normals",
    "compute_covariances",
    "compute_geometric_descriptors",
    "compute_multiscale_features",
    "ransac_plane",
    "extract_ground_plane",
    "cluster",
    "adaptive_geometry_clustering",
    "region_growing_segmentation",
    "hdbscan_clustering",
    "icp",
    "icp_point_to_point",
    "icp_point_to_plane",
    "gicp_registration",
    "global_registration_ransac",
    "LiDAROdometry",
    "TSDFVolume",
    "OccupancyGrid3D",
    "save_mesh_obj",
    "compute_oriented_bounding_box",
    "compute_axis_aligned_bounding_box",
    "SemanticSceneGraph",
    "compute_obstacle_clearance",
    "compute_traversability_map",
    "PointNetLite",
    "predict_point_semantics",
    "evaluate_trajectory",
    "evaluate_clustering",
    "evaluate_segmentation",
    "evaluate_registration",
    "bootstrap_confidence_interval",
    "paired_significance_test",
    "BenchmarkProfiler",
    "generate_interactive_html",
]
