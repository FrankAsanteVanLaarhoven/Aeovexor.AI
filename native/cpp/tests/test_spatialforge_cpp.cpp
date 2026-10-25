#include "spatialforge_core.hpp"
#include <iostream>
#include <cassert>
#include <cmath>

int main() {
    std::cout << "[TEST] Running C++ native spatial test suite...\n";

    // 1. Version test
    const char* ver = sf_cpp_version();
    assert(ver != nullptr);
    std::cout << "  ✓ Version check passed: " << ver << "\n";

    // 2. Voxel filter test
    std::vector<spatialforge::Point3D> cloud;
    // Create 100 points tightly clustered in a 1x1x1 cube
    for (int i = 0; i < 100; ++i) {
        float offset = static_cast<float>(i) * 0.01f;
        cloud.push_back({offset, offset, offset, 0.8f});
    }
    auto down = spatialforge::voxel_grid_downsample(cloud, 0.5f);
    assert(!down.empty() && down.size() < cloud.size());
    std::cout << "  ✓ Voxel grid downsampled: " << cloud.size() << " -> " << down.size() << " points\n";

    // 3. Statistical outlier removal test
    std::vector<spatialforge::Point3D> noisy_cloud = {
        {0.0f, 0.0f, 0.0f, 1.0f},
        {0.1f, 0.0f, 0.0f, 1.0f},
        {0.0f, 0.1f, 0.0f, 1.0f},
        {0.1f, 0.1f, 0.0f, 1.0f},
        {50.0f, 50.0f, 50.0f, 1.0f} // Extreme outlier
    };
    auto inliers = spatialforge::statistical_outlier_removal(noisy_cloud, 2, 1.0f);
    assert(inliers.size() == 4);
    for (const auto& p : inliers) {
        assert(p.x < 10.0f && p.y < 10.0f && p.z < 10.0f);
    }
    std::cout << "  ✓ SOR filter successfully isolated and removed 3D outlier\n";

    // 4. Cloth simulation filter test
    std::vector<spatialforge::Point3D> terrain = {
        {0.0f, 0.0f, 0.0f, 0.5f},   // Ground
        {1.0f, 0.0f, 0.0f, 0.5f},   // Ground
        {0.0f, 1.0f, 0.0f, 0.5f},   // Ground
        {0.5f, 0.5f, 2.5f, 0.9f}    // Elevated object (e.g. vehicle)
    };
    std::vector<spatialforge::Point3D> ground, non_ground;
    spatialforge::cloth_simulation_filter(terrain, 1.0f, 1.0f, ground, non_ground);
    assert(ground.size() == 3);
    assert(non_ground.size() == 1);
    assert(std::abs(non_ground[0].z - 2.5f) < 1e-4f);
    std::cout << "  ✓ CSF ground separation correctly classified terrain vs obstacle\n";

    // 5. C2C Distance test
    auto dists = spatialforge::compute_c2c_distances(non_ground, ground);
    assert(dists.size() == 1);
    assert(dists[0] > 2.0f);
    std::cout << "  ✓ C2C Euclidean distance computed: " << dists[0] << "m\n";

    std::cout << "[SUCCESS] All C++ spatial native tests PASSED!\n";
    return 0;
}
