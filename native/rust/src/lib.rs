//! Aeovexor.AI High-Performance Spatial Core in Rust
//! High-throughput zero-copy LiDAR point cloud parser, spatial indexing, and filtering.

use std::collections::HashMap;

#[repr(C)]
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Point3D {
    pub x: f32,
    pub y: f32,
    pub z: f32,
    pub intensity: f32,
}

#[repr(C)]
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct BoundingBox3D {
    pub center: [f32; 3],
    pub size: [f32; 3],
    pub heading: f32,
    pub confidence: f32,
    pub class_id: i32,
}

/// Zero-copy parser for binary LiDAR streams (KITTI / Velodyne format: 4 x float32 per point)
pub fn parse_kitti_bin(bytes: &[u8]) -> Result<Vec<Point3D>, String> {
    if bytes.len() % 16 != 0 {
        return Err(format!(
            "Invalid buffer length: {} bytes is not a multiple of 16 (4 * float32)",
            bytes.len()
        ));
    }
    let count = bytes.len() / 16;
    let mut points = Vec::with_capacity(count);

    for chunk in bytes.chunks_exact(16) {
        let x = f32::from_le_bytes([chunk[0], chunk[1], chunk[2], chunk[3]]);
        let y = f32::from_le_bytes([chunk[4], chunk[5], chunk[6], chunk[7]]);
        let z = f32::from_le_bytes([chunk[8], chunk[9], chunk[10], chunk[11]]);
        let intensity = f32::from_le_bytes([chunk[12], chunk[13], chunk[14], chunk[15]]);
        points.push(Point3D { x, y, z, intensity });
    }
    Ok(points)
}

/// High-throughput voxel grid filter using integer coordinates
pub fn voxel_downsample(points: &[Point3D], leaf_size: f32) -> Vec<Point3D> {
    if leaf_size <= 0.0 || points.is_empty() {
        return points.to_vec();
    }
    let inv_leaf = 1.0 / leaf_size;
    let mut grid: HashMap<(i64, i64, i64), (f64, f64, f64, f64, usize)> = HashMap::with_capacity(points.len() / 2);

    for p in points {
        let key = (
            (p.x * inv_leaf).floor() as i64,
            (p.y * inv_leaf).floor() as i64,
            (p.z * inv_leaf).floor() as i64,
        );
        let entry = grid.entry(key).or_insert((0.0, 0.0, 0.0, 0.0, 0));
        entry.0 += p.x as f64;
        entry.1 += p.y as f64;
        entry.2 += p.z as f64;
        entry.3 += p.intensity as f64;
        entry.4 += 1;
    }

    let mut out = Vec::with_capacity(grid.len());
    for (_, (sx, sy, sz, si, count)) in grid {
        let inv_c = 1.0 / (count as f64);
        out.push(Point3D {
            x: (sx * inv_c) as f32,
            y: (sy * inv_c) as f32,
            z: (sz * inv_c) as f32,
            intensity: (si * inv_c) as f32,
        });
    }
    out
}

/// Statistical outlier removal (SOR) filter
pub fn sor_filter(points: &[Point3D], k: usize, std_ratio: f32) -> Vec<Point3D> {
    let n = points.len();
    if n <= k || k == 0 {
        return points.to_vec();
    }

    let mut avg_dists = Vec::with_capacity(n);
    let effective_k = k.min(n - 1);

    for (i, pi) in points.iter().enumerate() {
        let mut dists = Vec::with_capacity(n);
        for (j, pj) in points.iter().enumerate() {
            if i == j {
                continue;
            }
            let dx = pi.x - pj.x;
            let dy = pi.y - pj.y;
            let dz = pi.z - pj.z;
            dists.push((dx * dx + dy * dy + dz * dz).sqrt());
        }
        dists.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
        let sum: f32 = dists.iter().take(effective_k).sum();
        avg_dists.push(sum / effective_k as f32);
    }

    let mean: f32 = avg_dists.iter().sum::<f32>() / n as f32;
    let var: f32 = avg_dists.iter().map(|d| (d - mean).powi(2)).sum::<f32>() / n as f32;
    let std_dev = var.sqrt();
    let threshold = mean + std_ratio * std_dev;

    points
        .iter()
        .zip(avg_dists.iter())
        .filter(|(_, &d)| d <= threshold)
        .map(|(&p, _)| p)
        .collect()
}

