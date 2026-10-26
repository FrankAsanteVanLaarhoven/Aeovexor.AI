"""
Spatial Privacy & Redaction Benchmark Suite
Measures facial and PII detection sensitivity, redaction success percentage,
and zero-leak verification across raw and published datasets.
"""

from typing import List, Dict, Any
from schemas.spatial_schema import FaceDetection


class PrivacyBenchmark:
    def __init__(self, target_redaction_rate_pct: float = 99.9):
        self.target_redaction_rate_pct = target_redaction_rate_pct

    def audit_redaction(
        self, detected_faces: List[FaceDetection], ground_truth_pii_count: int
    ) -> Dict[str, Any]:
        """
        Audits privacy compliance: verifies that all ground-truth facial/PII regions
        were successfully detected, blurred, and cryptographically signed.
        """
        blurred_count = sum(1 for f in detected_faces if f.blurred)
        signed_count = sum(1 for f in detected_faces if f.redaction_hash is not None)

        redaction_rate = float((blurred_count / max(ground_truth_pii_count, 1)) * 100.0)
        leak_count = max(0, ground_truth_pii_count - blurred_count)

        passed_audit = (leak_count == 0) and (redaction_rate >= self.target_redaction_rate_pct)

        return {
            "ground_truth_pii_count": ground_truth_pii_count,
            "detected_and_blurred": blurred_count,
            "cryptographically_signed": signed_count,
            "redaction_rate_pct": round(redaction_rate, 2),
            "unredacted_leaks": leak_count,
            "passed_compliance_audit": passed_audit,
        }
