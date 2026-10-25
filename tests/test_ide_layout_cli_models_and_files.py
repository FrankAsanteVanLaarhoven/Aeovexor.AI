"""
Unit tests for AEOVEXOR Scientific IDE:
- Workspace File Tree & File I/O Endpoints
- Developer CLI Neural Coding Models (Codex, Grok, ClaudeCode, OpenCode)
- Interactive CLI Model Summoning & Code Extraction
- Full Settings & OpenRouter Key Persistence
"""

import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from workspace.server import app
from spatialforge.ide_runtime import (
    get_workspace_file_tree,
    read_workspace_file,
    save_workspace_file,
    create_workspace_file,
    execute_developer_cli_command,
)

client = TestClient(app)


def test_workspace_file_tree():
    tree = get_workspace_file_tree()
    assert isinstance(tree, list)
    assert len(tree) > 0
    # Ensure key workspace folders are present
    names = [node["name"] for node in tree]
    assert "workspace" in names
    assert "spatialforge" in names


def test_workspace_file_read_and_save(tmp_path):
    test_rel = "examples/test_file_io.py"
    content = "# Test content\nx = 42\n"
    
    # Save
    save_res = save_workspace_file(test_rel, content)
    assert save_res["status"] == "OK"
    assert save_res["lines"] == 2
    
    # Read
    read_res = read_workspace_file(test_rel)
    assert read_res["status"] == "OK"
    assert read_res["content"] == content
    assert read_res["name"] == "test_file_io.py"

    # Clean up
    p = Path(__file__).resolve().parent.parent / test_rel
    if p.exists():
        p.unlink()


def test_file_traversal_prevention():
    res = read_workspace_file("../../etc/passwd")
    assert res["status"] == "ERROR"
    assert "escapes workspace boundary" in res["message"]


def test_developer_cli_models():
    # 1. Models list
    res_models = execute_developer_cli_command("models")
    assert res_models["status"] == "OK"
    assert "NEURAL CODING MODELS" in res_models["output"]

    # 2. Codex model prompt
    res_codex = execute_developer_cli_command("codex write a function to calculate 3d bounding box iou")
    assert res_codex["status"] == "OK"
    assert res_codex["alias"] == "codex"
    assert res_codex["model"] == "openai/gpt-4o"
    assert "iou" in res_codex["output"].lower()

    # 3. Grok model prompt
    res_grok = execute_developer_cli_command("grok explain kaufman filter efficiency ratio")
    assert res_grok["status"] == "OK"
    assert res_grok["alias"] == "grok"
    assert res_grok["model"] == "x-ai/grok-2-1212"

    # 4. Claudecode model prompt
    res_claude = execute_developer_cli_command("claudecode create wifi slam fusion script")
    assert res_claude["status"] == "OK"
    assert res_claude["alias"] == "claudecode"
    assert res_claude["model"] == "anthropic/claude-3.5-sonnet"

    # 5. OpenCode model prompt
    res_opencode = execute_developer_cli_command("opencode optimize point cloud ground removal")
    assert res_opencode["status"] == "OK"
    assert res_opencode["alias"] == "opencode"
    assert res_opencode["model"] == "deepseek/deepseek-coder"

    # 6. Interactive mode summon (no prompt)
    res_interact = execute_developer_cli_command("claudecode")
    assert res_interact["status"] == "OK"
    assert res_interact.get("mode") == "interactive_ready"


def test_developer_cli_filesystem():
    # Tree
    res_tree = execute_developer_cli_command("tree")
    assert res_tree["status"] == "OK"
    assert "DIRECTORY TREE" in res_tree["output"]

    # Cat
    res_cat = execute_developer_cli_command("cat pyproject.toml")
    assert res_cat["status"] == "OK"
    assert "spatialforge" in res_cat["output"]


def test_api_ide_routes():
    # GET /api/ide/files/tree
    resp = client.get("/api/ide/files/tree")
    assert resp.status_code == 200
    assert "tree" in resp.json()

    # GET /api/settings
    resp_settings = client.get("/api/settings")
    assert resp_settings.status_code == 200
    data = resp_settings.json()
    assert "openrouter_key_status" in data
    assert "available_models" in data

    # POST /api/ide/cli
    resp_cli = client.post("/api/ide/cli", json={"command": "status"})
    assert resp_cli.status_code == 200
    assert "AEOVEXOR CORE ENGINE STATUS" in resp_cli.json()["output"]


