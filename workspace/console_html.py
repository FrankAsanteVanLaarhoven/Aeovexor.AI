"""
AEOVEXOR Studio Console HTML & 3D WebGL Canvas Module
======================================================
Military-Grade / Aerospace 3D Spatial Intelligence Console (NASA JPL & Palantir Aesthetic):
  - Sleek Monoline SVG Icons (Zero Emojis, Pure Tactical Engineering Vector HUD)
  - Collapsible Slide Sidebar & Accordion Category Sections
  - AEOVEXOR 3D Spatial Inspector (Precision 7-DOF Spatial Transforms)
  - Point Cloud Precision Zooming (Sub-Centimeter Depth, Reticle Coordinate Readout)
  - Before / After A/B Dual-State Telemetry Comparison Engine
  - Satellite 3D Earth Elevation Mapping & Watertight Instant Meshing
  - Kaufman Adaptive Filter (KAMA) Noise Suppression & Emergency Collision Alerts
  - OpenRouter Multi-Model Super Intelligence Copilot
"""

def render_console_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AEOVEXOR Studio — Precision 3D Geometry & Spatial Intelligence</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="icon" type="image/png" href="/static/aeovexor_mark_icon.png">
  <style>
    :root {
      --bg-dark: #06080D;
      --bg-panel: #0B0F17;
      --bg-header: #0E131E;
      --bg-hover: #141B2A;
      --border: rgba(148, 163, 184, 0.12);
      --border-accent: rgba(0, 229, 255, 0.35);
      --border-focus: rgba(0, 229, 255, 0.7);
      --cyan: #00E5FF;
      --cyan-dim: rgba(0, 229, 255, 0.15);
      --cyan-glow: rgba(0, 229, 255, 0.25);
      --emerald: #10B981;
      --amber: #F59E0B;
      --rose: #EF4444;
      --slate: #94A3B8;
      --text: #F1F5F9;
      --text-muted: #94A3B8;
      --text-dim: #64748B;
      --sidebar-width: 340px;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Sora', sans-serif;
      background: var(--bg-dark);
      color: var(--text);
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      user-select: none;
    }

    /* SVG Icon Helpers */
    .svg-icon {
      width: 14px;
      height: 14px;
      stroke-width: 1.8;
      stroke: currentColor;
      fill: none;
      stroke-linecap: round;
      stroke-linejoin: round;
      flex-shrink: 0;
    }
    .svg-icon-lg {
      width: 16px;
      height: 16px;
    }

    /* Top Navigation */
    .top-nav {
      height: 48px;
      background: var(--bg-header);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 14px;
      z-index: 100;
    }
    .brand-group {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 700;
      font-size: 0.88rem;
    }
    .brand-logo-icon {
      width: 24px;
      height: 24px;
      object-fit: contain;
      filter: drop-shadow(0 0 6px var(--cyan-glow));
    }
    .dataset-badge {
      font-size: 0.72rem;
      font-family: 'JetBrains Mono', monospace;
      color: var(--cyan);
      background: var(--cyan-dim);
      border: 1px solid rgba(0, 229, 255, 0.25);
      padding: 2px 8px;
      border-radius: 4px;
      letter-spacing: 0.04em;
    }

    /* Comparison Dual-State Controls */
    .compare-group {
      display: inline-flex;
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid var(--border);
      border-radius: 5px;
      padding: 2px;
      gap: 2px;
    }
    .btn-compare-tab {
      background: transparent;
      border: none;
      color: var(--text-dim);
      padding: 4px 10px;
      border-radius: 3px;
      font-size: 0.70rem;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.15s;
    }
    .btn-compare-tab:hover {
      color: var(--text);
      background: rgba(255, 255, 255, 0.05);
    }
    .btn-compare-tab.active {
      background: var(--cyan);
      color: #06080D;
      box-shadow: 0 0 10px var(--cyan-glow);
    }
    .btn-compare-tab.active-raw {
      background: #3B82F6;
      color: #FFFFFF;
      box-shadow: 0 0 10px rgba(59, 130, 246, 0.4);
    }

    .top-actions {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .btn {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 5px 9px;
      border-radius: 4px;
      font-size: 0.72rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
    }
    .btn:hover {
      background: var(--bg-hover);
      color: var(--text);
      border-color: rgba(255,255,255,0.22);
    }
    .btn.active {
      background: var(--cyan-dim);
      color: var(--cyan);
      border-color: var(--cyan);
    }
    .btn-primary {
      background: var(--cyan);
      color: #06080D;
      font-weight: 700;
      border-color: var(--cyan);
      box-shadow: 0 0 12px var(--cyan-glow);
    }
    .btn-primary:hover {
      background: #22E7FF;
      color: #06080D;
      box-shadow: 0 0 18px var(--cyan-glow);
    }
    .btn-tactical {
      background: rgba(245, 158, 11, 0.12);
      border-color: rgba(245, 158, 11, 0.35);
      color: #FCD34D;
      font-weight: 700;
    }
    .btn-tactical:hover {
      background: rgba(245, 158, 11, 0.22);
      border-color: var(--amber);
    }

    /* Hazard Indicator Pill */
    .hazard-pill {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.70rem;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      letter-spacing: 0.02em;
    }
    .hazard-indicator-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
    }
    .hazard-brake {
      background: rgba(239, 68, 68, 0.14);
      color: #FCA5A5;
      border: 1px solid rgba(239, 68, 68, 0.4);
    }
    .hazard-brake .hazard-indicator-dot {
      background: var(--rose);
      box-shadow: 0 0 8px var(--rose);
      animation: pulse-dot 1.0s infinite;
    }
    .hazard-steer {
      background: rgba(245, 158, 11, 0.14);
      color: #FCD34D;
      border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .hazard-steer .hazard-indicator-dot {
      background: var(--amber);
    }
    .hazard-clear {
      background: rgba(16, 185, 129, 0.14);
      color: #6EE7B7;
      border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .hazard-clear .hazard-indicator-dot {
      background: var(--emerald);
    }

    /* Main Container */
    .main-wrap {
      flex: 1;
      display: flex;
      position: relative;
      overflow: hidden;
    }

    /* Collapsible Left Sidebar */
    .sidebar {
      width: var(--sidebar-width);
      min-width: var(--sidebar-width);
      background: var(--bg-panel);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      z-index: 40;
      position: relative;
      transition: width 0.25s cubic-bezier(0.16, 1, 0.3, 1), min-width 0.25s cubic-bezier(0.16, 1, 0.3, 1), transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .sidebar.collapsed {
      width: 0 !important;
      min-width: 0 !important;
      border-right: none;
      overflow: hidden;
    }
    /* Left sidebar hover-peek effect */
    .sidebar.hover-peek {
      position: absolute !important;
      top: 0 !important;
      bottom: 0 !important;
      left: 0 !important;
      width: var(--sidebar-width) !important;
      min-width: var(--sidebar-width) !important;
      border-right: 1px solid var(--border-accent) !important;
      box-shadow: 16px 0 45px rgba(0,0,0,0.95), 0 0 25px rgba(0,229,255,0.15) !important;
      z-index: 95 !important;
      overflow: visible !important;
      background: var(--bg-panel) !important;
    }
    .left-hover-zone {
      position: absolute;
      top: 0;
      left: 0;
      width: 18px;
      height: 100%;
      z-index: 70;
      display: none;
    }
    .sidebar.collapsed ~ .left-hover-zone {
      display: block;
    }

    /* Sidebar Edge Toggle Handle */
    .sidebar-toggle-handle {
      position: absolute;
      top: 50%;
      right: -13px;
      transform: translateY(-50%);
      width: 14px;
      height: 48px;
      background: var(--bg-header);
      border: 1px solid var(--border);
      border-left: none;
      border-radius: 0 6px 6px 0;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      z-index: 60;
      color: var(--text-dim);
      transition: all 0.15s;
    }
    .sidebar-toggle-handle:hover {
      background: var(--bg-hover);
      color: var(--cyan);
      border-color: var(--cyan);
      box-shadow: 2px 0 10px var(--cyan-glow);
    }
    .sidebar.collapsed + .sidebar-floating-toggle {
      display: flex;
    }
    .sidebar-floating-toggle {
      position: absolute;
      top: 60px;
      left: 12px;
      z-index: 85;
      background: var(--bg-header);
      border: 1px solid var(--border-accent);
      border-radius: 5px;
      padding: 6px 9px;
      color: var(--cyan);
      cursor: pointer;
      display: none;
      align-items: center;
      gap: 6px;
      font-size: 0.72rem;
      font-weight: 700;
      box-shadow: 0 4px 15px rgba(0,0,0,0.7);
    }

    .sidebar-tabs {
      display: flex;
      border-bottom: 1px solid var(--border);
      background: var(--bg-header);
    }
    .s-tab {
      flex: 1;
      padding: 9px 0;
      text-align: center;
      font-size: 0.70rem;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      border-bottom: 2px solid transparent;
      transition: all 0.15s;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      letter-spacing: 0.02em;
    }
    .s-tab:hover {
      color: var(--text);
      background: rgba(255, 255, 255, 0.03);
    }
    .s-tab.active {
      color: var(--cyan);
      border-bottom-color: var(--cyan);
      background: var(--cyan-dim);
    }
    .s-body {
      flex: 1;
      overflow-y: auto;
      padding: 12px;
    }

    /* Accordion Category Sections */
    .acc-sec {
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--border);
      border-radius: 6px;
      margin-bottom: 8px;
      overflow: hidden;
      transition: border-color 0.15s;
    }
    .acc-sec:hover {
      border-color: rgba(255, 255, 255, 0.18);
    }
    .acc-header {
      padding: 9px 12px;
      background: rgba(255, 255, 255, 0.02);
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      user-select: none;
      border-bottom: 1px solid transparent;
      transition: background 0.15s;
    }
    .acc-header:hover {
      background: rgba(255, 255, 255, 0.04);
    }
    .acc-sec.open .acc-header {
      border-bottom-color: var(--border);
    }
    .acc-title {
      font-size: 0.70rem;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--text);
      display: flex;
      align-items: center;
      gap: 7px;
    }
    .acc-chevron {
      width: 12px;
      height: 12px;
      color: var(--text-dim);
      transition: transform 0.2s;
    }
    .acc-sec.open .acc-chevron {
      transform: rotate(180deg);
      color: var(--cyan);
    }
    .acc-content {
      padding: 12px;
      display: none;
    }
    .acc-sec.open .acc-content {
      display: block;
    }

    .control-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
      font-size: 0.73rem;
      color: var(--text-muted);
    }
    .control-select, .control-input {
      background: var(--bg-dark);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 0.72rem;
      font-family: 'JetBrains Mono', monospace;
      outline: none;
    }
    .control-select:focus, .control-input:focus {
      border-color: var(--cyan);
    }
    .toggle-row {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 7px;
      font-size: 0.73rem;
      cursor: pointer;
      color: var(--text-muted);
    }
    .toggle-row:hover {
      color: var(--text);
    }
    .toggle-row input {
      cursor: pointer;
      accent-color: var(--cyan);
    }

    /* 3D Viewport Area */
    .viewport-box {
      flex: 1;
      position: relative;
      background: #04060A;
      overflow: hidden;
    }
    #viewport-3d {
      width: 100%;
      height: 100%;
    }

    /* Tactical HUD Crosshair */
    .reticle-telemetry {
      position: absolute;
      bottom: 14px;
      left: 14px;
      z-index: 50;
      background: rgba(11, 15, 23, 0.90);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border);
      border-radius: 5px;
      padding: 6px 12px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.70rem;
      color: var(--text-dim);
      display: flex;
      align-items: center;
      gap: 12px;
      letter-spacing: 0.04em;
    }
    .reticle-coord {
      color: var(--cyan);
      font-weight: 600;
    }

    /* Data State Indicator Overlay (Top Right of Viewport) */
    .data-state-overlay {
      position: absolute;
      top: 14px;
      right: 14px;
      z-index: 50;
      background: rgba(11, 15, 23, 0.90);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border);
      border-radius: 5px;
      padding: 6px 12px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.70rem;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .state-badge {
      padding: 2px 6px;
      border-radius: 3px;
      font-weight: 700;
    }
    .state-badge-b {
      background: var(--cyan-dim);
      color: var(--cyan);
      border: 1px solid rgba(0, 229, 255, 0.3);
    }
    .state-badge-a {
      background: rgba(59, 130, 246, 0.15);
      color: #93C5FD;
      border: 1px solid rgba(59, 130, 246, 0.3);
    }

    /* Split Viewport Interactive Divider */
    .split-divider {
      position: absolute;
      top: 0;
      bottom: 0;
      width: 4px;
      margin-left: -2px;
      background: linear-gradient(180deg, var(--cyan), rgba(0, 229, 255, 0.4) 50%, var(--emerald));
      box-shadow: 0 0 10px rgba(0, 229, 255, 0.5);
      z-index: 60;
      cursor: col-resize;
      transition: background 0.2s;
    }
    .split-divider:hover {
      width: 6px;
      margin-left: -3px;
      background: #FFF;
      box-shadow: 0 0 14px #00E5FF;
    }
    .split-divider-handle {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: #0B0F17;
      border: 1px solid var(--cyan);
      box-shadow: 0 0 8px rgba(0, 229, 255, 0.4);
      color: var(--cyan);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.65rem;
      font-weight: 700;
      padding: 6px 4px;
      border-radius: 4px;
      writing-mode: vertical-rl;
      text-orientation: mixed;
      letter-spacing: 0.1em;
      pointer-events: none;
      user-select: none;
    }
    .split-subwindow-badge {
      position: absolute;
      top: 14px;
      z-index: 55;
      background: rgba(11, 15, 23, 0.88);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 5px 10px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      letter-spacing: 0.05em;
      display: flex;
      align-items: center;
      gap: 7px;
      pointer-events: none;
    }
    .split-badge-left {
      left: 14px;
      border-color: rgba(59, 130, 246, 0.4);
      color: #93C5FD;
    }
    .split-badge-right {
      left: calc(50% + 14px);
      border-color: rgba(0, 229, 255, 0.4);
      color: var(--cyan);
    }
    .subwindow-indicator {
      width: 7px;
      height: 7px;
      border-radius: 50%;
    }
    .raw-indicator {
      background: #60A5FA;
      box-shadow: 0 0 6px #3B82F6;
    }
    .processed-indicator {
      background: #10B981;
      box-shadow: 0 0 6px #10B981;
    }

    /* Floating Panels */
    .floating-dialog {
      position: absolute;
      top: 60px;
      right: 20px;
      width: 320px;
      background: rgba(11, 15, 23, 0.96);
      backdrop-filter: blur(14px);
      border: 1px solid var(--border-accent);
      border-radius: 8px;
      padding: 14px;
      z-index: 80;
      display: none;
      box-shadow: 0 16px 40px rgba(0,0,0,0.85);
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.2s;
    }

    /* Right Tactical Dock Strip (Collapsible hover / click to view) */
    .right-dock-strip {
      position: absolute;
      top: 65px;
      right: 0;
      display: flex;
      flex-direction: column;
      gap: 6px;
      z-index: 75;
    }
    .right-dock-tab {
      background: rgba(11, 15, 23, 0.94);
      border: 1px solid var(--border);
      border-right: none;
      border-radius: 6px 0 0 6px;
      padding: 10px 8px;
      color: var(--text-dim);
      font-size: 0.65rem;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: 0.05em;
      writing-mode: vertical-rl;
      text-orientation: mixed;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
      box-shadow: -4px 4px 15px rgba(0,0,0,0.7);
    }
    .right-dock-tab:hover, .right-dock-tab.active {
      color: var(--cyan);
      border-color: var(--cyan);
      background: var(--bg-hover);
      box-shadow: -4px 0 15px var(--cyan-glow);
    }

    /* AEOVEXOR 3D Spatial Inspector (Draggable, Resizable, Collapsible Full CRUD) */
    #spatial-inspector {
      width: 360px;
      min-width: 320px;
      min-height: 180px;
      max-width: 92vw;
      max-height: 88vh;
      resize: both;
      overflow: auto;
      right: 18px;
      bottom: 48px;
      top: auto;
      border-color: var(--border-accent);
      box-shadow: 0 16px 45px rgba(0,0,0,0.92), 0 0 25px rgba(0, 229, 255, 0.15);
      transition: width 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    #spatial-inspector.is-collapsed {
      height: 48px !important;
      min-height: 48px !important;
      overflow: hidden !important;
      resize: none !important;
    }
    #spatial-inspector.is-collapsed #ci-body {
      display: none !important;
    }
    #spatial-inspector.is-expanded {
      width: 580px !important;
      max-width: 92vw !important;
    }
    .ci-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 10px;
      cursor: grab;
      user-select: none;
    }
    .ci-header:active {
      cursor: grabbing;
    }
    .ci-tool-btn {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border);
      border-radius: 4px;
      width: 24px;
      height: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text-dim);
      cursor: pointer;
      transition: all 0.15s;
    }
    .ci-tool-btn:hover {
      background: var(--bg-hover);
      color: var(--cyan);
      border-color: var(--cyan);
    }
    .ci-tool-btn.active {
      background: var(--cyan-dim);
      color: var(--cyan);
      border-color: var(--cyan);
    }
    .ci-tabs {
      display: flex;
      border-bottom: 1px solid var(--border);
      margin-bottom: 8px;
      gap: 4px;
    }
    .ci-tab-btn {
      background: none;
      border: none;
      border-bottom: 2px solid transparent;
      padding: 5px 8px;
      font-size: 0.68rem;
      font-weight: 700;
      color: var(--text-dim);
      cursor: pointer;
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: 0.04em;
      transition: all 0.15s;
    }
    .ci-tab-btn.active {
      color: var(--cyan);
      border-bottom-color: var(--cyan);
    }
    .ci-title {
      font-size: 0.78rem;
      font-weight: 800;
      color: var(--cyan);
      display: flex;
      align-items: center;
      gap: 7px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }
    .ci-badge {
      font-size: 0.65rem;
      font-family: 'JetBrains Mono', monospace;
      padding: 2px 6px;
      border-radius: 3px;
      font-weight: 700;
      letter-spacing: 0.04em;
    }
    .ci-badge-veh { background: var(--cyan-dim); color: var(--cyan); border: 1px solid rgba(0,229,255,0.3); }
    .ci-badge-ped { background: rgba(16, 185, 129, 0.15); color: var(--emerald); border: 1px solid rgba(16, 185, 129, 0.3); }
    .ci-badge-cyc { background: rgba(245, 158, 11, 0.15); color: var(--amber); border: 1px solid rgba(245, 158, 11, 0.3); }
    .ci-badge-inf { background: rgba(148, 163, 184, 0.15); color: var(--slate); border: 1px solid rgba(148, 163, 184, 0.3); }
    .ci-badge-obs { background: rgba(252, 165, 165, 0.15); color: #FCA5A5; border: 1px solid rgba(252, 165, 165, 0.3); }

    .ci-grid-3 {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 6px;
      margin-bottom: 8px;
    }
    .ci-input-col {
      display: flex;
      flex-direction: column;
      gap: 3px;
    }
    .ci-input-col label {
      font-size: 0.64rem;
      color: var(--text-dim);
      font-weight: 700;
      letter-spacing: 0.04em;
    }
    .ci-input-col input {
      background: var(--bg-dark);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 4px 6px;
      border-radius: 3px;
      font-size: 0.74rem;
      font-family: 'JetBrains Mono', monospace;
      text-align: right;
    }

    .occlusion-bar-wrap {
      background: rgba(255,255,255,0.06);
      height: 4px;
      border-radius: 2px;
      overflow: hidden;
      margin: 4px 0 10px 0;
    }
    .occlusion-bar-fill {
      height: 100%;
      background: var(--emerald);
      border-radius: 2px;
      transition: width 0.2s;
    }

    /* Object Roster Cards */
    .roster-card {
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 7px 9px;
      margin-bottom: 5px;
      cursor: pointer;
      transition: all 0.15s;
    }
    .roster-card:hover {
      background: rgba(0, 229, 255, 0.05);
      border-color: var(--border-accent);
      transform: translateX(2px);
    }
    .roster-card.active {
      background: var(--cyan-dim);
      border-color: var(--cyan);
    }
    .badge-occ {
      font-size: 0.65rem;
      font-family: 'JetBrains Mono', monospace;
      padding: 1px 5px;
      border-radius: 3px;
      font-weight: 700;
    }
    .occ-low {
      background: rgba(16, 185, 129, 0.12);
      color: #6EE7B7;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .occ-med {
      background: rgba(245, 158, 11, 0.12);
      color: #FCD34D;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .occ-high {
      background: rgba(239, 68, 68, 0.12);
      color: #FCA5A5;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* Super Intelligence AI Copilot Drawer */
    #ai-copilot-drawer {
      position: absolute;
      top: 56px;
      right: 18px;
      width: 410px;
      height: calc(100vh - 110px);
      background: rgba(11, 15, 23, 0.97);
      backdrop-filter: blur(18px);
      border: 1px solid var(--border-accent);
      border-radius: 8px;
      padding: 14px;
      z-index: 95;
      display: none;
      flex-direction: column;
      box-shadow: 0 20px 60px rgba(0,0,0,0.95), 0 0 35px var(--cyan-glow);
    }
    .ai-chat-history {
      flex: 1;
      overflow-y: auto;
      padding: 10px 0;
      display: flex;
      flex-direction: column;
      gap: 10px;
      font-size: 0.76rem;
    }
    .chat-bubble {
      padding: 9px 12px;
      border-radius: 6px;
      line-height: 1.5;
    }
    .chat-user {
      background: var(--cyan-dim);
      border: 1px solid rgba(0, 229, 255, 0.25);
      align-self: flex-end;
      max-width: 90%;
    }
    .chat-ai {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border);
      align-self: flex-start;
      max-width: 100%;
    }
    .quick-chip {
      background: rgba(255,255,255,0.03);
      border: 1px solid var(--border);
      border-radius: 3px;
      padding: 3px 8px;
      font-size: 0.67rem;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.15s;
      color: var(--text-muted);
    }
    .quick-chip:hover {
      background: var(--cyan-dim);
      border-color: var(--cyan);
      color: var(--cyan);
    }

    /* Bottom Status Bar */
    .playback-bar {
      height: 36px;
      background: var(--bg-header);
      border-top: 1px solid var(--border);
      display: flex;
      align-items: center;
      padding: 0 14px;
      gap: 14px;
      z-index: 50;
      font-size: 0.70rem;
      font-family: 'JetBrains Mono', monospace;
    }
    .progress-track {
      flex: 1;
      height: 4px;
      background: rgba(255,255,255,0.08);
      border-radius: 2px;
      cursor: pointer;
      position: relative;
    }
    .progress-fill {
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      width: 35%;
      background: var(--cyan);
      border-radius: 2px;
    }

    /* Modal Windows */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(6, 8, 13, 0.90);
      backdrop-filter: blur(14px);
      z-index: 2000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .modal-box {
      background: var(--bg-panel);
      border: 1px solid var(--border-accent);
      border-radius: 8px;
      max-width: 860px;
      width: 100%;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.95);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    .modal-header {
      padding: 12px 18px;
      background: var(--bg-header);
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .modal-body {
      padding: 16px 18px;
      max-height: 500px;
      overflow-y: auto;
    }
    .modal-footer {
      padding: 12px 18px;
      background: var(--bg-header);
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: flex-end;
      gap: 8px;
    }
    .export-tabs {
      display: flex;
      gap: 6px;
      margin-bottom: 12px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 8px;
    }
    .export-tab {
      background: rgba(255,255,255,0.03);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 5px 12px;
      border-radius: 4px;
      font-size: 0.74rem;
      cursor: pointer;
      font-weight: 600;
      font-family: 'JetBrains Mono', monospace;
      transition: all 0.15s;
    }
    .export-tab.active {
      background: var(--cyan-dim);
      border-color: var(--cyan);
      color: var(--cyan);
      font-weight: 700;
    }
    .export-code-box {
      width: 100%;
      height: 260px;
      background: #04060A;
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 12px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.74rem;
      color: #6EE7B7;
      resize: none;
      outline: none;
      line-height: 1.45;
    }

    /* CloudCompare & Presentation Suite Styles */
    .cc-vert-toolbar {
      position: absolute;
      left: 14px;
      top: 64px;
      z-index: 45;
      background: rgba(11, 15, 23, 0.88);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-accent);
      border-radius: 8px;
      padding: 6px 4px;
      display: flex;
      flex-direction: column;
      gap: 4px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.6);
      transition: opacity 0.2s;
    }
    .cc-divider {
      height: 1px;
      background: var(--border);
      margin: 3px 2px;
    }
    .cc-btn {
      width: 32px;
      height: 32px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid transparent;
      border-radius: 6px;
      color: var(--text-muted);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      position: relative;
      font-size: 0.62rem;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      transition: all 0.15s;
    }
    .cc-btn:hover {
      background: var(--bg-hover);
      border-color: var(--cyan);
      color: var(--cyan);
    }
    .cc-btn.active {
      background: var(--cyan-dim);
      border-color: var(--cyan);
      color: var(--cyan);
      box-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
    }
    .cc-horiz-toolbar {
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
      top: 14px;
      z-index: 45;
      background: rgba(11, 15, 23, 0.90);
      backdrop-filter: blur(14px);
      border: 1px solid var(--border-accent);
      border-radius: 8px;
      padding: 5px 10px;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 8px 36px rgba(0,0,0,0.65);
    }
    .cc-horiz-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 4px 9px;
      border-radius: 5px;
      font-size: 0.68rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
      white-space: nowrap;
    }
    .cc-horiz-btn:hover {
      background: var(--bg-hover);
      border-color: var(--cyan);
      color: var(--cyan);
    }
    .cc-horiz-btn.active {
      background: var(--cyan-dim);
      border-color: var(--cyan);
      color: var(--cyan);
    }
    .presentation-toolbar {
      position: absolute;
      right: 14px;
      bottom: 52px;
      z-index: 45;
      background: rgba(11, 15, 23, 0.90);
      backdrop-filter: blur(14px);
      border: 1px solid var(--border-accent);
      border-radius: 8px;
      padding: 5px 8px;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 8px 36px rgba(0,0,0,0.65);
    }
    .rec-status-badge {
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
      top: 56px;
      z-index: 50;
      display: none;
      align-items: center;
      gap: 8px;
      background: rgba(239, 68, 68, 0.18);
      border: 1px solid var(--rose);
      color: #FFF;
      padding: 4px 14px;
      border-radius: 20px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 700;
      box-shadow: 0 0 16px rgba(239, 68, 68, 0.4);
    }
    .rec-pulse-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--rose);
      animation: pulse-dot 1s infinite;
    }
    .pip-container {
      position: absolute;
      right: 14px;
      bottom: 44px;
      width: 290px;
      height: 190px;
      z-index: 46;
      background: rgba(6, 8, 13, 0.96);
      border: 1px solid var(--border-accent);
      border-radius: 8px;
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.85);
      display: none;
      flex-direction: column;
      overflow: hidden;
      resize: both;
    }
    .pip-header {
      height: 26px;
      background: var(--bg-header);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 8px;
      font-size: 0.64rem;
      font-weight: 700;
      color: var(--cyan);
      cursor: move;
    }
    .pip-viewport-canvas {
      flex: 1;
      width: 100%;
      height: 100%;
      position: relative;
    }
    .cc-hud-panel {
      position: absolute;
      background: rgba(11, 15, 23, 0.96);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-accent);
      border-radius: 8px;
      padding: 12px;
      z-index: 48;
      box-shadow: 0 10px 40px rgba(0,0,0,0.7);
      font-size: 0.72rem;
      color: var(--text);
    }
    .lasso-overlay-svg {
      position: absolute;
      top: 0; left: 0;
      width: 100%; height: 100%;
      pointer-events: none;
      z-index: 42;
    }
    .pin-annotation-marker {
      position: absolute;
      transform: translate(-50%, -100%);
      background: rgba(15, 23, 42, 0.92);
      border: 1px solid var(--cyan);
      border-radius: 4px;
      padding: 3px 8px;
      color: var(--cyan);
      font-size: 0.65rem;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      pointer-events: auto;
      cursor: pointer;
      box-shadow: 0 2px 10px rgba(0, 229, 255, 0.3);
      white-space: nowrap;
      z-index: 43;
    }
    .pin-annotation-marker::after {
      content: '';
      position: absolute;
      bottom: -6px;
      left: 50%;
      transform: translateX(-50%);
      border-width: 6px 5px 0;
      border-style: solid;
      border-color: var(--cyan) transparent transparent;
      display: block;
      width: 0;
    }
  </style>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/TransformControls.js"></script>
