"""CORS security regression tests for the metrics-input service.

Security control verified: Cross-Origin Resource Sharing (CWE-942, Overly
Permissive CORS). The service's configured CORS allow-list must never contain the
wildcard ``*``, must reject empty or malformed origin lists (fail closed), and must
accept only explicit http(s) origins. The control under test is the ``CORS_ORIGINS``
validator on ``config.Settings`` (and the shipped default it produces), which the
service's ``main.create_app`` passes to ``CORSMiddleware``.

``config.py`` imports cleanly on its own (it no longer pulls the application package),
so ``Settings`` is imported directly here rather than through any stub -- the real
production validator is exercised. Binding to the real ``main.create_app`` middleware
is attempted in ``test_real_app_*`` below; the application package has a pre-existing,
out-of-scope defect (``app/__init__.py`` contains a stray Markdown fence that raises
``SyntaxError``) that ``main.py`` imports at module scope. Per AAP 0.8.2 that
pre-existing non-security defect is not fixed here, so the real-factory test is marked
``xfail`` to keep the blocker visible rather than masking it behind a stub. Rationale
detail lives in ``docs/security/decision-log.md``.
"""

import os

import pytest
from pydantic import ValidationError

# config.py constructs a module-level ``settings = load_settings()`` at import time,
# which requires these non-security fields; supplied with setdefault so an externally
# supplied value (e.g. CI) is preserved.
os.environ.setdefault("database_url", "postgresql://user:pass@localhost:5432/testdb")
os.environ.setdefault("api_key", "test-api-key")
os.environ.setdefault("log_level", "INFO")
# The module-level ``settings`` must reflect the shipped default allow-list under test,
# so any ambient CORS_ORIGINS is removed before import (each case sets its own value via
# init kwargs). This also avoids a Pydantic complex-field env JSON-parse error if an
# ambient value is not the documented JSON-array form (see .env.sample).
os.environ.pop("CORS_ORIGINS", None)

from src.backend.metrics_input_service.config import Settings

# Non-security fields required by Settings, supplied explicitly so construction is
# independent of the process environment.
_REQUIRED_FIELDS = {
    "database_url": "postgresql://user:pass@localhost:5432/testdb",
    "api_key": "test-api-key",
    "log_level": "INFO",
}


def _make_settings(**overrides):
    """Construct Settings with required fields supplied and .env reading disabled.

    Init kwargs take precedence over the environment in Pydantic v1, so any
    ``CORS_ORIGINS`` override passed here is deterministic regardless of ambient env
    and runs through the real production validator.
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


def test_origin_with_credentials_rejected():
    # An origin carrying userinfo is not a bare serialized origin and must be rejected.
    with pytest.raises(ValidationError):
        _make_settings(CORS_ORIGINS=["http://user:pass@host"])


def test_explicit_allowlist_accepted():
    # An explicit http(s) allow-list is accepted and never contains "*".
    settings = _make_settings(CORS_ORIGINS=["https://app.example.com"])
    assert settings.CORS_ORIGINS == ["https://app.example.com"]
    assert "*" not in settings.CORS_ORIGINS


def test_shipped_settings_default_not_wildcard():
    # The module-level settings instance actually used by the service is non-wildcard.
    from src.backend.metrics_input_service.config import settings as shipped_settings
    assert "*" not in shipped_settings.CORS_ORIGINS
    assert len(shipped_settings.CORS_ORIGINS) >= 1


# --- Real application factory: middleware wiring (visible pre-existing blocker) ----

@pytest.mark.xfail(
    reason=(
        "Pre-existing out-of-scope defect (AAP 0.8.2): "
        "app/__init__.py contains a stray Markdown fence that raises SyntaxError, and "
        "main.py imports that package at module scope, so main.create_app cannot be "
        "imported. Kept visible as xfail; see docs/security/decision-log.md."
    ),
    strict=False,
    raises=Exception,
)
def test_real_app_cors_never_wildcard_with_credentials():
    """The real app must reflect only configured origins, never '*' with credentials."""
    from fastapi.testclient import TestClient

    from src.backend.metrics_input_service.main import create_app

    client = TestClient(create_app())
    resp = client.get("/", headers={"Origin": "http://evil.example.com"})
    acao = resp.headers.get("access-control-allow-origin")
    assert acao != "*"
    assert acao != "http://evil.example.com"