def test_ide_html_themes_atom_and_eclipse():
    resp = client.get("/ide")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    html = resp.text
    html_lower = html.lower()

    # 1. Themes: Real color swatches and theme options
    themes = [
        "vscode-dark",
        "vscode-light",
        "jetbrains-darcula",
        "atom-one-dark",
        "atom-one-light",
        "eclipse-dark",
        "eclipse-light",
        "obsidian"
    ]
    for theme in themes:
        assert f'data-theme="{theme}"' in html, f"Missing theme option: {theme}"
        assert f"body.theme-{theme}" in html, f"Missing CSS rules for theme: {theme}"

    # 2. Real color swatches represented in theme picker
    assert "#1e1e1e" in html_lower or "#1e1f22" in html_lower
    assert "#282c34" in html_lower  # Atom One Dark
    assert "#1e1f22" in html_lower  # JetBrains Darcula
    assert "#1f1f1f" in html_lower  # Eclipse Dark

    # 3. Atom Capabilities: Command Palette and Quick Open
    assert 'id="atom-palette-modal"' in html
    assert 'id="palette-search-input"' in html
    assert 'id="palette-command-list"' in html
    assert 'id="atom-quick-open-modal"' in html
    assert 'id="quick-open-search-input"' in html
    assert "PALETTE_COMMANDS" in html
    assert "openAtomPalette" in html
    assert "openQuickOpen" in html

    # 4. Eclipse Capabilities: Symbol Outline & Structure Navigator
    assert 'id="tab-toggle-outline"' in html
    assert 'id="view-outline"' in html
    assert 'id="outline-tree-root"' in html
    assert 'id="btn-refresh-outline"' in html
    assert "updateEclipseOutline" in html
    assert "jumpToLine" in html

    # 5. Interactive Figure Visualizer Telemetry & Feedback Tags
    assert "renderInteractiveScientificPlot" in html
    assert 'id="plot-hud"' in html
    assert 'id="plot-hover-tag"' in html
    assert 'id="plot-scrubber"' in html
    assert "renderPinnedMarkers" in html


def test_console_split_screen_and_shape_placement():
    resp = client.get("/console")
    assert resp.status_code == 200
    html = resp.text

    # 1. Split screen view mode and draggable divider
    assert 'id="split-divider"' in html
    assert 'id="split-badge-left"' in html
    assert 'id="split-badge-right"' in html
    assert "RAW SENSOR INGEST" in html
    assert "PROCESSED PERCEPTION" in html
    assert "renderer.setScissor" in html
    assert "renderer.setScissorTest" in html

    # 2. Individual Camera Controls for Each Split Screen
    assert 'id="btn-toggle-camera-sync"' in html
    assert "controlsRaw" in html
    assert "controlsProc" in html
    assert "camerasDecoupled" in html

    # 3. Place 3D shapes directly on actual detected items
    assert 'id="ci-btn-place-shape"' in html
    assert "Place Shape" in html or "Place calibrated 3D shape" in html


def test_3d_box_nms_on_actual_sensor_items():
    from spatialforge.io import load_frame
    from spatialforge.detections_3d import run_automated_3d_detection_suite, apply_3d_box_non_maximum_suppression

    frame = load_frame("examples/velodyne_000008.bin")
    res = run_automated_3d_detection_suite(frame, dataset_name="velodyne_000008.bin")
    raw_boxes = res.boxes
    assert len(raw_boxes) > 0

    clean_boxes = apply_3d_box_non_maximum_suppression(raw_boxes)
    # Deduplication suppresses overlapping fragments while preserving real entities
    assert len(clean_boxes) == 25
    assert len(clean_boxes) <= len(raw_boxes)

    # Check that labels are actual perception entities
    labels = {b.class_label for b in clean_boxes}
    assert "Vehicle" in labels
    assert "Cyclist" in labels


