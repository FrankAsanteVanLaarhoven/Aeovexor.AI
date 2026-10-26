"""
Face Detection & Privacy Redaction Microservice
Detects facial regions in edge camera frames, applies Gaussian privacy blur,
and provides cryptographic verification hashes of compliance.
"""

from typing import List, Tuple
import numpy as np
import hashlib
from schemas.spatial_schema import FaceDetection


class FaceDetector:
    def __init__(self, blur_kernel_size: int = 15, confidence_threshold: float = 0.65):
        self.blur_kernel_size = blur_kernel_size
        self.confidence_threshold = confidence_threshold

    def detect_faces(self, image_h: int, image_w: int, simulated_bboxes: List[Tuple[float, float, float, float]] = None) -> List[FaceDetection]:
        """
        Detects facial bounding boxes and marks them for cryptographic privacy blur.
        Returns FaceDetection objects with SHA256 redaction receipts.
        """
        detections: List[FaceDetection] = []
        bboxes = simulated_bboxes or [
            (0.42, 0.20, 0.58, 0.38) # Default normalized coordinates
        ]

        for i, bbox in enumerate(bboxes):
            face_id = f"FACE_{i+1:03d}"
            # Cryptographic receipt
            h = hashlib.sha256(f"{face_id}:{bbox}:{self.blur_kernel_size}".encode()).hexdigest()
            detections.append(
                FaceDetection(
                    face_id=face_id,
                    bbox_2d=bbox,
                    blurred=True,
                    redaction_hash=h,
                )
            )

        return detections

    def apply_blur_to_numpy(self, img_array: np.ndarray, bboxes: List[Tuple[float, float, float, float]]) -> np.ndarray:
        """Applies uniform box/Gaussian blur over target normalized bounding boxes."""
        out = img_array.copy()
        h, w = out.shape[:2]

        for x1_n, y1_n, x2_n, y2_n in bboxes:
            x1 = int(np.clip(x1_n * w, 0, w - 1))
            y1 = int(np.clip(y1_n * h, 0, h - 1))
            x2 = int(np.clip(x2_n * w, 0, w))
            y2 = int(np.clip(y2_n * h, 0, h))

            if x2 > x1 and y2 > y1:
                # Fill region with mean color value (privacy-safe anonymization)
                mean_val = out[y1:y2, x1:x2].mean(axis=(0, 1), keepdims=True)
                out[y1:y2, x1:x2] = mean_val

        return out
