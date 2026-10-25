PYTHON ?= /Library/Frameworks/Python.framework/Versions/3.11/bin/python3
UVICORN ?= /Library/Frameworks/Python.framework/Versions/3.11/bin/uvicorn
PORT ?= 8765
HOST ?= 127.0.0.1

.PHONY: help install test test-all studio benchmark verify-gaps slam detect segment nav twin clean build-cpp build-rust build-go build-all telemetry-service

help:
	@echo "AEOVEXOR 3D Spatial Intelligence Platform & Universal Testbed"
	@echo "============================================================="
	@echo "POLYGLOT CORE: C++ (SIMD/CSF) · Rust (Zero-Copy) · Go (Telemetry) · Python (FastAPI/AI)"
	@echo "  make build-all    - Build C++, Rust, and Go native acceleration binaries"
	@echo "  make build-cpp    - Compile C++ SIMD shared library & test suite"
	@echo "  make build-rust   - Compile Rust zero-copy LiDAR CLI & cdylib"
	@echo "  make build-go     - Compile Go high-concurrency telemetry streaming service"
	@echo "  make test-all     - Run full polyglot test suite across Python, C++, Rust, and Go"
	@echo "  make telemetry-service - Launch Go telemetry streaming daemon on :8766"
	@echo "  make test         - Run Python unit and mathematical regression tests"
	@echo "  make studio       - Launch FastAPI & Uvicorn Research Console on $(HOST):$(PORT)"
	@echo "  make clean        - Remove caches and build artifacts"

build-cpp:
	mkdir -p native/cpp/build && cd native/cpp/build && cmake .. && make

build-rust:
	cd native/rust && cargo build --release

build-go:
	cd services/go-telemetry && go build -o aeovexor-telemetry-service .

build-all: build-cpp build-rust build-go

test-all:
	@echo "=== [1/4] Running C++ Native Core Tests ==="
	cd native/cpp/build && ./test_spatialforge_cpp
	@echo "=== [2/4] Running Rust Spatial Core Tests ==="
	cd native/rust && cargo test
	@echo "=== [3/4] Running Go Telemetry Engine Tests ==="
	cd services/go-telemetry && go test -v ./...
	@echo "=== [4/4] Running Python & Polyglot Integration Tests ==="
	PYTHONPATH=. $(PYTHON) -m pytest -v tests

telemetry-service:
	./services/go-telemetry/aeovexor-telemetry-service --port 8766

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
