use aeovexor_spatial_core::{parse_kitti_bin, voxel_downsample};
use std::env;
use std::fs;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 || args[1] == "--help" || args[1] == "-h" {
        println!("Aeovexor.AI High-Performance Spatial CLI (Rust Core v2.4.0)");
        println!("Usage:");
        println!("  aeovexor-spatial-cli --version");
        println!("  aeovexor-spatial-cli --benchmark <path/to/lidar.bin>");
        println!("  aeovexor-spatial-cli --filter <path/to/lidar.bin> [voxel_leaf_size]");
        return;
    }

    match args[1].as_str() {
        "--version" | "-v" => {
            println!("aeovexor-spatial-cli v2.4.0 (Rust engine)");
        }
        "--benchmark" => {
            if args.len() < 3 {
                eprintln!("Error: Missing file path. Usage: aeovexor-spatial-cli --benchmark <file.bin>");
                std::process::exit(1);
            }
            let file_path = &args[2];
            println!("[AEOVEXOR RUST] Reading binary LiDAR frame: {}", file_path);
            let t0 = Instant::now();
            let bytes = fs::read(file_path).expect("Failed to read LiDAR file");
            let read_duration = t0.elapsed();

            let t1 = Instant::now();
            let points = parse_kitti_bin(&bytes).expect("Failed to parse LiDAR bytes");
            let parse_duration = t1.elapsed();

            let t2 = Instant::now();
            let downsampled = voxel_downsample(&points, 0.2);
            let voxel_duration = t2.elapsed();

            println!("  * Raw File Size:    {:.2} MB", bytes.len() as f64 / 1_048_576.0);
            println!("  * Raw Points:       {}", points.len());
            println!("  * Downsampled (0.2m): {}", downsampled.len());
            println!("  * File Read Time:   {:?}", read_duration);
            println!("  * Zero-Copy Parse:  {:?} ({:.2} Mpts/sec)",
                     parse_duration,
                     (points.len() as f64 / 1_000_000.0) / parse_duration.as_secs_f64());
            println!("  * Voxel Grid Time:  {:?}", voxel_duration);
            println!("[AEOVEXOR RUST] Benchmark Completed Successfully.");
        }
        "--filter" => {
            if args.len() < 3 {
                eprintln!("Error: Missing file path. Usage: aeovexor-spatial-cli --filter <file.bin> [leaf_size]");
                std::process::exit(1);
            }
            let file_path = &args[2];
            let leaf = if args.len() > 3 {
                args[3].parse::<f32>().unwrap_or(0.2)
            } else {
                0.2
            };
            let bytes = fs::read(file_path).expect("Failed to read file");
            let points = parse_kitti_bin(&bytes).expect("Failed to parse points");
            let filtered = voxel_downsample(&points, leaf);
            println!("Filtered: {} -> {} points (leaf = {}m)", points.len(), filtered.len(), leaf);
        }
        other => {
            eprintln!("Unknown command: {}", other);
            std::process::exit(1);
        }
    }
}