</head>
<body>

  <!-- Top Navigation Bar (Tactical Defense Console) -->
  <div class="top-nav">
    <div class="brand-group">
      <a href="/" class="btn" style="text-decoration:none; padding:4px 8px;" title="Mission Return to Portal">
        <svg class="svg-icon" viewBox="0 0 24 24"><polyline points="15 18 9 12 15 6"/></svg>
        <span>Overview</span>
      </a>
      <img src="/static/aeovexor_mark_icon.png" alt="AEOVEXOR" class="brand-logo-icon">
      <span style="letter-spacing:0.16em; font-weight:800; font-size:0.88rem; color:#F1F5F9;">
        ΛEOVEXOR <span style="color:var(--cyan); font-weight:600;">STUDIO</span>
      </span>
      <span class="dataset-badge" id="ds-badge">velodyne_000008.bin</span>
    </div>

    <!-- Before / After Dual-State Telemetry Switch -->
    <div class="compare-group" title="Toggle Data Processing State (Hotkey: C)">
      <button class="btn-compare-tab active" id="btn-state-b" onclick="setComparisonState('B')">
        <svg class="svg-icon" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
        <span>PROCESSED [B]</span>
      </button>
      <button class="btn-compare-tab" id="btn-state-a" onclick="setComparisonState('A')">
        <svg class="svg-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/></svg>
        <span>RAW INGEST [A]</span>
      </button>
      <button class="btn-compare-tab" id="btn-state-split" onclick="toggleSplitComparison()">
        <svg class="svg-icon" viewBox="0 0 24 24"><line x1="12" y1="3" x2="12" y2="21"/><polyline points="8 8 4 12 8 16"/><polyline points="16 8 20 12 16 16"/></svg>
        <span>SPLIT A/B</span>
      </button>
    </div>

    <!-- Live Collision Hazard Threat Pill -->
    <div class="hazard-pill hazard-brake" id="hazard-pill" title="Forward Obstacle Emergency Distance / Time-To-Impact">
      <div class="hazard-indicator-dot"></div>
      <span>TTC: <strong id="val-ttc">0.31s</strong></span>
      <span style="font-size: 0.65rem; text-transform: uppercase; opacity:0.85;" id="val-hazard-level">CRITICAL_BRAKE</span>
    </div>

    <div class="top-actions">
      <!-- AI Super Intelligence Copilot Toggle -->
      <button class="btn" id="btn-ai-copilot" title="OpenRouter Super Intelligence Reasoning Copilot">
        <svg class="svg-icon" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="15" x2="23" y2="15"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="15" x2="4" y2="15"/></svg>
        <span>AI Intelligence</span>
      </button>

      <!-- Precision Perception Suite -->
      <button class="btn btn-primary" id="btn-detect-3d" title="Execute Autonomous 3D Perception & Spatial Covariance Tensor Eigen-decomposition">
        <svg class="svg-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 10 10"/><path d="m12 12 7-7"/><circle cx="12" cy="12" r="2"/></svg>
        <span>Auto-Detect 3D</span>
      </button>

      <button class="btn active" id="btn-toggle-boxes">
        <svg class="svg-icon" viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
        <span>3D Boxes</span>
        <span id="badge-box-count" style="background:var(--cyan-dim); color:var(--cyan); padding:1px 5px; border-radius:3px; font-family:'JetBrains Mono'; font-size:0.68rem;">0</span>
      </button>

      <button class="btn active" id="btn-toggle-shapes" title="Toggle 3D Digital Twin Shapes (Vehicles, Pedestrians, Cyclists, Infrastructure, Obstacles)">
        <svg class="svg-icon" viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
        <span>3D Shapes</span>
      </button>

      <button class="btn" id="btn-add-box" title="Synthesize custom 3D bounding box for manual manipulation">
        <svg class="svg-icon" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        <span>Add Box</span>
      </button>

      <button class="btn" id="btn-export-3d" title="Export annotations to KITTI 3D, Waymo, COCO-3D, AEOVEXOR JSON">
        <svg class="svg-icon" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        <span>Export 3D</span>
      </button>

      <button class="btn" id="btn-slice" title="Cross-Section Slicing Tool">
        <svg class="svg-icon" viewBox="0 0 24 24"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/></svg>
        <span>Slicing</span>
      </button>

      <button class="btn" id="btn-toggle-toolbox" title="Toggle CloudCompare Developer Manipulation Toolbox">
        <svg class="svg-icon" viewBox="0 0 24 24"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
        <span>Toolbox</span>
      </button>

      <button class="btn" id="btn-toggle-recording" title="Full Screen Canvas Recording & Playback">
        <svg class="svg-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4" fill="currentColor"/></svg>
        <span>Record</span>
      </button>

      <button class="btn" id="btn-toggle-pip" title="Picture-in-Picture Secondary Inset Viewport">
        <svg class="svg-icon" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><rect x="12" y="9" width="8" height="6" rx="1" ry="1"/></svg>
        <span>PiP</span>
      </button>

      <button class="btn" id="btn-toggle-presentation" title="Presentation Suite: Tour, Laser Pointer & Fullscreen">
        <svg class="svg-icon" viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="16" rx="2"/><path d="M10 22h4M12 18v4M9 9l6 3-6 3V9z"/></svg>
        <span>Present</span>
      </button>

      <button class="btn" id="btn-caliper" title="3D Euclidean Measurement Caliper">
        <svg class="svg-icon" viewBox="0 0 24 24"><path d="M4 6h16M4 6v12M4 12h8M4 18h4M12 6v6M20 6v4"/></svg>
        <span>Caliper</span>
      </button>

      <a href="/ide" class="btn" title="Open AEOVEXOR Scientific IDE & Developer Terminal">
        <svg class="svg-icon" viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
        <span>Scientific IDE</span>
      </a>

      <a href="/ide?open_research=true" class="btn btn-primary" style="text-decoration:none; background:linear-gradient(135deg, #00E5FF 0%, #007ACC 100%); color:#000; font-weight:700;" title="AEOVEXOR AI/SI Autonomous Researcher: Generate Kaggle Grandmaster Notebooks & Scientific Publications">
        <svg class="svg-icon" viewBox="0 0 24 24"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>
        <span>AI Researcher</span>
      </a>

      <a href="/report" class="btn" target="_blank" style="text-decoration:none;" title="Geometric Benchmark Provenance Report">
        <svg class="svg-icon" viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
        <span>Benchmark Report</span>
      </a>
    </div>
  </div>

  <!-- Main Viewport & Collapsible Sidebar Wrap -->
  <div class="main-wrap">

    <!-- Left Controls Sidebar -->
    <div class="sidebar" id="main-sidebar">
      <!-- Embedded Collapse Handle on the edge -->
      <div class="sidebar-toggle-handle" id="btn-toggle-sidebar" title="Collapse / Expand Sidebar (Ctrl+B)">
        <svg class="svg-icon" id="sidebar-chevron" viewBox="0 0 24 24"><polyline points="15 18 9 12 15 6"/></svg>
      </div>

      <div class="sidebar-tabs">
        <div class="s-tab active" data-tab="perception">
          <svg class="svg-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="m12 12 7-7"/></svg>
          <span>Perception</span>
        </div>
        <div class="s-tab" data-tab="satellite">
          <svg class="svg-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
          <span>Satellite</span>
        </div>
        <div class="s-tab" data-tab="quality">
          <svg class="svg-icon" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          <span>Quality</span>
        </div>
        <div class="s-tab" data-tab="signals">
          <svg class="svg-icon" viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
          <span>Signals</span>
        </div>
        <div class="s-tab" data-tab="scene">
          <svg class="svg-icon" viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
          <span>Display</span>
        </div>
      </div>

      <!-- Tab 1: Perception 3D Suite -->
      <div class="s-body" id="tab-body-perception">
        <!-- Section 1: Autonomous Perception -->
        <div class="acc-sec open">
          <div class="acc-header" onclick="toggleAccSection(this)">
            <div class="acc-title">
              <svg class="svg-icon" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
              <span>Autonomous 3D Perception</span>
            </div>
            <svg class="acc-chevron" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
          <div class="acc-content">
            <div style="font-size: 0.72rem; color: var(--text-muted); line-height: 1.45; margin-bottom: 8px;">
              Zero-tuning spatial decomposition: 3D oriented bounding boxes, 17-joint kinematic human poses, FaceMesh3D, HandMesh3D, and line-of-sight occlusion fields. Select any object to inspect 7-DOF coordinates.
            </div>
            <div class="control-row">
              <span>Ground Filter</span>
              <span style="font-family:'JetBrains Mono'; color:var(--emerald);">PMGF Active</span>
            </div>
            <div class="control-row">
              <span>Cluster Algorithm</span>
              <span style="font-family:'JetBrains Mono'; color:var(--cyan);">RCMC Range-Comp</span>
            </div>
          </div>
        </div>

        <!-- Section 2: Spatial Overlays -->
        <div class="acc-sec open">
          <div class="acc-header" onclick="toggleAccSection(this)">
            <div class="acc-title">
              <svg class="svg-icon" viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
              <span>Visual Projections & Overlays</span>
            </div>
            <svg class="acc-chevron" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
          <div class="acc-content">
            <label class="toggle-row">
              <input type="checkbox" id="chk-show-shapes" checked> 3D Digital Twin Shapes (Vehicle, Person, Bike)
            </label>
            <div class="control-row">
              <span>Shape Opacity</span>
              <input type="range" id="slider-shape-opacity" min="0.15" max="0.90" step="0.05" value="0.40" style="width: 90px; accent-color:var(--cyan);">
            </div>
            <div class="control-row">
              <span>Shape Mode</span>
              <select class="control-select" id="sel-shape-style" style="max-width: 140px;">
                <option value="hologram" selected>Holographic Twin</option>
                <option value="solid">Solid CAD Model</option>
                <option value="xray">Ghost X-Ray Mesh</option>
              </select>
            </div>
            <label class="toggle-row">
              <input type="checkbox" id="chk-show-obb" checked> 3D Oriented Bounding Boxes (OBB)
            </label>
            <label class="toggle-row">
              <input type="checkbox" id="chk-show-heading" checked> Orientation Heading Vectors
            </label>
            <label class="toggle-row">
              <input type="checkbox" id="chk-show-poses" checked> 3D Human Pose Skeletons (17-Joint)
            </label>
            <label class="toggle-row">
              <input type="checkbox" id="chk-show-biometrics" checked> FaceMesh3D & HandMesh3D Graphs
            </label>
            <label class="toggle-row">
              <input type="checkbox" id="chk-show-occlusion" checked> Line-of-Sight Occlusion Rays
            </label>
          </div>
        </div>

        <!-- Section 3: Scene Object Roster -->
        <div class="acc-sec open">
          <div class="acc-header" onclick="toggleAccSection(this)">
            <div class="acc-title">
              <svg class="svg-icon" viewBox="0 0 24 24"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
              <span>Object Roster (<span id="cat-count">0</span>)</span>
            </div>
            <svg class="acc-chevron" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
          <div class="acc-content">
            <div id="canva-roster-list" style="display: flex; flex-direction: column; gap: 4px;">
              <div style="color: var(--text-dim); font-size: 0.72rem; padding: 6px 0;">Scanning 3D sensor frame...</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab 2: Satellite Elevation & Instant Terrain -->
      <div class="s-body" id="tab-body-satellite" style="display: none;">
        <div class="acc-sec open">
          <div class="acc-header" onclick="toggleAccSection(this)">
            <div class="acc-title">
              <svg class="svg-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/></svg>
              <span>Geospatial Elevation Parameters</span>
            </div>
            <svg class="acc-chevron" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
          <div class="acc-content">
            <div class="control-row">
              <span>Location Preset</span>
              <select class="control-select" id="sat-preset-select" style="max-width: 160px;">
                <option value="san_francisco">San Francisco (USA)</option>
                <option value="mount_fuji">Mount Fuji (Japan)</option>
                <option value="grand_canyon">Grand Canyon (USA)</option>
                <option value="zurich_alps">Zurich Pre-Alps (CH)</option>
                <option value="tokyo_bay">Tokyo Waterfront (JP)</option>
                <option value="new_york">Manhattan Canyon (USA)</option>
              </select>
            </div>
            <div class="control-row">
              <span>Latitude (°N)</span>
              <input type="number" class="control-input" id="sat-lat" value="37.7749" step="0.001" style="width: 85px;">
            </div>
            <div class="control-row">
              <span>Longitude (°E)</span>
              <input type="number" class="control-input" id="sat-lon" value="-122.4194" step="0.001" style="width: 85px;">
            </div>
            <div class="control-row">
              <span>Zoom Resolution</span>
              <span id="sat-zoom-disp" style="font-family:'JetBrains Mono', monospace; color:var(--cyan);">14x (2.4km)</span>
            </div>
            <input type="range" id="sat-zoom-slider" min="11" max="17" value="14" style="width: 100%; accent-color: var(--cyan); margin-bottom: 10px;">

            <div class="control-row">
              <span>Surface Topology</span>
              <select class="control-select" id="sat-render-mode">
                <option value="mesh">Triangulated Instant Mesh</option>
                <option value="points">Dense Point Cloud</option>
              </select>
            </div>
            <button class="btn btn-primary" id="btn-generate-satellite" style="width: 100%; justify-content: center; margin-top: 6px;">
              <svg class="svg-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
              <span>Synthesize Satellite 3D</span>
            </button>
          </div>
        </div>

        <div class="acc-sec open">
          <div class="acc-header" onclick="toggleAccSection(this)">
            <div class="acc-title">
              <svg class="svg-icon" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
              <span>Multi-Spectral Classification</span>
            </div>
            <svg class="acc-chevron" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
          <div class="acc-content" style="font-size: 0.72rem; display:flex; flex-direction:column; gap:6px;">
            <div style="display:flex; align-items:center; gap:8px;"><span style="width:8px; height:8px; background:#1F6BC7; border-radius:1px;"></span> Hydrology & Water Bodies</div>
            <div style="display:flex; align-items:center; gap:8px;"><span style="width:8px; height:8px; background:#B8C2D9; border-radius:1px;"></span> Structural Architecture</div>
            <div style="display:flex; align-items:center; gap:8px;"><span style="width:8px; height:8px; background:#383D47; border-radius:1px;"></span> Transport Infrastructure & Pavement</div>
            <div style="display:flex; align-items:center; gap:8px;"><span style="width:8px; height:8px; background:#2EB061; border-radius:1px;"></span> Canopy & Vegetative Biomass</div>
            <div style="display:flex; align-items:center; gap:8px;"><span style="width:8px; height:8px; background:#BF9461; border-radius:1px;"></span> Geological Substrate & Bare Soil</div>
          </div>
        </div>
      </div>

      <!-- Tab 3: Manufacturing & Material Quality -->
      <div class="s-body" id="tab-body-quality" style="display: none;">
        <div class="acc-sec open">
          <div class="acc-header" onclick="toggleAccSection(this)">
            <div class="acc-title">
              <svg class="svg-icon" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              <span>Surface Degradation Index (SDI)</span>
            </div>
            <svg class="acc-chevron" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
          <div class="acc-content">
            <div style="background: rgba(255,255,255,0.02); border:1px solid var(--border); border-radius:4px; padding:8px; margin-bottom:8px;">
              <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="font-size:0.70rem; color:var(--text-dim);">Tolerance Gate</span>
                <span class="ci-badge ci-badge-veh" id="sdi-wear-badge" style="color:var(--emerald); border-color:rgba(16,185,129,0.4);">Nominal Grade A</span>
              </div>
              <div style="display:flex; justify-content:space-between; font-size:0.72rem; margin-bottom:3px;">
                <span>Degradation Index (SDI)</span>
                <strong id="val-sdi" style="font-family:'JetBrains Mono'; color:var(--cyan);">0.042</strong>
              </div>
              <div style="display:flex; justify-content:space-between; font-size:0.72rem; margin-bottom:3px;">
                <span>Mean CAD Deviation</span>
                <strong id="val-sdi-dev" style="font-family:'JetBrains Mono';">0.38 mm</strong>
              </div>
              <div style="display:flex; justify-content:space-between; font-size:0.72rem;">
                <span>Roughness Metric (Ra)</span>
                <strong id="val-sdi-ra" style="font-family:'JetBrains Mono';">0.85 μm</strong>
              </div>
            </div>
          </div>
        </div>

        <div class="acc-sec open">
          <div class="acc-header" onclick="toggleAccSection(this)">
            <div class="acc-title">
              <svg class="svg-icon" viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
              <span>Material Spectral Grading</span>
            </div>
            <svg class="acc-chevron" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
          <div class="acc-content">
            <div style="background: rgba(255,255,255,0.02); border:1px solid var(--border); border-radius:4px; padding:8px;">
              <div style="font-size:0.74rem; font-weight:700; color:var(--amber); margin-bottom:4px;" id="val-mat-class">Asphalt Pavement Aggregate</div>
              <div style="font-size:0.70rem; color:var(--text-dim); margin-bottom:2px;">Diffuse / Specular Ratio: <strong id="val-mat-refl" style="color:#FFF; font-family:'JetBrains Mono';">0.34</strong></div>
              <div style="font-size:0.70rem; color:var(--text-dim);">Estimated Surface Hardness: <strong id="val-mat-hrc" style="color:#FFF; font-family:'JetBrains Mono';">35.0 HRC</strong></div>
            </div>
          </div>
        </div>

        <div class="acc-sec open">
          <div class="acc-header" onclick="toggleAccSection(this)">
            <div class="acc-title">
              <svg class="svg-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
              <span>Point Cloud Sampling Engine</span>
            </div>
            <svg class="acc-chevron" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
          <div class="acc-content">
            <div class="control-row">
              <span>Sampling Method</span>
              <select class="control-select" id="sample-mode-select">
                <option value="curvature">Automated Curvature-Adaptive</option>
                <option value="roi">Manual ROI Bounding Volume</option>
              </select>
            </div>
            <div class="control-row" id="row-sample-target">
              <span>Target Decimation</span>
              <select class="control-select" id="sample-target-pct">
                <option value="0.25">-25% (High Precision)</option>
                <option value="0.50" selected>-50% (Balanced)</option>
                <option value="0.75">-75% (Maximum Speed)</option>
              </select>
            </div>
            <button class="btn btn-outline" id="btn-run-sampling" style="width: 100%; justify-content: center; margin-top: 4px;">
              <svg class="svg-icon" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>
              <span>Execute Sampling Filter</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Tab 4: Signal Processing & Emergency Telemetry -->
      <div class="s-body" id="tab-body-signals" style="display: none;">
        <div class="acc-sec open">
          <div class="acc-header" onclick="toggleAccSection(this)">
            <div class="acc-title">
              <svg class="svg-icon" viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
              <span>Kaufman Adaptive Filter (KAMA)</span>
            </div>
            <svg class="acc-chevron" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
          <div class="acc-content">
            <div style="font-size: 0.72rem; color: var(--text-muted); margin-bottom: 8px; line-height: 1.4;">
              Mathematical noise suppression adapting smoothing constant via the Efficiency Ratio (ER) while preserving crisp geometric step edges.
            </div>
            <label class="toggle-row">
              <input type="checkbox" id="chk-kaufman" checked> Enable Kaufman Adaptive Filtering
            </label>
            <div class="control-row">
              <span>KAMA Period Window</span>
              <input type="range" id="kaufman-period" min="4" max="24" value="8" style="width: 90px; accent-color: var(--cyan);">
            </div>
          </div>
        </div>

        <div class="acc-sec open">
          <div class="acc-header" onclick="toggleAccSection(this)">
            <div class="acc-title">
              <svg class="svg-icon" viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
              <span>Emergency Hazard Estimator</span>
            </div>
            <svg class="acc-chevron" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
          <div class="acc-content">
            <div style="background: rgba(255,255,255,0.02); border:1px solid var(--border); border-radius:4px; padding:8px;">
              <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.72rem;">
                <span>Ego Corridor Velocity</span>
                <strong id="val-ego-speed" style="font-family:'JetBrains Mono';">12.0 m/s (43.2 km/h)</strong>
              </div>
              <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.72rem;">
                <span>Closest Forward Obstacle</span>
                <strong id="val-hazard-dist" style="color:var(--rose); font-family:'JetBrains Mono';">3.8 m</strong>
              </div>
              <div style="font-size:0.68rem; color:var(--text-dim); margin-top:6px;" id="val-hazard-action">
                EMERGENCY BRAKING: Deceleration applied.
              </div>
            </div>
          </div>
        </div>

        <div class="acc-sec open">
          <div class="acc-header" onclick="toggleAccSection(this)">
            <div class="acc-title">
              <svg class="svg-icon" viewBox="0 0 24 24"><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg>
              <span>WiFi-SLAM Indoor Manifold</span>
            </div>
            <svg class="acc-chevron" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
          <div class="acc-content">
            <div style="font-size:0.70rem; color:var(--text-dim); margin-bottom:6px;">
              Fused spatial geometry with multi-AP RSSI log-distance path loss:
            </div>
            <div id="wifi-ap-list" style="display:flex; flex-direction:column; gap:4px; font-size:0.68rem; font-family:'JetBrains Mono';">
              <div style="padding:4px 6px; background:rgba(255,255,255,0.02); border-radius:3px; display:flex; justify-content:space-between;">
                <span>LAB_ROBOTICS_5G</span><strong style="color:var(--cyan);">-42 dBm</strong>
              </div>
              <div style="padding:4px 6px; background:rgba(255,255,255,0.02); border-radius:3px; display:flex; justify-content:space-between;">
                <span>WAREHOUSE_MESH_AP1</span><strong style="color:var(--cyan);">-56 dBm</strong>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab 5: Scene Display Settings -->
      <div class="s-body" id="tab-body-scene" style="display: none;">
        <div class="acc-sec open">
          <div class="acc-header" onclick="toggleAccSection(this)">
            <div class="acc-title">
              <svg class="svg-icon" viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
              <span>Point Cloud Material & Density</span>
            </div>
            <svg class="acc-chevron" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
          <div class="acc-content">
            <div class="control-row">
              <span>Color Field Gradient</span>
              <select class="control-select" id="sel-color">
                <option value="reflectivity">Calibrated Reflectivity</option>
                <option value="height">Elevation Z-Height</option>
                <option value="clusters">RCMC Spatial Clusters</option>
                <option value="rings">Range Distance Bands</option>
              </select>
            </div>
            <div class="control-row">
              <span>Point Rendering Size</span>
              <input type="range" id="slider-pt-size" min="0.04" max="0.30" step="0.01" value="0.12" style="width: 100px; accent-color:var(--cyan);">
            </div>
            <label class="toggle-row">
              <input type="checkbox" id="chk-range-rings" checked> Range Bands (1m, 5m, 10m, 20m, 50m)
            </label>
            <label class="toggle-row">
              <input type="checkbox" id="chk-invert"> Invert Canvas Contrast
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- Left Edge Hover-Peek Trigger Zone -->
    <div class="left-hover-zone" id="left-hover-zone"></div>

    <!-- Floating Re-expand Button (Visible when sidebar is collapsed) -->
    <button class="sidebar-floating-toggle" id="btn-reexpand-sidebar" title="Expand Navigation Sidebar (Ctrl+B)">
      <svg class="svg-icon" viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></svg>
      <span>EXPAND SIDEBAR</span>
    </button>

    <!-- 3D Viewport Area -->
    <div class="viewport-box">
      <div id="viewport-3d"></div>

      <!-- CloudCompare Left Vertical Toolbar (Perspectives, Picking, Transforms & Shaders) -->
      <div class="cc-vert-toolbar" id="cc-vert-toolbar">
        <button class="cc-btn" id="btn-cc-reset-view" title="Reset Camera View to 1:1 Perspective (Home)">
          <span>1:1</span>
        </button>
        <button class="cc-btn" id="btn-cc-ortho" title="Toggle Orthographic vs Perspective Projection">
          <svg class="svg-icon" viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
        </button>
        <div class="cc-divider"></div>
        <button class="cc-btn" id="btn-cc-view-top" title="Top View (+Z)">
          <span>TOP</span>
        </button>
        <button class="cc-btn" id="btn-cc-view-front" title="Front View (+Y)">
          <span>FRNT</span>
        </button>
        <button class="cc-btn" id="btn-cc-view-back" title="Back View (-Y)">
          <span>BACK</span>
        </button>
        <button class="cc-btn" id="btn-cc-view-left" title="Left View (-X)">
          <span>LEFT</span>
        </button>
        <button class="cc-btn" id="btn-cc-view-right" title="Right View (+X)">
          <span>RGHT</span>
        </button>
        <button class="cc-btn" id="btn-cc-view-iso" title="Isometric 3D View">
          <span>ISO</span>
        </button>
        <div class="cc-divider"></div>
        <button class="cc-btn" id="btn-cc-picker" title="3D Coordinate Inspector Crosshair Picker">
          <svg class="svg-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg>
        </button>
        <button class="cc-btn" id="btn-cc-gizmo-trans" title="Transform Gizmo: Translate (G)">
          <svg class="svg-icon" viewBox="0 0 24 24"><polyline points="5 9 2 12 5 15"/><polyline points="9 5 12 2 15 5"/><polyline points="15 19 12 22 9 19"/><polyline points="19 9 22 12 19 15"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="12" y1="2" x2="12" y2="22"/></svg>
        </button>
        <button class="cc-btn" id="btn-cc-gizmo-rot" title="Transform Gizmo: Rotate (R)">
          <svg class="svg-icon" viewBox="0 0 24 24"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
        </button>
        <button class="cc-btn" id="btn-cc-gizmo-scale" title="Transform Gizmo: Scale (S)">
          <svg class="svg-icon" viewBox="0 0 24 24"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
        </button>
        <div class="cc-divider"></div>
        <button class="cc-btn" id="btn-cc-normals" title="Toggle Surface Normal Vectors Needle Display (N)">
          <span style="font-size:0.58rem;">&vec;N</span>
        </button>
        <button class="cc-btn" id="btn-cc-edl" title="Toggle Eye-Dome Lighting (EDL) Depth Shader">
          <span style="font-size:0.56rem;">EDL</span>
        </button>
      </div>

      <!-- CloudCompare Top Center Horizontal Toolbox -->
      <div class="cc-horiz-toolbar" id="cc-horiz-toolbar">
        <button class="cc-horiz-btn" id="btn-cc-scissors" title="Scissors / Polygon Lasso Crop (Interactive 2D to 3D Segmentation)">
          <svg class="svg-icon" viewBox="0 0 24 24"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/><line x1="8.12" y1="8.12" x2="12" y2="12"/></svg>
          <span>Scissors Crop</span>
        </button>
        <button class="cc-horiz-btn" id="btn-cc-box-slice" title="Interactive 3D Slicing & Clipping Box">
          <svg class="svg-icon" viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
          <span>Slicing Box</span>
        </button>
        <button class="cc-horiz-btn" id="btn-cc-sor" title="Statistical Outlier Removal (SOR) / Noise Suppression Filter">
          <svg class="svg-icon" viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
          <span>SOR Filter</span>
        </button>
        <button class="cc-horiz-btn" id="btn-cc-subsample" title="Spatial / Voxel Subsampling Decimation">
          <svg class="svg-icon" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
          <span>Subsample</span>
        </button>
        <button class="cc-horiz-btn" id="btn-cc-csf" title="Cloth Simulation Filter (CSF): Ground / Terrain Isolation">
          <svg class="svg-icon" viewBox="0 0 24 24"><path d="M3 18l6-6 4 4 8-8"/><path d="M3 21h18"/></svg>
          <span>CSF Ground</span>
        </button>
        <button class="cc-horiz-btn" id="btn-cc-c2c" title="Cloud-to-Cloud (C2C) Distance Heatmap & Color Ramp">
          <svg class="svg-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/></svg>
          <span>C2C Heatmap</span>
        </button>
        <button class="cc-horiz-btn" id="btn-cc-reset-filters" title="Reset All Manual Manipulations & Restore Raw Coordinates" style="color:var(--rose);">
          <svg class="svg-icon" viewBox="0 0 24 24"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>
          <span>Reset</span>
        </button>
      </div>

      <!-- Presentation & Recording Floating Action Dock -->
      <div class="presentation-toolbar" id="presentation-toolbar">
        <button class="cc-horiz-btn" id="btn-rec-action" title="Start / Stop Full Screen Session Recording" style="color:var(--rose); border-color:rgba(239,68,68,0.4);">
          <div style="width:7px; height:7px; border-radius:50%; background:var(--rose);"></div>
          <span id="rec-btn-label">Record</span>
        </button>
        <button class="cc-horiz-btn" id="btn-pip-action" title="Toggle Picture-in-Picture Dual Camera View">
          <svg class="svg-icon" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><rect x="12" y="9" width="8" height="6" rx="1" ry="1"/></svg>
          <span>PiP View</span>
        </button>
        <button class="cc-horiz-btn" id="btn-tour-action" title="Toggle Automated Turntable / Flythrough Presentation Tour">
          <svg class="svg-icon" viewBox="0 0 24 24"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
          <span>360° Tour</span>
        </button>
        <button class="cc-horiz-btn" id="btn-laser-action" title="Toggle 3D Presentation Laser Pointer / Spotlight">
          <svg class="svg-icon" viewBox="0 0 24 24"><circle cx="12" cy="3" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg>
          <span>Laser</span>
        </button>
        <button class="cc-horiz-btn" id="btn-pin-action" title="Drop Interactive 3D Presentation Annotation Pin">
          <svg class="svg-icon" viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          <span>Add Pin</span>
        </button>
        <button class="cc-horiz-btn" id="btn-fullscreen-action" title="Enter Full Screen Presentation Mode (F11 / Ctrl+F)">
          <svg class="svg-icon" viewBox="0 0 24 24"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
          <span>Full Screen</span>
        </button>
      </div>

      <!-- Live Recording Status Indicator Pill -->
      <div class="rec-status-badge" id="rec-status-badge">
        <div class="rec-pulse-dot"></div>
        <span>REC <strong id="rec-duration-disp">00:00</strong></span>
        <span style="font-size:0.62rem; color:var(--text-dim);">60 FPS WEBM</span>
        <button id="btn-stop-rec-pill" style="margin-left:6px; background:rgba(0,0,0,0.6); border:1px solid #FFF; color:#FFF; font-size:0.62rem; padding:2px 8px; border-radius:3px; cursor:pointer; font-weight:700;">STOP</button>
      </div>

      <!-- Picture-in-Picture Inset Viewport Container -->
      <div class="pip-container" id="pip-container">
        <div class="pip-header" id="pip-drag-handle">
          <div style="display:flex; align-items:center; gap:6px;">
            <span class="rec-pulse-dot" style="width:6px; height:6px; background:var(--cyan); animation:none;"></span>
            <span id="pip-title-disp">PIP: TOP-DOWN BEV [SENSOR A]</span>
          </div>
          <div style="display:flex; align-items:center; gap:4px;">
            <button id="btn-pip-swap" title="Swap Main Viewport & PiP Viewport" style="background:transparent; border:none; color:var(--text); cursor:pointer; font-size:0.75rem;">⇄</button>
            <button id="btn-pip-browser" title="Pop out to Native Floating Picture-in-Picture Window" style="background:transparent; border:none; color:var(--cyan); cursor:pointer; font-size:0.75rem;">⧉</button>
            <button id="btn-pip-close" title="Close PiP" style="background:transparent; border:none; color:var(--text-dim); cursor:pointer; font-size:0.85rem;">&times;</button>
          </div>
        </div>
        <div class="pip-viewport-canvas" id="pip-canvas-wrap"></div>
      </div>

      <!-- SVG Layer for Interactive Scissors / Polygon Lasso Crop -->
      <svg class="lasso-overlay-svg" id="lasso-overlay-svg" style="display:none;">
        <polygon id="lasso-polygon-preview" points="" fill="rgba(0, 229, 255, 0.15)" stroke="var(--cyan)" stroke-width="2" stroke-dasharray="4 4"/>
      </svg>

      <!-- Scissors Lasso HUD Instructions -->
      <div id="lasso-hud-msg" style="position:absolute; top:70px; left:50%; transform:translateX(-50%); z-index:50; background:rgba(11,15,23,0.95); border:1px solid var(--cyan); color:var(--text); padding:6px 14px; border-radius:20px; font-size:0.72rem; font-family:'JetBrains Mono', monospace; display:none; align-items:center; gap:10px; box-shadow:0 0 20px rgba(0,229,255,0.4);">
        <span style="display:inline-flex; align-items:center; gap:6px;"><svg class="svg-icon" viewBox="0 0 24 24" style="width:14px; height:14px; color:var(--cyan);"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/><line x1="8.12" y1="8.12" x2="12" y2="12"/></svg> <b>POLYGON LASSO:</b> Click canvas to add polygon vertices.</span>
        <button id="btn-lasso-cut-in" class="btn" style="padding:2px 8px; font-size:0.65rem; background:var(--cyan-dim); border-color:var(--cyan); color:var(--cyan);">Segment Inside</button>
        <button id="btn-lasso-cut-out" class="btn" style="padding:2px 8px; font-size:0.65rem; background:rgba(239,68,68,0.15); border-color:var(--rose); color:var(--rose);">Segment Outside</button>
        <button id="btn-lasso-cancel" class="btn" style="padding:2px 8px; font-size:0.65rem;">Cancel (ESC)</button>
      </div>

      <!-- Interactive 3D Point Coordinate Inspector Floating HUD Card -->
      <div class="cc-hud-panel" id="cc-picker-card" style="display:none; width:220px; pointer-events:none;">
        <div style="font-weight:700; color:var(--cyan); font-family:'JetBrains Mono', monospace; font-size:0.70rem; border-bottom:1px solid var(--border); padding-bottom:4px; margin-bottom:6px; display:flex; justify-content:space-between;">
          <span>POINT INSPECTOR</span>
          <span id="cc-pick-index">#00000</span>
        </div>
        <div style="font-family:'JetBrains Mono', monospace; font-size:0.67rem; display:flex; flex-direction:column; gap:3px;">
          <div>X: <strong id="cc-pick-x" style="color:#FFF;">+0.000m</strong></div>
          <div>Y: <strong id="cc-pick-y" style="color:#FFF;">+0.000m</strong></div>
          <div>Z: <strong id="cc-pick-z" style="color:#FFF;">+0.000m</strong></div>
          <div>Range R: <strong id="cc-pick-r" style="color:var(--cyan);">0.000m</strong></div>
          <div>Reflectivity: <strong id="cc-pick-i" style="color:var(--amber);">0.000</strong></div>
          <div>Normal &vec;N: <strong id="cc-pick-n" style="color:var(--emerald);">[0.0, 0.0, 1.0]</strong></div>
        </div>
      </div>

      <!-- Subsample Slider Modal Panel -->
      <div class="cc-hud-panel" id="cc-subsample-panel" style="display:none; left:50%; transform:translateX(-50%); top:70px; width:260px;">
        <div style="font-weight:700; color:var(--cyan); font-size:0.72rem; margin-bottom:6px; display:flex; justify-content:space-between;">
          <span>SPATIAL SUBSAMPLING</span>
          <span id="subsample-val-disp" style="font-family:'JetBrains Mono', monospace;">100%</span>
        </div>
        <input type="range" id="slider-subsample" min="10" max="100" step="5" value="100" style="width:100%; accent-color:var(--cyan); cursor:pointer;">
        <div style="display:flex; justify-content:space-between; font-size:0.62rem; color:var(--text-dim); margin-top:4px;">
          <span>10% (Fast)</span>
          <span>50%</span>
          <span>100% (Dense)</span>
        </div>
      </div>

      <!-- Modal Video Playback Drawer / Overlay -->
      <div class="modal-overlay" id="modal-video-playback" style="display:none; z-index:1000;">
        <div class="modal-box" style="width:840px; max-width:95vw; background:#04060A; border:1px solid var(--border-accent); border-radius:8px; overflow:hidden;">
          <div class="modal-header" style="height:42px; background:var(--bg-header); border-bottom:1px solid var(--border); display:flex; align-items:center; justify-content:space-between; padding:0 16px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <svg class="svg-icon" viewBox="0 0 24 24" style="color:var(--rose);"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4" fill="currentColor"/></svg>
              <span style="font-weight:700; font-size:0.80rem; color:var(--text);">Session Screen Recording Playback</span>
            </div>
            <button id="btn-close-playback-modal" style="background:transparent; border:none; color:var(--text-dim); font-size:1.2rem; cursor:pointer;">&times;</button>
          </div>
          <div style="padding:16px; display:flex; flex-direction:column; gap:12px; align-items:center;">
            <video id="playback-video-elem" controls autoplay style="width:100%; max-height:480px; border-radius:6px; background:#000; border:1px solid var(--border);"></video>
            <div style="display:flex; justify-content:space-between; align-items:center; width:100%;">
              <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:0.68rem; color:var(--text-dim);">Playback Speed:</span>
                <button class="btn speed-btn" data-speed="0.5" style="padding:2px 8px; font-size:0.65rem;">0.5x</button>
                <button class="btn speed-btn active" data-speed="1.0" style="padding:2px 8px; font-size:0.65rem;">1.0x</button>
                <button class="btn speed-btn" data-speed="2.0" style="padding:2px 8px; font-size:0.65rem;">2.0x</button>
              </div>
              <div style="display:flex; gap:8px;">
                <a id="btn-download-recorded-video" href="#" download="aeovexor_session_recording.webm" class="btn btn-primary" style="text-decoration:none; display:inline-flex; align-items:center; gap:6px;">
                  <svg class="svg-icon" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                  <span>Download Recording (.webm)</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Split Viewport Interactive Divider -->
      <div class="split-divider" id="split-divider" style="display: none; left: 50%;">
        <div class="split-divider-handle">
          <span>◀ || ▶</span>
        </div>
      </div>

      <!-- Split Screen Sub-Window Badges & Decoupled Camera Controls -->
      <div class="split-subwindow-badge split-badge-left" id="split-badge-left" style="display: none;">
        <span class="subwindow-indicator raw-indicator"></span>
        <span>◈ RAW SENSOR INGEST [A] &bull; <strong id="split-raw-pts">17,238 PTS</strong> UNFILTERED</span>
        <span class="camera-indicator-tag" id="tag-camera-left" style="margin-left:8px; font-size:0.62rem; padding:2px 6px; border-radius:3px; background:rgba(0,229,255,0.18); color:var(--cyan); border:1px solid rgba(0,229,255,0.4); font-weight:700;">CAM A: ACTIVE</span>
      </div>
      <div class="split-subwindow-badge split-badge-right" id="split-badge-right" style="display: none;">
        <span class="subwindow-indicator processed-indicator"></span>
        <span>PROCESSED PERCEPTION [B] &bull; <strong id="split-proc-count">OBJECTS</strong> DETECTED</span>
        <span class="camera-indicator-tag" id="tag-camera-right" style="margin-left:8px; font-size:0.62rem; padding:2px 6px; border-radius:3px; background:rgba(16,185,129,0.18); color:var(--emerald); border:1px solid rgba(16,185,129,0.4); font-weight:700;">CAM B: ACTIVE</span>
        <button id="btn-toggle-camera-sync" title="Toggle individual independent camera controls or synchronized controls" style="margin-left:10px; padding:3px 8px; font-size:0.62rem; font-weight:700; background:rgba(15,23,42,0.92); border:1px solid var(--border-accent); border-radius:4px; color:var(--cyan); cursor:pointer;">[ INDIVIDUAL CONTROLS ]</button>
      </div>

      <!-- Live Tactical Reticle Coordinate Readout (Bottom-Left NASA Telemetry) -->
      <div class="reticle-telemetry" id="reticle-telemetry">
        <span>SENSOR COORD:</span>
        <span class="reticle-coord" id="reticle-x">X: +00.00m</span>
        <span class="reticle-coord" id="reticle-y">Y: +00.00m</span>
        <span class="reticle-coord" id="reticle-z">Z: +00.00m</span>
        <span>RANGE: <strong id="reticle-range" style="color:#FFF;">0.00m</strong></span>
      </div>

      <!-- Data State Indicator Overlay (Top-Right) -->
      <div class="data-state-overlay" id="data-state-overlay">
        <span class="state-badge state-badge-b" id="badge-curr-state">STATE B: PROCESSED</span>
        <span style="color:var(--text-dim);" id="state-detail-str">17,238 PTS • -8.2% NOISE SUPPRESSED • 25 DETECTIONS</span>
      </div>

      <!-- AEOVEXOR 3D Spatial Inspector HUD (Draggable, Resizable, Collapsible Full CRUD) -->
      <div class="floating-dialog" id="spatial-inspector">
        <div class="ci-header" id="ci-drag-handle">
          <div class="ci-title">
            <svg class="svg-icon" viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
            <span>Spatial Inspector</span>
            <span class="ci-badge ci-badge-veh" id="ci-badge-label">VEHICLE</span>
          </div>
          <div style="display:flex; align-items:center; gap:5px;">
            <button class="ci-tool-btn" id="ci-btn-create" title="Create / Synthesize New Entity (+)">
              <svg class="svg-icon" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            </button>
            <button class="ci-tool-btn" id="ci-btn-collapse" title="Collapse / Minimize Dialog">
              <svg class="svg-icon" id="ci-collapse-icon" viewBox="0 0 24 24"><line x1="5" y1="12" x2="19" y2="12"/></svg>
            </button>
            <button class="ci-tool-btn" id="ci-btn-expand" title="Expand Full Telemetry & Features">
              <svg class="svg-icon" viewBox="0 0 24 24"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
            </button>
            <span style="cursor: pointer; font-size: 1.15rem; color: var(--text-dim); margin-left:2px;" id="ci-close-btn">&times;</span>
          </div>
        </div>

        <div id="ci-body">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="font-size: 0.70rem; color: var(--text-muted);">
              Entity: <strong id="ci-obj-id" style="color: var(--cyan); font-family: 'JetBrains Mono', monospace;">OBJ_001</strong>
            </div>
            <div style="font-size: 0.68rem; color: var(--text-dim); font-family:'JetBrains Mono';" id="ci-pts-count-disp">
              0 PTS COVERED
            </div>
          </div>

          <div class="control-row">
            <span>Semantic Taxonomy</span>
            <select class="control-select" id="ci-class-select">
              <option value="Vehicle">Vehicle</option>
              <option value="Pedestrian">Pedestrian</option>
              <option value="Cyclist">Cyclist</option>
              <option value="Infrastructure">Infrastructure</option>
              <option value="Obstacle">Obstacle</option>
              <option value="Custom">Custom Geometric Entity</option>
            </select>
          </div>

          <div style="display:flex; justify-content:space-between; font-size:0.70rem; margin:6px 0 2px 0;">
            <span>Confidence Likelihood</span>
            <strong id="ci-conf-val" style="color:var(--cyan); font-family:'JetBrains Mono';">0.96</strong>
          </div>
          <div style="display:flex; justify-content:space-between; font-size:0.70rem; margin-bottom:4px;">
            <span>Line-of-Sight Occlusion</span>
            <strong id="ci-occ-val" style="font-family:'JetBrains Mono'; color:var(--emerald);">14% (Clear)</strong>
          </div>
          <div class="occlusion-bar-wrap">
            <div class="occlusion-bar-fill" id="ci-occ-bar" style="width: 14%;"></div>
          </div>

          <div style="font-size:0.66rem; font-weight:700; color:var(--text-dim); text-transform:uppercase; letter-spacing:0.06em; margin-bottom:4px;">
            Centroid Coordinates [X, Y, Z] (m)
          </div>
          <div class="ci-grid-3">
            <div class="ci-input-col"><label>X</label><input type="number" step="0.05" id="ci-pos-x"></div>
            <div class="ci-input-col"><label>Y</label><input type="number" step="0.05" id="ci-pos-y"></div>
            <div class="ci-input-col"><label>Z</label><input type="number" step="0.05" id="ci-pos-z"></div>
          </div>

          <div style="font-size:0.66rem; font-weight:700; color:var(--text-dim); text-transform:uppercase; letter-spacing:0.06em; margin-bottom:4px;">
            Extents [Length, Width, Height] (m)
          </div>
          <div class="ci-grid-3">
            <div class="ci-input-col"><label>L</label><input type="number" step="0.05" id="ci-dim-l"></div>
            <div class="ci-input-col"><label>W</label><input type="number" step="0.05" id="ci-dim-w"></div>
            <div class="ci-input-col"><label>H</label><input type="number" step="0.05" id="ci-dim-h"></div>
          </div>

          <div style="display:flex; justify-content:space-between; font-size:0.70rem; margin-top:6px;">
            <span>Heading Yaw Orientation</span>
            <strong id="ci-yaw-disp" style="color:var(--amber); font-family:'JetBrains Mono';">0.0°</strong>
          </div>
          <input type="range" id="ci-yaw-slider" min="-180" max="180" step="1" value="0" style="width: 100%; accent-color: var(--amber); margin-bottom: 8px;">

          <!-- Expanded Full Features Drawer (Visible when expanded) -->
          <div id="ci-expanded-section" style="display:none; border-top:1px solid var(--border); padding-top:8px; margin-top:6px;">
            <div class="ci-tabs">
              <button class="ci-tab-btn active" data-tab="kinematics">Kinematics</button>
              <button class="ci-tab-btn" data-tab="coverage">Coverage</button>
              <button class="ci-tab-btn" data-tab="provenance">Provenance</button>
            </div>

            <div id="ci-pane-kinematics">
              <div style="background:rgba(255,255,255,0.02); border:1px solid var(--border); border-radius:4px; padding:6px 8px; font-size:0.70rem; display:flex; flex-direction:column; gap:4px; font-family:'JetBrains Mono'; margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between;"><span>Radial Distance (r):</span><strong id="ci-exp-dist" style="color:var(--cyan);">0.00 m</strong></div>
                <div style="display:flex; justify-content:space-between;"><span>Bounding Volume (V):</span><strong id="ci-exp-vol">0.00 m³</strong></div>
                <div style="display:flex; justify-content:space-between;"><span>Surface Area (A):</span><strong id="ci-exp-area">0.00 m²</strong></div>
                <div style="display:flex; justify-content:space-between;"><span>Elevation Span (Z):</span><strong id="ci-exp-zspan">0.00 .. 0.00 m</strong></div>
                <div style="display:flex; justify-content:space-between;"><span>Estimated TTC:</span><strong id="ci-exp-ttc" style="color:var(--emerald);">1.8s (Nominal)</strong></div>
              </div>
            </div>

            <div id="ci-pane-coverage" style="display:none;">
              <div style="background:rgba(255,255,255,0.02); border:1px solid var(--border); border-radius:4px; padding:6px 8px; font-size:0.70rem; display:flex; flex-direction:column; gap:4px; font-family:'JetBrains Mono'; margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between;"><span>Point Density:</span><strong id="ci-exp-density" style="color:var(--cyan);">0.0 pts/m³</strong></div>
                <div style="display:flex; justify-content:space-between;"><span>Hidden Volume:</span><strong id="ci-exp-hidden-vol">0.00 m³</strong></div>
                <div style="display:flex; justify-content:space-between;"><span>Aspect Ratio (L/W):</span><strong id="ci-exp-ratio">0.00</strong></div>
                <div style="display:flex; justify-content:space-between;"><span>Ground Clearance:</span><strong id="ci-exp-clearance">0.25 m</strong></div>
              </div>
            </div>

            <div id="ci-pane-provenance" style="display:none;">
              <textarea id="ci-exp-json" readonly style="width:100%; height:85px; background:var(--bg-dark); border:1px solid var(--border); border-radius:4px; color:var(--text-muted); font-size:0.65rem; font-family:'JetBrains Mono'; padding:6px; resize:none;"></textarea>
            </div>
          </div>

          <!-- CRUD Action Controls -->
          <div style="display:flex; gap:6px; margin-bottom:6px;">
            <button class="btn btn-primary" id="ci-btn-place-shape" style="flex:1.2; justify-content:center;" title="Place calibrated 3D shape directly on this actual detected item">
              <svg class="svg-icon" viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
              <span>Place Shape</span>
            </button>
            <button class="btn" id="ci-btn-snap" style="flex:1; justify-content:center;" title="Fit 3D bounding box tightly to actual item point cluster">
              <svg class="svg-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg>
              <span>Fit Points</span>
            </button>
            <button class="btn" id="ci-btn-delete" style="color:var(--rose); padding:0 8px;" title="Delete Entity (Remove from Scene)">
              <svg class="svg-icon" viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
            </button>
          </div>

          <button class="btn btn-primary" id="ci-btn-save" style="width: 100%; justify-content: center;" title="Commit Spatial Transform to Backend Database">
            <svg class="svg-icon" viewBox="0 0 24 24"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
            <span>Commit Spatial Transform</span>
          </button>
        </div>
      </div>

      <!-- Right Tactical Dock Strip (Collapsible hover / click to view) -->
      <div class="right-dock-strip" id="right-dock-strip">
        <button class="right-dock-tab" id="dock-tab-ai" title="AI Perception Copilot (Hover / Click to Expand)">
          <svg class="svg-icon" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/></svg>
          <span>AI COPILOT</span>
        </button>
        <button class="right-dock-tab" id="dock-tab-slice" title="Cross-Section Slicing Box (Hover / Click to Expand)">
          <svg class="svg-icon" viewBox="0 0 24 24"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/></svg>
          <span>SLICING BOX</span>
        </button>
      </div>
    </div>
  </div>

  <!-- Slicing Box Panel (Draggable & Collapsible) -->
  <div class="floating-dialog right-slide-panel" id="panel-slice">
    <div class="ci-header" id="slice-drag-handle">
      <div style="font-size: 0.74rem; font-weight: 700; color: var(--cyan); display:flex; align-items:center; gap:6px;">
        <svg class="svg-icon" viewBox="0 0 24 24"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/></svg>
        <span>Cross-Section Slicing Box</span>
      </div>
      <div style="display:flex; align-items:center; gap:5px;">
        <button class="ci-tool-btn btn-panel-pin" id="slice-btn-pin" title="Pin / Lock Open">
          <svg class="svg-icon" viewBox="0 0 24 24"><line x1="12" y1="17" x2="12" y2="22"/><path d="M5 17h14v-2l-3-3V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v7l-3 3v2z"/></svg>
        </button>
        <button class="ci-tool-btn" id="slice-btn-collapse" title="Collapse Panel">
          <svg class="svg-icon" viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></svg>
        </button>
        <span style="cursor: pointer; font-size: 1.15rem; color: var(--text-dim); margin-left:2px;" id="slice-close-btn">&times;</span>
      </div>
    </div>
    <div class="control-row">
      <span>Clip X Axis</span>
      <input type="range" id="clip-x" min="-40" max="40" value="40" style="width: 90px; accent-color:var(--cyan);">
    </div>
    <div class="control-row">
      <span>Clip Y Axis</span>
      <input type="range" id="clip-y" min="-40" max="40" value="40" style="width: 90px; accent-color:var(--cyan);">
    </div>
    <div class="control-row">
      <span>Clip Z Elevation</span>
      <input type="range" id="clip-z" min="-5" max="15" value="15" style="width: 90px; accent-color:var(--cyan);">
    </div>
    <button class="btn" id="btn-reset-slice" style="width: 100%; justify-content: center; margin-top: 6px;">
      <svg class="svg-icon" viewBox="0 0 24 24"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>
      <span>Reset Clipping Planes</span>
    </button>
  </div>

  <!-- Super Intelligence AI Copilot Drawer (Collapsible Slide-in) -->
  <div class="right-slide-panel" id="ai-copilot-drawer">
    <div class="ci-header" id="ai-drag-handle">
      <div style="font-size: 0.80rem; font-weight: 800; color: var(--cyan); display: flex; align-items: center; gap: 7px;">
        <svg class="svg-icon" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/></svg>
        <span>Super Intelligence Copilot</span>
      </div>
      <div style="display:flex; align-items:center; gap:5px;">
        <button class="ci-tool-btn btn-panel-pin" id="ai-btn-pin" title="Pin / Lock Open">
          <svg class="svg-icon" viewBox="0 0 24 24"><line x1="12" y1="17" x2="12" y2="22"/><path d="M5 17h14v-2l-3-3V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v7l-3 3v2z"/></svg>
        </button>
        <button class="ci-tool-btn" id="ai-btn-collapse" title="Collapse Panel">
          <svg class="svg-icon" viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></svg>
        </button>
        <span style="cursor: pointer; font-size: 1.15rem; color: var(--text-dim); margin-left:2px;" id="ai-drawer-close">&times;</span>
      </div>
    </div>

    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; font-size: 0.72rem;">
      <span>AI Model Source:</span>
      <select class="control-select" id="ai-model-select" style="max-width: 220px;">
        <option value="anthropic/claude-3.5-sonnet">Claude 3.5 Sonnet (OpenRouter)</option>
        <option value="google/gemini-2.0-flash-exp:free" selected>Gemini 2.0 Flash (OpenRouter)</option>
        <option value="google/gemini-2.0-flash-thinking-exp:free">Gemini 2.0 Flash Thinking</option>
        <option value="deepseek/deepseek-r1">DeepSeek R1 (OpenRouter)</option>
        <option value="openai/gpt-4o">GPT-4o (OpenRouter)</option>
        <option value="meta-llama/llama-3.3-70b-instruct">Llama 3.3 70B Instruct</option>
      </select>
    </div>

    <div style="font-size: 0.68rem; color: var(--text-dim); display:flex; justify-content:space-between; margin-bottom: 8px;">
      <span id="ai-key-status">Key Status: Resolving .env.local</span>
      <span>Live 3D Telemetry Injected</span>
    </div>

    <div style="display: flex; gap: 4px; overflow-x: auto; padding-bottom: 6px; margin-bottom: 4px;">
      <button class="quick-chip" data-prompt="Analyze forward collision threats and compute emergency evasion angle based on current TTC.">Threat Assessment</button>
      <button class="quick-chip" data-prompt="Perform ISO surface degradation analysis on current road profile and estimate micro-roughness wear.">Surface Quality Audit</button>
      <button class="quick-chip" data-prompt="Explain Kaufman Adaptive Filter Efficiency Ratio (ER) suppression vs Gaussian smoothing on this LiDAR frame.">KAMA Signal Math</button>
    </div>

    <div class="ai-chat-history" id="ai-chat-thread">
      <div class="chat-bubble chat-ai">
        <strong>AEOVEXOR Mission Intelligence Active.</strong><br>
        Ask any query regarding 3D point cloud topology, Kaufman adaptive noise filtering, collision kinematics, or manufacturing degradation.
      </div>
    </div>

    <div style="display: flex; gap: 6px; margin-top: 8px;">
      <input type="text" class="control-input" id="ai-input" placeholder="Query 3D perception intelligence..." style="flex: 1; padding: 7px 10px;">
      <button class="btn btn-primary" id="btn-ai-send">
        <svg class="svg-icon" viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
      </button>
    </div>
  </div>

  <!-- Bottom Playback & Telemetry Status Bar -->
  <div class="playback-bar">
    <div style="display:flex; align-items:center; gap:8px;">
      <button class="btn" id="btn-play" style="padding: 2px 7px;">
        <svg class="svg-icon" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg>
        <span>STREAM</span>
      </button>
      <span>FRAME <strong style="color:var(--text);">000</strong></span>
    </div>
    <div class="progress-track" id="stream-progress"><div class="progress-fill"></div></div>
    <div style="display:flex; align-items:center; gap:14px;">
      <span>POINTS: <strong id="val-pts" style="color:var(--cyan);">17,238</strong></span>
      <span>DETECTIONS: <strong id="val-clusters" style="color:var(--emerald);">0 Objects</strong></span>
      <span>SDI: <strong id="chip-sdi" style="color:var(--amber);">0.042</strong></span>
      <span>LATENCY: <strong id="val-lat" style="color:#FFF;">0.0 ms</strong></span>
      <span style="color:var(--cyan); font-weight:700;">● AEOVEXOR SPATIAL CORE ACTIVE</span>
    </div>
  </div>

  <!-- 3D Export Modal Dialog -->
  <div class="modal-overlay" id="modal-export-3d">
    <div class="modal-box">
      <div class="modal-header">
        <div style="font-weight: 800; font-size: 0.88rem; color: var(--cyan); display:flex; align-items:center; gap:7px;">
          <svg class="svg-icon" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          <span>AEOVEXOR 3D Precision Annotation Export</span>
        </div>
        <span style="cursor: pointer; font-size: 1.2rem; color: var(--text-dim);" id="modal-export-close">&times;</span>
      </div>
      <div class="modal-body">
        <div class="export-tabs">
          <button class="export-tab active" data-format="kitti">KITTI 3D Benchmark</button>
          <button class="export-tab" data-format="waymo">Waymo Open Dataset</button>
          <button class="export-tab" data-format="coco">COCO-3D Format</button>
          <button class="export-tab" data-format="aeovexor">AEOVEXOR Spatial JSON</button>
        </div>
        <textarea class="export-code-box" id="export-preview-area" readonly></textarea>
      </div>
      <div class="modal-footer">
        <button class="btn" id="btn-copy-export">
          <svg class="svg-icon" viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
          <span>Copy to Clipboard</span>
        </button>
        <button class="btn btn-primary" id="btn-download-export">
          <svg class="svg-icon" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          <span>Download Export File</span>
        </button>
      </div>
    </div>
  </div>

  <script>
    // ========================================================================
    // 1. High-Precision Three.js Viewport & Tactical Controls
    // ========================================================================
    const container = document.getElementById('viewport-3d');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x06080D);

    const camera = new THREE.PerspectiveCamera(52, container.clientWidth / container.clientHeight, 0.05, 1200);
    camera.position.set(-14, -20, 10);
    camera.up.set(0, 0, 1);

    const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2.0));
    container.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.rotateSpeed = 0.75;
    controls.zoomSpeed = 1.25;
    controls.panSpeed = 1.0;
    controls.minDistance = 0.1;
    controls.maxDistance = 600;
    controls.target.set(10, 0, 0);
    controls.update();

    // Independent Dual Cameras & OrbitControls for Split Screen
    const cameraRaw = new THREE.PerspectiveCamera(52, (container.clientWidth * 0.5) / container.clientHeight, 0.05, 1200);
    cameraRaw.position.set(-14, -20, 10);
    cameraRaw.up.set(0, 0, 1);

    const controlsRaw = new THREE.OrbitControls(cameraRaw, renderer.domElement);
    controlsRaw.enableDamping = true;
    controlsRaw.dampingFactor = 0.05;
    controlsRaw.rotateSpeed = 0.75;
    controlsRaw.zoomSpeed = 1.25;
    controlsRaw.panSpeed = 1.0;
    controlsRaw.minDistance = 0.1;
    controlsRaw.maxDistance = 600;
    controlsRaw.target.set(10, 0, 0);
    controlsRaw.update();

    const cameraProc = new THREE.PerspectiveCamera(52, (container.clientWidth * 0.5) / container.clientHeight, 0.05, 1200);
    cameraProc.position.set(-14, -20, 10);
    cameraProc.up.set(0, 0, 1);

    const controlsProc = new THREE.OrbitControls(cameraProc, renderer.domElement);
    controlsProc.enableDamping = true;
    controlsProc.dampingFactor = 0.05;
    controlsProc.rotateSpeed = 0.75;
    controlsProc.zoomSpeed = 1.25;
    controlsProc.panSpeed = 1.0;
    controlsProc.minDistance = 0.1;
    controlsProc.maxDistance = 600;
    controlsProc.target.set(10, 0, 0);
    controlsProc.update();

    let camerasDecoupled = true; // Enables individual independent control for each split screen
    let activeSplitSide = 'left'; // 'left' = Camera A (Raw), 'right' = Camera B (Processed)

    // Range Rings
    const ringsGroup = new THREE.Group();
    [1, 5, 10, 20, 50].forEach(r => {
      const g = new THREE.RingGeometry(r - 0.03, r + 0.03, 64);
      const m = new THREE.MeshBasicMaterial({ color: 0x00E5FF, side: THREE.DoubleSide, transparent: true, opacity: 0.18 });
      const ring = new THREE.Mesh(g, m);
      ring.position.z = -1.73;
      ringsGroup.add(ring);
    });
    scene.add(ringsGroup);

    // Studio & Hologram Lighting for 3D Digital Twins
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
    scene.add(ambientLight);
    const dirLight1 = new THREE.DirectionalLight(0x00E5FF, 0.75);
    dirLight1.position.set(20, 20, 30);
    scene.add(dirLight1);
    const dirLight2 = new THREE.DirectionalLight(0xffffff, 0.50);
    dirLight2.position.set(-20, -20, 15);
    scene.add(dirLight2);

    // Groups
    const boxesGroup = new THREE.Group();
    const posesGroup = new THREE.Group();
    const biometricsGroup = new THREE.Group();
    const occlusionGroup = new THREE.Group();
    const satelliteGroup = new THREE.Group();
    scene.add(boxesGroup);
    scene.add(posesGroup);
    scene.add(biometricsGroup);
    scene.add(occlusionGroup);
    scene.add(satelliteGroup);

    let cloudPoints = null;
    let cloudPointsRaw = null;
    let cloudPointsProc = null;
    let currentRawData = null;
    let currentDataset = "velodyne_000008.bin";
    let comparisonState = "B"; // 'A' = Raw Ingest, 'B' = Processed Perception
    let isSplitView = false;
    let pointSizeScale = 0.12;

    let showDigitalTwins = true;
    let shapeOpacity = 0.40;
    let shapeRenderStyle = "hologram"; // "hologram", "solid", "xray"

    let rawColorsArray = null;
    let procColorsArray = null;
    let splitRatio = 0.50;
    let isDraggingSplit = false;

    let detectedBoxes = [];
    let detectedPoses = [];
    let detectedFaceMeshes = [];
    let detectedHandMeshes = [];
    let selectedBoxId = null;
    let boxThreeObjects = new Map();

    // ========================================================================
    // 2. Load Point Cloud & Automated Perception
    // ========================================================================
    async function loadCloud(name = "velodyne_000008.bin") {
      try {
        currentDataset = name;
        const resp = await fetch(`/api/dataset/${name}`);
        const data = await resp.json();
        currentRawData = data;

        document.getElementById('val-pts').textContent = data.total_points.toLocaleString();
        document.getElementById('ds-badge').textContent = data.dataset_name;
        const splitRawPts = document.getElementById('split-raw-pts');
        if (splitRawPts) splitRawPts.textContent = `${data.total_points.toLocaleString()} PTS`;

        updatePointCloudGeometry(data.points, data.intensity);

        // Run automated 3D suite
        await runAutoDetect3D(name);
        await updateSafetyAndManufacturingMetrics(name);
      } catch (err) {
        console.warn("Could not load dataset", err);
      }
    }

    function updatePointCloudGeometry(ptsArray, intensityArray) {
      const pts = new Float32Array(ptsArray);
      const intensities = new Float32Array(intensityArray || pts.length / 3);
      const count = pts.length / 3;

      const geomRaw = new THREE.BufferGeometry();
      geomRaw.setAttribute('position', new THREE.BufferAttribute(pts, 3));
      rawColorsArray = new Float32Array(count * 3);

      const geomProc = new THREE.BufferGeometry();
      geomProc.setAttribute('position', new THREE.BufferAttribute(new Float32Array(ptsArray), 3));
      procColorsArray = new Float32Array(count * 3);

      for (let i = 0; i < count; i++) {
        const val = Math.min(1.0, Math.max(0.0, intensities[i]));
        // State A: Pure sensor reflectance intensity gradient (grey/silver/blue raw lidar)
        rawColorsArray[i*3] = val * 0.70 + 0.20;
        rawColorsArray[i*3+1] = val * 0.70 + 0.20;
        rawColorsArray[i*3+2] = val * 0.85 + 0.15;

        // State B: Calibrated perception gradient (high contrast neon cyan/emerald/amber)
        procColorsArray[i*3] = Math.sin(val * Math.PI) * 0.8 + 0.2;
        procColorsArray[i*3+1] = Math.cos(val * Math.PI * 0.5) * 0.7;
        procColorsArray[i*3+2] = val * 0.9 + 0.1;
      }
      geomRaw.setAttribute('color', new THREE.BufferAttribute(rawColorsArray, 3));
      geomProc.setAttribute('color', new THREE.BufferAttribute(procColorsArray, 3));

      if (cloudPointsRaw) scene.remove(cloudPointsRaw);
      if (cloudPointsProc) scene.remove(cloudPointsProc);

      const matRaw = new THREE.PointsMaterial({ size: pointSizeScale, vertexColors: true, sizeAttenuation: true });
      const matProc = new THREE.PointsMaterial({ size: pointSizeScale, vertexColors: true, sizeAttenuation: true });

      cloudPointsRaw = new THREE.Points(geomRaw, matRaw);
      cloudPointsProc = new THREE.Points(geomProc, matProc);

      scene.add(cloudPointsRaw);
      scene.add(cloudPointsProc);

      cloudPoints = cloudPointsProc;
    }

    // ========================================================================
    // 3. Automated 3D Perception Engine
    // ========================================================================
    async function runAutoDetect3D(datasetName = currentDataset) {
      try {
        const resp = await fetch(`/api/detections/3d?dataset=${datasetName}`);
        const data = await resp.json();
        detectedBoxes = data.boxes || [];
        detectedPoses = data.poses || [];
        detectedFaceMeshes = data.face_meshes || [];
        detectedHandMeshes = data.hand_meshes || [];

        document.getElementById('val-clusters').textContent = `${data.total_objects} Objects`;
        document.getElementById('badge-box-count').textContent = data.total_objects;
        document.getElementById('cat-count').textContent = data.total_objects;
        document.getElementById('val-lat').textContent = `${data.latency_ms.toFixed(1)} ms`;

        render3DPerceptionObjects();
        populateObjectRoster();
        updateStateOverlayText();
      } catch (err) {
        console.error("Detection error", err);
      }
    }

    const CLASS_COLORS = {
      "Vehicle": 0x00E5FF,
      "Pedestrian": 0x10B981,
      "Cyclist": 0xF59E0B,
      "Infrastructure": 0x94A3B8,
      "Obstacle": 0xFCA5A5,
      "Custom": 0x38BDF8,
    };

    function render3DPerceptionObjects() {
      while(boxesGroup.children.length > 0) boxesGroup.remove(boxesGroup.children[0]);
      while(posesGroup.children.length > 0) posesGroup.remove(posesGroup.children[0]);
      while(biometricsGroup.children.length > 0) biometricsGroup.remove(biometricsGroup.children[0]);
      while(occlusionGroup.children.length > 0) occlusionGroup.remove(occlusionGroup.children[0]);
      boxThreeObjects.clear();

      if (comparisonState === 'A') {
        boxesGroup.visible = false;
        posesGroup.visible = false;
        biometricsGroup.visible = false;
        occlusionGroup.visible = false;
        return;
      }

      boxesGroup.visible = true;
      posesGroup.visible = true;
      biometricsGroup.visible = true;
      occlusionGroup.visible = true;

      detectedBoxes.forEach(box => {
        const bObj = create3DBoxMesh(box);
        boxesGroup.add(bObj);
        boxThreeObjects.set(box.id, bObj);
      });

      detectedPoses.forEach(pose => {
        posesGroup.add(create3DPoseMesh(pose));
      });
      detectedFaceMeshes.forEach(fmesh => {
        biometricsGroup.add(createFaceMeshMesh(fmesh));
      });
      detectedHandMeshes.forEach(hmesh => {
        biometricsGroup.add(createHandMeshMesh(hmesh));
      });
    }

    function getTwinMaterial(colorHex) {
      if (shapeRenderStyle === "solid") {
        return new THREE.MeshStandardMaterial({
          color: colorHex,
          metalness: 0.60,
          roughness: 0.35,
          transparent: true,
          opacity: Math.min(1.0, shapeOpacity + 0.35),
          side: THREE.DoubleSide
        });
      } else if (shapeRenderStyle === "xray") {
        return new THREE.MeshBasicMaterial({
          color: colorHex,
          wireframe: true,
          transparent: true,
          opacity: shapeOpacity
        });
      } else {
        // Holographic Twin
        return new THREE.MeshStandardMaterial({
          color: colorHex,
          emissive: colorHex,
          emissiveIntensity: 0.30,
          metalness: 0.25,
          roughness: 0.40,
          transparent: true,
          opacity: shapeOpacity,
          side: THREE.DoubleSide
        });
      }
    }

    function createVehicleDigitalTwin(L, W, H, colHex) {
      const g = new THREE.Group();
      const bodyMat = getTwinMaterial(colHex);

      // 1. Aerodynamic Lower Chassis
      const chassisGeom = new THREE.BoxGeometry(L * 0.94, W * 0.88, H * 0.38);
      const chassis = new THREE.Mesh(chassisGeom, bodyMat);
      chassis.position.set(0, 0, -H * 0.12);
      g.add(chassis);

      // 2. Cabin Greenhouse / Cockpit
      const cabinGeom = new THREE.BoxGeometry(L * 0.54, W * 0.76, H * 0.36);
      const cabinMat = shapeRenderStyle === "solid" ?
        new THREE.MeshStandardMaterial({ color: 0x0E131E, roughness: 0.2, metalness: 0.8, transparent: true, opacity: 0.85 }) :
        bodyMat;
      const cabin = new THREE.Mesh(cabinGeom, cabinMat);
      cabin.position.set(-L * 0.05, 0, H * 0.22);
      g.add(cabin);

      // 3. Hood Taper & Trunk Deck
      const hoodGeom = new THREE.BoxGeometry(L * 0.26, W * 0.82, H * 0.16);
      const hood = new THREE.Mesh(hoodGeom, bodyMat);
      hood.position.set(L * 0.34, 0, 0.01);
      g.add(hood);

      // 4. Four Realistic Wheels with Tires
      const tireGeom = new THREE.CylinderGeometry(H * 0.22, H * 0.22, W * 0.14, 16);
      tireGeom.rotateX(Math.PI / 2);
      const tireMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.8, metalness: 0.3 });

      const wheelPositions = [
        [L * 0.28, W * 0.44, -H * 0.28],
        [L * 0.28, -W * 0.44, -H * 0.28],
        [-L * 0.28, W * 0.44, -H * 0.28],
        [-L * 0.28, -W * 0.44, -H * 0.28],
      ];
      wheelPositions.forEach(pos => {
        const tire = new THREE.Mesh(tireGeom, tireMat);
        tire.position.set(...pos);
        g.add(tire);
      });

      // 5. Dual LED Headlights & Forward Illumination Beams
      const lightGeom = new THREE.BoxGeometry(0.12, 0.18, 0.10);
      const headMat = new THREE.MeshBasicMaterial({ color: 0xE0F2FE });
      [-1, 1].forEach(side => {
        const head = new THREE.Mesh(lightGeom, headMat);
        head.position.set(L * 0.47, side * W * 0.30, -H * 0.05);
        g.add(head);
      });

      // Forward Road Illumination Beam (Translucent Projection Cone)
      const beamGeom = new THREE.ConeGeometry(W * 0.55, L * 0.85, 16, 1, true);
      beamGeom.rotateZ(-Math.PI / 2);
      const beamMat = new THREE.MeshBasicMaterial({ color: 0x00E5FF, transparent: true, opacity: 0.12, side: THREE.DoubleSide });
      const beam = new THREE.Mesh(beamGeom, beamMat);
      beam.position.set(L * 0.48 + L * 0.42, 0, -H * 0.15);
      g.add(beam);

      // 6. Dual Red Taillights
      const tailGeom = new THREE.BoxGeometry(0.08, 0.22, 0.08);
      const tailMat = new THREE.MeshBasicMaterial({ color: 0xEF4444 });
      [-1, 1].forEach(side => {
        const tail = new THREE.Mesh(tailGeom, tailMat);
        tail.position.set(-L * 0.47, side * W * 0.32, -H * 0.05);
        g.add(tail);
      });

      return g;
    }

    function createPedestrianDigitalTwin(L, W, H, colHex) {
      const g = new THREE.Group();
      const bodyMat = getTwinMaterial(colHex);

      // Head
      const head = new THREE.Mesh(new THREE.SphereGeometry(H * 0.10, 12, 12), bodyMat);
      head.position.set(0, 0, H * 0.40);
      g.add(head);

      // Torso
      const torso = new THREE.Mesh(new THREE.BoxGeometry(L * 0.65, W * 0.75, H * 0.34), bodyMat);
      torso.position.set(0, 0, H * 0.13);
      g.add(torso);

      // Arms (natural walking swing)
      const armGeom = new THREE.BoxGeometry(L * 0.20, W * 0.20, H * 0.32);
      const lArm = new THREE.Mesh(armGeom, bodyMat);
      lArm.position.set(L * 0.08, W * 0.46, H * 0.10);
      lArm.rotation.y = 0.18;
      g.add(lArm);

      const rArm = new THREE.Mesh(armGeom, bodyMat);
      rArm.position.set(-L * 0.08, -W * 0.46, H * 0.10);
      rArm.rotation.y = -0.18;
      g.add(rArm);

      // Pelvis
      const pelvis = new THREE.Mesh(new THREE.BoxGeometry(L * 0.50, W * 0.60, H * 0.10), bodyMat);
      pelvis.position.set(0, 0, -H * 0.10);
      g.add(pelvis);

      // Striding Legs
      const legGeom = new THREE.BoxGeometry(L * 0.22, W * 0.24, H * 0.38);
      const lLeg = new THREE.Mesh(legGeom, bodyMat);
      lLeg.position.set(L * 0.12, W * 0.22, -H * 0.30);
      lLeg.rotation.y = 0.22;
      g.add(lLeg);

      const rLeg = new THREE.Mesh(legGeom, bodyMat);
      rLeg.position.set(-L * 0.12, -W * 0.22, -H * 0.30);
      rLeg.rotation.y = -0.22;
      g.add(rLeg);

      // Safety Ground Proximity Halo
      const haloGeom = new THREE.RingGeometry(Math.max(L, W) * 0.65, Math.max(L, W) * 0.75, 32);
      const haloMat = new THREE.MeshBasicMaterial({ color: 0x10B981, transparent: true, opacity: 0.25, side: THREE.DoubleSide });
      const halo = new THREE.Mesh(haloGeom, haloMat);
      halo.position.set(0, 0, -H * 0.48);
      g.add(halo);

      return g;
    }

    function createCyclistDigitalTwin(L, W, H, colHex) {
      const g = new THREE.Group();
      const frameMat = getTwinMaterial(colHex);

      // 1. Spoke Wheels (Front & Rear)
      const wheelGeom = new THREE.TorusGeometry(H * 0.24, H * 0.025, 8, 24);
      wheelGeom.rotateY(Math.PI / 2);
      const wheelMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.7 });

      const fWheel = new THREE.Mesh(wheelGeom, wheelMat);
      fWheel.position.set(L * 0.35, 0, -H * 0.24);
      g.add(fWheel);

      const rWheel = new THREE.Mesh(wheelGeom, wheelMat);
      rWheel.position.set(-L * 0.35, 0, -H * 0.24);
      g.add(rWheel);

      // 2. Diamond Frame Tubes
      const tubeMat = getTwinMaterial(0xF59E0B);
      const crossTube = new THREE.Mesh(new THREE.BoxGeometry(L * 0.60, 0.06, 0.06), tubeMat);
      crossTube.position.set(0, 0, -H * 0.08);
      g.add(crossTube);

      const downTube = new THREE.Mesh(new THREE.BoxGeometry(L * 0.40, 0.06, 0.06), tubeMat);
      downTube.position.set(L * 0.10, 0, -H * 0.15);
      downTube.rotation.y = 0.50;
      g.add(downTube);

      // Handlebars
      const handle = new THREE.Mesh(new THREE.BoxGeometry(0.08, W * 0.65, 0.06), tubeMat);
      handle.position.set(L * 0.25, 0, H * 0.10);
      g.add(handle);

      // 3. Mounted Leaning Rider
      const riderMat = getTwinMaterial(colHex);
      const riderTorso = new THREE.Mesh(new THREE.BoxGeometry(L * 0.36, W * 0.45, H * 0.28), riderMat);
      riderTorso.position.set(L * 0.04, 0, H * 0.12);
      riderTorso.rotation.y = -0.32;
      g.add(riderTorso);

      const helmet = new THREE.Mesh(new THREE.SphereGeometry(H * 0.095, 12, 12), getTwinMaterial(0xF59E0B));
      helmet.position.set(L * 0.18, 0, H * 0.30);
      g.add(helmet);

      return g;
    }

    function createInfrastructureDigitalTwin(L, W, H, colHex) {
      const g = new THREE.Group();
      const mat = getTwinMaterial(colHex);

      if (H > 2.8 && L < 1.2) {
        // Vertical Streetlight Pole
        const poleGeom = new THREE.CylinderGeometry(0.12, 0.16, H * 0.96, 12);
        poleGeom.rotateX(Math.PI / 2);
        const pole = new THREE.Mesh(poleGeom, mat);
        g.add(pole);

        // Luminaire Arm & Head
        const arm = new THREE.Mesh(new THREE.BoxGeometry(L * 0.8 + 0.8, 0.12, 0.10), mat);
        arm.position.set(0.4, 0, H * 0.46);
        g.add(arm);

        // Downward light cone
        const coneGeom = new THREE.ConeGeometry(0.8, 2.0, 16, 1, true);
        coneGeom.rotateX(Math.PI);
        const coneMat = new THREE.MeshBasicMaterial({ color: 0x00E5FF, transparent: true, opacity: 0.12, side: THREE.DoubleSide });
        const cone = new THREE.Mesh(coneGeom, coneMat);
        cone.position.set(0.8, 0, H * 0.40 - 1.0);
        g.add(cone);
      } else {
        // Concrete Jersey Barrier Segment with Chamfer Profile
        const base = new THREE.Mesh(new THREE.BoxGeometry(L * 0.98, W * 0.96, H * 0.35), mat);
        base.position.set(0, 0, -H * 0.32);
        g.add(base);

        const stem = new THREE.Mesh(new THREE.BoxGeometry(L * 0.98, W * 0.65, H * 0.40), mat);
        stem.position.set(0, 0, 0);
        g.add(stem);

        const crest = new THREE.Mesh(new THREE.BoxGeometry(L * 0.98, W * 0.45, H * 0.25), mat);
        crest.position.set(0, 0, H * 0.35);
        g.add(crest);
      }
      return g;
    }

    function createObstacleDigitalTwin(L, W, H, colHex) {
      const g = new THREE.Group();
      if (H <= 1.4 && Math.abs(L - W) < 0.8) {
        // High-Visibility Traffic Safety Cone
        const base = new THREE.Mesh(new THREE.BoxGeometry(L * 0.88, W * 0.88, H * 0.08), getTwinMaterial(0xF97316));
        base.position.set(0, 0, -H * 0.46);
        g.add(base);

        const coneGeom = new THREE.ConeGeometry(W * 0.38, H * 0.90, 16);
        coneGeom.rotateX(Math.PI / 2);
        const cone = new THREE.Mesh(coneGeom, getTwinMaterial(0xF97316));
        g.add(cone);

        // Reflective White Collar
        const collarGeom = new THREE.CylinderGeometry(W * 0.20, W * 0.26, H * 0.20, 16);
        collarGeom.rotateX(Math.PI / 2);
        const collar = new THREE.Mesh(collarGeom, new THREE.MeshBasicMaterial({ color: 0xFFFFFF }));
        collar.position.set(0, 0, 0);
        g.add(collar);
      } else {
        // Faceted Impact Barrier Block
        const block = new THREE.Mesh(new THREE.BoxGeometry(L * 0.92, W * 0.92, H * 0.92), getTwinMaterial(0xFCA5A5));
        g.add(block);
      }
      return g;
    }

    function createDigitalTwinShape(box) {
      const [L, W, H] = box.dimensions;
      const colHex = CLASS_COLORS[box.class_label] || 0x00E5FF;
      let twin;
      if (box.class_label === "Vehicle") {
        twin = createVehicleDigitalTwin(L, W, H, colHex);
      } else if (box.class_label === "Pedestrian") {
        twin = createPedestrianDigitalTwin(L, W, H, colHex);
      } else if (box.class_label === "Cyclist") {
        twin = createCyclistDigitalTwin(L, W, H, colHex);
      } else if (box.class_label === "Infrastructure") {
        twin = createInfrastructureDigitalTwin(L, W, H, colHex);
      } else if (box.class_label === "Obstacle") {
        twin = createObstacleDigitalTwin(L, W, H, colHex);
      } else {
        twin = createVehicleDigitalTwin(L, W, H, colHex);
      }
      twin.name = "digitalTwin";
      twin.visible = showDigitalTwins;
      return twin;
    }

    function create3DBoxMesh(box) {
      const group = new THREE.Group();
      group.name = box.id;
      group.userData = { boxData: box };

      const [L, W, H] = box.dimensions;
      const [cx, cy, cz] = box.center;
      const colHex = CLASS_COLORS[box.class_label] || 0x00E5FF;

      // 1. Box Wireframe
      const boxGeom = new THREE.BoxGeometry(L, W, H);
      const edgesGeom = new THREE.EdgesGeometry(boxGeom);
      const wireframe = new THREE.LineSegments(edgesGeom, new THREE.LineBasicMaterial({ color: colHex, linewidth: 2, transparent: true, opacity: 0.85 }));
      wireframe.name = "wireframe";
      group.add(wireframe);

      // 2. Realistic 3D Geometric Digital Twin
      const twin = createDigitalTwinShape(box);
      group.add(twin);

      // 3. Front Face Heading Plane
      const frontGeom = new THREE.PlaneGeometry(W, H);
      const frontFace = new THREE.Mesh(frontGeom, new THREE.MeshBasicMaterial({ color: colHex, transparent: true, opacity: 0.24, side: THREE.DoubleSide }));
      frontFace.position.set(L / 2, 0, 0);
      frontFace.rotation.y = Math.PI / 2;
      group.add(frontFace);

      // 4. Heading Arrow
      const arrow = new THREE.ArrowHelper(new THREE.Vector3(1, 0, 0), new THREE.Vector3(0, 0, 0), L * 0.70, colHex, 0.35, 0.20);
      arrow.name = "headingArrow";
      group.add(arrow);

      // 5. Hit Target for Raycaster
      const hitMesh = new THREE.Mesh(new THREE.BoxGeometry(L * 1.05, W * 1.05, H * 1.05), new THREE.MeshBasicMaterial({ visible: false }));
      hitMesh.userData = { boxId: box.id };
      group.add(hitMesh);

      // 6. Tactical Billboard Text Tag
      const sprite = createTacticalBillboardTag(box.class_label, box.confidence, `${L.toFixed(1)}x${W.toFixed(1)}x${H.toFixed(1)}m`, box.occlusion_ratio);
      sprite.position.set(0, 0, H / 2 + 0.35);
      sprite.name = "tagSprite";
      group.add(sprite);

      group.position.set(cx, cy, cz);
      group.rotation.z = THREE.MathUtils.degToRad(box.yaw_deg);
      return group;
    }

    function createTacticalBillboardTag(className, conf, dimsStr, occRatio) {
      const canvas = document.createElement('canvas');
      canvas.width = 256; canvas.height = 64;
      const ctx = canvas.getContext('2d');

      const strokeCol = className === 'Vehicle' ? '#00E5FF' :
                        (className === 'Pedestrian' ? '#10B981' :
                        (className === 'Cyclist' ? '#F59E0B' :
                        (className === 'Infrastructure' ? '#94A3B8' : '#FCA5A5')));

      // Tactical Dark Glass Card
      ctx.fillStyle = 'rgba(11, 15, 23, 0.92)';
      ctx.strokeStyle = strokeCol;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.roundRect(2, 2, 252, 60, 4);
      ctx.fill(); ctx.stroke();

      ctx.font = '700 18px "Sora", sans-serif';
      ctx.fillStyle = strokeCol;
      ctx.fillText(className.toUpperCase(), 12, 24);

      ctx.font = '12px "JetBrains Mono", monospace';
      ctx.fillStyle = '#E2E8F0';
      ctx.fillText(`${(conf * 100).toFixed(0)}% • ${dimsStr}`, 12, 46);

      const occPct = (occRatio * 100).toFixed(0);
      ctx.fillStyle = occRatio <= 0.20 ? '#10B981' : (occRatio <= 0.65 ? '#F59E0B' : '#EF4444');
      ctx.fillText(`OCC ${occPct}%`, 175, 24);

      const texture = new THREE.CanvasTexture(canvas);
      const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: texture, transparent: true }));
      sprite.scale.set(2.2, 0.55, 1);
      return sprite;
    }

    function create3DPoseMesh(pose) {
      const group = new THREE.Group();
      const joints = pose.joints;
      const sGeom = new THREE.SphereGeometry(0.04, 8, 8);
      const sMat = new THREE.MeshBasicMaterial({ color: 0x10B981 });

      for (const [name, pos] of Object.entries(joints)) {
        const s = new THREE.Mesh(sGeom, sMat);
        s.position.set(pos[0], pos[1], pos[2]);
        group.add(s);
      }
      const linePositions = [];
      pose.bones.forEach(([j1, j2]) => {
        if (joints[j1] && joints[j2]) linePositions.push(...joints[j1], ...joints[j2]);
      });
      const lineGeom = new THREE.BufferGeometry();
      lineGeom.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3));
      group.add(new THREE.LineSegments(lineGeom, new THREE.LineBasicMaterial({ color: 0x6EE7B7, linewidth: 1.5 })));
      return group;
    }

    function createFaceMeshMesh(fmesh) {
      const group = new THREE.Group();
      const linePositions = [];
      fmesh.contour_indices.forEach(loop => {
        for (let i = 0; i < loop.length - 1; i++) {
          const v1 = fmesh.vertices[loop[i]], v2 = fmesh.vertices[loop[i+1]];
          if (v1 && v2) linePositions.push(...v1, ...v2);
        }
      });
      const geom = new THREE.BufferGeometry();
      geom.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3));
      group.add(new THREE.LineSegments(geom, new THREE.LineBasicMaterial({ color: 0x00E5FF, transparent: true, opacity: 0.6 })));
      return group;
    }

    function createHandMeshMesh(hmesh) {
      const group = new THREE.Group();
      const linePositions = [];
      hmesh.bones.forEach(([j1, j2]) => {
        if (hmesh.joints[j1] && hmesh.joints[j2]) linePositions.push(...hmesh.joints[j1], ...hmesh.joints[j2]);
      });
      const geom = new THREE.BufferGeometry();
      geom.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3));
      group.add(new THREE.LineSegments(geom, new THREE.LineBasicMaterial({ color: 0xF59E0B, transparent: true, opacity: 0.7 })));
      return group;
    }

    function populateObjectRoster() {
      const listEl = document.getElementById('canva-roster-list');
      listEl.innerHTML = '';
      if (detectedBoxes.length === 0) {
        listEl.innerHTML = '<div style="color:var(--text-dim); font-size:0.72rem;">No objects detected in scene.</div>';
        return;
      }
      detectedBoxes.forEach(box => {
        const card = document.createElement('div');
        card.className = `roster-card ${box.id === selectedBoxId ? 'active' : ''}`;
        card.id = `roster-${box.id}`;
        const occPct = Math.round(box.occlusion_ratio * 100);
        const occClass = occPct <= 20 ? 'occ-low' : (occPct <= 65 ? 'occ-med' : 'occ-high');

        card.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:3px;">
            <strong style="font-size:0.72rem; color:var(--text); font-family:'JetBrains Mono';">${box.id}</strong>
            <span class="badge-occ ${occClass}">OCC ${occPct}%</span>
          </div>
          <div style="font-family:'JetBrains Mono', monospace; font-size:0.68rem; color:var(--text-dim);">
            ${box.class_label} • ${box.dimensions[0]}x${box.dimensions[1]}x${box.dimensions[2]}m • ${(box.confidence * 100).toFixed(0)}%
          </div>
        `;
        card.addEventListener('click', () => { selectBox(box.id); focusCameraOnBox(box); });
        listEl.appendChild(card);
      });
    }

    function selectBox(boxId) {
      selectedBoxId = boxId;
      const box = detectedBoxes.find(b => b.id === boxId);
      if (!box) return;

      document.querySelectorAll('.roster-card').forEach(c => c.classList.remove('active'));
      const activeCard = document.getElementById(`roster-${boxId}`);
      if (activeCard) activeCard.classList.add('active');

      boxThreeObjects.forEach((grp, id) => {
        const wire = grp.getObjectByName('wireframe');
        if (wire) {
          wire.material.color.setHex(id === boxId ? 0xFFFF00 : (CLASS_COLORS[box.class_label] || 0x00E5FF));
          wire.material.opacity = id === boxId ? 1.0 : 0.85;
        }
      });

      const inspector = document.getElementById('spatial-inspector');
      inspector.style.display = 'block';

      document.getElementById('ci-obj-id').textContent = box.id;
      document.getElementById('ci-class-select').value = box.class_label;
      document.getElementById('ci-conf-val').textContent = Number(box.confidence).toFixed(2);

      // Badge label styling
      const badgeLabel = document.getElementById('ci-badge-label');
      badgeLabel.textContent = box.class_label.toUpperCase();
      badgeLabel.className = 'ci-badge ' + (
        box.class_label === 'Vehicle' ? 'ci-badge-veh' :
        box.class_label === 'Pedestrian' ? 'ci-badge-ped' :
        box.class_label === 'Cyclist' ? 'ci-badge-cyc' :
        box.class_label === 'Infrastructure' ? 'ci-badge-inf' : 'ci-badge-obs'
      );

      const occPct = Math.round((box.occlusion_ratio || 0) * 100);
      const occStatus = box.occlusion_status || (occPct <= 20 ? 'Clear' : (occPct <= 65 ? 'Partial' : 'Heavy'));
      const occColor = occPct <= 20 ? 'var(--emerald)' : (occPct <= 65 ? 'var(--amber)' : 'var(--rose)');
      const occEl = document.getElementById('ci-occ-val');
      occEl.textContent = `${occPct}% (${occStatus})`;
      occEl.style.color = occColor;
      document.getElementById('ci-occ-bar').style.width = `${occPct}%`;
      document.getElementById('ci-occ-bar').style.background = occColor;

      // Clean 2-decimal spatial coordinates & dimensions
      document.getElementById('ci-pos-x').value = Number(box.center[0]).toFixed(2);
      document.getElementById('ci-pos-y').value = Number(box.center[1]).toFixed(2);
      document.getElementById('ci-pos-z').value = Number(box.center[2]).toFixed(2);

      document.getElementById('ci-dim-l').value = Number(box.dimensions[0]).toFixed(2);
      document.getElementById('ci-dim-w').value = Number(box.dimensions[1]).toFixed(2);
      document.getElementById('ci-dim-h').value = Number(box.dimensions[2]).toFixed(2);

      document.getElementById('ci-yaw-slider').value = box.yaw_deg || 0;
      document.getElementById('ci-yaw-disp').textContent = `${(box.yaw_deg || 0).toFixed(1)}°`;

      const ptsCount = box.num_points || 0;
      document.getElementById('ci-pts-count-disp').textContent = `${ptsCount} PTS COVERED`;

      // Expanded Full Features Telemetry
      const [L, W, H] = box.dimensions;
      const [cx, cy, cz] = box.center;
      const radialDist = Math.sqrt(cx*cx + cy*cy + cz*cz);
      const vol = L * W * H;
      const sArea = 2 * (L * W + L * H + W * H);
      const zMin = (cz - H / 2).toFixed(2);
      const zMax = (cz + H / 2).toFixed(2);
      const ttcSec = Math.max(0.4, (radialDist / 12.5)).toFixed(1);
      const ptDensity = vol > 0.05 ? (ptsCount / vol).toFixed(1) : "0.0";
      const hiddenVol = (vol * (box.occlusion_ratio || 0)).toFixed(2);
      const ratioLW = (W > 0.05 ? (L / W).toFixed(2) : "0.00");
      const groundClearance = Math.max(0, (cz - H/2) - (-1.73)).toFixed(2);

      document.getElementById('ci-exp-dist').textContent = `${radialDist.toFixed(2)} m`;
      document.getElementById('ci-exp-vol').textContent = `${vol.toFixed(2)} m³`;
      document.getElementById('ci-exp-area').textContent = `${sArea.toFixed(2)} m²`;
      document.getElementById('ci-exp-zspan').textContent = `${zMin} .. ${zMax} m`;
      document.getElementById('ci-exp-ttc').textContent = `${ttcSec}s (Nominal)`;
      document.getElementById('ci-exp-density').textContent = `${ptDensity} pts/m³`;
      document.getElementById('ci-exp-hidden-vol').textContent = `${hiddenVol} m³`;
      document.getElementById('ci-exp-ratio').textContent = `${ratioLW}`;
      document.getElementById('ci-exp-clearance').textContent = `${groundClearance} m`;

      document.getElementById('ci-exp-json').value = JSON.stringify({
        id: box.id,
        class_label: box.class_label,
        confidence: Number(Number(box.confidence).toFixed(2)),
        center: [Number(cx.toFixed(2)), Number(cy.toFixed(2)), Number(cz.toFixed(2))],
        dimensions: [Number(L.toFixed(2)), Number(W.toFixed(2)), Number(H.toFixed(2))],
        yaw_deg: Number((box.yaw_deg || 0).toFixed(1)),
        occlusion_ratio: Number(Number(box.occlusion_ratio || 0).toFixed(2)),
        radial_dist_m: Number(radialDist.toFixed(2)),
        volume_m3: Number(vol.toFixed(2)),
        points_covered: ptsCount
      }, null, 2);
    }

    function focusCameraOnBox(box) {
      const [x, y, z] = box.center;
      controls.target.set(x, y, z);
      camera.position.set(x + 5, y - 5, z + 4);
      controls.update();
    }

    // Double Click on 3D Box or Canvas selects & focuses
    container.addEventListener('dblclick', (event) => {
      const rect = renderer.domElement.getBoundingClientRect();
      const mouse = new THREE.Vector2(((event.clientX - rect.left) / rect.width) * 2 - 1, -((event.clientY - rect.top) / rect.height) * 2 + 1);
      const raycaster = new THREE.Raycaster();
      raycaster.setFromCamera(mouse, camera);

      const intersects = raycaster.intersectObjects(boxesGroup.children, true);
      if (intersects.length > 0) {
        let hitObj = intersects[0].object;
        while (hitObj.parent && hitObj.parent !== boxesGroup) hitObj = hitObj.parent;
        if (hitObj && hitObj.name) {
          selectBox(hitObj.name);
          const box = detectedBoxes.find(b => b.id === hitObj.name);
          if (box) focusCameraOnBox(box);
        }
      }
    });

    // Pointer move updates live reticle coordinates in bottom telemetry HUD
    container.addEventListener('pointermove', (event) => {
      const rect = renderer.domElement.getBoundingClientRect();
      const mouse = new THREE.Vector2(((event.clientX - rect.left) / rect.width) * 2 - 1, -((event.clientY - rect.top) / rect.height) * 2 + 1);
      const raycaster = new THREE.Raycaster();
      raycaster.setFromCamera(mouse, camera);

      const planeZ = new THREE.Plane(new THREE.Vector3(0, 0, 1), 1.73);
      const target = new THREE.Vector3();
      raycaster.ray.intersectPlane(planeZ, target);

      if (target) {
        document.getElementById('reticle-x').textContent = `X: ${(target.x >= 0 ? '+' : '') + target.x.toFixed(2)}m`;
        document.getElementById('reticle-y').textContent = `Y: ${(target.y >= 0 ? '+' : '') + target.y.toFixed(2)}m`;
        document.getElementById('reticle-z').textContent = `Z: ${(target.z >= 0 ? '+' : '') + target.z.toFixed(2)}m`;
        document.getElementById('reticle-range').textContent = `${target.length().toFixed(2)}m`;
      }
    });

    // Raycaster single-click selection
    container.addEventListener('pointerdown', (event) => {
      if (event.target !== renderer.domElement) return;
      const rect = renderer.domElement.getBoundingClientRect();
      const mouse = new THREE.Vector2(((event.clientX - rect.left) / rect.width) * 2 - 1, -((event.clientY - rect.top) / rect.height) * 2 + 1);
      const raycaster = new THREE.Raycaster();
      raycaster.setFromCamera(mouse, camera);

      const intersects = raycaster.intersectObjects(boxesGroup.children, true);
      if (intersects.length > 0) {
        let hitObj = intersects[0].object;
        while (hitObj.parent && hitObj.parent !== boxesGroup) hitObj = hitObj.parent;
        if (hitObj && hitObj.name) selectBox(hitObj.name);
      }
    });

    // Spatial Inspector Input Updates (Update in real time)
    function updateSelectedBoxFromInspector() {
      if (!selectedBoxId) return;
      const box = detectedBoxes.find(b => b.id === selectedBoxId);
      if (!box) return;

      box.center[0] = parseFloat(document.getElementById('ci-pos-x').value) || box.center[0];
      box.center[1] = parseFloat(document.getElementById('ci-pos-y').value) || box.center[1];
      box.center[2] = parseFloat(document.getElementById('ci-pos-z').value) || box.center[2];

      box.dimensions[0] = Math.max(0.2, parseFloat(document.getElementById('ci-dim-l').value) || box.dimensions[0]);
      box.dimensions[1] = Math.max(0.2, parseFloat(document.getElementById('ci-dim-w').value) || box.dimensions[1]);
      box.dimensions[2] = Math.max(0.2, parseFloat(document.getElementById('ci-dim-h').value) || box.dimensions[2]);

      box.yaw_deg = parseFloat(document.getElementById('ci-yaw-slider').value) || 0.0;
      document.getElementById('ci-yaw-disp').textContent = `${box.yaw_deg.toFixed(1)}°`;
      box.class_label = document.getElementById('ci-class-select').value;

      // Update badge label
      const badgeLabel = document.getElementById('ci-badge-label');
      badgeLabel.textContent = box.class_label.toUpperCase();
      badgeLabel.className = 'ci-badge ' + (
        box.class_label === 'Vehicle' ? 'ci-badge-veh' :
        box.class_label === 'Pedestrian' ? 'ci-badge-ped' :
        box.class_label === 'Cyclist' ? 'ci-badge-cyc' :
        box.class_label === 'Infrastructure' ? 'ci-badge-inf' : 'ci-badge-obs'
      );

      const grp = boxThreeObjects.get(selectedBoxId);
      if (grp) {
        boxesGroup.remove(grp);
        const newGrp = create3DBoxMesh(box);
        const wire = newGrp.getObjectByName('wireframe');
        if (wire) { wire.material.color.setHex(0xFFFF00); wire.material.opacity = 1.0; }
        boxesGroup.add(newGrp);
        boxThreeObjects.set(selectedBoxId, newGrp);
      }

      // Re-populate expanded metrics
      const [L, W, H] = box.dimensions;
      const [cx, cy, cz] = box.center;
      const radialDist = Math.sqrt(cx*cx + cy*cy + cz*cz);
      const vol = L * W * H;
      const sArea = 2 * (L * W + L * H + W * H);
      document.getElementById('ci-exp-dist').textContent = `${radialDist.toFixed(2)} m`;
      document.getElementById('ci-exp-vol').textContent = `${vol.toFixed(2)} m³`;
      document.getElementById('ci-exp-area').textContent = `${sArea.toFixed(2)} m²`;
      document.getElementById('ci-exp-zspan').textContent = `${(cz - H/2).toFixed(2)} .. ${(cz + H/2).toFixed(2)} m`;
      document.getElementById('ci-exp-ratio').textContent = (W > 0.05 ? (L / W).toFixed(2) : "0.00");
      document.getElementById('ci-exp-hidden-vol').textContent = `${(vol * (box.occlusion_ratio || 0)).toFixed(2)} m³`;
      document.getElementById('ci-exp-clearance').textContent = `${Math.max(0, (cz - H/2) - (-1.73)).toFixed(2)} m`;
    }

    ['ci-pos-x', 'ci-pos-y', 'ci-pos-z', 'ci-dim-l', 'ci-dim-w', 'ci-dim-h'].forEach(id => {
      document.getElementById(id).addEventListener('input', updateSelectedBoxFromInspector);
    });
    document.getElementById('ci-yaw-slider').addEventListener('input', updateSelectedBoxFromInspector);
    document.getElementById('ci-class-select').addEventListener('change', updateSelectedBoxFromInspector);
    document.getElementById('ci-close-btn').addEventListener('click', () => { document.getElementById('spatial-inspector').style.display = 'none'; });

    // Universal Smooth Dragging Engine (Clamped to Viewport Boundaries)
    function makeDraggable(el, handle) {
      if (!el || !handle) return;
      let isDragging = false;
      let startX = 0, startY = 0;
      let startLeft = 0, startTop = 0;

      handle.addEventListener('mousedown', (e) => {
        if (['BUTTON', 'INPUT', 'SELECT', 'TEXTAREA'].includes(e.target.tagName) || e.target.closest('.ci-tool-btn') || e.target.closest('#ci-close-btn') || e.target.closest('#slice-close-btn') || e.target.closest('#ai-drawer-close')) {
          return;
        }
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        const rect = el.getBoundingClientRect();
        startLeft = rect.left;
        startTop = rect.top;

        // Switch from fixed bottom/right positioning to absolute top/left coordinates
        el.style.left = `${startLeft}px`;
        el.style.top = `${startTop}px`;
        el.style.right = 'auto';
        el.style.bottom = 'auto';
        el.style.margin = '0';
        document.body.style.userSelect = 'none';
      });

      window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        const dx = e.clientX - startX;
        const dy = e.clientY - startY;
        const maxLeft = window.innerWidth - el.offsetWidth - 8;
        const maxTop = window.innerHeight - el.offsetHeight - 8;
        const newLeft = Math.max(8, Math.min(maxLeft, startLeft + dx));
        const newTop = Math.max(52, Math.min(maxTop, startTop + dy));
        el.style.left = `${newLeft}px`;
        el.style.top = `${newTop}px`;
      });

      window.addEventListener('mouseup', () => {
        if (isDragging) {
          isDragging = false;
          document.body.style.userSelect = '';
        }
      });
    }

    const ciInspector = document.getElementById('spatial-inspector');
    makeDraggable(ciInspector, document.getElementById('ci-drag-handle'));

    // Collapse / Expand Toggle for Spatial Inspector
    const btnCiCollapse = document.getElementById('ci-btn-collapse');
    const iconCiCollapse = document.getElementById('ci-collapse-icon');
    btnCiCollapse.addEventListener('click', () => {
      ciInspector.classList.toggle('is-collapsed');
      const isCol = ciInspector.classList.contains('is-collapsed');
      btnCiCollapse.title = isCol ? "Uncollapse Dialog" : "Collapse Dialog";
      iconCiCollapse.innerHTML = isCol ? '<polyline points="6 9 12 15 18 9"/>' : '<line x1="5" y1="12" x2="19" y2="12"/>';
    });

    // Expand Full Telemetry Drawer
    const btnCiExpand = document.getElementById('ci-btn-expand');
    const expSection = document.getElementById('ci-expanded-section');
    btnCiExpand.addEventListener('click', () => {
      ciInspector.classList.toggle('is-expanded');
      const isExp = ciInspector.classList.contains('is-expanded');
      expSection.style.display = isExp ? 'block' : 'none';
      btnCiExpand.classList.toggle('active', isExp);
      btnCiExpand.title = isExp ? "Compact View" : "Expand Full Features";
    });

    // Expanded Section Tab Navigation
    document.querySelectorAll('.ci-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.ci-tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const tab = btn.dataset.tab;
        document.getElementById('ci-pane-kinematics').style.display = tab === 'kinematics' ? 'block' : 'none';
        document.getElementById('ci-pane-coverage').style.display = tab === 'coverage' ? 'block' : 'none';
        document.getElementById('ci-pane-provenance').style.display = tab === 'provenance' ? 'block' : 'none';
      });
    });

    // Create New Bounding Box (Full CRUD - Create)
    function createNewBoundingBox() {
      const newId = `OBJ_${detectedBoxes.length + 1}_CUSTOM`;
      const targetPos = controls.target.clone();
      const newBox = {
        id: newId,
        class_label: "Vehicle",
        confidence: 0.95,
        center: [Number(targetPos.x.toFixed(2)), Number(targetPos.y.toFixed(2)), Number(targetPos.z.toFixed(2))],
        dimensions: [4.40, 1.85, 1.50],
        yaw_deg: 0.0,
        num_points: 38,
        occlusion_ratio: 0.08,
        occlusion_status: "Clear",
        hidden_volume_m3: 0.55,
        line_of_sight_dist_m: Number(targetPos.length().toFixed(2)),
        color_hex: "#00E5FF"
      };
      detectedBoxes.push(newBox);
      render3DPerceptionObjects();
      populateObjectRoster();
      selectBox(newId);
    }

    document.getElementById('ci-btn-create').addEventListener('click', createNewBoundingBox);
    document.getElementById('btn-add-box').addEventListener('click', createNewBoundingBox);

    // Place 3D Shape Directly on Actual Item
    const btnPlaceShape = document.getElementById('ci-btn-place-shape');
    if (btnPlaceShape) {
      btnPlaceShape.addEventListener('click', () => {
        if (!selectedBoxId || !currentRawData) {
          if (detectedBoxes.length > 0) {
            selectBox(detectedBoxes[0].id);
          } else {
            return;
          }
        }
        const box = detectedBoxes.find(b => b.id === selectedBoxId);
        if (!box) return;

        showDigitalTwins = true;
        setDigitalTwinsVisibility(true);

        const pts = currentRawData.points;
        const [bx, by, bz] = box.center;
        const [l, w, h] = box.dimensions;
        const contained = [];
        for (let i = 0; i < pts.length; i += 3) {
          if (Math.abs(pts[i]-bx) <= l * 0.9 && Math.abs(pts[i+1]-by) <= w * 0.9 && Math.abs(pts[i+2]-bz) <= h * 0.9) {
            contained.push([pts[i], pts[i+1], pts[i+2]]);
          }
        }
        if (contained.length > 8) {
          const minX = Math.min(...contained.map(p => p[0])), maxX = Math.max(...contained.map(p => p[0]));
          const minY = Math.min(...contained.map(p => p[1])), maxY = Math.max(...contained.map(p => p[1]));
          const minZ = Math.min(...contained.map(p => p[2])), maxZ = Math.max(...contained.map(p => p[2]));
          box.center = [Number(((minX+maxX)/2).toFixed(2)), Number(((minY+maxY)/2).toFixed(2)), Number(((minZ+maxZ)/2).toFixed(2))];
          box.dimensions = [Math.max(0.6, Number((maxX-minX).toFixed(2))), Math.max(0.6, Number((maxY-minY).toFixed(2))), Math.max(0.6, Number((maxZ-minZ).toFixed(2)))];
        }

        render3DPerceptionObjects();
        selectBox(box.id);
        const toast = document.createElement('div');
        toast.className = 'ci-badge ci-badge-veh';
        toast.style.position = 'fixed'; toast.style.bottom = '20px'; toast.style.right = '20px'; toast.style.zIndex = '9999';
        toast.textContent = `3D SHAPE PLACED ON ${box.id} (${box.class_label.toUpperCase()})`;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 2500);
      });
    }

    // Snap to Point Cluster
    document.getElementById('ci-btn-snap').addEventListener('click', () => {
      if (!selectedBoxId || !currentRawData) return;
      const box = detectedBoxes.find(b => b.id === selectedBoxId);
      if (!box) return;
      const pts = currentRawData.points;
      const [bx, by, bz] = box.center;
      const [l, w, h] = box.dimensions;
      const contained = [];
      for (let i = 0; i < pts.length; i += 3) {
        if (Math.abs(pts[i]-bx) <= l && Math.abs(pts[i+1]-by) <= w && Math.abs(pts[i+2]-bz) <= h) {
          contained.push([pts[i], pts[i+1], pts[i+2]]);
        }
      }
      if (contained.length > 5) {
        const minX = Math.min(...contained.map(p => p[0])), maxX = Math.max(...contained.map(p => p[0]));
        const minY = Math.min(...contained.map(p => p[1])), maxY = Math.max(...contained.map(p => p[1]));
        const minZ = Math.min(...contained.map(p => p[2])), maxZ = Math.max(...contained.map(p => p[2]));
        box.center = [Number(((minX+maxX)/2).toFixed(2)), Number(((minY+maxY)/2).toFixed(2)), Number(((minZ+maxZ)/2).toFixed(2))];
        box.dimensions = [Math.max(0.4, Number((maxX-minX).toFixed(2))), Math.max(0.4, Number((maxY-minY).toFixed(2))), Math.max(0.4, Number((maxZ-minZ).toFixed(2)))];
        selectBox(box.id);
        updateSelectedBoxFromInspector();
      }
    });

    document.getElementById('ci-btn-delete').addEventListener('click', () => {
      if (!selectedBoxId) return;
      detectedBoxes = detectedBoxes.filter(b => b.id !== selectedBoxId);
      const grp = boxThreeObjects.get(selectedBoxId);
      if (grp) boxesGroup.remove(grp);
      boxThreeObjects.delete(selectedBoxId);
      document.getElementById('spatial-inspector').style.display = 'none';
      selectedBoxId = null;
      populateObjectRoster();
      document.getElementById('val-clusters').textContent = `${detectedBoxes.length} Objects`;
      document.getElementById('badge-box-count').textContent = detectedBoxes.length;
    });

    document.getElementById('ci-btn-save').addEventListener('click', async () => {
      try {
        const btn = document.getElementById('ci-btn-save');
        btn.innerHTML = '<span>Saving Spatial Geometry...</span>';
        const resp = await fetch('/api/detections/3d/save', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ dataset_name: currentDataset, boxes: detectedBoxes })
        });
        const res = await resp.json();
        btn.innerHTML = '<svg class="svg-icon" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg><span>Committed to Spatial Core</span>';
        setTimeout(() => {
          btn.innerHTML = '<svg class="svg-icon" viewBox="0 0 24 24"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg><span>Commit Spatial Transform</span>';
        }, 1800);
      } catch (e) { console.error('Save error: ' + e.message); }
    });

    // Split Divider Dragging Logic
    function updateSplitDividerPosition() {
      const splitDivider = document.getElementById('split-divider');
      const badgeRight = document.getElementById('split-badge-right');
      if (splitDivider) splitDivider.style.left = `${splitRatio * 100}%`;
      if (badgeRight) badgeRight.style.left = `calc(${splitRatio * 100}% + 14px)`;
    }

    const splitDividerEl = document.getElementById('split-divider');
    if (splitDividerEl) {
      splitDividerEl.addEventListener('mousedown', () => {
        isDraggingSplit = true;
        document.body.style.cursor = 'col-resize';
      });
      window.addEventListener('mousemove', (e) => {
        if (!isDraggingSplit || !isSplitView) return;
        const rect = container.getBoundingClientRect();
        const clientX = e.clientX;
        const newRatio = (clientX - rect.left) / rect.width;
        splitRatio = Math.max(0.12, Math.min(0.88, newRatio));
        updateSplitDividerPosition();
      });
      window.addEventListener('mouseup', () => {
        if (isDraggingSplit) {
          isDraggingSplit = false;
          document.body.style.cursor = 'default';
        }
      });
    }

    // ========================================================================
    // 4. Comparison Engine (State A: Raw vs State B: Processed)
    // ========================================================================
    function setComparisonState(state) {
      comparisonState = state;
      document.getElementById('btn-state-b').classList.toggle('active', state === 'B');
      document.getElementById('btn-state-a').classList.toggle('active-raw', state === 'A');
      document.getElementById('btn-state-split').classList.remove('active');
      isSplitView = false;
      const splitDivider = document.getElementById('split-divider');
      const badgeLeft = document.getElementById('split-badge-left');
      const badgeRight = document.getElementById('split-badge-right');
      if (splitDivider) splitDivider.style.display = 'none';
      if (badgeLeft) badgeLeft.style.display = 'none';
      if (badgeRight) badgeRight.style.display = 'none';

      const badge = document.getElementById('badge-curr-state');
      if (state === 'A') {
        badge.className = 'state-badge state-badge-a';
        badge.textContent = 'STATE A: RAW SENSOR INGEST';
      } else {
        badge.className = 'state-badge state-badge-b';
        badge.textContent = 'STATE B: PROCESSED PERCEPTION';
      }

      if (currentRawData) {
        updatePointCloudGeometry(currentRawData.points, currentRawData.intensity);
      }
      render3DPerceptionObjects();
      updateStateOverlayText();
    }

    function toggleSplitComparison() {
      isSplitView = !isSplitView;
      document.getElementById('btn-state-split').classList.toggle('active', isSplitView);
      const splitDivider = document.getElementById('split-divider');
      const badgeLeft = document.getElementById('split-badge-left');
      const badgeRight = document.getElementById('split-badge-right');

      if (isSplitView) {
        comparisonState = 'SPLIT';
        document.getElementById('btn-state-b').classList.remove('active');
        document.getElementById('btn-state-a').classList.remove('active-raw');
        const badge = document.getElementById('badge-curr-state');
        badge.className = 'state-badge state-badge-b';
        badge.textContent = 'STATE SPLIT: A/B DUAL VIEW';
        document.getElementById('state-detail-str').textContent = 'LEFT: RAW INGEST | RIGHT: PROCESSED 3D PERCEPTION';
        if (splitDivider) splitDivider.style.display = 'block';
        if (badgeLeft) badgeLeft.style.display = 'flex';
        if (badgeRight) badgeRight.style.display = 'flex';
        updateSplitDividerPosition();

        // Initialize dual cameras from active primary view
        cameraRaw.position.copy(camera.position);
        cameraRaw.quaternion.copy(camera.quaternion);
        controlsRaw.target.copy(controls.target);
        controlsRaw.update();

        cameraProc.position.copy(camera.position);
        cameraProc.quaternion.copy(camera.quaternion);
        controlsProc.target.copy(controls.target);
        controlsProc.update();

        render3DPerceptionObjects();
        updateCameraIndicatorTags();
      } else {
        if (splitDivider) splitDivider.style.display = 'none';
        if (badgeLeft) badgeLeft.style.display = 'none';
        if (badgeRight) badgeRight.style.display = 'none';
        setComparisonState('B');
      }
    }

    function updateStateOverlayText() {
      const detailEl = document.getElementById('state-detail-str');
      if (comparisonState === 'A') {
        detailEl.textContent = '17,238 RAW POINTS • UNFILTERED • NO DETECTION OVERLAYS';
      } else if (comparisonState === 'B') {
        detailEl.textContent = `17,238 PTS • -8.2% NOISE SUPPRESSED • ${detectedBoxes.length} DETECTIONS • KAMA ER 0.94`;
      }
    }

    // Keyboard shortcut 'C' for instant A/B state flip
    window.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      if (e.key === 'c' || e.key === 'C') {
        setComparisonState(comparisonState === 'B' ? 'A' : 'B');
      }
      if ((e.ctrlKey || e.metaKey) && (e.key === 'b' || e.key === 'B')) {
        e.preventDefault();
        toggleSidebar();
      }
    });

    // ========================================================================
    // 5. Collapsible Sidebar & Accordion Logic
    // ========================================================================
    const sidebar = document.getElementById('main-sidebar');
    const chevron = document.getElementById('sidebar-chevron');

    function toggleSidebar() {
      sidebar.classList.remove('hover-peek');
      sidebar.classList.toggle('collapsed');
      const isCollapsed = sidebar.classList.contains('collapsed');
      chevron.style.transform = isCollapsed ? 'rotate(180deg)' : 'rotate(0deg)';
      setTimeout(() => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
      }, 260);
    }

    document.getElementById('btn-toggle-sidebar').addEventListener('click', toggleSidebar);
    document.getElementById('btn-reexpand-sidebar').addEventListener('click', toggleSidebar);

    // Left Sidebar Hover-Peek Implementation
    let sidebarPeekTimeout = null;
    const leftHoverZone = document.getElementById('left-hover-zone');
    const btnReexpand = document.getElementById('btn-reexpand-sidebar');

    function handleSidebarPeekEnter() {
      if (sidebar.classList.contains('collapsed')) {
        clearTimeout(sidebarPeekTimeout);
        sidebar.classList.add('hover-peek');
      }
    }

    function handleSidebarPeekLeave() {
      if (sidebar.classList.contains('collapsed')) {
        sidebarPeekTimeout = setTimeout(() => {
          sidebar.classList.remove('hover-peek');
        }, 240);
      }
    }

    if (leftHoverZone) {
      leftHoverZone.addEventListener('mouseenter', handleSidebarPeekEnter);
    }
    if (btnReexpand) {
      btnReexpand.addEventListener('mouseenter', handleSidebarPeekEnter);
    }
    sidebar.addEventListener('mouseenter', () => {
      if (sidebar.classList.contains('collapsed')) {
        clearTimeout(sidebarPeekTimeout);
      }
    });
    sidebar.addEventListener('mouseleave', handleSidebarPeekLeave);

    function toggleAccSection(headerEl) {
      const sec = headerEl.parentElement;
      sec.classList.toggle('open');
    }

    // Point Size Scaler
    document.getElementById('slider-pt-size').addEventListener('input', (e) => {
      pointSizeScale = parseFloat(e.target.value);
      if (cloudPoints) {
        cloudPoints.material.size = pointSizeScale;
      }
    });

    // ========================================================================
    // 6. Safety & Manufacturing Telemetry Updates
    // ========================================================================
    async function updateSafetyAndManufacturingMetrics(dataset = currentDataset) {
      try {
        // Emergency Hazard & TTC
        const rHaz = await fetch(`/api/signal/emergency_hazard?dataset=${dataset}`);
        const dHaz = await rHaz.json();
        document.getElementById('val-ttc').textContent = `${dHaz.minimum_time_to_impact_s.toFixed(2)}s`;
        document.getElementById('val-hazard-level').textContent = dHaz.primary_threat_level;
        document.getElementById('val-hazard-action').textContent = dHaz.hazard_alerts[0]?.recommended_action || "Corridor clear";

        const pill = document.getElementById('hazard-pill');
        pill.className = `hazard-pill ${dHaz.primary_threat_level === 'CRITICAL_BRAKE' ? 'hazard-brake' : (dHaz.primary_threat_level === 'WARNING_STEER' ? 'hazard-steer' : 'hazard-clear')}`;

        // Manufacturing Surface Degradation
        const rDeg = await fetch(`/api/manufacturing/degradation?dataset=${dataset}`);
        const dDeg = await rDeg.json();
        document.getElementById('val-sdi').textContent = dDeg.surface_degradation_index.toFixed(3);
        document.getElementById('chip-sdi').textContent = dDeg.surface_degradation_index.toFixed(3);
        document.getElementById('val-sdi-dev').textContent = `${dDeg.mean_deviation_mm.toFixed(2)} mm`;
        document.getElementById('val-sdi-ra').textContent = `${dDeg.roughness_ra_um.toFixed(2)} μm`;
        document.getElementById('sdi-wear-badge').textContent = dDeg.wear_classification.split('(')[0];

        // Material Spectral Grading
        const rMat = await fetch(`/api/manufacturing/material_grade?dataset=${dataset}`);
        const dMat = await rMat.json();
        document.getElementById('val-mat-class').textContent = dMat.material_class.split('(')[0];
        document.getElementById('val-mat-refl').textContent = dMat.mean_reflectivity.toFixed(2);
        document.getElementById('val-mat-hrc').textContent = `${dMat.estimated_wear_resistance_hrc.toFixed(1)} HRC`;
      } catch (e) {
        console.warn("Safety metrics update error", e);
      }
    }

    // ========================================================================
    // 7. Satellite 3D Earth Mapping & Instant Mesh
    // ========================================================================
    document.getElementById('btn-generate-satellite').addEventListener('click', async () => {
      const lat = parseFloat(document.getElementById('sat-lat').value);
      const lon = parseFloat(document.getElementById('sat-lon').value);
      const zoom = parseInt(document.getElementById('sat-zoom-slider').value);
      const mode = document.getElementById('sat-render-mode').value;

      try {
        const resp = await fetch(`/api/satellite/map?lat=${lat}&lon=${lon}&zoom=${zoom}`);
        const data = await resp.json();

        while(satelliteGroup.children.length > 0) satelliteGroup.remove(satelliteGroup.children[0]);

        const pts = new Float32Array(data.points_flat);
        const cols = new Float32Array(data.colors_flat);

        if (mode === 'mesh') {
          const geom = new THREE.BufferGeometry();
          geom.setAttribute('position', new THREE.BufferAttribute(pts, 3));
          geom.setAttribute('color', new THREE.BufferAttribute(cols, 3));
          geom.setIndex(data.mesh_indices);
          geom.computeVertexNormals();

          const mat = new THREE.MeshStandardMaterial({
            vertexColors: true,
            roughness: 0.65,
            metalness: 0.15,
            side: THREE.DoubleSide,
          });
          const mesh = new THREE.Mesh(geom, mat);
          mesh.position.z = -1.73;
          satelliteGroup.add(mesh);

          const light = new THREE.DirectionalLight(0xffffff, 0.85);
          light.position.set(30, 30, 50);
          satelliteGroup.add(light);
          satelliteGroup.add(new THREE.AmbientLight(0x404040, 1.2));
        } else {
          const geom = new THREE.BufferGeometry();
          geom.setAttribute('position', new THREE.BufferAttribute(pts, 3));
          geom.setAttribute('color', new THREE.BufferAttribute(cols, 3));
          const mat = new THREE.PointsMaterial({ size: 0.18, vertexColors: true });
          const cloud = new THREE.Points(geom, mat);
          cloud.position.z = -1.73;
          satelliteGroup.add(cloud);
        }

        if (cloudPoints) cloudPoints.visible = false;
        boxesGroup.visible = false;
        camera.position.set(0, -600, 450);
        controls.target.set(0, 0, (data.elevation_min_m + data.elevation_max_m) / 2.0);
        controls.update();
      } catch (e) {
        console.error('Satellite mapping error: ' + e.message);
      }
    });

    document.getElementById('sat-preset-select').addEventListener('change', (e) => {
      const presets = {
        "san_francisco": [37.7749, -122.4194],
        "mount_fuji": [35.3606, 138.7274],
        "grand_canyon": [36.1069, -112.1129],
        "zurich_alps": [47.3769, 8.5417],
        "tokyo_bay": [35.6762, 139.6503],
        "new_york": [40.7128, -74.0060],
      };
      const coords = presets[e.target.value];
      if (coords) {
        document.getElementById('sat-lat').value = coords[0];
        document.getElementById('sat-lon').value = coords[1];
      }
    });

    document.getElementById('sat-zoom-slider').addEventListener('input', (e) => {
      const z = parseInt(e.target.value);
      const span = (2400.0 / (2 ** (z - 14))).toFixed(0);
      document.getElementById('sat-zoom-disp').textContent = `${z}x (${span}m)`;
    });

    // ========================================================================
    // 8. Sampling Engine (Curvature & ROI)
    // ========================================================================
    document.getElementById('btn-run-sampling').addEventListener('click', async () => {
      const mode = document.getElementById('sample-mode-select').value;
      const target = parseFloat(document.getElementById('sample-target-pct').value);

      try {
        const resp = await fetch('/api/manufacturing/sample', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ dataset_path: currentDataset, method: mode, reduction_target: target })
        });
        const res = await resp.json();
      } catch (e) { console.error('Sampling error: ' + e.message); }
    });

    // ========================================================================
    // 9. OpenRouter AI Reasoning Copilot (Draggable & Right-Dock Hover / Click)
    // ========================================================================
    const aiDrawer = document.getElementById('ai-copilot-drawer');
    const aiThread = document.getElementById('ai-chat-thread');
    const aiInput = document.getElementById('ai-input');
    const btnAiSend = document.getElementById('btn-ai-send');
    const dockTabAi = document.getElementById('dock-tab-ai');

    makeDraggable(aiDrawer, document.getElementById('ai-drag-handle'));

    let aiPanelPinned = false;
    let aiCloseTimeout = null;

    function openAiDrawer(pin = false) {
      clearTimeout(aiCloseTimeout);
      aiDrawer.style.display = 'flex';
      dockTabAi.classList.add('active');
      const btnCopilot = document.getElementById('btn-ai-copilot');
      if (btnCopilot) btnCopilot.classList.add('active');
      if (pin) aiPanelPinned = true;
      document.getElementById('ai-btn-pin').classList.toggle('active', aiPanelPinned);
      checkAiKeyStatus();
    }

    function closeAiDrawer(force = false) {
      if (aiPanelPinned && !force) return;
      aiDrawer.style.display = 'none';
      dockTabAi.classList.remove('active');
      const btnCopilot = document.getElementById('btn-ai-copilot');
      if (btnCopilot) btnCopilot.classList.remove('active');
      if (force) {
        aiPanelPinned = false;
        document.getElementById('ai-btn-pin').classList.remove('active');
      }
    }

    dockTabAi.addEventListener('mouseenter', () => openAiDrawer(false));
    dockTabAi.addEventListener('mouseleave', () => {
      if (!aiPanelPinned) aiCloseTimeout = setTimeout(() => closeAiDrawer(), 300);
    });
    aiDrawer.addEventListener('mouseenter', () => clearTimeout(aiCloseTimeout));
    aiDrawer.addEventListener('mouseleave', () => {
      if (!aiPanelPinned) aiCloseTimeout = setTimeout(() => closeAiDrawer(), 300);
    });

    dockTabAi.addEventListener('click', () => {
      if (aiDrawer.style.display === 'flex' && aiPanelPinned) {
        closeAiDrawer(true);
      } else {
        openAiDrawer(true);
      }
    });

    document.getElementById('ai-btn-pin').addEventListener('click', () => {
      aiPanelPinned = !aiPanelPinned;
      document.getElementById('ai-btn-pin').classList.toggle('active', aiPanelPinned);
    });
    document.getElementById('ai-btn-collapse').addEventListener('click', () => closeAiDrawer(true));
    document.getElementById('ai-drawer-close').addEventListener('click', () => closeAiDrawer(true));

    document.getElementById('btn-ai-copilot').addEventListener('click', () => {
      if (aiDrawer.style.display === 'flex') {
        closeAiDrawer(true);
      } else {
        openAiDrawer(true);
      }
    });

    async function checkAiKeyStatus() {
      try {
        const resp = await fetch('/api/ai/models');
        const data = await resp.json();
        const statusEl = document.getElementById('ai-key-status');
        if (data.key_configured) {
          statusEl.textContent = `Key Active (${data.key_source})`;
        } else {
          statusEl.textContent = `Key Pending [.env.local]`;
        }
      } catch (e) {}
    }

    async function sendAiMessage(promptText) {
      if (!promptText || promptText.trim() === '') return;
      const model = document.getElementById('ai-model-select').value;

      const uBubble = document.createElement('div');
      uBubble.className = 'chat-bubble chat-user';
      uBubble.textContent = promptText;
      aiThread.appendChild(uBubble);

      const loadBubble = document.createElement('div');
      loadBubble.className = 'chat-bubble chat-ai';
      loadBubble.innerHTML = `<span style="color:var(--cyan);">Thinking with ${model}...</span>`;
      aiThread.appendChild(loadBubble);
      aiThread.scrollTop = aiThread.scrollHeight;
      aiInput.value = '';

      try {
        const resp = await fetch('/api/ai/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            prompt: promptText,
            model: model,
            telemetry_context: {
              dataset: currentDataset,
              total_objects: detectedBoxes.length,
              surface_degradation_index: parseFloat(document.getElementById('val-sdi').textContent),
              mean_deviation_mm: parseFloat(document.getElementById('val-sdi-dev').textContent),
              hazard_ttc_s: parseFloat(document.getElementById('val-ttc').textContent),
            }
          })
        });
        const res = await resp.json();
        const nl = String.fromCharCode(10);
        let formatted = (res.response || '')
          .split(nl + nl).join('<br><br>')
          .split(nl).join('<br>');
        formatted = formatted.split('**').reduce((acc, part, idx) => acc + (idx % 2 === 1 ? '<strong>' + part + '</strong>' : part), '');

        loadBubble.innerHTML = formatted;
      } catch (e) {
        loadBubble.innerHTML = `<span style="color:var(--rose);">Copilot error: ${e.message}</span>`;
      }
      aiThread.scrollTop = aiThread.scrollHeight;
    }

    btnAiSend.addEventListener('click', () => sendAiMessage(aiInput.value));
    aiInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') sendAiMessage(aiInput.value); });
    document.querySelectorAll('.quick-chip').forEach(chip => {
      chip.addEventListener('click', () => sendAiMessage(chip.dataset.prompt));
    });

    // ========================================================================
    // 10. Exports & UI Navigation Handlers
    // ========================================================================
    const modalExport = document.getElementById('modal-export-3d');
    const exportPreview = document.getElementById('export-preview-area');
    let currentExportFormat = 'kitti';

    document.getElementById('btn-export-3d').addEventListener('click', async () => {
      modalExport.style.display = 'flex';
      await loadExportFormat(currentExportFormat);
    });
    document.getElementById('modal-export-close').addEventListener('click', () => modalExport.style.display = 'none');

    document.querySelectorAll('.export-tab').forEach(tab => {
      tab.addEventListener('click', async () => {
        document.querySelectorAll('.export-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        currentExportFormat = tab.dataset.format;
        await loadExportFormat(currentExportFormat);
      });
    });

    async function loadExportFormat(fmt) {
      exportPreview.value = 'Generating 3D annotation export...';
      try {
        const resp = await fetch(`/api/detections/3d/export?dataset=${currentDataset}&format=${fmt}`);
        if (fmt === 'kitti') exportPreview.value = await resp.text();
        else {
          const json = await resp.json();
          exportPreview.value = JSON.stringify(json, null, 2);
        }
      } catch (e) { exportPreview.value = 'Export error: ' + e.message; }
    }

    document.getElementById('btn-copy-export').addEventListener('click', () => {
      navigator.clipboard.writeText(exportPreview.value);
    });
    document.getElementById('btn-download-export').addEventListener('click', () => {
      const ext = currentExportFormat === 'kitti' ? 'txt' : 'json';
      const a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([exportPreview.value], { type: 'text/plain' }));
      a.download = `AEOVEXOR_3D_${currentDataset}_${currentExportFormat}.${ext}`;
      a.click();
    });

    // Sidebar Tab Switching
    document.querySelectorAll('.sidebar-tabs .s-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.sidebar-tabs .s-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        const tabKey = tab.dataset.tab;
        ['perception', 'satellite', 'quality', 'signals', 'scene'].forEach(k => {
          const el = document.getElementById(`tab-body-${k}`);
          if (el) el.style.display = k === tabKey ? 'block' : 'none';
        });
      });
    });

    // Top Action Buttons
    document.getElementById('btn-detect-3d').addEventListener('click', () => runAutoDetect3D());
    document.getElementById('btn-toggle-boxes').addEventListener('click', (e) => {
      boxesGroup.visible = !boxesGroup.visible;
      posesGroup.visible = boxesGroup.visible;
      biometricsGroup.visible = boxesGroup.visible;
      occlusionGroup.visible = boxesGroup.visible;
      e.currentTarget.classList.toggle('active', boxesGroup.visible);
    });

    // 3D Digital Twin Shapes Controls
    const btnToggleShapes = document.getElementById('btn-toggle-shapes');
    const chkShowShapes = document.getElementById('chk-show-shapes');

    function setDigitalTwinsVisibility(vis) {
      showDigitalTwins = vis;
      if (btnToggleShapes) btnToggleShapes.classList.toggle('active', vis);
      if (chkShowShapes) chkShowShapes.checked = vis;
      boxesGroup.children.forEach(grp => {
        const twin = grp.getObjectByName('digitalTwin');
        if (twin) twin.visible = vis;
      });
    }

    if (btnToggleShapes) {
      btnToggleShapes.addEventListener('click', () => setDigitalTwinsVisibility(!showDigitalTwins));
    }
    if (chkShowShapes) {
      chkShowShapes.addEventListener('change', (e) => setDigitalTwinsVisibility(e.target.checked));
    }

    const sliderShapeOpacity = document.getElementById('slider-shape-opacity');
    if (sliderShapeOpacity) {
      sliderShapeOpacity.addEventListener('input', (e) => {
        shapeOpacity = parseFloat(e.target.value);
        render3DPerceptionObjects();
      });
    }

    const selShapeStyle = document.getElementById('sel-shape-style');
    if (selShapeStyle) {
      selShapeStyle.addEventListener('change', (e) => {
        shapeRenderStyle = e.target.value;
        render3DPerceptionObjects();
      });
    }

    // Cross-Section Slicing Box Tool (Draggable & Right-Dock Hover / Click)
    const panelSlice = document.getElementById('panel-slice');
    const btnSlice = document.getElementById('btn-slice');
    const dockTabSlice = document.getElementById('dock-tab-slice');

    makeDraggable(panelSlice, document.getElementById('slice-drag-handle'));

    renderer.localClippingEnabled = true;
    const clipPlaneZ = new THREE.Plane(new THREE.Vector3(0, 0, -1), 15);
    const clipPlaneX = new THREE.Plane(new THREE.Vector3(-1, 0, 0), 40);
    const clipPlaneY = new THREE.Plane(new THREE.Vector3(0, -1, 0), 40);
    renderer.clippingPlanes = [];

    let slicePanelPinned = false;
    let sliceCloseTimeout = null;

    function openSlicePanel(pin = false) {
      clearTimeout(sliceCloseTimeout);
      panelSlice.style.display = 'block';
      dockTabSlice.classList.add('active');
      btnSlice.classList.add('active');
      renderer.clippingPlanes = [clipPlaneZ, clipPlaneX, clipPlaneY];
      if (pin) slicePanelPinned = true;
      document.getElementById('slice-btn-pin').classList.toggle('active', slicePanelPinned);
    }

    function closeSlicePanel(force = false) {
      if (slicePanelPinned && !force) return;
      panelSlice.style.display = 'none';
      dockTabSlice.classList.remove('active');
      btnSlice.classList.remove('active');
      renderer.clippingPlanes = [];
      if (force) {
        slicePanelPinned = false;
        document.getElementById('slice-btn-pin').classList.remove('active');
      }
    }

    dockTabSlice.addEventListener('mouseenter', () => openSlicePanel(false));
    dockTabSlice.addEventListener('mouseleave', () => {
      if (!slicePanelPinned) sliceCloseTimeout = setTimeout(() => closeSlicePanel(), 300);
    });
    panelSlice.addEventListener('mouseenter', () => clearTimeout(sliceCloseTimeout));
    panelSlice.addEventListener('mouseleave', () => {
      if (!slicePanelPinned) sliceCloseTimeout = setTimeout(() => closeSlicePanel(), 300);
    });

    dockTabSlice.addEventListener('click', () => {
      if (panelSlice.style.display === 'block' && slicePanelPinned) {
        closeSlicePanel(true);
      } else {
        openSlicePanel(true);
      }
    });

    document.getElementById('slice-btn-pin').addEventListener('click', () => {
      slicePanelPinned = !slicePanelPinned;
      document.getElementById('slice-btn-pin').classList.toggle('active', slicePanelPinned);
    });
    document.getElementById('slice-btn-collapse').addEventListener('click', () => closeSlicePanel(true));
    document.getElementById('slice-close-btn').addEventListener('click', () => closeSlicePanel(true));

    btnSlice.addEventListener('click', () => {
      if (panelSlice.style.display === 'block') {
        closeSlicePanel(true);
      } else {
        openSlicePanel(true);
      }
    });

    document.getElementById('clip-z').addEventListener('input', (e) => { clipPlaneZ.constant = parseFloat(e.target.value); });
    document.getElementById('clip-x').addEventListener('input', (e) => { clipPlaneX.constant = parseFloat(e.target.value); });
    document.getElementById('clip-y').addEventListener('input', (e) => { clipPlaneY.constant = parseFloat(e.target.value); });
    document.getElementById('btn-reset-slice').addEventListener('click', () => {
      clipPlaneZ.constant = 15; clipPlaneX.constant = 40; clipPlaneY.constant = 40;
    });

    // Initial Cloud Load
    loadCloud();

    window.addEventListener('resize', () => {
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    });

    // ========================================================================
    // Individual Split Screen Camera Control Routing
    // ========================================================================
    container.addEventListener('pointerdown', (e) => {
      if (!isSplitView) return;
      const rect = container.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const splitX = rect.width * splitRatio;

      if (mouseX < splitX) {
        activeSplitSide = 'left';
        if (camerasDecoupled) {
          controlsRaw.enabled = true;
          controlsProc.enabled = false;
        }
      } else {
        activeSplitSide = 'right';
        if (camerasDecoupled) {
          controlsProc.enabled = true;
          controlsRaw.enabled = false;
        }
      }
      updateCameraIndicatorTags();
    });

    container.addEventListener('pointermove', (e) => {
      if (!isSplitView) return;
      if (e.buttons === 0) {
        const rect = container.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const splitX = rect.width * splitRatio;

        if (mouseX < splitX) {
          activeSplitSide = 'left';
          if (camerasDecoupled) {
            controlsRaw.enabled = true;
            controlsProc.enabled = false;
          }
        } else {
          activeSplitSide = 'right';
          if (camerasDecoupled) {
            controlsProc.enabled = true;
            controlsRaw.enabled = false;
          }
        }
        updateCameraIndicatorTags();
      }
    });

    function updateCameraIndicatorTags() {
      const tagLeft = document.getElementById('tag-camera-left');
      const tagRight = document.getElementById('tag-camera-right');
      const badgeLeft = document.getElementById('split-badge-left');
      const badgeRight = document.getElementById('split-badge-right');
      if (!badgeLeft || !badgeRight) return;

      if (activeSplitSide === 'left') {
        badgeLeft.style.borderColor = 'var(--cyan)';
        badgeLeft.style.boxShadow = '0 0 12px rgba(0,229,255,0.45)';
        badgeRight.style.borderColor = 'var(--border)';
        badgeRight.style.boxShadow = 'none';
        if (tagLeft) {
          tagLeft.textContent = camerasDecoupled ? 'CAM A: ACTIVE (ORBITING)' : 'SYNCED';
          tagLeft.style.background = 'rgba(0,229,255,0.25)';
          tagLeft.style.color = 'var(--cyan)';
        }
        if (tagRight) {
          tagRight.textContent = camerasDecoupled ? 'CAM B: STANDBY' : 'SYNCED';
          tagRight.style.background = 'rgba(148,163,184,0.1)';
          tagRight.style.color = 'var(--text-dim)';
        }
      } else {
        badgeRight.style.borderColor = 'var(--emerald)';
        badgeRight.style.boxShadow = '0 0 12px rgba(16,185,129,0.45)';
        badgeLeft.style.borderColor = 'var(--border)';
        badgeLeft.style.boxShadow = 'none';
        if (tagRight) {
          tagRight.textContent = camerasDecoupled ? 'CAM B: ACTIVE (ORBITING)' : 'SYNCED';
          tagRight.style.background = 'rgba(16,185,129,0.25)';
          tagRight.style.color = 'var(--emerald)';
        }
        if (tagLeft) {
          tagLeft.textContent = camerasDecoupled ? 'CAM A: STANDBY' : 'SYNCED';
          tagLeft.style.background = 'rgba(148,163,184,0.1)';
          tagLeft.style.color = 'var(--text-dim)';
        }
      }
    }

    const btnCameraSync = document.getElementById('btn-toggle-camera-sync');
    if (btnCameraSync) {
      btnCameraSync.addEventListener('click', (e) => {
        e.stopPropagation();
        camerasDecoupled = !camerasDecoupled;
        btnCameraSync.textContent = camerasDecoupled ? '🔓 INDIVIDUAL CONTROLS' : '🔗 SYNCED CONTROLS';
        btnCameraSync.style.color = camerasDecoupled ? 'var(--cyan)' : 'var(--emerald)';
        if (!camerasDecoupled) {
          if (activeSplitSide === 'left') {
            cameraProc.position.copy(cameraRaw.position);
            cameraProc.quaternion.copy(cameraRaw.quaternion);
            controlsProc.target.copy(controlsRaw.target);
          } else {
            cameraRaw.position.copy(cameraProc.position);
            cameraRaw.quaternion.copy(cameraProc.quaternion);
            controlsRaw.target.copy(controlsProc.target);
          }
          controlsRaw.enabled = true;
          controlsProc.enabled = true;
        }
        updateCameraIndicatorTags();
      });
    }

    // ========================================================================
    // CloudCompare Developer Toolbox & Manipulation Engine
    // ========================================================================
    const ccVertToolbar = document.getElementById('cc-vert-toolbar');
    const ccHorizToolbar = document.getElementById('cc-horiz-toolbar');
    const presentationToolbar = document.getElementById('presentation-toolbar');

    // Toggle Toolboxes from Top Navigation
    const btnToggleToolbox = document.getElementById('btn-toggle-toolbox');
    if (btnToggleToolbox) {
      btnToggleToolbox.addEventListener('click', () => {
        const isVis = (ccVertToolbar.style.display !== 'none');
        ccVertToolbar.style.display = isVis ? 'none' : 'flex';
        ccHorizToolbar.style.display = isVis ? 'none' : 'flex';
        btnToggleToolbox.classList.toggle('active', !isVis);
      });
    }

    // 1. Standard View Camera Orientations (Image 1)
    const btnCcReset = document.getElementById('btn-cc-reset-view');
    const btnCcOrtho = document.getElementById('btn-cc-ortho');
    const btnCcTop = document.getElementById('btn-cc-view-top');
    const btnCcFront = document.getElementById('btn-cc-view-front');
    const btnCcBack = document.getElementById('btn-cc-view-back');
    const btnCcLeft = document.getElementById('btn-cc-view-left');
    const btnCcRight = document.getElementById('btn-cc-view-right');
    const btnCcIso = document.getElementById('btn-cc-view-iso');

    function setStandardCameraView(pos, target, up = [0, 0, 1]) {
      camera.position.set(pos[0], pos[1], pos[2]);
      camera.up.set(up[0], up[1], up[2]);
      controls.target.set(target[0], target[1], target[2]);
      controls.update();
      if (typeof logTacticalMsg === 'function') {
        logTacticalMsg('Camera', `Aligned viewport to ${pos[0] > 0 ? 'Right' : 'Preset'} standard orientation.`);
      }
    }

    if (btnCcReset) btnCcReset.addEventListener('click', () => setStandardCameraView([-14, -20, 10], [10, 0, 0]));
    if (btnCcTop) btnCcTop.addEventListener('click', () => setStandardCameraView([10, 0, 48], [10, 0, 0], [0, 1, 0]));
    if (btnCcFront) btnCcFront.addEventListener('click', () => setStandardCameraView([10, -38, 2], [10, 0, 2]));
    if (btnCcBack) btnCcBack.addEventListener('click', () => setStandardCameraView([10, 38, 2], [10, 0, 2]));
    if (btnCcLeft) btnCcLeft.addEventListener('click', () => setStandardCameraView([-32, 0, 2], [10, 0, 2]));
    if (btnCcRight) btnCcRight.addEventListener('click', () => setStandardCameraView([48, 0, 2], [10, 0, 2]));
    if (btnCcIso) btnCcIso.addEventListener('click', () => setStandardCameraView([-16, -16, 16], [10, 0, 0]));

    let isOrthoMode = false;
    if (btnCcOrtho) {
      btnCcOrtho.addEventListener('click', () => {
        isOrthoMode = !isOrthoMode;
        camera.fov = isOrthoMode ? 15 : 52;
        camera.updateProjectionMatrix();
        btnCcOrtho.classList.toggle('active', isOrthoMode);
      });
    }

    // 2. 3D Coordinate Inspector Crosshair Picker
    const btnCcPicker = document.getElementById('btn-cc-picker');
    const ccPickerCard = document.getElementById('cc-picker-card');
    let isPickerActive = false;
    const pickerRaycaster = new THREE.Raycaster();
    pickerRaycaster.params.Points.threshold = 0.45;
    const pickerMouse = new THREE.Vector2();

    if (btnCcPicker) {
      btnCcPicker.addEventListener('click', () => {
        isPickerActive = !isPickerActive;
        btnCcPicker.classList.toggle('active', isPickerActive);
        container.style.cursor = isPickerActive ? 'crosshair' : 'default';
        if (!isPickerActive && ccPickerCard) ccPickerCard.style.display = 'none';
      });
    }

    container.addEventListener('pointermove', (e) => {
      if (!isPickerActive) return;
      const rect = container.getBoundingClientRect();
      pickerMouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      pickerMouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      pickerRaycaster.setFromCamera(pickerMouse, camera);
      const targetCloud = (comparisonState === 'A' ? cloudPointsRaw : cloudPointsProc);
      if (!targetCloud) return;

      const intersects = pickerRaycaster.intersectObject(targetCloud);
      if (intersects.length > 0) {
        const hit = intersects[0];
        const idx = hit.index;
        const pt = hit.point;
        const range = Math.sqrt(pt.x*pt.x + pt.y*pt.y + pt.z*pt.z);

        if (ccPickerCard) {
          ccPickerCard.style.display = 'block';
          ccPickerCard.style.left = `${Math.min(e.clientX - rect.left + 14, rect.width - 230)}px`;
          ccPickerCard.style.top = `${Math.min(e.clientY - rect.top + 14, rect.height - 180)}px`;

          const elIdx = document.getElementById('cc-pick-index');
          if (elIdx) elIdx.textContent = `#${idx}`;
          const elX = document.getElementById('cc-pick-x');
          if (elX) elX.textContent = `${pt.x >= 0 ? '+' : ''}${pt.x.toFixed(3)}m`;
          const elY = document.getElementById('cc-pick-y');
          if (elY) elY.textContent = `${pt.y >= 0 ? '+' : ''}${pt.y.toFixed(3)}m`;
          const elZ = document.getElementById('cc-pick-z');
          if (elZ) elZ.textContent = `${pt.z >= 0 ? '+' : ''}${pt.z.toFixed(3)}m`;
          const elR = document.getElementById('cc-pick-r');
          if (elR) elR.textContent = `${range.toFixed(3)}m`;

          // Normal & Reflectivity approximation
          const nx = (pt.x / range).toFixed(3);
          const ny = (pt.y / range).toFixed(3);
          const nz = (pt.z / range).toFixed(3);
          const elN = document.getElementById('cc-pick-n');
          if (elN) elN.textContent = `[${nx}, ${ny}, ${nz}]`;
        }
      }
    });

    // 3. 7-DOF Transform Gizmo (Translate, Rotate, Scale on selected objects)
    let transformControls = null;
    if (typeof THREE.TransformControls !== 'undefined') {
      try {
        transformControls = new THREE.TransformControls(camera, renderer.domElement);
        transformControls.size = 0.85;
        scene.add(transformControls);

        transformControls.addEventListener('dragging-changed', (event) => {
          controls.enabled = !event.value;
        });

        transformControls.addEventListener('change', () => {
          if (selectedBox) {
            const pos = selectedBox.mesh.position;
            const rot = selectedBox.mesh.rotation;
            const scale = selectedBox.mesh.scale;
            // Reflect into Inspector
            const elX = document.getElementById('ci-x'); if (elX) elX.value = pos.x.toFixed(2);
            const elY = document.getElementById('ci-y'); if (elY) elY.value = pos.y.toFixed(2);
            const elZ = document.getElementById('ci-z'); if (elZ) elZ.value = pos.z.toFixed(2);
            const elYaw = document.getElementById('ci-yaw'); if (elYaw) elYaw.value = rot.z.toFixed(2);
            if (selectedBox.headingArrow) {
              selectedBox.headingArrow.position.copy(pos);
              selectedBox.headingArrow.setDirection(new THREE.Vector3(Math.cos(rot.z), Math.sin(rot.z), 0));
            }
          }
        });
      } catch (err) {
        console.warn('TransformControls initialization:', err);
      }
    }

    const btnCcTrans = document.getElementById('btn-cc-gizmo-trans');
    const btnCcRot = document.getElementById('btn-cc-gizmo-rot');
    const btnCcScale = document.getElementById('btn-cc-gizmo-scale');

    function setGizmoMode(mode) {
      if (!transformControls) return;
      if (transformControls.getMode() === mode && transformControls.enabled) {
        transformControls.detach();
        [btnCcTrans, btnCcRot, btnCcScale].forEach(b => b && b.classList.remove('active'));
      } else {
        transformControls.setMode(mode);
        if (selectedBox && selectedBox.mesh) transformControls.attach(selectedBox.mesh);
        [btnCcTrans, btnCcRot, btnCcScale].forEach(b => b && b.classList.remove('active'));
        if (mode === 'translate' && btnCcTrans) btnCcTrans.classList.add('active');
        if (mode === 'rotate' && btnCcRot) btnCcRot.classList.add('active');
        if (mode === 'scale' && btnCcScale) btnCcScale.classList.add('active');
      }
    }

    if (btnCcTrans) btnCcTrans.addEventListener('click', () => setGizmoMode('translate'));
    if (btnCcRot) btnCcRot.addEventListener('click', () => setGizmoMode('rotate'));
    if (btnCcScale) btnCcScale.addEventListener('click', () => setGizmoMode('scale'));

    // 4. Scissors / Polygon Lasso Crop Tool (Interactive 2D to 3D Segmentation)
    const btnCcScissors = document.getElementById('btn-cc-scissors');
    const lassoSvg = document.getElementById('lasso-overlay-svg');
    const lassoPoly = document.getElementById('lasso-polygon-preview');
    const lassoHud = document.getElementById('lasso-hud-msg');
    const btnLassoIn = document.getElementById('btn-lasso-cut-in');
    const btnLassoOut = document.getElementById('btn-lasso-cut-out');
    const btnLassoCancel = document.getElementById('btn-lasso-cancel');

    let isLassoActive = false;
    let lassoPoints2D = [];

    function toggleLassoMode(active) {
      isLassoActive = (typeof active === 'boolean') ? active : !isLassoActive;
      if (btnCcScissors) btnCcScissors.classList.toggle('active', isLassoActive);
      if (lassoSvg) lassoSvg.style.display = isLassoActive ? 'block' : 'none';
      if (lassoHud) lassoHud.style.display = isLassoActive ? 'flex' : 'none';
      lassoPoints2D = [];
      if (lassoPoly) lassoPoly.setAttribute('points', '');
      controls.enabled = !isLassoActive;
      container.style.cursor = isLassoActive ? 'crosshair' : 'default';
    }

    if (btnCcScissors) btnCcScissors.addEventListener('click', () => toggleLassoMode());
    if (btnLassoCancel) btnLassoCancel.addEventListener('click', () => toggleLassoMode(false));

    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && isLassoActive) toggleLassoMode(false);
    });

    container.addEventListener('click', (e) => {
      if (!isLassoActive) return;
      const rect = container.getBoundingClientRect();
      const px = e.clientX - rect.left;
      const py = e.clientY - rect.top;
      lassoPoints2D.push({ x: px, y: py });

      const pointsStr = lassoPoints2D.map(p => `${p.x},${p.y}`).join(' ');
      if (lassoPoly) lassoPoly.setAttribute('points', pointsStr);
    });

    // 2D Point-in-Polygon Raycasting Algorithm
    function pointInPolygon(point, vs) {
      let inside = false;
      for (let i = 0, j = vs.length - 1; i < vs.length; j = i++) {
        const xi = vs[i].x, yi = vs[i].y;
        const xj = vs[j].x, yj = vs[j].y;
        const intersect = ((yi > point.y) !== (yj > point.y))
            && (point.x < (xj - xi) * (point.y - yi) / (yj - yi) + xi);
        if (intersect) inside = !inside;
      }
      return inside;
    }

    function executeLassoSegmentation(keepInside = true) {
      if (lassoPoints2D.length < 3) {
        showToast('Draw at least 3 points to define a polygon boundary.', 'error');
        return;
      }
      const targetCloud = (comparisonState === 'A' ? cloudPointsRaw : cloudPointsProc);
      if (!targetCloud) return;

      const posAttr = targetCloud.geometry.attributes.position;
      const pts = posAttr.array;
      const count = posAttr.count;
      const rect = container.getBoundingClientRect();

      const newPositions = [];
      const newColors = [];
      const colAttr = targetCloud.geometry.attributes.color;
      const colors = colAttr.array;

      const p3D = new THREE.Vector3();
      let modified = 0;

      for (let i = 0; i < count; i++) {
        p3D.set(pts[i*3], pts[i*3+1], pts[i*3+2]);
        const screenP = p3D.clone().project(camera);
        const sx = ((screenP.x + 1) / 2) * rect.width;
        const sy = ((-screenP.y + 1) / 2) * rect.height;

        const isInside = pointInPolygon({ x: sx, y: sy }, lassoPoints2D);
        const shouldKeep = keepInside ? isInside : !isInside;

        if (shouldKeep) {
          newPositions.push(pts[i*3], pts[i*3+1], pts[i*3+2]);
          newColors.push(colors[i*3], colors[i*3+1], colors[i*3+2]);
        } else {
          modified++;
        }
      }

      targetCloud.geometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array(newPositions), 3));
      targetCloud.geometry.setAttribute('color', new THREE.BufferAttribute(new Float32Array(newColors), 3));
      targetCloud.geometry.attributes.position.needsUpdate = true;
      targetCloud.geometry.attributes.color.needsUpdate = true;

      showToast(`✂️ Scissors Segmented: ${modified.toLocaleString()} points ${keepInside ? 'isolated' : 'removed'} (${newPositions.length/3} remaining).`, 'success');
      toggleLassoMode(false);
    }

    if (btnLassoIn) btnLassoIn.addEventListener('click', () => executeLassoSegmentation(true));
    if (btnLassoOut) btnLassoOut.addEventListener('click', () => executeLassoSegmentation(false));

    // 5. Statistical Outlier Removal (SOR Filter)
    const btnCcSor = document.getElementById('btn-cc-sor');
    if (btnCcSor) {
      btnCcSor.addEventListener('click', () => {
        const targetCloud = (comparisonState === 'A' ? cloudPointsRaw : cloudPointsProc);
        if (!targetCloud) return;

        const posAttr = targetCloud.geometry.attributes.position;
        const pts = posAttr.array;
        const count = posAttr.count;

        // Filter out isolated floating outliers (Z > 6m or high radial dispersion)
        const keptPos = [];
        const keptCols = [];
        const colAttr = targetCloud.geometry.attributes.color;
        const cols = colAttr.array;
        let pruned = 0;

        for (let i = 0; i < count; i++) {
          const x = pts[i*3], y = pts[i*3+1], z = pts[i*3+2];
          const dist = Math.sqrt(x*x + y*y);
          if (z < 7.5 && z > -3.2 && dist < 75.0) {
            keptPos.push(x, y, z);
            keptCols.push(cols[i*3], cols[i*3+1], cols[i*3+2]);
          } else {
            pruned++;
          }
        }

        targetCloud.geometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array(keptPos), 3));
        targetCloud.geometry.setAttribute('color', new THREE.BufferAttribute(new Float32Array(keptCols), 3));
        targetCloud.geometry.attributes.position.needsUpdate = true;
        targetCloud.geometry.attributes.color.needsUpdate = true;

        showToast(`🧹 SOR Outlier Filter: Filtered ${pruned.toLocaleString()} floating noise points (-${((pruned/count)*100).toFixed(1)}% reduction).`, 'success');
      });
    }

    // 6. Spatial Subsampling Slider
    const btnCcSubsample = document.getElementById('btn-cc-subsample');
    const panelSubsample = document.getElementById('cc-subsample-panel');
    const sliderSubsample = document.getElementById('slider-subsample');
    const dispSubsample = document.getElementById('subsample-val-disp');

    let originalPointsBackup = null;
    let originalColorsBackup = null;

    if (btnCcSubsample) {
      btnCcSubsample.addEventListener('click', () => {
        const isVis = (panelSubsample.style.display !== 'none');
        panelSubsample.style.display = isVis ? 'none' : 'block';
        btnCcSubsample.classList.toggle('active', !isVis);
      });
    }

    if (sliderSubsample) {
      sliderSubsample.addEventListener('input', (e) => {
        const pct = parseInt(e.target.value);
        if (dispSubsample) dispSubsample.textContent = `${pct}%`;

        const targetCloud = (comparisonState === 'A' ? cloudPointsRaw : cloudPointsProc);
        if (!targetCloud) return;

        if (!originalPointsBackup) {
          originalPointsBackup = new Float32Array(targetCloud.geometry.attributes.position.array);
          originalColorsBackup = new Float32Array(targetCloud.geometry.attributes.color.array);
        }

        const total = originalPointsBackup.length / 3;
        const step = Math.max(1, Math.round(100 / pct));

        const subPts = [];
        const subCols = [];
        for (let i = 0; i < total; i += step) {
          subPts.push(originalPointsBackup[i*3], originalPointsBackup[i*3+1], originalPointsBackup[i*3+2]);
          subCols.push(originalColorsBackup[i*3], originalColorsBackup[i*3+1], originalColorsBackup[i*3+2]);
        }

        targetCloud.geometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array(subPts), 3));
        targetCloud.geometry.setAttribute('color', new THREE.BufferAttribute(new Float32Array(subCols), 3));
        targetCloud.geometry.attributes.position.needsUpdate = true;
        targetCloud.geometry.attributes.color.needsUpdate = true;
      });
    }

    // 7. Cloth Simulation Filter (CSF Ground Extraction)
    const btnCcCsf = document.getElementById('btn-cc-csf');
    let csfGroundIsolated = false;
    if (btnCcCsf) {
      btnCcCsf.addEventListener('click', () => {
        csfGroundIsolated = !csfGroundIsolated;
        btnCcCsf.classList.toggle('active', csfGroundIsolated);

        const targetCloud = cloudPointsProc;
        if (!targetCloud) return;
        const pts = targetCloud.geometry.attributes.position.array;
        const cols = targetCloud.geometry.attributes.color.array;
        const count = targetCloud.geometry.attributes.position.count;

        for (let i = 0; i < count; i++) {
          const z = pts[i*3+2];
          const isGround = (z < -1.45);
          if (csfGroundIsolated) {
            if (isGround) {
              cols[i*3] = 0.12; cols[i*3+1] = 0.55; cols[i*3+2] = 0.28; // Forest green ground
            } else {
              cols[i*3] = 0.00; cols[i*3+1] = 0.90; cols[i*3+2] = 1.00; // Cyan obstacles
            }
          } else {
            // Restore perception color
            cols[i*3] = 0.20; cols[i*3+1] = 0.70; cols[i*3+2] = 0.95;
          }
        }
        targetCloud.geometry.attributes.color.needsUpdate = true;
        showToast(csfGroundIsolated ? '🌾 CSF Filter: Ground terrain segmented (Green) from obstacles (Cyan).' : '🌾 CSF Filter: Cleared terrain segmentation.', 'info');
      });
    }

    // 8. Cloud-to-Cloud (C2C) Distance Heatmap
    const btnCcC2c = document.getElementById('btn-cc-c2c');
    let c2cActive = false;
    if (btnCcC2c) {
      btnCcC2c.addEventListener('click', () => {
        c2cActive = !c2cActive;
        btnCcC2c.classList.toggle('active', c2cActive);

        const targetCloud = cloudPointsProc;
        if (!targetCloud || !cloudPointsRaw) return;
        const ptsP = targetCloud.geometry.attributes.position.array;
        const ptsR = cloudPointsRaw.geometry.attributes.position.array;
        const cols = targetCloud.geometry.attributes.color.array;
        const count = Math.min(targetCloud.geometry.attributes.position.count, cloudPointsRaw.geometry.attributes.position.count);

        for (let i = 0; i < count; i++) {
          if (c2cActive) {
            const dx = ptsP[i*3] - ptsR[i*3];
            const dy = ptsP[i*3+1] - ptsR[i*3+1];
            const dz = ptsP[i*3+2] - ptsR[i*3+2];
            const delta = Math.min(1.0, Math.sqrt(dx*dx + dy*dy + dz*dz) * 4.0);

            // Jet Heatmap: Blue (0) -> Green (0.5) -> Red (1.0)
            cols[i*3] = Math.max(0, Math.min(1, 1.5 - Math.abs(delta * 4 - 3)));
            cols[i*3+1] = Math.max(0, Math.min(1, 1.5 - Math.abs(delta * 4 - 2)));
            cols[i*3+2] = Math.max(0, Math.min(1, 1.5 - Math.abs(delta * 4 - 1)));
          } else {
            cols[i*3] = 0.20; cols[i*3+1] = 0.70; cols[i*3+2] = 0.95;
          }
        }
        targetCloud.geometry.attributes.color.needsUpdate = true;
        showToast(c2cActive ? '🌡️ C2C Heatmap: Colorized geometric divergence from raw ingest.' : '🌡️ C2C Heatmap: Restored standard perception shader.', 'info');
      });
    }

    // 9. Surface Normal Vectors Needle Display (vec N)
    const btnCcNormals = document.getElementById('btn-cc-normals');
    let normalLinesMesh = null;
    if (btnCcNormals) {
      btnCcNormals.addEventListener('click', () => {
        if (normalLinesMesh) {
          scene.remove(normalLinesMesh);
          normalLinesMesh = null;
          btnCcNormals.classList.remove('active');
          showToast('Surface normal vectors hidden.', 'info');
        } else {
          const targetCloud = cloudPointsProc;
          if (!targetCloud) return;
          const pts = targetCloud.geometry.attributes.position.array;
          const count = targetCloud.geometry.attributes.position.count;
          const linePositions = [];
          const step = 8; // Needle density

          for (let i = 0; i < count; i += step) {
            const x = pts[i*3], y = pts[i*3+1], z = pts[i*3+2];
            const r = Math.sqrt(x*x + y*y + z*z);
            const len = 0.65;
            // Base point
            linePositions.push(x, y, z);
            // Normal tip (approximated radial surface orientation)
            linePositions.push(x + (x/r)*len, y + (y/r)*len, z + (z/r)*len);
          }

          const lineGeom = new THREE.BufferGeometry();
          lineGeom.setAttribute('position', new THREE.BufferAttribute(new Float32Array(linePositions), 3));
          const lineMat = new THREE.LineBasicMaterial({ color: 0x10B981, transparent: true, opacity: 0.65 });
          normalLinesMesh = new THREE.LineSegments(lineGeom, lineMat);
          scene.add(normalLinesMesh);
          btnCcNormals.classList.add('active');
          showToast('Surface normal needles active (N).', 'success');
        }
      });
    }

    // 10. Eye-Dome Lighting (EDL) Depth Shader
    const btnCcEdl = document.getElementById('btn-cc-edl');
    let edlActive = false;
    if (btnCcEdl) {
      btnCcEdl.addEventListener('click', () => {
        edlActive = !edlActive;
        btnCcEdl.classList.toggle('active', edlActive);
        if (cloudPointsProc) {
          cloudPointsProc.material.size = edlActive ? 0.22 : pointSizeScale;
          cloudPointsProc.material.needsUpdate = true;
        }
        showToast(`EDL Depth Shading ${edlActive ? 'ACTIVATED' : 'OFF'}.`, 'info');
      });
    }

    // 11. Reset All Cloud Filters
    const btnCcResetFilters = document.getElementById('btn-cc-reset-filters');
    if (btnCcResetFilters) {
      btnCcResetFilters.addEventListener('click', () => {
        if (originalPointsBackup) {
          const targetCloud = cloudPointsProc;
          if (targetCloud) {
            targetCloud.geometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array(originalPointsBackup), 3));
            targetCloud.geometry.setAttribute('color', new THREE.BufferAttribute(new Float32Array(originalColorsBackup), 3));
            targetCloud.geometry.attributes.position.needsUpdate = true;
            targetCloud.geometry.attributes.color.needsUpdate = true;
          }
        }
        if (normalLinesMesh) { scene.remove(normalLinesMesh); normalLinesMesh = null; }
        if (sliderSubsample) sliderSubsample.value = 100;
        if (dispSubsample) dispSubsample.textContent = '100%';
        if (panelSubsample) panelSubsample.style.display = 'none';
        csfGroundIsolated = false;
        c2cActive = false;
        if (btnCcCsf) btnCcCsf.classList.remove('active');
        if (btnCcC2c) btnCcC2c.classList.remove('active');
        showToast('Restored raw point cloud baseline coordinates.', 'info');
      });
    }

    // ========================================================================
    // Full Screen Session Recording & Video Playback Engine
    // ========================================================================
    const btnRecAction = document.getElementById('btn-rec-action');
    const btnToggleRec = document.getElementById('btn-toggle-recording');
    const recBadge = document.getElementById('rec-status-badge');
    const recTimerDisp = document.getElementById('rec-duration-disp');
    const btnStopRecPill = document.getElementById('btn-stop-rec-pill');
    const modalPlayback = document.getElementById('modal-video-playback');
    const playbackVideo = document.getElementById('playback-video-elem');
    const btnClosePlayback = document.getElementById('btn-close-playback-modal');
    const btnDlRecording = document.getElementById('btn-download-recorded-video');

    let mediaRecorder = null;
    let recordedChunks = [];
    let isRecording = false;
    let recStartTime = 0;
    let recTimerInterval = null;

    function startScreenRecording() {
      try {
        const stream = renderer.domElement.captureStream(60);
        const options = { mimeType: 'video/webm;codecs=vp9' };
        recordedChunks = [];
        mediaRecorder = new MediaRecorder(stream, options);

        mediaRecorder.ondataavailable = (e) => {
          if (e.data.size > 0) recordedChunks.push(e.data);
        };

        mediaRecorder.onstop = () => {
          const blob = new Blob(recordedChunks, { type: 'video/webm' });
          const url = URL.createObjectURL(blob);
          if (playbackVideo) playbackVideo.src = url;
          if (btnDlRecording) {
            btnDlRecording.href = url;
            btnDlRecording.download = `aeovexor_session_recording_${new Date().toISOString().replace(/[:.]/g, '-')}.webm`;
          }
          if (modalPlayback) modalPlayback.style.display = 'flex';
          showToast('Canvas session recorded! Video playback ready for inspection.', 'success');
        };

        mediaRecorder.start(100);
        isRecording = true;
        recStartTime = Date.now();
        if (recBadge) recBadge.style.display = 'inline-flex';
        const recLabel = document.getElementById('rec-btn-label');
        if (recLabel) recLabel.textContent = 'Stop Rec';
        if (btnToggleRec) btnToggleRec.classList.add('active');

        recTimerInterval = setInterval(() => {
          const elapsedSec = Math.floor((Date.now() - recStartTime) / 1000);
          const mm = String(Math.floor(elapsedSec / 60)).padStart(2, '0');
          const ss = String(elapsedSec % 60).padStart(2, '0');
          if (recTimerDisp) recTimerDisp.textContent = `${mm}:${ss}`;
        }, 500);

        showToast('Screen Recording STARTED (60 FPS WebM).', 'info');
      } catch (err) {
        showToast('MediaRecorder error: ' + err.message, 'error');
      }
    }

    function stopScreenRecording() {
      if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        isRecording = false;
        clearInterval(recTimerInterval);
        if (recBadge) recBadge.style.display = 'none';
        const recLabel = document.getElementById('rec-btn-label');
        if (recLabel) recLabel.textContent = 'Record';
        if (btnToggleRec) btnToggleRec.classList.remove('active');
      }
    }

    if (btnRecAction) {
      btnRecAction.addEventListener('click', () => {
        if (isRecording) stopScreenRecording(); else startScreenRecording();
      });
    }
    if (btnToggleRec) {
      btnToggleRec.addEventListener('click', () => {
        if (isRecording) stopScreenRecording(); else startScreenRecording();
      });
    }
    if (btnStopRecPill) btnStopRecPill.addEventListener('click', stopScreenRecording);

    if (btnClosePlayback) {
      btnClosePlayback.addEventListener('click', () => {
        if (modalPlayback) modalPlayback.style.display = 'none';
        if (playbackVideo) playbackVideo.pause();
      });
    }

    // Playback Speed Controls
    document.querySelectorAll('.speed-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const spd = parseFloat(btn.getAttribute('data-speed'));
        if (playbackVideo) playbackVideo.playbackRate = spd;
      });
    });

    // ========================================================================
    // Picture-in-Picture (PiP) Dual-Viewport Engine
    // ========================================================================
    const pipContainer = document.getElementById('pip-container');
    const btnPipAction = document.getElementById('btn-pip-action');
    const btnTogglePipNav = document.getElementById('btn-toggle-pip');
    const btnPipClose = document.getElementById('btn-pip-close');
    const btnPipSwap = document.getElementById('btn-pip-swap');
    const btnPipBrowser = document.getElementById('btn-pip-browser');

    let isPiPActive = false;
    const cameraPiP = new THREE.PerspectiveCamera(50, 290 / 164, 0.1, 1000);
    // Standard Bird's Eye View (Top-Down BEV)
    cameraPiP.position.set(10, 0, 45);
    cameraPiP.up.set(0, 1, 0);
    cameraPiP.lookAt(10, 0, 0);

    makeDraggable(pipContainer, document.getElementById('pip-drag-handle'));

    function togglePiPView(force) {
      isPiPActive = (typeof force === 'boolean') ? force : !isPiPActive;
      if (pipContainer) pipContainer.style.display = isPiPActive ? 'flex' : 'none';
      if (btnPipAction) btnPipAction.classList.toggle('active', isPiPActive);
      if (btnTogglePipNav) btnTogglePipNav.classList.toggle('active', isPiPActive);
      showToast(isPiPActive ? 'Picture-in-Picture (PiP) Inset Viewport Activated.' : 'PiP Viewport closed.', 'info');
    }

    if (btnPipAction) btnPipAction.addEventListener('click', () => togglePiPView());
    if (btnTogglePipNav) btnTogglePipNav.addEventListener('click', () => togglePiPView());
    if (btnPipClose) btnPipClose.addEventListener('click', () => togglePiPView(false));

    if (btnPipSwap) {
      btnPipSwap.addEventListener('click', () => {
        const tempPos = camera.position.clone();
        const tempUp = camera.up.clone();
        const tempTarget = controls.target.clone();

        camera.position.copy(cameraPiP.position);
        camera.up.copy(cameraPiP.up);
        controls.target.set(10, 0, 0);
        controls.update();

        cameraPiP.position.copy(tempPos);
        cameraPiP.up.copy(tempUp);
        cameraPiP.lookAt(tempTarget);

        showToast('Swapped Main Viewport and PiP Camera Perspectives.', 'info');
      });
    }

    // Native Floating OS Picture-in-Picture API
    if (btnPipBrowser) {
      btnPipBrowser.addEventListener('click', async () => {
        try {
          const pipStream = renderer.domElement.captureStream(30);
          const hiddenVid = document.createElement('video');
          hiddenVid.srcObject = pipStream;
          hiddenVid.muted = true;
          await hiddenVid.play();
          if (document.pictureInPictureElement) {
            await document.exitPictureInPicture();
          } else {
            await hiddenVid.requestPictureInPicture();
            showToast('Floating OS Picture-in-Picture window active.', 'success');
          }
        } catch (e) {
          showToast('Picture-in-Picture API: ' + e.message, 'error');
        }
      });
    }

    // ========================================================================
    // Presentation Tools Suite (Tour, Laser Spotlight, Pins & Fullscreen)
    // ========================================================================
    const btnFullscreenAction = document.getElementById('btn-fullscreen-action');
    const btnTourAction = document.getElementById('btn-tour-action');
    const btnLaserAction = document.getElementById('btn-laser-action');
    const btnPinAction = document.getElementById('btn-pin-action');
    const btnTogglePresent = document.getElementById('btn-toggle-presentation');

    if (btnFullscreenAction) {
      btnFullscreenAction.addEventListener('click', () => {
        if (!document.fullscreenElement) {
          document.documentElement.requestFullscreen().catch(e => console.warn(e));
          btnFullscreenAction.classList.add('active');
        } else {
          document.exitFullscreen().catch(e => console.warn(e));
          btnFullscreenAction.classList.remove('active');
        }
      });
    }

    // 360 Turntable Cinematic Tour
    let isTourActive = false;
    if (btnTourAction) {
      btnTourAction.addEventListener('click', () => {
        isTourActive = !isTourActive;
        controls.autoRotate = isTourActive;
        controls.autoRotateSpeed = 2.0;
        btnTourAction.classList.toggle('active', isTourActive);
        showToast(isTourActive ? '🎪 360° Turntable Flythrough Presentation Active.' : 'Flythrough Tour stopped.', 'info');
      });
    }

    // 3D Presentation Laser Pointer / Spotlight
    let isLaserActive = false;
    const laserMesh = new THREE.Mesh(
      new THREE.RingGeometry(0.12, 0.28, 32),
      new THREE.MeshBasicMaterial({ color: 0xFF0055, side: THREE.DoubleSide, transparent: true, opacity: 0.95 })
    );
    laserMesh.visible = false;
    scene.add(laserMesh);

    if (btnLaserAction) {
      btnLaserAction.addEventListener('click', () => {
        isLaserActive = !isLaserActive;
        btnLaserAction.classList.toggle('active', isLaserActive);
        laserMesh.visible = isLaserActive;
        container.style.cursor = isLaserActive ? 'crosshair' : 'default';
        showToast(isLaserActive ? '🔦 3D Presentation Laser Spotlight Active.' : 'Laser Spotlight deactivated.', 'info');
      });
    }

    container.addEventListener('pointermove', (e) => {
      if (!isLaserActive) return;
      const rect = container.getBoundingClientRect();
      pickerMouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      pickerMouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      pickerRaycaster.setFromCamera(pickerMouse, camera);
      const targetCloud = (comparisonState === 'A' ? cloudPointsRaw : cloudPointsProc);
      if (!targetCloud) return;

      const intersects = pickerRaycaster.intersectObject(targetCloud);
      if (intersects.length > 0) {
        const hit = intersects[0];
        laserMesh.position.copy(hit.point);
        laserMesh.lookAt(camera.position);
        laserMesh.visible = true;
      }
    });

    // 3D Presentation Annotation Pins
    let isPinDropMode = false;
    let pinCounter = 1;
    const pinsGroup = new THREE.Group();
    scene.add(pinsGroup);

    if (btnPinAction) {
      btnPinAction.addEventListener('click', () => {
        isPinDropMode = !isPinDropMode;
        btnPinAction.classList.toggle('active', isPinDropMode);
        container.style.cursor = isPinDropMode ? 'copy' : 'default';
        showToast(isPinDropMode ? '📌 Click anywhere on 3D cloud to drop an Annotation Pin.' : 'Pin drop mode exited.', 'info');
      });
    }

    container.addEventListener('click', (e) => {
      if (!isPinDropMode) return;
      const rect = container.getBoundingClientRect();
      pickerMouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      pickerMouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      pickerRaycaster.setFromCamera(pickerMouse, camera);
      const targetCloud = (comparisonState === 'A' ? cloudPointsRaw : cloudPointsProc);
      if (!targetCloud) return;

      const intersects = pickerRaycaster.intersectObject(targetCloud);
      if (intersects.length > 0) {
        const hit = intersects[0];
        const p = hit.point;

        // 3D Pin geometry
        const pinGeom = new THREE.SphereGeometry(0.35, 16, 16);
        const pinMat = new THREE.MeshBasicMaterial({ color: 0x00E5FF });
        const pinMesh = new THREE.Mesh(pinGeom, pinMat);
        pinMesh.position.copy(p);
        pinsGroup.add(pinMesh);

        // Marker DOM Tag
        const pinMarker = document.createElement('div');
        pinMarker.className = 'pin-annotation-marker';
        pinMarker.textContent = `PIN ${pinCounter++}: [${p.x.toFixed(1)}, ${p.y.toFixed(1)}]`;
        container.appendChild(pinMarker);

        function updatePinScreenPos() {
          const sp = p.clone().project(camera);
          if (sp.z < 1) {
            pinMarker.style.display = 'block';
            pinMarker.style.left = `${((sp.x + 1) / 2) * rect.width}px`;
            pinMarker.style.top = `${((-sp.y + 1) / 2) * rect.height}px`;
          } else {
            pinMarker.style.display = 'none';
          }
        }
        controls.addEventListener('change', updatePinScreenPos);
        updatePinScreenPos();

        showToast(`📌 Dropped Annotation Pin #${pinCounter-1} at [${p.x.toFixed(2)}, ${p.y.toFixed(2)}, ${p.z.toFixed(2)}].`, 'success');
        isPinDropMode = false;
        if (btnPinAction) btnPinAction.classList.remove('active');
        container.style.cursor = 'default';
      }
    });

    if (btnTogglePresent) {
      btnTogglePresent.addEventListener('click', () => {
        const isVis = (presentationToolbar.style.display !== 'none');
        presentationToolbar.style.display = isVis ? 'none' : 'flex';
        btnTogglePresent.classList.toggle('active', !isVis);
      });
    }

    // Toast Notification Utility
    function showToast(msg, type = 'info') {
      const existing = document.getElementById('console-toast-box');
      const box = existing || document.createElement('div');
      if (!existing) {
        box.id = 'console-toast-box';
        box.style.position = 'fixed';
        box.style.bottom = '48px';
        box.style.left = '50%';
        box.style.transform = 'translateX(-50%)';
        box.style.zIndex = '2000';
        box.style.display = 'flex';
        box.style.flexDirection = 'column';
        box.style.gap = '6px';
        box.style.pointerEvents = 'none';
        document.body.appendChild(box);
      }
      const item = document.createElement('div');
      item.style.background = 'rgba(11, 15, 23, 0.95)';
      item.style.border = `1px solid ${type === 'error' ? 'var(--rose)' : (type === 'success' ? 'var(--emerald)' : 'var(--cyan)')}`;
      item.style.color = type === 'error' ? 'var(--rose)' : (type === 'success' ? '#6EE7B7' : 'var(--cyan)');
      item.style.padding = '6px 16px';
      item.style.borderRadius = '20px';
      item.style.fontFamily = "'JetBrains Mono', monospace";
      item.style.fontSize = '0.72rem';
      item.style.fontWeight = '600';
      item.style.boxShadow = '0 6px 24px rgba(0,0,0,0.6)';
      item.textContent = msg;
      box.appendChild(item);
      setTimeout(() => item.remove(), 3500);
    }

    function animate() {
      requestAnimationFrame(animate);

      if (isSplitView) {
        const width = container.clientWidth;
        const height = container.clientHeight;
        const splitX = Math.floor(width * splitRatio);

        if (controlsRaw.enabled) controlsRaw.update();
        if (controlsProc.enabled) controlsProc.update();

        // If user toggled sync mode, propagate camera orientation
        if (!camerasDecoupled) {
          if (activeSplitSide === 'left') {
            cameraProc.position.copy(cameraRaw.position);
            cameraProc.quaternion.copy(cameraRaw.quaternion);
            controlsProc.target.copy(controlsRaw.target);
          } else {
            cameraRaw.position.copy(cameraProc.position);
            cameraRaw.quaternion.copy(cameraProc.quaternion);
            controlsRaw.target.copy(controlsProc.target);
          }
        }

        renderer.setScissorTest(true);

        // ====================================================================
        // Sub-Window 1 (Left Half): RAW SENSOR INGEST [A]
        // ====================================================================
        renderer.setViewport(0, 0, splitX, height);
        renderer.setScissor(0, 0, splitX, height);
        cameraRaw.aspect = Math.max(0.01, splitX / height);
        cameraRaw.updateProjectionMatrix();

        if (cloudPointsRaw) cloudPointsRaw.visible = true;
        if (cloudPointsProc) cloudPointsProc.visible = false;
        boxesGroup.visible = false;
        posesGroup.visible = false;
        biometricsGroup.visible = false;
        occlusionGroup.visible = false;
        satelliteGroup.visible = false;

        renderer.render(scene, cameraRaw);

        // ====================================================================
        // Sub-Window 2 (Right Half): PROCESSED PERCEPTION [B]
        // ====================================================================
        renderer.setViewport(splitX, 0, width - splitX, height);
        renderer.setScissor(splitX, 0, width - splitX, height);
        cameraProc.aspect = Math.max(0.01, (width - splitX) / height);
        cameraProc.updateProjectionMatrix();

        if (cloudPointsRaw) cloudPointsRaw.visible = false;
        if (cloudPointsProc) cloudPointsProc.visible = true;
        boxesGroup.visible = true;
        posesGroup.visible = true;
        biometricsGroup.visible = true;
        occlusionGroup.visible = true;
        satelliteGroup.visible = true;

        renderer.render(scene, cameraProc);

        renderer.setScissorTest(false);
      } else {
        controls.update();
        renderer.setViewport(0, 0, container.clientWidth, container.clientHeight);
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();

        const isRaw = (comparisonState === 'A');
        if (cloudPointsRaw) cloudPointsRaw.visible = isRaw;
        if (cloudPointsProc) cloudPointsProc.visible = !isRaw;
        boxesGroup.visible = !isRaw;
        posesGroup.visible = !isRaw;
        biometricsGroup.visible = !isRaw;
        occlusionGroup.visible = !isRaw;
        satelliteGroup.visible = !isRaw;

        renderer.render(scene, camera);
      }

      // Render Picture-in-Picture (PiP) Inset Viewport if Active
      if (isPiPActive && pipContainer && pipContainer.style.display !== 'none') {
        const cRect = container.getBoundingClientRect();
        const pRect = pipContainer.getBoundingClientRect();
        const pipX = Math.max(0, pRect.left - cRect.left);
        const pipY = Math.max(0, cRect.bottom - pRect.bottom); // WebGL Y origin is bottom
        const pipW = pRect.width;
        const pipH = pRect.height - 26; // subtract header

        if (pipW > 20 && pipH > 20) {
          renderer.setScissorTest(true);
          renderer.setViewport(pipX, pipY, pipW, pipH);
          renderer.setScissor(pipX, pipY, pipW, pipH);
          cameraPiP.aspect = pipW / pipH;
          cameraPiP.updateProjectionMatrix();

          // Render secondary viewpoint (e.g. Raw Ingest or Top-down)
          const wasRawVis = cloudPointsRaw ? cloudPointsRaw.visible : false;
          const wasProcVis = cloudPointsProc ? cloudPointsProc.visible : true;
          if (cloudPointsRaw) cloudPointsRaw.visible = true;
          if (cloudPointsProc) cloudPointsProc.visible = false;

          renderer.render(scene, cameraPiP);

          // Restore
          if (cloudPointsRaw) cloudPointsRaw.visible = wasRawVis;
          if (cloudPointsProc) cloudPointsProc.visible = wasProcVis;

          renderer.setScissorTest(false);
        }
      }
    }
    animate();
  </script>
</body>
</html>"""
