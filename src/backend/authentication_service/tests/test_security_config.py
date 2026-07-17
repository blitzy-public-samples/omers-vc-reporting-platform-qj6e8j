# src/backend/authentication_service/tests/test_security_config.py

"""
JWT security regression tests for the authentication service.

Security control verified: JWT decoding is restricted to HS256 (CWE-347 /
CVE-2022-29217, algorithm confusion). These tests forge an ``alg=none`` token and
drive it through the *production* decode path -- the ``/protected`` route of the
application returned by ``create_app`` calls ``app/security.py::validate_token``,
whose sole ``jwt.decode(..., algorithms=["HS256"])`` site is the control under
test. A positive control (a genuine HS256 token is accepted) guarantees the
negative assertions are not vacuously green, so a regression that widened the
accepted algorithm set (e.g. permitting ``none``) would be caught here.
"""

import base64
import json
import os

# Import-time ordering constraint mirrors tests/test_security_cors.py: config.py
# validates required settings at import (raises if SECRET_KEY is missing or < 32
# chars, or if DATABASE_URL is missing) and main.py -> app/security.py load the
# configuration during import. Provision the required environment BEFORE importing
# the application. SECRET_KEY/DATABASE_URL use setdefault so a CI-supplied value is
# preserved; CORS_ORIGINS is set explicitly for determinism.
os.environ.setdefault("SECRET_KEY", "test-secret-key-thirty-two-chars-min-000")
os.environ.setdefault("DATABASE_URL", "postgresql://user:pass@localhost:5432/testdb")
os.environ["CORS_ORIGINS"] = "http://localhost:3000"

# The application uses absolute ``src.backend...`` imports; ensure the repository
# root is importable regardless of the current working directory.
import sys

_REPO_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import jwt
import pytest
from fastapi.testclient import TestClient

from src.backend.authentication_service.app.security import (
    generate_token,
    validate_token,
)
from src.backend.authentication_service.main import create_app


@pytest.fixture(scope="module")
def client():
    """Return a TestClient bound to a freshly constructed application."""
    return TestClient(create_app())


def _forge_alg_none_token(payload):
    """Build an unsigned ``alg=none`` JWT (the classic algorithm-confusion forge).

    Constructed by hand rather than via ``jwt.encode`` so the test does not depend
    on the encoder's willingness to emit the ``none`` algorithm; it represents
    exactly what an attacker would submit.
    """

    def _b64(segment):
        raw = json.dumps(segment, separators=(",", ":")).encode("utf-8")
        return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")

    header = {"alg": "none", "typ": "JWT"}
    # A trailing dot with an empty signature is the wire format for alg=none.
    return f"{_b64(header)}.{_b64(payload)}."


def test_valid_hs256_token_is_accepted(client):
    """Positive control: a genuine HS256 token reaches the protected resource.

    Ensures the negative (forged-token) assertions below are meaningful rather
    than vacuously passing because every request is rejected.
    """
    token = generate_token("user123")
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "user123" in response.json()["message"]


def test_alg_none_forged_token_is_rejected(client):
    """A forged ``alg=none`` token must be rejected by the production decode path."""
    forged = _forge_alg_none_token({"sub": "attacker"})
    response = client.get("/protected", headers={"Authorization": f"Bearer {forged}"})
    assert response.status_code == 401


def test_validate_token_rejects_alg_none_directly():
    """The sole production decode site rejects an ``alg=none`` token (returns None).

    Exercises ``app/security.py::validate_token`` directly so a regression that
    dropped ``algorithms=["HS256"]`` (accepting ``none``) is detected even without
    the HTTP layer.
    """
    forged = _forge_alg_none_token({"sub": "attacker"})
    assert validate_token(forged) is None


def test_jwt_decode_restricted_to_hs256():
    """A token signed with a different algorithm (HS512) is not accepted as HS256.

    Confirms the decode site enforces the specific algorithm rather than any HMAC
    variant, guarding the algorithm-confusion class (CVE-2022-29217).
    """
    from src.backend.authentication_service.config import SECRET_KEY

    other_alg_token = jwt.encode({"sub": "attacker"}, SECRET_KEY, algorithm="HS512")
    assert validate_token(other_alg_token) is None
