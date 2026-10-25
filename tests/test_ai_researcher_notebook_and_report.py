"""
Unit & Integration Tests for AEOVEXOR AI/SI Autonomous Researcher & Publication Generator
"""

import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from workspace.server import app
from spatialforge.ai_researcher import (
    DataIngestionEngine,
    generate_kaggle_grandmaster_notebook,
    generate_publication_research_report,
    discuss_research_with_ai,
    RESEARCH_DATA_DIR,
    RESEARCH_OUTPUTS_DIR,
)

client = TestClient(app)


def test_data_ingestion_inspect_telemetry():
    telemetry = DataIngestionEngine.inspect_dataset_telemetry("examples/velodyne_000008.bin")
    assert telemetry["filename"] == "velodyne_000008.bin"
    assert telemetry["point_count"] == 17238
    assert len(telemetry["bounds_min"]) == 3
    assert len(telemetry["bounds_max"]) == 3
    assert telemetry["distance_stats_meters"]["mean"] > 0
    assert len(telemetry["sha256"]) == 64


def test_generate_kaggle_grandmaster_notebook():
    res = generate_kaggle_grandmaster_notebook(
        dataset_path_or_name="examples/velodyne_000008.bin",
        research_title="Autonomous 3D LiDAR Perception Production Benchmark",
        focus_domain="3D Object Detection & Kaufman Adaptive Filtering",
        author_name="Frank / Leroy & AEOVEXOR Team",
    )
    assert res["status"] == "success"
    assert res["cell_count"] >= 15
    assert res["code_cell_count"] >= 5
    assert res["markdown_cell_count"] >= 5
    assert Path(res["file_path"]).exists()

    # Verify JSON validity and nbformat v4 structure
    with open(res["file_path"], "r", encoding="utf-8") as f:
        nb_json = json.load(f)
    assert nb_json["nbformat"] == 4
    assert "cells" in nb_json
    assert "metadata" in nb_json

    # Check for Grandmaster badge and mathematical formula text
    content_all = json.dumps(nb_json)
    assert "Kaggle Grandmaster" in content_all
    assert "ER_t" in content_all
    assert "Wilcoxon" in content_all
    assert "Kaufman" in content_all


def test_generate_publication_research_report():
    res = generate_publication_research_report(
        dataset_path_or_name="examples/velodyne_000008.bin",
        paper_title="Adaptive 3D Point Cloud Perception via Kaufman Filtering",
        target_venue="IEEE Transactions on Robotics (T-RO)",
        author_name="Frank / Leroy, Ph.D.",
    )
    assert res["status"] == "success"
    assert "markdown_content" in res
    assert "html_content" in res

    md_path = RESEARCH_OUTPUTS_DIR / res["md_filename"]
    html_path = RESEARCH_OUTPUTS_DIR / res["html_filename"]
    assert md_path.exists()
    assert html_path.exists()

    md_text = md_path.read_text(encoding="utf-8")
    assert "# Adaptive 3D Point Cloud Perception" in md_text
    assert "Abstract" in md_text
    assert "Table 1:" in md_text
    assert "Wilcoxon" in md_text
    assert "References" in md_text


def test_discuss_research_with_ai():
    # Test query on Kaufman filtering
    res_kaufman = discuss_research_with_ai("Why use Kaufman adaptive filter instead of Kalman?")
    assert res_kaufman["status"] == "success"
    assert "Kaufman" in res_kaufman["response"]
    assert "Efficiency Ratio" in res_kaufman["response"] or "ER_t" in res_kaufman["response"]

    # Test query on 3D NMS
    res_nms = discuss_research_with_ai("Explain the 3D NMS containment ratio logic")
    assert res_nms["status"] == "success"
    assert "Containment" in res_nms["response"] or "IoU" in res_nms["response"]


def test_api_research_endpoints():
    # 1. Inspect dataset
    resp = client.get("/api/research/inspect_dataset?dataset=examples/velodyne_000008.bin")
    assert resp.status_code == 200
    data = resp.json()
    assert data["point_count"] == 17238

    # 2. Generate Notebook via API
    nb_payload = {
        "dataset": "examples/velodyne_000008.bin",
        "title": "API Automated Production Kaggle Benchmark",
        "focus_domain": "3D LiDAR Perception & Non-Maximum Suppression",
        "include_live_telemetry": True,
        "author": "AEOVEXOR Autonomous Scientist",
    }
    resp = client.post("/api/research/generate_notebook", json=nb_payload)
    assert resp.status_code == 200
    nb_res = resp.json()
    assert nb_res["status"] == "success"
    nb_filename = nb_res["filename"]

    # 3. Direct Download Notebook attachment
    dl_resp = client.get(f"/api/research/download/notebook?filename={nb_filename}")
    assert dl_resp.status_code == 200
    assert "application/x-ipynb+json" in dl_resp.headers.get("content-type", "")
    assert f'filename="{nb_filename}"' in dl_resp.headers.get("content-disposition", "")

    # 4. Generate Research Paper via API
    paper_payload = {
        "dataset": "examples/velodyne_000008.bin",
        "title": "Real-Time 3D Spatial Intelligence Paper",
        "venue": "CVPR Workshop",
        "author": "Frank / Leroy",
    }
    resp = client.post("/api/research/generate_paper", json=paper_payload)
    assert resp.status_code == 200
    paper_res = resp.json()
    assert paper_res["status"] == "success"
    md_filename = paper_res["md_filename"]

    # 5. Direct Download Paper attachment
    dl_paper = client.get(f"/api/research/download/paper?filename={md_filename}&format=md")
    assert dl_paper.status_code == 200
    assert f'filename="{md_filename}"' in dl_paper.headers.get("content-disposition", "")

    # 6. Discuss research endpoint
    discuss_payload = {
        "query": "What is the latency trade-off on NVIDIA Jetson Orin?",
        "dataset": "examples/velodyne_000008.bin",
    }
    resp = client.post("/api/research/discuss", json=discuss_payload)
    assert resp.status_code == 200
    disc_data = resp.json()
    assert disc_data["status"] == "success"
    assert "Jetson" in disc_data["response"] or "Orin" in disc_data["response"]

    # 7. List artifacts endpoint
    resp = client.get("/api/research/artifacts")
    assert resp.status_code == 200
    artifacts = resp.json()
    assert "notebooks" in artifacts
    assert "reports" in artifacts
    assert len(artifacts["notebooks"]) > 0
    assert len(artifacts["reports"]) > 0
