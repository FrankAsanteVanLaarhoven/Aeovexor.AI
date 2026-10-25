PYTHON ?= /Library/Frameworks/Python.framework/Versions/3.11/bin/python3
UVICORN ?= /Library/Frameworks/Python.framework/Versions/3.11/bin/uvicorn
PORT ?= 8765
HOST ?= 127.0.0.1

.PHONY: help install test studio benchmark verify-gaps slam detect segment nav twin clean

help:
	@echo "AEOVEXOR 3D Spatial Intelligence Platform & Universal Testbed"
	@echo "============================================================="
	@echo "PERCEIVE · RECONSTRUCT · UNDERSTAND"
	@echo "  make install      - Install package with workspace, dev, and full extras"
	@echo "  make test         - Run all 23 unit & mathematical regression tests"
	@echo "  make studio       - Launch FastAPI & Uvicorn Research Console on $(HOST):$(PORT)"
	@echo "  make benchmark    - Run E1-E5 research experiment suite on Velodyne"
	@echo "  make verify-gaps  - Verify all 8 critical blueprint research gaps"
	@echo "  make slam         - Run 3D mapping and SLAM trajectory reconstruction"
	@echo "  make detect       - Run 3D object detection (vehicles, people, obstacles)"
	@echo "  make segment      - Run point-cloud semantic surface segmentation"
	@echo "  make nav          - Run autonomous navigation clearance & traversability"
	@echo "  make twin         - Generate digital twin watertight TSDF surface mesh"
	@echo "  make clean        - Remove caches and build artifacts"

install:
	$(PYTHON) -m pip install -e ".[workspace,dev,full]"

test:
	PYTHONPATH=. $(PYTHON) -m pytest -v tests

studio:
	PYTHONPATH=. $(UVICORN) workspace.server:app --host $(HOST) --port $(PORT) --reload

benchmark:
	PYTHONPATH=. $(PYTHON) -m spatialforge.cli experiment examples/velodyne_000008.bin

verify-gaps:
	PYTHONPATH=. $(PYTHON) -m spatialforge.cli verify-gaps

slam:
	PYTHONPATH=. $(PYTHON) -m spatialforge.cli slam examples/velodyne_000008.bin examples/velodyne_000008.bin

detect:
	PYTHONPATH=. $(PYTHON) -m spatialforge.cli detect examples/velodyne_000008.bin

segment:
	PYTHONPATH=. $(PYTHON) -m spatialforge.cli segment examples/velodyne_000008.bin

nav:
	PYTHONPATH=. $(PYTHON) -m spatialforge.cli nav examples/velodyne_000008.bin

twin:
	PYTHONPATH=. $(PYTHON) -m spatialforge.cli twin examples/velodyne_000008.bin --export-obj artifacts/twin_mesh.obj

clean:
	rm -rf .pytest_cache __pycache__ *.egg-info build dist
