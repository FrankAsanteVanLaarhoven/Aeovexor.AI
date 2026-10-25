# Research programme and deployment gates

## Phase 1: ingestion and provenance (weeks 1-2)
Add ROS 2 Humble PointCloud2/TF2/bag2 adapter in a ROS-specific package; enforce units, coordinate conventions, clock offsets, calibration IDs, sequence digests, and reproducible scene splits. Acceptance: 100% schema validation and exact sample counts.

## Phase 2: baselines (weeks 3-4)
Evaluate tuned DBSCAN, HDBSCAN, OPTICS, voxel filtering, PCA and point-to-point ICP on independent scene-held-out real sequences. Save search spaces and tuning budgets. Acceptance: three independent reruns and full provenance.

## Phase 3: registration and mapping (weeks 5-7)
Add GICP, NDT, TEASER++, KISS-ICP and RTAB-Map as pinned, external adapters. Compute ATE, RPE, loop-closure precision/recall, map completeness, dynamic-scene failures, and p95 latency. No pose alignment without reporting aligned/unaligned variants.

## Phase 4: learning (weeks 8-10)
Add SemanticKITTI and nuScenes dataset adapters with official split metadata and label remapping; Point Transformer and sparse convolution baseline; report mIoU, per-class IoU, class balance, latency, energy, memory, and out-of-domain performance.

## Phase 5: publication (weeks 11-12)
Frozen evaluation container, dataset licenses, reproducible seeds, bootstrap CIs over sequences, ablations, failure taxonomy, risk register, model/data cards and independent replication. Publish only after real-data measurements.

## SMART research targets (proposed, not measured)
- Within 2 weeks: 100% input validation across a 50-file fixture suite.
- Within 4 weeks: 3 clustering baselines on 3 held-out sequences with recorded runtime and ARI.
- Within 7 weeks: 2 SLAM baselines with synchronized ground truth and ATE/RPE.
- Within 10 weeks: 2 semantic segmentation baselines and mIoU on an official split.
- Within 12 weeks: 3 reruns, 95% sequence-bootstrap confidence intervals and zero missing provenance fields.

## Risks
Density variation; pose convention errors; non-rigid objects; adverse weather; GPU/VRAM limits; dataset licenses; sensor timestamp drift; domain shift; overfitting to synthetic examples.
