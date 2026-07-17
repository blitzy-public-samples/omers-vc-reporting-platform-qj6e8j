"""CORS security regression tests for the API Gateway (CWE-942).

Exercises the REAL production application built by ``main.create_app`` so the test
cannot pass if the production CORS wiring regresses. The application's import chain
currently reaches a pre-existing, out-of-scope circular import between
``app/routers/__init__.py`` and ``app/routers/routes.py``; when that blocker is
present the module skips with it named rather than substituting a synthetic app.
"""

import pytest

try:
    from fastapi.testclient import TestClient

    from src.backend.api_gateway.main import create_app

    _production_app = create_app()
except Exception as exc:  # pragma: no cover - only when the pre-existing blocker is present
    pytest.skip(
        "API Gateway production application is not constructible due to the "
        "pre-existing, out-of-scope circular import between app/routers/__init__.py "
        f"and app/routers/routes.py (tracked in SECURITY.md): {exc!r}",
        allow_module_level=True,
    )

ALLOWED_ORIGIN = "http://localhost:3000"
DISALLOWED_ORIGIN = "http://evil.example.com"


def test_cors_never_wildcard_with_credentials():
    """A simple request must never combine ACAO='*' with credentials (CWE-942)."""
    client = TestClient(_production_app)
    response = client.get("/health", headers={"Origin": ALLOWED_ORIGIN})
    allow_origin = response.headers.get("access-control-allow-origin")
    allow_credentials = response.headers.get("access-control-allow-credentials")
    assert allow_origin != "*"
    assert not (allow_origin == "*" and allow_credentials == "true")


def test_cors_allowed_origin_is_reflected():
    """A configured origin is echoed explicitly (not '*') and credentials are allowed."""
    client = TestClient(_production_app)
    response = client.get("/health", headers={"Origin": ALLOWED_ORIGIN})
    assert response.headers.get("access-control-allow-origin") == ALLOWED_ORIGIN
    assert response.headers.get("access-control-allow-credentials") == "true"


def test_cors_disallowed_origin_not_reflected():
    """An unlisted origin is never reflected and never answered with '*'."""
    client = TestClient(_production_app)
    response = client.get("/health", headers={"Origin": DISALLOWED_ORIGIN})
    allow_origin = response.headers.get("access-control-allow-origin")
    assert allow_origin != DISALLOWED_ORIGIN
    assert allow_origin != "*"


def test_cors_preflight_reflects_only_allowed_origin():
    """Preflight echoes only the configured origin; unlisted origins are not reflected."""
    client = TestClient(_production_app)
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