/// Compute 3D oriented bounding box axis-aligned intersection volume approximation
pub fn box_3d_iou(b1: &BoundingBox3D, b2: &BoundingBox3D) -> f32 {
    let min1_x = b1.center[0] - b1.size[0] / 2.0;
    let max1_x = b1.center[0] + b1.size[0] / 2.0;
    let min1_y = b1.center[1] - b1.size[1] / 2.0;
    let max1_y = b1.center[1] + b1.size[1] / 2.0;
    let min1_z = b1.center[2] - b1.size[2] / 2.0;
    let max1_z = b1.center[2] + b1.size[2] / 2.0;

    let min2_x = b2.center[0] - b2.size[0] / 2.0;
    let max2_x = b2.center[0] + b2.size[0] / 2.0;
    let min2_y = b2.center[1] - b2.size[1] / 2.0;
    let max2_y = b2.center[1] + b2.size[1] / 2.0;
    let min2_z = b2.center[2] - b2.size[2] / 2.0;
    let max2_z = b2.center[2] + b2.size[2] / 2.0;

    let inter_x = (max1_x.min(max2_x) - min1_x.max(min2_x)).max(0.0);
    let inter_y = (max1_y.min(max2_y) - min1_y.max(min2_y)).max(0.0);
    let inter_z = (max1_z.min(max2_z) - min1_z.max(min2_z)).max(0.0);

    let inter_vol = inter_x * inter_y * inter_z;
    let vol1 = b1.size[0] * b1.size[1] * b1.size[2];
    let vol2 = b2.size[0] * b2.size[1] * b2.size[2];
    let union_vol = vol1 + vol2 - inter_vol;

    if union_vol <= 0.0 {
        0.0
    } else {
        inter_vol / union_vol
    }
}

// C-ABI Exports for FFI
#[no_mangle]
pub extern "C" fn sf_rust_version() -> *const std::os::raw::c_char {
    c"aeovexor-rust-core-2.4.0".as_ptr()
}

#[no_mangle]
pub extern "C" fn sf_rust_parse_kitti_bin(
    raw_ptr: *const u8,
    len: usize,
    out_points: *mut Point3D,
    max_out: usize,
) -> i32 {
    if raw_ptr.is_null() || out_points.is_null() {
        return -1;
    }
    let slice = unsafe { std::slice::from_raw_parts(raw_ptr, len) };
    match parse_kitti_bin(slice) {
        Ok(pts) => {
            let copy_count = pts.len().min(max_out);
            unsafe {
                std::ptr::copy_nonoverlapping(pts.as_ptr(), out_points, copy_count);
            }
            copy_count as i32
        }
        Err(_) => -2,
    }
}

#[no_mangle]
pub extern "C" fn sf_rust_voxel_filter(
    in_points: *const Point3D,
    count: usize,
    leaf_size: f32,
    out_points: *mut Point3D,
    max_out: usize,
) -> i32 {
    if in_points.is_null() || out_points.is_null() {
        return -1;
    }
    let slice = unsafe { std::slice::from_raw_parts(in_points, count) };
    let down = voxel_downsample(slice, leaf_size);
    let copy_count = down.len().min(max_out);
    unsafe {
        std::ptr::copy_nonoverlapping(down.as_ptr(), out_points, copy_count);
    }
    copy_count as i32
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kitti_parser() {
        let mut buf = Vec::new();
        // Point 1: (1.0, 2.0, 3.0, 0.5)
        buf.extend_from_slice(&1.0f32.to_le_bytes());
        buf.extend_from_slice(&2.0f32.to_le_bytes());
        buf.extend_from_slice(&3.0f32.to_le_bytes());
        buf.extend_from_slice(&0.5f32.to_le_bytes());

        let pts = parse_kitti_bin(&buf).unwrap();
        assert_eq!(pts.len(), 1);
        assert_eq!(pts[0].x, 1.0);
        assert_eq!(pts[0].y, 2.0);
        assert_eq!(pts[0].z, 3.0);
        assert_eq!(pts[0].intensity, 0.5);
    }

    #[test]
    fn test_voxel_filter() {
        let pts = vec![
            Point3D { x: 0.1, y: 0.1, z: 0.1, intensity: 1.0 },
            Point3D { x: 0.2, y: 0.2, z: 0.2, intensity: 1.0 },
            Point3D { x: 5.0, y: 5.0, z: 5.0, intensity: 1.0 },
        ];
        let filtered = voxel_downsample(&pts, 1.0);
        assert_eq!(filtered.len(), 2);
    }

    #[test]
    fn test_sor_filter() {
        let pts = vec![
            Point3D { x: 0.0, y: 0.0, z: 0.0, intensity: 1.0 },
            Point3D { x: 0.1, y: 0.0, z: 0.0, intensity: 1.0 },
            Point3D { x: 0.0, y: 0.1, z: 0.0, intensity: 1.0 },
            Point3D { x: 100.0, y: 100.0, z: 100.0, intensity: 1.0 }, // Outlier
        ];
        let inliers = sor_filter(&pts, 2, 1.0);
        assert_eq!(inliers.len(), 3);
        assert!(!inliers.iter().any(|p| p.x > 50.0));
    }

    #[test]
    fn test_box_3d_iou() {
        let b1 = BoundingBox3D {
            center: [0.0, 0.0, 0.0],
            size: [2.0, 2.0, 2.0],
            heading: 0.0,
            confidence: 1.0,
            class_id: 1,
        };
        let b2 = BoundingBox3D {
            center: [0.0, 0.0, 0.0],
            size: [2.0, 2.0, 2.0],
            heading: 0.0,
            confidence: 1.0,
            class_id: 1,
        };
        let iou = box_3d_iou(&b1, &b2);
        assert!((iou - 1.0).abs() < 1e-4);
    }
}
