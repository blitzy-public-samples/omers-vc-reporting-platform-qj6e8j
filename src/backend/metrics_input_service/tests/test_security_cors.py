"""CORS security regression tests for the metrics-input service.

Security control verified: Cross-Origin Resource Sharing (CWE-942, Overly
Permissive CORS). The service's configured CORS allow-list must never contain the
wildcard ``*``, must reject empty or malformed origin lists (fail closed), and must
accept only explicit http(s) origins. The control under test is the ``CORS_ORIGINS``
validator on ``config.Settings`` (and the shipped default it produces).

Isolation note: the service application package has a pre-existing, out-of-scope
import defect (``app/__init__.py`` contains a stray Markdown fence that raises
``SyntaxError``), and ``config.py`` imports that application chain at module scope.
The broken application submodules are therefore stubbed in ``sys.modules`` only for
the duration of the ``config`` import and are removed immediately afterwards, so this
test never masks the real (broken) application import for any other module in the
session. Rationale detail lives in ``docs/security/decision-log.md``.
"""

import os
import sys
import types

import pytest
from pydantic import ValidationError

# config.py constructs a module-level ``settings = load_settings()`` at import time,
# which requires these non-security fields. They are provisioned with setdefault so an
# externally supplied value (e.g. from CI) is preserved.
os.environ.setdefault("database_url", "postgresql://user:pass@localhost:5432/testdb")
os.environ.setdefault("api_key", "test-api-key")
os.environ.setdefault("log_level", "INFO")

# Leaf application modules imported by config.py (lines 73-74). app/__init__.py has a
# pre-existing SyntaxError, so these are stubbed only around the config import.
_STUB_MODULES = {
    "src.backend.metrics_input_service.app": {},
    "src.backend.metrics_input_service.app.models": {},
    "src.backend.metrics_input_service.app.models.models": {"MetricsInput": object},
    "src.backend.metrics_input_service.app.routers": {},
    "src.backend.metrics_input_service.app.routers.metrics": {"router": object()},
}


def _import_settings_isolated():
    """Import ``config.Settings`` without executing the broken application package.

    Stubs the leaf application modules that ``config`` imports, performs the import,
    then removes exactly the stubs it added so a later import of the real application
    (e.g. by ``test_metrics.py``) still fails loudly rather than resolving a stub.
    """
    added = []
    for name, attrs in _STUB_MODULES.items():
        if name not in sys.modules:
            module = types.ModuleType(name)
            for attr, value in attrs.items():
                setattr(module, attr, value)
            sys.modules[name] = module
            added.append(name)
    try:
        from src.backend.metrics_input_service.config import Settings
        return Settings
    finally:
        for name in added:
            sys.modules.pop(name, None)


Settings = _import_settings_isolated()

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


def test_shipped_settings_default_not_wildcard():
    # The module-level settings instance actually used by the service is non-wildcard.
    from src.backend.metrics_input_service.config import settings as shipped_settings
    assert "*" not in shipped_settings.CORS_ORIGINS
    assert len(shipped_settings.CORS_ORIGINS) >= 1
