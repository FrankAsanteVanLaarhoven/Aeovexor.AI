"""
Spatial Policy & Compliance Engine Microservice
Enforces privacy zoning, automated PII redaction rules, and spatial data
export restrictions according to enterprise regulatory compliance standards.
"""

from typing import List, Dict, Any, Optional
from schemas.spatial_schema import PolicyRule, BoundingBox3D, FaceDetection


class PolicyEngine:
    def __init__(self):
        self.rules: Dict[str, PolicyRule] = {
            "RULE_PUBLIC_DEF": PolicyRule(
                rule_id="RULE_PUBLIC_DEF",
                description="Public operational zone requires face blur and restricts raw point export",
                zone_type="PUBLIC",
                require_face_blur=True,
                allow_raw_sensor_export=False,
                max_retention_days=14,
            ),
            "RULE_RESTRICTED_DEF": PolicyRule(
                rule_id="RULE_RESTRICTED_DEF",
                description="Industrial / testing ground zone permits raw sensor export under authorization",
                zone_type="RESTRICTED",
                require_face_blur=True,
                allow_raw_sensor_export=True,
                max_retention_days=90,
            ),
        }

    def evaluate_export_permission(self, zone_type: str, user_role: str) -> bool:
        """Determines if a user or system is authorized to export raw unredacted sensor data."""
        if user_role == "admin" or user_role == "researcher":
            return True
        rule = self.rules.get(f"RULE_{zone_type}_DEF")
        if rule:
            return rule.allow_raw_sensor_export
        return False

    def enforce_face_redaction(self, faces: List[FaceDetection], zone_type: str) -> List[FaceDetection]:
        """Ensures all faces are blurred if the active zone requires privacy preservation."""
        rule = self.rules.get(f"RULE_{zone_type}_DEF")
        if rule and rule.require_face_blur:
            for face in faces:
                face.blurred = True
        return faces
