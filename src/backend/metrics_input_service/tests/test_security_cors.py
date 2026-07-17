"""CORS security regression tests for the metrics-input service (CWE-942).

Security control verified: Cross-Origin Resource Sharing (CWE-942, Overly
Permissive CORS). These tests exercise the control at two layers:

1. The REAL application built by ``main.create_app`` — the production
   ``CORSMiddleware`` wiring is constructed and driven with a live
   ``TestClient``. A configured origin is reflected with credentials enabled,
   while an untrusted origin is never reflected and never answered with ``*``.
2. The ``CORS_ORIGINS`` validator on ``config.Settings`` — the shipped default
   is explicit and non-wildcard, wildcard/empty/malformed allow-lists fail
   closed, and both a comma-separated and a JSON-array environment value are
   accepted (the operator-ergonomics fix, F-CORS-FMT).

The application package now imports cleanly (the stray Markdown fence in
``app/__init__.py`` and the ``config`` <-> ``app.routers.metrics`` circular
import have been removed), so no ``sys.modules`` stubbing of the application is
required. Rationale detail lives in ``docs/security/decision-log.md``.
"""

import os

# config.py builds a module-level ``settings = load_settings()`` at import time and
# ``Settings`` requires these non-security fields. Provision them with setdefault so an
# externally supplied value (e.g. from CI) is preserved, BEFORE importing the app.
os.environ.setdefault("database_url", "postgresql://user:pass@localhost:5432/testdb")
os.environ.setdefault("api_key", "test-api-key")
os.environ.setdefault("log_level", "INFO")
# Hard-set (not setdefault) so the real app's allow-list is exactly ALLOWED_ORIGIN.
# create_app() reads this at construction time, so an ambient CORS_ORIGINS cannot make
# the positive-reflection assertions non-deterministic.
os.environ["CORS_ORIGINS"] = "http://localhost:3000"

# The application uses absolute ``src.backend...`` imports; ensure the repository
# root is importable regardless of the current working directory.
import sys

_REPO_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

# Import the application and settings only after the environment is configured.
from src.backend.metrics_input_service.main import create_app
from src.backend.metrics_input_service.config import Settings

ALLOWED_ORIGIN = "http://localhost:3000"
DISALLOWED_ORIGIN = "http://evil.example.com"

# A path guaranteed not to hit the database. Preflight (OPTIONS) is answered by
# CORSMiddleware without routing, and a simple GET to an unmatched path returns 404
# with the CORS headers the middleware attaches -- neither touches ``get_db``.
_PROBE_PATH = "/api/v1/metrics/metrics/"

client = TestClient(create_app())


# --------------------------------------------------------------------------- #
# Real-application CORSMiddleware behavior (production wiring in main.create_app)
# --------------------------------------------------------------------------- #

def test_real_app_cors_never_wildcard_with_credentials():
    """A simple request must never combine ACAO='*' with credentials (CWE-942)."""
    response = client.get("/", headers={"Origin": ALLOWED_ORIGIN})
    allow_origin = response.headers.get("access-control-allow-origin")
    allow_credentials = response.headers.get("access-control-allow-credentials")
    assert allow_origin != "*"
    assert not (allow_origin == "*" and allow_credentials == "true")


def test_real_app_allowed_origin_reflected_with_credentials():
    """A configured origin is echoed explicitly (not '*'); credentials are allowed."""
    response = client.get("/", headers={"Origin": ALLOWED_ORIGIN})
    # Assert credentials unconditionally so an allow_credentials=False regression is
    # detected; a guarded 'if header is not None' check would silently pass when the
    # header disappears. Credentialed CORS requires this header to be exactly 'true'.
    assert response.headers.get("access-control-allow-origin") == ALLOWED_ORIGIN
    assert response.headers.get("access-control-allow-credentials") == "true"


def test_real_app_disallowed_origin_not_reflected():
    """An unlisted origin is never reflected and never answered with '*'."""
    response = client.get("/", headers={"Origin": DISALLOWED_ORIGIN})
    allow_origin = response.headers.get("access-control-allow-origin")
    assert allow_origin != DISALLOWED_ORIGIN
    assert allow_origin != "*"


def test_real_app_preflight_reflects_only_allowed_origin():
    """Preflight echoes only the configured origin (exactly, not '*')."""
    allowed = client.options(
        _PROBE_PATH,
        headers={
            "Origin": ALLOWED_ORIGIN,
            "Access-Control-Request-Method": "GET",
        },
    )
    assert allowed.headers.get("access-control-allow-origin") == ALLOWED_ORIGIN
    assert allowed.headers.get("access-control-allow-origin") != "*"


