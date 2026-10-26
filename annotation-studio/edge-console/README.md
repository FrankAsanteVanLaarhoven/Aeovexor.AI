# Aeovexor.AI Annotation Studio & Edge Console

The **Annotation Studio** provides real-time, field-deployable 3D oriented bounding box (OBB) annotation, multi-camera overlay, and telemetry monitoring for autonomous perception systems.

## Features
- **7-DOF 3D Bounding Box Manipulation**: Sub-millimeter position $(x, y, z)$, scale $(dx, dy, dz)$, and heading yaw angle $(\theta)$.
- **Semantic Class Taxonomy**: Color-coded classes for Vehicles (Cyan), Pedestrians (Rose), Cyclists (Amber), Road Signs (Emerald), and Obstacles (Purple).
- **Ground Truth Format Exporters**:
  - **KITTI 3D** Benchmark Format (`.txt`)
  - **NuScenes JSON** Format (`.json`)
  - **Aeovexor Spatial Schema** (`.json`)
- **Scientific GPU Colormaps**: Viridis, Turbo, Plasma, Elevation ($Z$), LiDAR Intensity, and Surface Normals.
- **Go SSE 60Hz Telemetry Link**: Low-latency edge connection to the `services/go-telemetry` streaming engine.

## Quickstart (Development Mode)
```bash
# From workspace root
cd frontend
npm install
npm run dev
```

The Edge Console will be available at `http://localhost:3000`.
To access the Developer IDE, navigate to `http://localhost:3000/ide`.
To view platform documentation, navigate to `http://localhost:3000/overview`.
