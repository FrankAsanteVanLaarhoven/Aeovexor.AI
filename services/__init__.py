"""
Aeovexor.AI Enterprise Services Module Exporter
Provides clean top-level imports for all vision, spatial, and policy microservices.
"""

import importlib.util
import sys
from pathlib import Path

_SERVICES_DIR = Path(__file__).parent


def _import_from_subpath(module_name: str, rel_path: str):
    file_path = _SERVICES_DIR / rel_path
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {file_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


# Dynamically load services with hyphenated directory names
ingest_mod = _import_from_subpath("services.ingestion", "ingestion/ingest_service.py")
person_mod = _import_from_subpath("services.person_detection", "person-detection/person_detector.py")
face_mod = _import_from_subpath("services.face_detection", "face-detection/face_detector.py")
pose_mod = _import_from_subpath("services.pose_estimation", "pose-estimation/pose_estimator.py")
human_seg_mod = _import_from_subpath("services.human_segmentation", "human-segmentation/human_segmentor.py")
obj_mod = _import_from_subpath("services.object_detection", "object-detection/object_detector.py")
tracker_mod = _import_from_subpath("services.temporal_tracking", "temporal-tracking/tracker.py")
occlusion_mod = _import_from_subpath("services.occlusion_reasoning", "occlusion-reasoning/occlusion_engine.py")
metadata_mod = _import_from_subpath("services.metadata_engine", "metadata-engine/metadata_engine.py")
credential_mod = _import_from_subpath("services.credential_verification", "credential-verification/credential_verifier.py")
policy_mod = _import_from_subpath("services.policy_engine", "policy-engine/policy_engine.py")

IngestionService = ingest_mod.IngestionService
PersonDetector = person_mod.PersonDetector
FaceDetector = face_mod.FaceDetector
PoseEstimator = pose_mod.PoseEstimator
HumanSegmentor = human_seg_mod.HumanSegmentor
ObjectDetector = obj_mod.ObjectDetector
TemporalTracker = tracker_mod.TemporalTracker
OcclusionEngine = occlusion_mod.OcclusionEngine
MetadataEngine = metadata_mod.MetadataEngine
CredentialVerifier = credential_mod.CredentialVerifier
PolicyEngine = policy_mod.PolicyEngine

__all__ = [
    "IngestionService",
    "PersonDetector",
    "FaceDetector",
    "PoseEstimator",
    "HumanSegmentor",
    "ObjectDetector",
    "TemporalTracker",
    "OcclusionEngine",
    "MetadataEngine",
    "CredentialVerifier",
    "PolicyEngine",
]
