#pragma once

#include <vector>
#include <cstdint>
#include <cstddef>

namespace spatialforge {

struct Point3D {
    float x;
    float y;
    float z;
    float intensity;
};

struct BoundingBox3D {
    float center[3];
    float size[3];
    float heading;
    float confidence;
    int32_t class_id;
};

// SIMD/Fast Voxel Downsampling
std::vector<Point3D> voxel_grid_downsample(const std::vector<Point3D>& points, float leaf_size);

// Statistical Outlier Removal (SOR) noise filtering
std::vector<Point3D> statistical_outlier_removal(const std::vector<Point3D>& points, int k_neighbors, float std_ratio);

// Cloth Simulation Filter (CSF) for Ground vs Non-Ground Classification
void cloth_simulation_filter(const std::vector<Point3D>& points,
                             float grid_res,
                             float rigidness,
                             std::vector<Point3D>& ground,
                             std::vector<Point3D>& non_ground);

// Cloud-to-Cloud (C2C) nearest neighbor distance comparison
std::vector<float> compute_c2c_distances(const std::vector<Point3D>& source,
                                        const std::vector<Point3D>& target);

// 6-DOF Fast Iterative Closest Point (ICP) registration
bool run_icp_registration(const std::vector<Point3D>& source,
                          const std::vector<Point3D>& target,
                          float transform_matrix[16],
                          float& final_fitness,
                          int max_iterations = 30,
                          float tolerance = 1e-4f);

} // namespace spatialforge

// C-compatible ABI exports for Python (ctypes), Rust (bindgen), and Go (cgo)
extern "C" {

typedef struct {
    float x, y, z, intensity;
} C_Point3D;

int32_t sf_cpp_voxel_filter(const C_Point3D* in_points,
                            int32_t count,
                            float leaf_size,
                            C_Point3D* out_points,
                            int32_t max_out);

int32_t sf_cpp_sor_filter(const C_Point3D* in_points,
                          int32_t count,
                          int32_t k_neighbors,
                          float std_ratio,
                          C_Point3D* out_points,
                          int32_t max_out);

int32_t sf_cpp_csf_ground(const C_Point3D* in_points,
                          int32_t count,
                          float grid_res,
                          float rigidness,
                          C_Point3D* out_ground,
                          int32_t max_ground,
                          int32_t* ground_count,
                          C_Point3D* out_non_ground,
                          int32_t max_non_ground,
                          int32_t* non_ground_count);

int32_t sf_cpp_c2c_distance(const C_Point3D* source,
                            int32_t src_count,
                            const C_Point3D* target,
                            int32_t tgt_count,
                            float* out_distances);

const char* sf_cpp_version();

}
