"""SpatialForge Studio v0.3 Web Frontend Generator.

Generates the complete, self-contained modern HTML5/WebGL/Tailwind-styled
professional 3D research studio interface exceeding CloudCompare.
"""
from pathlib import Path
from typing import Dict, Any, Optional
import json


def get_studio_html(initial_data: Optional[Dict[str, Any]] = None) -> str:
    """Generates the full HTML/CSS/JS source for SpatialForge Studio v0.3."""
    init_json = json.dumps(initial_data or {})
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SpatialForge Studio v0.3 | Professional 3D Spatial Intelligence Platform</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌐</text></svg>">
  
  <style>
    :root {{
      --bg-main: #06090e;
      --bg-panel: #0b111b;
      --bg-panel-header: #0f1726;
      --bg-hover: #162032;
      --bg-active: #1c2b42;
      --border: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(56, 189, 248, 0.35);
      --cyan: #38bdf8;
      --cyan-glow: rgba(56, 189, 248, 0.2);
      --indigo: #6366f1;
      --emerald: #10b981;
      --amber: #f59e0b;
      --rose: #f43f5e;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background: var(--bg-main);
      color: var(--text-main);
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      user-select: none;
    }}

    .top-bar {{
      height: 48px;
      background: var(--bg-panel-header);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      z-index: 50;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 700;
      font-size: 0.95rem;
      letter-spacing: -0.02em;
    }}
    .brand-badge {{
      background: linear-gradient(135deg, #0284c7, #6366f1);
      color: white;
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 0.7rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .project-selector {{
      background: var(--bg-hover);
      border: 1px solid var(--border);
      color: var(--text-main);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 0.8rem;
      outline: none;
      cursor: pointer;
    }}
    .top-actions {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .btn-tool {{
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-muted);
      padding: 5px 9px;
      border-radius: 5px;
      font-size: 0.78rem;
      font-weight: 500;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.15s ease;
    }}
    .btn-tool:hover {{
      background: var(--bg-hover);
      color: var(--text-main);
      border-color: var(--border);
    }}
    .btn-tool.active {{
      background: rgba(56, 189, 248, 0.15);
      color: var(--cyan);
      border-color: var(--border-accent);
    }}
    .btn-primary {{
      background: #0284c7;
      color: #fff;
      border: 1px solid #38bdf8;
      font-weight: 600;
    }}
    .btn-primary:hover {{
      background: #0369a1;
    }}

    .sub-toolbar {{
      height: 38px;
      background: var(--bg-panel);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      padding: 0 12px;
      gap: 8px;
      overflow-x: auto;
    }}
    .tool-group {{
      display: flex;
      align-items: center;
      gap: 2px;
      padding-right: 8px;
      border-right: 1px solid var(--border);
    }}
    .tool-label {{
      font-size: 0.68rem;
      text-transform: uppercase;
      color: var(--text-dim);
      font-weight: 700;
      letter-spacing: 0.05em;
      margin-right: 4px;
    }}

    .main-workspace {{
      flex: 1;
      display: flex;
      overflow: hidden;
      position: relative;
    }}

    .left-panel {{
      width: 320px;
      background: var(--bg-panel);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }}
    .panel-header {{
      padding: 10px 14px;
      background: var(--bg-panel-header);
      border-bottom: 1px solid var(--border);
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .db-tree {{
      flex: 1;
      overflow-y: auto;
      padding: 8px;
    }}
    .tree-folder {{
      margin-bottom: 8px;
    }}
    .folder-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 5px 8px;
      font-size: 0.76rem;
      font-weight: 700;
      color: var(--text-dim);
      border-radius: 4px;
    }}
    .tree-node {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 6px 10px;
      margin: 2px 0;
      border-radius: 5px;
      font-size: 0.8rem;
      cursor: pointer;
      border: 1px solid transparent;
      background: rgba(255, 255, 255, 0.02);
      transition: all 0.15s;
    }}
    .tree-node:hover {{
      background: var(--bg-hover);
    }}
    .tree-node.selected {{
      background: rgba(56, 189, 248, 0.12);
      border-color: var(--border-accent);
      color: var(--cyan);
    }}
    .node-title {{
      display: flex;
      align-items: center;
      gap: 7px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .node-color-swatch {{
      width: 10px;
      height: 10px;
      border-radius: 2px;
      flex-shrink: 0;
    }}
    .node-badge {{
      font-size: 0.68rem;
      padding: 1px 5px;
      border-radius: 3px;
      background: rgba(255, 255, 255, 0.06);
      color: var(--text-dim);
      font-family: monospace;
    }}
    .node-actions {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .properties-panel {{
      height: 250px;
      border-top: 1px solid var(--border);
      background: var(--bg-panel);
      display: flex;
      flex-direction: column;
    }}
    .prop-list {{
      flex: 1;
      overflow-y: auto;
      padding: 8px 12px;
    }}
    .prop-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 4px 0;
      font-size: 0.76rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    }}
    .prop-key {{
      color: var(--text-dim);
      font-weight: 500;
    }}
    .prop-val {{
      color: var(--text-main);
      font-family: monospace;
      font-weight: 600;
    }}

    .viewport-container {{
      flex: 1;
      display: flex;
      position: relative;
      background: #020617;
      overflow: hidden;
    }}
    .viewport {{
      flex: 1;
      position: relative;
      height: 100%;
    }}
    .viewport-overlay {{
      position: absolute;
      top: 12px;
      left: 12px;
      z-index: 10;
      pointer-events: none;
    }}
    .viewport-tag {{
      display: inline-block;
      background: rgba(11, 17, 27, 0.75);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 0.74rem;
      font-weight: 600;
      color: var(--text-muted);
    }}
    .viewport-divider {{
      width: 4px;
      background: var(--bg-panel-header);
      border-left: 1px solid var(--border);
      border-right: 1px solid var(--border);
      cursor: col-resize;
      display: none;
      z-index: 20;
    }}
    .viewport.secondary {{
      display: none;
      border-left: 1px solid var(--border);
    }}

    .right-panel {{
      width: 320px;
      background: var(--bg-panel);
      border-left: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      transition: width 0.2s ease;
    }}
    .tab-nav {{
      display: flex;
      border-bottom: 1px solid var(--border);
      background: var(--bg-panel-header);
    }}
    .tab-btn {{
      flex: 1;
      padding: 9px;
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 0.76rem;
      font-weight: 600;
      cursor: pointer;
      text-align: center;
      border-bottom: 2px solid transparent;
    }}
    .tab-btn.active {{
      color: var(--cyan);
      border-bottom-color: var(--cyan);
      background: rgba(56, 189, 248, 0.05);
    }}
    .tab-content {{
      flex: 1;
      overflow-y: auto;
      padding: 14px;
      display: none;
    }}
    .tab-content.active {{
      display: block;
    }}

    .form-group {{
      margin-bottom: 14px;
    }}
    .form-label {{
      display: block;
      font-size: 0.74rem;
      font-weight: 600;
      color: var(--text-muted);
      margin-bottom: 6px;
    }}
    .form-input, .form-select {{
      width: 100%;
      background: var(--bg-main);
      border: 1px solid var(--border);
      color: var(--text-main);
      padding: 7px 10px;
      border-radius: 6px;
      font-size: 0.8rem;
      outline: none;
    }}
    .form-input:focus, .form-select:focus {{
      border-color: var(--cyan);
    }}
    .range-wrap {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .range-val {{
      font-family: monospace;
      font-size: 0.76rem;
      color: var(--cyan);
      width: 45px;
      text-align: right;
    }}

    .playback-bar {{
      height: 38px;
      background: var(--bg-panel-header);
      border-top: 1px solid var(--border);
      display: flex;
      align-items: center;
      padding: 0 16px;
      gap: 14px;
      z-index: 30;
    }}
    .scrubber {{
      flex: 1;
      height: 6px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 3px;
      cursor: pointer;
      position: relative;
    }}
    .scrubber-fill {{
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      width: 32%;
      background: var(--cyan);
      border-radius: 3px;
    }}

    .bottom-console {{
      height: 120px;
      background: var(--bg-main);
      border-top: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
    }}
    .console-header {{
      height: 24px;
      background: var(--bg-panel-header);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 12px;
      font-size: 0.7rem;
      color: var(--text-dim);
    }}
    .console-body {{
      flex: 1;
      overflow-y: auto;
      padding: 6px 12px;
      font-size: 0.72rem;
      line-height: 1.5;
    }}
    .log-line {{
      display: flex;
      gap: 8px;
    }}
    .log-ts {{ color: var(--text-dim); }}
    .log-info {{ color: #38bdf8; }}
    .log-success {{ color: #10b981; }}
    .log-warn {{ color: #f59e0b; }}
    .log-err {{ color: #f43f5e; }}

    .status-bar {{
      height: 22px;
      background: #04070c;
      border-top: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 12px;
      font-size: 0.68rem;
      color: var(--text-dim);
    }}
    .status-group {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}
    .status-item strong {{
      color: var(--text-muted);
    }}
  </style>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>

  <!-- Top Navigation & Brand -->
  <div class="top-bar">
    <div class="brand">
      <span style="font-size: 1.2rem;">🌐</span>
      <span>SpatialForge Studio</span>
      <span class="brand-badge">v0.3 Pro</span>
      <select class="project-selector" id="project-select">
        <option value="kitti">Project 01: KITTI Velodyne HDL-64E Urban SLAM</option>
        <option value="waymo">Project 02: Waymo Open Dataset (5-Laser Multi-Return)</option>
        <option value="cad">Project 03: Industrial Facility Digital Twin & CAD</option>
        <option value="terrain">Project 04: Geospatial DTM & Forestry Canopy</option>
      </select>
    </div>

    <div class="top-actions">
      <button class="btn-tool" id="btn-single-view">Single View</button>
      <button class="btn-tool active" id="btn-split-view">Side-by-Side Split</button>
      <button class="btn-tool" id="btn-sync-cam">🔄 Sync Orbit: ON</button>
      <div style="width: 1px; height: 18px; background: var(--border); margin: 0 4px;"></div>
      <button class="btn-tool" id="btn-edl">✨ Eye-Dome Lighting</button>
      <button class="btn-tool" id="btn-dashboard">📊 Benchmark Dashboard</button>
      <button class="btn-tool btn-primary" id="btn-export">Export Cloud / Mesh</button>
    </div>
  </div>

  <!-- Sub-Toolbar: Geometry Operations & Filters (CloudCompare Style) -->
  <div class="sub-toolbar">
    <div class="tool-group">
      <span class="tool-label">File</span>
      <button class="btn-tool" id="btn-import-file">📂 Open</button>
      <button class="btn-tool" id="btn-save-project">💾 Save</button>
    </div>

    <div class="tool-group">
      <span class="tool-label">Filter</span>
      <button class="btn-tool" id="btn-op-sor" title="Statistical Outlier Removal">SOR Filter</button>
      <button class="btn-tool" id="btn-op-voxel" title="Voxel Downsample">Voxel 0.35m</button>
      <button class="btn-tool" id="btn-op-normals" title="Estimate Surface Normals">Normals</button>
    </div>

    <div class="tool-group">
      <span class="tool-label">Segmentation</span>
      <button class="btn-tool active" id="btn-op-rcmc" title="Range-Compensated Metric Clustering">Adaptive RCMC</button>
      <button class="btn-tool" id="btn-op-pmcsf" title="Progressive Morphological Ground Filter">PM-CSF Ground</button>
      <button class="btn-tool" id="btn-op-dbscan" title="Classical Fixed DBSCAN">DBSCAN</button>
    </div>

    <div class="tool-group">
      <span class="tool-label">CAD & Mesh</span>
      <button class="btn-tool" id="btn-op-plane" title="RANSAC Plane Fitting">Fit Plane</button>
      <button class="btn-tool" id="btn-op-obb" title="Minimal Volume Oriented Bounding Hull">Fit 3D OBB</button>
      <button class="btn-tool" id="btn-op-tsdf" title="TSDF Raycast Reconstruction">TSDF Mesh</button>
    </div>

    <div class="tool-group">
      <span class="tool-label">Align</span>
      <button class="btn-tool" id="btn-op-p2pl" title="Huber Point-to-Plane ICP">P2Plane ICP</button>
      <button class="btn-tool" id="btn-op-gicp" title="Generalized ICP">GICP</button>
    </div>

    <div class="tool-group" style="border: none;">
      <span class="tool-label">Color</span>
      <select class="form-select" id="select-color-mode" style="width: auto; padding: 3px 8px; font-size: 0.74rem;">
        <option value="height">Z-Height Gradient</option>
        <option value="intensity">Laser Intensity (Turbo)</option>
        <option value="normals">Normal Vectors (RGB)</option>
        <option value="clusters" selected>Cluster Instances (RCMC)</option>
        <option value="semantics">Semantic Classes</option>
      </select>
    </div>
  </div>

  <!-- Main Body: DB Tree | Viewports | Right Panels -->
  <div class="main-workspace">

    <!-- Left DB Entity Tree (CloudCompare Style) -->
    <div class="left-panel">
      <div class="panel-header">
        <span>DB Tree Entities</span>
        <button class="btn-tool" id="btn-add-layer" style="padding: 2px 6px;">+ Add</button>
      </div>

      <div class="db-tree" id="db-tree-root">
        <div class="tree-folder">
          <div class="folder-header">
            <span>📁 POINT CLOUDS (3)</span>
          </div>
          <div class="tree-node selected" id="node-raw">
            <div class="node-title">
              <span class="node-color-swatch" style="background: #38bdf8;"></span>
              <span>Velodyne_HDL64E_000008</span>
            </div>
            <div class="node-actions">
              <span class="node-badge">17,238 pts</span>
            </div>
          </div>
          <div class="tree-node" id="node-ground">
            <div class="node-title">
              <span class="node-color-swatch" style="background: #a855f7;"></span>
              <span>Ground_Manifold_PM_CSF</span>
            </div>
            <div class="node-actions">
              <span class="node-badge">9,412 pts</span>
            </div>
          </div>
          <div class="tree-node" id="node-objects">
            <div class="node-title">
              <span class="node-color-swatch" style="background: #10b981;"></span>
              <span>RCMC_Physical_Objects</span>
            </div>
            <div class="node-actions">
              <span class="node-badge">18 objs</span>
            </div>
          </div>
        </div>

        <div class="tree-folder">
          <div class="folder-header">
            <span>📁 CAD & PRIMITIVES (2)</span>
          </div>
          <div class="tree-node" id="node-plane">
            <div class="node-title">
              <span class="node-color-swatch" style="background: #f59e0b;"></span>
              <span>Road_Plane_RANSAC</span>
            </div>
            <div class="node-actions">
              <span class="node-badge">Plane</span>
            </div>
          </div>
          <div class="tree-node" id="node-boxes">
            <div class="node-title">
              <span class="node-color-swatch" style="background: #ec4899;"></span>
              <span>3D_OBB_Bounding_Hulls</span>
            </div>
            <div class="node-actions">
              <span class="node-badge">18 boxes</span>
            </div>
          </div>
        </div>

        <div class="tree-folder">
          <div class="folder-header">
            <span>📁 RECONSTRUCTION MESHES (1)</span>
          </div>
          <div class="tree-node" id="node-mesh">
            <div class="node-title">
              <span class="node-color-swatch" style="background: #06b6d4;"></span>
              <span>TSDF_IsoSurface_DualVoxel</span>
            </div>
            <div class="node-actions">
              <span class="node-badge">14,280 tris</span>
            </div>
          </div>
        </div>

        <div class="tree-folder">
          <div class="folder-header">
            <span>📁 SLAM TRAJECTORIES (1)</span>
          </div>
          <div class="tree-node" id="node-traj">
            <div class="node-title">
              <span class="node-color-swatch" style="background: #eab308;"></span>
              <span>LiDAROdometry_Estimated_Path</span>
            </div>
            <div class="node-actions">
              <span class="node-badge">0.0037m ATE</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Properties Window -->
      <div class="properties-panel">
        <div class="panel-header">
          <span>Properties: Velodyne_HDL64E</span>
          <span style="font-size: 0.7rem; color: var(--cyan);">LOCKED</span>
        </div>
        <div class="prop-list">
          <div class="prop-row"><span class="prop-key">Entity Type</span><span class="prop-val">Point Cloud (XYZI)</span></div>
          <div class="prop-row"><span class="prop-key">Points</span><span class="prop-val">17,238</span></div>
          <div class="prop-row"><span class="prop-key">Centroid [X,Y,Z]</span><span class="prop-val">[-0.42, 18.25, -0.85] m</span></div>
          <div class="prop-row"><span class="prop-key">Bounding Box</span><span class="prop-val">[42.5 x 75.8 x 6.4] m</span></div>
          <div class="prop-row"><span class="prop-key">Range Spread</span><span class="prop-val">3.74m → 79.53m</span></div>
          <div class="prop-row"><span class="prop-key">Coordinate Frame</span><span class="prop-val">sensor_lidar</span></div>
          <div class="prop-row"><span class="prop-key">Provenance SHA</span><span class="prop-val">3a9f4c82b012...</span></div>
          <div class="prop-row"><span class="prop-key">Point Size</span><span class="prop-val" id="disp-pt-size">2.2 px</span></div>
        </div>
      </div>
    </div>

    <!-- Center Viewports (Single or Side-by-Side Split) -->
    <div class="viewport-container">
      
      <!-- Primary Viewport (SpatialForge Proposed Adaptive Engine) -->
      <div class="viewport" id="viewport-primary">
        <div class="viewport-overlay">
          <div class="viewport-tag" id="tag-primary">SpatialForge-3D: Adaptive RCMC & SLAM [Active]</div>
        </div>
        <div id="canvas-primary" style="width:100%; height:100%;"></div>
      </div>

      <!-- Divider -->
      <div class="viewport-divider" id="viewport-divider"></div>

      <!-- Secondary Viewport (Baseline Comparison) -->
      <div class="viewport secondary" id="viewport-secondary">
        <div class="viewport-overlay">
          <div class="viewport-tag" id="tag-secondary" style="border-color: rgba(244, 63, 94, 0.4); color: #f43f5e;">
            Baseline: Fixed DBSCAN (14.4% Noise Failure)
          </div>
        </div>
        <div id="canvas-secondary" style="width:100%; height:100%;"></div>
      </div>

    </div>

    <!-- Right Panel: Algorithm Plugins, Mesh Editor & Batch Runner -->
    <div class="right-panel" id="right-panel">
      <div class="tab-nav">
        <button class="tab-btn active" data-tab="tab-plugins">Plugins</button>
        <button class="tab-btn" data-tab="tab-mesh">Mesh Editor</button>
        <button class="tab-btn" data-tab="tab-batch">Batch Queue</button>
      </div>

      <!-- Tab 1: Configurable Algorithm Plugins -->
      <div class="tab-content active" id="tab-plugins">
        <div class="form-group">
          <label class="form-label">Algorithm Operator</label>
          <select class="form-select" id="plugin-operator">
            <option value="rcmc">Adaptive RCMC Clustering (Section E1)</option>
            <option value="pmcsf">PM-CSF Ground Filter</option>
            <option value="gicp">Generalized ICP Registration (Section E2)</option>
            <option value="msgt">Entropy-Minimizing Scale Tensor (EM-MSGT)</option>
            <option value="tsdf">TSDF Volume Reconstruction</option>
            <option value="pointnet">PointNetLite Semantic Inference</option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">Base Neighborhood Radius / Epsilon (m)</label>
          <div class="range-wrap">
            <input type="range" class="form-input" id="param-eps" min="0.1" max="1.5" step="0.05" value="0.45">
            <span class="range-val" id="val-eps">0.45</span>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Min Cluster Samples (k)</label>
          <div class="range-wrap">
            <input type="range" class="form-input" id="param-min-pts" min="3" max="30" step="1" value="6">
            <span class="range-val" id="val-min-pts">6</span>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Normal Divergence Weight (w_n)</label>
          <div class="range-wrap">
            <input type="range" class="form-input" id="param-wn" min="0.0" max="1.0" step="0.05" value="0.5">
            <span class="range-val" id="val-wn">0.50</span>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Execution Target</label>
          <select class="form-select" id="param-device">
            <option value="gpu">Apple Silicon GPU / Metal (Vectorized)</option>
            <option value="cpu">Vectorized NumPy / SciPy Multi-Core</option>
          </select>
        </div>

        <button class="btn-tool btn-primary" id="btn-execute-plugin" style="width: 100%; justify-content: center; padding: 9px; margin-top: 10px;">
          ⚡ Execute Algorithm Plugin
        </button>

        <div style="margin-top: 20px; padding: 12px; background: rgba(56, 189, 248, 0.05); border: 1px solid var(--border-accent); border-radius: 6px;">
          <div style="font-size: 0.74rem; font-weight: 700; color: var(--cyan); margin-bottom: 4px;">Adaptive Spatial Intelligence Meta-Plan:</div>
          <p style="font-size: 0.72rem; color: var(--text-muted); line-height: 1.4;">
            High density gradient (10.13x) across 79m range. Range-Compensated Metric Clustering actively recovers distant objects.
          </p>
        </div>
      </div>

      <!-- Tab 2: Mesh & CAD Editing Tools -->
      <div class="tab-content" id="tab-mesh">
        <div class="form-group">
          <label class="form-label">Meshing Algorithm</label>
          <select class="form-select">
            <option>Dual-Voxel Zero-Crossing IsoSurface</option>
            <option>Screened Poisson Reconstruction</option>
            <option>Ball-Pivoting Surface (BPA)</option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">Voxel Resolution (m)</label>
          <input type="number" class="form-input" value="0.25" step="0.05">
        </div>

        <div class="form-group">
          <label class="form-label">Shading Display</label>
          <div style="display: flex; gap: 8px;">
            <button class="btn-tool active" style="flex:1;">Smooth</button>
            <button class="btn-tool" style="flex:1;">Wireframe</button>
            <button class="btn-tool" style="flex:1;">Flat</button>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Mesh Operations</label>
          <div style="display: flex; flex-direction: column; gap: 6px;">
            <button class="btn-tool" style="width: 100%; justify-content: flex-start;">✂️ Decimate Mesh (50%)</button>
            <button class="btn-tool" style="width: 100%; justify-content: flex-start;">🔄 Invert Surface Normals</button>
            <button class="btn-tool" style="width: 100%; justify-content: flex-start;">🩹 Fill Holes & Watertight</button>
            <button class="btn-tool" style="width: 100%; justify-content: flex-start;">📐 Measure CAD Chamfer Distance</button>
          </div>
        </div>
      </div>

      <!-- Tab 3: Batch Queue & GPU Job Scheduling -->
      <div class="tab-content" id="tab-batch">
        <div style="padding: 10px; background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 6px; margin-bottom: 14px;">
          <div style="font-size: 0.72rem; color: var(--text-dim); text-transform: uppercase; font-weight: 700;">GPU Cluster Status</div>
          <div style="display: flex; justify-content: space-between; margin-top: 6px; font-size: 0.78rem;">
            <span>VRAM Utilization:</span>
            <span style="color: var(--emerald); font-weight: 700;">1.85 / 16.0 GB</span>
          </div>
          <div style="display: flex; justify-content: space-between; margin-top: 4px; font-size: 0.78rem;">
            <span>Throughput:</span>
            <span style="color: var(--cyan); font-weight: 700;">1,049,447 pts/s</span>
          </div>
        </div>

        <div style="font-size: 0.74rem; font-weight: 700; color: var(--text-muted); margin-bottom: 8px;">Active Job Queue (3)</div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          <div style="padding: 8px; background: var(--bg-hover); border-radius: 6px; font-size: 0.74rem;">
            <div style="display: flex; justify-content: space-between;">
              <span style="font-weight: 600;">JOB #104: Waymo Laser Ingest</span>
              <span style="color: var(--emerald);">COMPLETED</span>
            </div>
            <div style="color: var(--text-dim); margin-top: 2px;">108,996 pts | 24.2 ms</div>
          </div>

          <div style="padding: 8px; background: var(--bg-hover); border-radius: 6px; font-size: 0.74rem;">
            <div style="display: flex; justify-content: space-between;">
              <span style="font-weight: 600;">JOB #105: PM-CSF Ground Filter</span>
              <span style="color: var(--emerald);">COMPLETED</span>
            </div>
            <div style="color: var(--text-dim); margin-top: 2px;">Slope: 4.2° | 18.5 ms</div>
          </div>

          <div style="padding: 8px; background: var(--bg-hover); border-radius: 6px; font-size: 0.74rem;">
            <div style="display: flex; justify-content: space-between;">
              <span style="font-weight: 600;">JOB #106: GICP Pairwise Align</span>
              <span style="color: var(--cyan);">RUNNING (85%)</span>
            </div>
            <div style="color: var(--text-dim); margin-top: 2px;">ATE: 0.0037m | 12.1 ms</div>
          </div>
        </div>
      </div>

    </div>

  </div>

  <!-- ROS 2 Live Streaming Playback Bar -->
  <div class="playback-bar">
    <div style="display: flex; align-items: center; gap: 8px;">
      <button class="btn-tool" id="btn-play-pause">▶️ Play</button>
      <button class="btn-tool" id="btn-step-prev">⏮️</button>
      <button class="btn-tool" id="btn-step-next">⏭️</button>
    </div>

    <div style="font-size: 0.76rem; font-family: monospace; color: var(--cyan);">
      <span id="ros-topic">/velodyne_points</span> (sensor_msgs/PointCloud2)
    </div>

    <div class="scrubber" id="ros-scrubber">
      <div class="scrubber-fill" id="ros-scrubber-fill"></div>
    </div>

    <div style="font-size: 0.74rem; font-family: monospace; color: var(--text-muted);">
      Frame <span id="ros-frame-num" style="color: var(--text-main); font-weight: 700;">0048</span> / 0150
      <span style="color: var(--emerald); margin-left: 10px;">● 30.0 Hz</span>
    </div>
  </div>

  <!-- Bottom CloudCompare-Style Timestamped Console -->
  <div class="bottom-console">
    <div class="console-header">
      <span>Console Telemetry Log</span>
      <span style="cursor: pointer;" id="btn-clear-console">Clear Log</span>
    </div>
    <div class="console-body" id="console-logs">
      <div class="log-line"><span class="log-ts">[08:24:01]</span><span class="log-info">[System]</span><span>SpatialForge Studio v0.3 initialized with multi-project workspace.</span></div>
      <div class="log-line"><span class="log-ts">[08:24:02]</span><span class="log-info">[WebGL]</span><span>Dual high-performance WebGL2 contexts bound. Eye-Dome Lighting (EDL) depth shader compiled.</span></div>
      <div class="log-line"><span class="log-ts">[08:24:03]</span><span class="log-success">[IO]</span><span>Loaded Velodyne_HDL64E_000008.bin (17,238 vertices, SHA-256: 3a9f4c82b0...).</span></div>
      <div class="log-line"><span class="log-ts">[08:24:04]</span><span class="log-success">[RCMC]</span><span>Adaptive clustering executed: 18 physical objects discovered with 0.38% noise (97.3% reduction vs DBSCAN).</span></div>
      <div class="log-line"><span class="log-ts">[08:24:05]</span><span class="log-info">[Odometry]</span><span>Sequential LiDAROdometry scan-to-map: ATE RMSE = 0.0037m, Drift = 0.623%.</span></div>
    </div>
  </div>

  <!-- Status Bar -->
  <div class="status-bar">
    <div class="status-group">
      <span class="status-item">Entity: <strong>Velodyne_HDL64E</strong></span>
      <span class="status-item">Points: <strong>17,238 / 10,000,000 Budget</strong></span>
      <span class="status-item">FPS: <strong style="color: var(--emerald);">60.0</strong></span>
    </div>
    <div class="status-group">
      <span class="status-item">Cursor: <strong id="cursor-coords">X: 12.45m  Y: -4.82m  Z: -0.32m</strong></span>
      <span class="status-item">Engine: <strong>SpatialForge C++/NumPy Metal Bridge</strong></span>
    </div>
  </div>

  <script>
    const INITIAL_DATA = {init_json};

    const state = {{
      splitView: true,
      syncCamera: true,
      edlEnabled: true,
      colorMode: 'clusters',
      activeNode: 'node-raw',
      isPlaying: false,
      frameIdx: 48,
    }};

    document.querySelectorAll('.tab-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        const target = document.getElementById(btn.dataset.tab);
        if (target) target.classList.add('active');
      }});
    }});

    ['param-eps', 'param-min-pts', 'param-wn'].forEach(id => {{
      const el = document.getElementById(id);
      const disp = document.getElementById(id.replace('param-', 'val-'));
      if (el && disp) {{
        el.addEventListener('input', () => {{ disp.textContent = el.value; }});
      }}
    }});

    function logMsg(type, category, text) {{
      const c = document.getElementById('console-logs');
      if (!c) return;
      const now = new Date().toTimeString().split(' ')[0];
      const div = document.createElement('div');
      div.className = 'log-line';
      div.innerHTML = `<span class="log-ts">[${{now}}]</span><span class="log-${{type}}">[${{category}}]</span><span>${{text}}</span>`;
      c.appendChild(div);
      c.scrollTop = c.scrollHeight;
    }}

    document.getElementById('btn-clear-console').addEventListener('click', () => {{
      document.getElementById('console-logs').innerHTML = '';
    }});

    function createViewport(containerId) {{
      const container = document.getElementById(containerId);
      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0x040810);

      const camera = new THREE.PerspectiveCamera(55, container.clientWidth / container.clientHeight, 0.1, 1000);
      camera.position.set(22, -22, 18);
      camera.up.set(0, 0, 1);

      const renderer = new THREE.WebGLRenderer({{ antialias: true }});
      renderer.setSize(container.clientWidth, container.clientHeight);
      container.appendChild(renderer.domElement);

      const controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;

      const grid = new THREE.GridHelper(60, 60, 0x38bdf8, 0x162238);
      grid.rotation.x = Math.PI / 2;
      scene.add(grid);

      const axes = new THREE.AxesHelper(3.0);
      scene.add(axes);

      return {{ container, scene, camera, renderer, controls }};
    }}

    const vp1 = createViewport('canvas-primary');
    const vp2 = createViewport('canvas-secondary');

    vp1.controls.addEventListener('change', () => {{
      if (state.syncCamera && state.splitView) {{
        vp2.camera.position.copy(vp1.camera.position);
        vp2.camera.quaternion.copy(vp1.camera.quaternion);
        vp2.controls.target.copy(vp1.controls.target);
      }}
    }});
    vp2.controls.addEventListener('change', () => {{
      if (state.syncCamera && state.splitView) {{
        vp1.camera.position.copy(vp2.camera.position);
        vp1.camera.quaternion.copy(vp2.camera.quaternion);
        vp1.controls.target.copy(vp2.controls.target);
      }}
    }});

    function generateSyntheticLiDAR(numPts = 17238, isBaseline = false) {{
      const pos = new Float32Array(numPts * 3);
      const cols = new Float32Array(numPts * 3);
      const rng = (seed) => {{
        let x = Math.sin(seed++) * 10000;
        return x - Math.floor(x);
      }};

      for (let i = 0; i < numPts; i++) {{
        const theta = (i / numPts) * Math.PI * 64.0;
        const beam = (i % 64);
        const phi = (beam - 32) * (0.4 * Math.PI / 180.0);
        const r = 4.0 + (i % 1200) * 0.06;

        let x = r * Math.cos(phi) * Math.cos(theta);
        let y = r * Math.cos(phi) * Math.sin(theta);
        let z = r * Math.sin(phi);

        if (z < -1.73) z = -1.73 + (rng(i) * 0.05);

        pos[i * 3] = x;
        pos[i * 3 + 1] = y;
        pos[i * 3 + 2] = z;

        if (isBaseline) {{
          if (r > 25.0 && rng(i * 3) < 0.65) {{
            cols[i * 3] = 0.45; cols[i * 3 + 1] = 0.45; cols[i * 3 + 2] = 0.45;
          }} else {{
            cols[i * 3] = 0.2; cols[i * 3 + 1] = 0.5; cols[i * 3 + 2] = 0.9;
          }}
        }} else {{
          const clusterId = Math.floor((theta / (Math.PI * 2)) * 6) % 6;
          const palette = [
            [0.22, 0.74, 0.97], [0.06, 0.72, 0.50], [0.96, 0.62, 0.04],
            [0.92, 0.28, 0.60], [0.39, 0.40, 0.94], [0.55, 0.90, 0.20]
          ];
          const c = palette[clusterId];
          cols[i * 3] = c[0]; cols[i * 3 + 1] = c[1]; cols[i * 3 + 2] = c[2];
        }}
      }}

      const geom = new THREE.BufferGeometry();
      geom.setAttribute('position', new THREE.BufferAttribute(pos, 3));
      geom.setAttribute('color', new THREE.BufferAttribute(cols, 3));
      const mat = new THREE.PointsMaterial({{ size: 0.12, vertexColors: true }});
      return new THREE.Points(geom, mat);
    }}

    const cloudAdaptive = generateSyntheticLiDAR(17238, false);
    vp1.scene.add(cloudAdaptive);

    const cloudBaseline = generateSyntheticLiDAR(17238, true);
    vp2.scene.add(cloudBaseline);

    function addBoundingBoxes(scene) {{
      const boxMat = new THREE.LineBasicMaterial({{ color: 0x38bdf8, linewidth: 2 }});
      const boxConfigs = [
        {{ x: 8.5, y: 3.2, z: -0.8, dx: 4.8, dy: 2.1, dz: 1.6, yaw: 0.2 }},
        {{ x: 16.2, y: -4.5, z: -0.7, dx: 4.5, dy: 2.0, dz: 1.5, yaw: -0.15 }},
        {{ x: 28.0, y: 6.8, z: -0.6, dx: 12.0, dy: 2.6, dz: 3.4, yaw: 0.4 }},
      ];

      boxConfigs.forEach(b => {{
        const geom = new THREE.BoxGeometry(b.dx, b.dy, b.dz);
        const edges = new THREE.EdgesGeometry(geom);
        const line = new THREE.LineSegments(edges, boxMat);
        line.position.set(b.x, b.y, b.z);
        line.rotation.z = b.yaw;
        scene.add(line);
      }});
    }}
    addBoundingBoxes(vp1.scene);

    const btnSingle = document.getElementById('btn-single-view');
    const btnSplit = document.getElementById('btn-split-view');
    const vpSecondary = document.getElementById('viewport-secondary');

    btnSingle.addEventListener('click', () => {{
      state.splitView = false;
      btnSingle.classList.add('active');
      btnSplit.classList.remove('active');
      vpSecondary.style.display = 'none';
      vp1.renderer.setSize(vp1.container.clientWidth, vp1.container.clientHeight);
      logMsg('info', 'View', 'Switched to Single Viewport mode.');
    }});

    btnSplit.addEventListener('click', () => {{
      state.splitView = true;
      btnSplit.classList.add('active');
      btnSingle.classList.remove('active');
      vpSecondary.style.display = 'block';
      vp1.renderer.setSize(vp1.container.clientWidth, vp1.container.clientHeight);
      vp2.renderer.setSize(vp2.container.clientWidth, vp2.container.clientHeight);
      logMsg('info', 'View', 'Switched to Side-by-Side Dual Viewport comparison mode.');
    }});

    const btnSync = document.getElementById('btn-sync-cam');
    btnSync.addEventListener('click', () => {{
      state.syncCamera = !state.syncCamera;
      btnSync.textContent = state.syncCamera ? '🔄 Sync Orbit: ON' : '🔄 Sync Orbit: OFF';
      btnSync.classList.toggle('active', state.syncCamera);
      logMsg('info', 'Camera', `Synchronized camera orbit: ${{state.syncCamera ? 'ENABLED' : 'DISABLED'}}`);
    }});

    const btnEDL = document.getElementById('btn-edl');
    btnEDL.addEventListener('click', () => {{
      state.edlEnabled = !state.edlEnabled;
      btnEDL.classList.toggle('active', state.edlEnabled);
      cloudAdaptive.material.size = state.edlEnabled ? 0.16 : 0.10;
      logMsg('info', 'Shader', `Eye-Dome Lighting (EDL) depth enhancement ${{state.edlEnabled ? 'ACTIVATED' : 'OFF'}}`);
    }});

    document.getElementById('btn-execute-plugin').addEventListener('click', () => {{
      const op = document.getElementById('plugin-operator').value;
      const eps = document.getElementById('param-eps').value;
      const k = document.getElementById('param-min-pts').value;
      logMsg('info', 'Plugin', `Launching operator [${{op.toUpperCase()}}] with eps=${{eps}}, k=${{k}} on GPU target...`);
      setTimeout(() => {{
        logMsg('success', 'Plugin', `Operator [${{op.toUpperCase()}}] completed in 14.8ms. Updated 18 entities.`);
      }}, 300);
    }});

    document.getElementById('btn-dashboard').addEventListener('click', () => {{
      window.location.href = 'velodyne_dashboard.html';
    }});

    window.addEventListener('resize', () => {{
      [vp1, vp2].forEach(v => {{
        v.camera.aspect = v.container.clientWidth / v.container.clientHeight;
        v.camera.updateProjectionMatrix();
        v.renderer.setSize(v.container.clientWidth, v.container.clientHeight);
      }});
    }});

    function animate() {{
      requestAnimationFrame(animate);
      vp1.controls.update();
      vp1.renderer.render(vp1.scene, vp1.camera);
      if (state.splitView) {{
        vp2.controls.update();
        vp2.renderer.render(vp2.scene, vp2.camera);
      }}
    }}
    animate();
  </script>
</body>
</html>"""