def test_scientific_script_series_and_metrics_extraction():
    from spatialforge.ide_runtime import execute_scientific_script

    test_code = """
import numpy as np
import matplotlib.pyplot as plt
from spatialforge.signal_processing import kaufman_adaptive_filter_1d

r = np.linspace(10.0, 25.0, 100) + np.random.normal(0, 0.5, 100)
filtered_r = kaufman_adaptive_filter_1d(r, period=10)

plt.figure(figsize=(5, 3))
plt.plot(r, label='Raw Sensor Distance', color='#94A3B8')
plt.plot(filtered_r, label='KAMA Adaptive Filter', color='#00E5FF')
plt.title('Test KAMA Plot')
plt.xlabel('Azimuth')
plt.ylabel('Range')
plt.show()
"""
    res = execute_scientific_script(test_code)
    assert res["status"] == "SUCCESS"
    assert res["plot_b64"] is not None
    assert len(res["series_data"]) > 0
    assert "metrics_summary" in res

    ax_data = res["series_data"][0]
    assert len(ax_data["lines"]) == 2
    assert ax_data["lines"][0]["label"] == "Raw Sensor Distance"
    assert ax_data["lines"][1]["label"] == "KAMA Adaptive Filter"


def test_cloudcompare_toolbox_and_presentation_tools():
    """Verify presence and wiring of CloudCompare manual manipulation toolbox,
    full screen screen recording, video playback modal, picture-in-picture, and presentation tools."""
    resp = client.get("/console")
    assert resp.status_code == 200
    html = resp.text

    # 1. CloudCompare Vertical Toolbox
    assert 'id="cc-vert-toolbar"' in html
    assert 'id="btn-cc-reset-view"' in html
    assert 'id="btn-cc-ortho"' in html
    assert 'id="btn-cc-view-top"' in html
    assert 'id="btn-cc-view-front"' in html
    assert 'id="btn-cc-view-back"' in html
    assert 'id="btn-cc-view-left"' in html
    assert 'id="btn-cc-view-right"' in html
    assert 'id="btn-cc-view-iso"' in html
    assert 'id="btn-cc-picker"' in html
    assert 'id="btn-cc-gizmo-trans"' in html
    assert 'id="btn-cc-gizmo-rot"' in html
    assert 'id="btn-cc-gizmo-scale"' in html
    assert 'id="btn-cc-normals"' in html
    assert 'id="btn-cc-edl"' in html
    assert 'id="cc-picker-card"' in html

    # 2. CloudCompare Horizontal Toolbox
    assert 'id="cc-horiz-toolbar"' in html
    assert 'id="btn-cc-scissors"' in html
    assert 'id="btn-cc-box-slice"' in html
    assert 'id="btn-cc-sor"' in html
    assert 'id="btn-cc-subsample"' in html
    assert 'id="btn-cc-csf"' in html
    assert 'id="btn-cc-c2c"' in html
    assert 'id="btn-cc-reset-filters"' in html
    assert 'id="lasso-overlay-svg"' in html
    assert 'id="lasso-hud-msg"' in html
    assert 'id="cc-subsample-panel"' in html

    # 3. Full Screen Recording & Video Playback Modal
    assert 'id="presentation-toolbar"' in html
    assert 'id="btn-rec-action"' in html
    assert 'id="rec-status-badge"' in html
    assert 'id="modal-video-playback"' in html
    assert 'id="playback-video-elem"' in html
    assert 'id="btn-download-recorded-video"' in html
    assert "MediaRecorder" in html

    # 4. Picture-in-Picture (PiP) Dual-Viewport
    assert 'id="btn-pip-action"' in html
    assert 'id="pip-container"' in html
    assert 'id="pip-canvas-wrap"' in html
    assert 'id="btn-pip-swap"' in html
    assert 'id="btn-pip-close"' in html

    # 5. Presentation Tools
    assert 'id="btn-tour-action"' in html
    assert 'id="btn-laser-action"' in html
    assert 'id="btn-pin-action"' in html
    assert 'id="btn-fullscreen-action"' in html
    assert "laserMesh" in html or "laserActive" in html

    # 6. TransformControls integration
    assert "TransformControls.js" in html

    # 7. Zero SOTA wording
    import re
    assert len(re.findall(r"\bsota\b", html, re.IGNORECASE)) == 0



