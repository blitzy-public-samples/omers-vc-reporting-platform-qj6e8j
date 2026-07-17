# src/backend/authentication_service/tests/test_security_cors.py

"""CORS regression tests for the authentication service (CWE-942).

Assert the real application never returns ``Access-Control-Allow-Origin: *``
together with ``Access-Control-Allow-Credentials: true``, reflects only the
configured origin, and rejects untrusted origins. Environment provisioning and
restoration are handled by the service-level conftest.
"""

import pytest
from fastapi.testclient import TestClient

from src.backend.authentication_service.main import create_app

# The configured (trusted) origin under test; matches CORS_ORIGINS in conftest.
ALLOWED_ORIGIN = "http://localhost:3000"
# An untrusted origin that must never be reflected back to the caller.
UNTRUSTED_ORIGIN = "http://evil.example.com"


@pytest.fixture(scope="module")
def client():
    """TestClient bound to a freshly constructed application."""
    return TestClient(create_app())


# Preflight method matches each route's real verb: /protected is GET, /token is POST.
@pytest.mark.parametrize("path,method", [("/protected", "GET"), ("/token", "POST")])
def test_cors_never_wildcard_with_credentials(client, path, method):
    """No preflight response may carry Access-Control-Allow-Origin '*'."""
    response = client.options(
        path,
        headers={
            "Origin": UNTRUSTED_ORIGIN,
            "Access-Control-Request-Method": method,
        },
    )
    assert response.headers.get("access-control-allow-origin") != "*"


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
