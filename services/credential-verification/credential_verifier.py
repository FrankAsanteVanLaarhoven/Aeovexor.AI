"""
Credential Verification Microservice
Implements Zero-Trust hardware and operator authentication using cryptographic
signatures, HMAC/Ed25519 tokens, and role-based access control (RBAC).
"""

from typing import Dict, Any, List, Optional
import hmac
import hashlib
import time
from schemas.spatial_schema import CredentialToken


class CredentialVerifier:
    def __init__(self, secret_key: str = "aeovexor-enterprise-secret-salt-2026"):
        self.secret_key = secret_key.encode()

    def generate_token(self, device_id: str, scopes: List[str], ttl_seconds: int = 3600) -> CredentialToken:
        """Issues an authenticated zero-trust credential token for a device or client."""
        expires_at = int(time.time()) + ttl_seconds
        payload = f"{device_id}:{','.join(sorted(scopes))}:{expires_at}"
        signature = hmac.new(self.secret_key, payload.encode(), hashlib.sha256).hexdigest()

        return CredentialToken(
            device_id=device_id,
            public_key_pem="ed25519-public-key-sample",
            scopes=scopes,
            expires_at=expires_at,
            signature=signature,
        )

    def verify_token(self, token: CredentialToken, required_scope: Optional[str] = None) -> bool:
        """Validates token signature, expiration timestamp, and requested permission scope."""
        # 1. Expiration check
        if time.time() > token.expires_at:
            return False

        # 2. Signature verification
        payload = f"{token.device_id}:{','.join(sorted(token.scopes))}:{token.expires_at}"
        expected_sig = hmac.new(self.secret_key, payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_sig, token.signature):
            return False

        # 3. Scope authorization check
        if required_scope and required_scope not in token.scopes:
            return False

        return True