def test_real_app_preflight_disallowed_origin_not_reflected():
    """Preflight for an unlisted origin is not reflected and never '*'."""
    denied = client.options(
        _PROBE_PATH,
        headers={
            "Origin": DISALLOWED_ORIGIN,
            "Access-Control-Request-Method": "GET",
        },
    )
    denied_origin = denied.headers.get("access-control-allow-origin")
    assert denied_origin != DISALLOWED_ORIGIN
    assert denied_origin != "*"


# --------------------------------------------------------------------------- #
# CORS_ORIGINS validator on the real Settings class (config layer, no stubs)
# --------------------------------------------------------------------------- #

_REQUIRED_FIELDS = {
    "database_url": "postgresql://user:pass@localhost:5432/testdb",
    "api_key": "test-api-key",
    "log_level": "INFO",
}


def _make_settings(**overrides):
    """Construct Settings with required fields supplied and .env reading disabled.

    Init kwargs take precedence over the environment in Pydantic v1, so any
    ``CORS_ORIGINS`` override passed here is deterministic regardless of ambient env.
    """
    params = dict(_REQUIRED_FIELDS)
    params.update(overrides)
    return Settings(_env_file=None, **params)


def test_default_cors_origins_not_wildcard(monkeypatch):
    # The shipped default allow-list must be explicit, non-empty, and never "*".
    monkeypatch.delenv("CORS_ORIGINS", raising=False)
    settings = _make_settings()
    assert "*" not in settings.CORS_ORIGINS
    assert len(settings.CORS_ORIGINS) >= 1
    assert settings.CORS_ORIGINS == ["http://localhost:3000", "https://localhost:3000"]


def test_wildcard_string_rejected():
    # A bare "*" origin must fail closed (CWE-942).
    with pytest.raises(ValidationError):
        _make_settings(CORS_ORIGINS="*")


def test_wildcard_only_list_rejected():
    # A list whose only entry is the wildcard must fail closed.
    with pytest.raises(ValidationError):
        _make_settings(CORS_ORIGINS=["*"])


def test_list_containing_wildcard_rejected():
    # A wildcard mixed with an otherwise valid origin must still fail closed.
    with pytest.raises(ValidationError):
        _make_settings(CORS_ORIGINS=["http://localhost:3000", "*"])


def test_empty_cors_origins_rejected():
    # An empty allow-list must fail closed rather than fall back to permissive.
    with pytest.raises(ValidationError):
        _make_settings(CORS_ORIGINS=[])


def test_malformed_origin_rejected():
    # An origin without an http(s) scheme and host must be rejected.
    with pytest.raises(ValidationError):
        _make_settings(CORS_ORIGINS=["not-a-url"])


def test_explicit_allowlist_accepted():
    # An explicit http(s) allow-list is accepted and never contains "*".
    settings = _make_settings(CORS_ORIGINS=["https://app.example.com"])
    assert settings.CORS_ORIGINS == ["https://app.example.com"]
    assert "*" not in settings.CORS_ORIGINS


def test_comma_separated_env_accepted(monkeypatch):
    # F-CORS-FMT: a comma-separated CORS_ORIGINS env value must be accepted (it must
    # NOT raise SettingsError as the old ``list`` field type did). It reaches the
    # validator as a string and is split into an explicit allow-list.
    monkeypatch.setenv(
        "CORS_ORIGINS", "https://a.example.com,https://b.example.com"
    )
    settings = Settings(_env_file=None, **_REQUIRED_FIELDS)
    assert settings.CORS_ORIGINS == ["https://a.example.com", "https://b.example.com"]
    assert "*" not in settings.CORS_ORIGINS


def test_json_array_env_accepted(monkeypatch):
    # F-CORS-FMT: a JSON-array CORS_ORIGINS env value must also still be accepted, so
    # the change is backward compatible with the previously documented format.
    monkeypatch.setenv("CORS_ORIGINS", '["https://a.example.com"]')
    settings = Settings(_env_file=None, **_REQUIRED_FIELDS)
    assert settings.CORS_ORIGINS == ["https://a.example.com"]
    assert "*" not in settings.CORS_ORIGINS


def test_shipped_settings_default_not_wildcard():
    # The module-level settings instance actually used by the service is non-wildcard.
    from src.backend.metrics_input_service.config import settings as shipped_settings
    assert "*" not in shipped_settings.CORS_ORIGINS
    assert len(shipped_settings.CORS_ORIGINS) >= 1
