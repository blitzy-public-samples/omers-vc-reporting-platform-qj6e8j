# src/backend/authentication_service/tests/test_security_cors.py

"""
CORS regression tests for the authentication service.

This module addresses the following requirement:
- Authentication and Authorization Implementation (Technical Requirements/Feature 4: Authentication and Authorization Implementation)

Security control verified: Cross-Origin Resource Sharing (CWE-942). Prior to
remediation the service configured ``allow_origins=["*"]`` together with
``allow_credentials=True``. These tests prove that the service now reflects only
explicitly configured origins and never emits
``Access-Control-Allow-Origin: *`` together with
``Access-Control-Allow-Credentials: true``.
"""

import os

# Import-time ordering constraint:
# config.py validates required settings when it is imported (it raises if
# SECRET_KEY is missing or shorter than 32 characters, or if DATABASE_URL is
# missing), and main.py -> app/security.py invoke load_config() during import.
# The required environment variables must therefore be defined BEFORE importing
# create_app. SECRET_KEY and DATABASE_URL use setdefault so an externally
# supplied value (e.g. from CI) is preserved; CORS_ORIGINS is set explicitly so
# the allowed origin under test is deterministic.
os.environ.setdefault("SECRET_KEY", "test-secret-key-thirty-two-chars-min-000")
os.environ.setdefault("DATABASE_URL", "postgresql://user:pass@localhost:5432/testdb")
os.environ["CORS_ORIGINS"] = "http://localhost:3000"

import pytest
from fastapi.testclient import TestClient

from src.backend.authentication_service.main import create_app

# The single configured (trusted) origin under test; matches CORS_ORIGINS above.
ALLOWED_ORIGIN = "http://localhost:3000"
# An untrusted origin that must never be reflected back to the caller.
UNTRUSTED_ORIGIN = "http://evil.example.com"


@pytest.fixture(scope="module")
def client():
    """Return a TestClient bound to a freshly constructed application."""
    return TestClient(create_app())


@pytest.mark.parametrize("path", ["/protected", "/token"])
def test_cors_never_wildcard_with_credentials(client, path):
    """No preflight response may reflect an untrusted origin or a wildcard.

    Guards the exact CWE-942 combination (wildcard origin with credentials)
    across the service's routed paths. With credentials enabled Starlette echoes
    the *specific* origin on preflight, so asserting only ``!= "*"`` would hold
    even in a wildcard-injected state; asserting the untrusted origin is not
    reflected makes this test sensitive to that regression.
    """
    response = client.options(
        path,
        headers={
            "Origin": UNTRUSTED_ORIGIN,
            "Access-Control-Request-Method": "GET",
        },
    )
    acao = response.headers.get("access-control-allow-origin")
    assert acao != "*"
    assert acao != UNTRUSTED_ORIGIN


def test_cors_allows_configured_origin_preflight(client):
    """A preflight from the configured origin is reflected with credentials."""
    response = client.options(
        "/protected",
        headers={
            "Origin": ALLOWED_ORIGIN,
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers.get("access-control-allow-origin") == ALLOWED_ORIGIN
    assert response.headers.get("access-control-allow-credentials") == "true"


def test_cors_rejects_untrusted_origin_preflight(client):
    """A preflight from an untrusted origin is neither reflected nor '*'."""
    response = client.options(
        "/protected",
        headers={
            "Origin": UNTRUSTED_ORIGIN,
            "Access-Control-Request-Method": "GET",
        },
    )
    acao = response.headers.get("access-control-allow-origin")
    assert acao != "*"
    assert acao != UNTRUSTED_ORIGIN


def test_cors_allows_configured_origin_simple_request(client):
    """A simple GET from the configured origin is reflected, never as '*'."""
    response = client.get("/protected", headers={"Origin": ALLOWED_ORIGIN})
    acao = response.headers.get("access-control-allow-origin")
    assert acao == ALLOWED_ORIGIN
    assert acao != "*"
    assert response.headers.get("access-control-allow-credentials") == "true"


def test_cors_rejects_untrusted_origin_simple_request(client):
    """A simple GET from an untrusted origin is neither reflected nor '*'."""
    response = client.get("/protected", headers={"Origin": UNTRUSTED_ORIGIN})
    acao = response.headers.get("access-control-allow-origin")
    assert acao != "*"
    assert acao != UNTRUSTED_ORIGIN
