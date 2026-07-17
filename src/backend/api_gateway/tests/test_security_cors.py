"""
CORS security regression tests for the API Gateway (CWE-942).

Guards against reintroduction of an overly-permissive CORS policy that combines
a wildcard origin (allow_origins=["*"]) with allow_credentials=True.
"""

# config.py instantiates settings at import time and the authentication_service
# config enforces a >=32 character SECRET_KEY, so the required environment must
# be present BEFORE importing the application module below.
import os

os.environ.setdefault("DATABASE_URL", "postgresql://user:pass@localhost:5432/testdb")
os.environ.setdefault("API_KEY", "test-api-key")
os.environ.setdefault("SECRET_KEY", "test-secret-key-at-least-32-characters-long")
os.environ.setdefault("CORS_ALLOW_ORIGINS", "http://localhost:3000")

# The application uses absolute ``src.backend...`` imports; ensure the repository
# root is importable regardless of the current working directory.
import sys

_REPO_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

# Import the application only after the environment is configured.
from fastapi.testclient import TestClient

from src.backend.api_gateway.main import create_app

ALLOWED_ORIGIN = "http://localhost:3000"
DISALLOWED_ORIGIN = "http://evil.example.com"

client = TestClient(create_app())


def test_cors_never_wildcard_with_credentials():
    """A simple request must never combine ACAO='*' with credentials (CWE-942)."""
    response = client.get("/health", headers={"Origin": ALLOWED_ORIGIN})
    allow_origin = response.headers.get("access-control-allow-origin")
    allow_credentials = response.headers.get("access-control-allow-credentials")
    assert allow_origin != "*"
    assert not (allow_origin == "*" and allow_credentials == "true")


def test_cors_allowed_origin_is_reflected():
    """A configured origin is echoed explicitly (not '*'); credentials are allowed."""
    response = client.get("/health", headers={"Origin": ALLOWED_ORIGIN})
    assert response.headers.get("access-control-allow-origin") == ALLOWED_ORIGIN
    allow_credentials = response.headers.get("access-control-allow-credentials")
    if allow_credentials is not None:
        assert allow_credentials == "true"


def test_cors_disallowed_origin_not_reflected():
    """An unlisted origin is never reflected and never answered with '*'."""
    response = client.get("/health", headers={"Origin": DISALLOWED_ORIGIN})
    allow_origin = response.headers.get("access-control-allow-origin")
    assert allow_origin != DISALLOWED_ORIGIN
    assert allow_origin != "*"


def test_cors_preflight_reflects_only_allowed_origin():
    """Preflight echoes only the configured origin; unlisted origins are not reflected."""
    allowed = client.options(
        "/health",
        headers={
            "Origin": ALLOWED_ORIGIN,
            "Access-Control-Request-Method": "GET",
        },
    )
    assert allowed.headers.get("access-control-allow-origin") == ALLOWED_ORIGIN

    denied = client.options(
        "/health",
        headers={
            "Origin": DISALLOWED_ORIGIN,
            "Access-Control-Request-Method": "GET",
        },
    )
    denied_origin = denied.headers.get("access-control-allow-origin")
    assert denied_origin != DISALLOWED_ORIGIN
    assert denied_origin != "*"
