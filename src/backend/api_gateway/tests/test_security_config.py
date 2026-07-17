"""
Configuration security regression tests for the API Gateway.

Covers two controls that the CORS regression tests do not reach through the
middleware layer:

* CWE-942 (Overly Permissive CORS): every wildcard form fed to the
  ``CORS_ALLOW_ORIGINS`` setting must be rejected at settings construction by the
  ``_split_cors_origins`` validator, so an insecure origin list can never be
  loaded in the first place.
* CWE-798 / CWE-259 (weak secret): ``SECRET_KEY`` is required from the
  environment with a >= 32 character minimum.

It also guards the reload-safety of the settings class (the validator carries
``allow_reuse=True``); without it, reloading the module raises a
``ConfigError: duplicate validator`` that masks the real missing-secret error.
"""

import importlib
import os
import sys

# config.py instantiates settings at import time (module-level ``load_settings()``)
# and requires DATABASE_URL, API_KEY, and a >= 32 char SECRET_KEY. Provision a valid
# baseline BEFORE importing the module so it imports cleanly in the service's own
# environment; individual tests override these via monkeypatch (auto-restored).
os.environ.setdefault("DATABASE_URL", "postgresql://user:pass@localhost:5432/testdb")
os.environ.setdefault("API_KEY", "test-api-key")
os.environ.setdefault("SECRET_KEY", "test-secret-key-at-least-32-characters-long")
os.environ.setdefault("CORS_ALLOW_ORIGINS", "http://localhost:3000")

# The application uses absolute ``src.backend...`` imports; ensure the repository
# root is importable regardless of the current working directory.
_REPO_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import pydantic
import pytest

import src.backend.api_gateway.config as config_module

MIN_SECRET_LEN = 32

# The non-CORS required settings; provided so construction reaches the CORS/secret
# validators under test rather than failing earlier on an unrelated missing field.
_REQUIRED_ENV = {
    "DATABASE_URL": "postgresql://user:pass@localhost:5432/testdb",
    "API_KEY": "test-api-key",
    "SECRET_KEY": "test-secret-key-at-least-32-characters-long",
}

# Every wildcard spelling the validator must reject (plain, JSON-ish, embedded in a
# CSV list, and whitespace-padded).
_WILDCARD_FORMS = ["*", '["*"]', "*,http://localhost:3000", " * "]


@pytest.fixture
def base_env(monkeypatch):
    """Provision the non-CORS required settings; monkeypatch auto-restores env."""
    for key, value in _REQUIRED_ENV.items():
        monkeypatch.setenv(key, value)
    return monkeypatch


@pytest.fixture
def restore_config():
    """Reload the config module back to a valid state after a mutating test."""
    yield
    for key, value in _REQUIRED_ENV.items():
        os.environ[key] = value
    os.environ["CORS_ALLOW_ORIGINS"] = "http://localhost:3000"
    importlib.reload(config_module)


@pytest.mark.parametrize("wildcard", _WILDCARD_FORMS)
def test_wildcard_cors_rejected_at_settings_construction(base_env, wildcard):
    """A wildcard origin list must never load; construction raises (CWE-942)."""
    base_env.setenv("CORS_ALLOW_ORIGINS", wildcard)
    with pytest.raises((pydantic.ValidationError, ValueError)):
        config_module.Settings()


def test_explicit_origin_list_is_accepted(base_env):
    """A concrete comma-separated allow-list is parsed into an explicit list."""
    base_env.setenv(
        "CORS_ALLOW_ORIGINS", "http://localhost:3000,https://app.example.com"
    )
    settings = config_module.Settings()
    assert settings.cors_origins == [
        "http://localhost:3000",
        "https://app.example.com",
    ]
    assert "*" not in settings.cors_origins


def test_secret_required_from_env(base_env):
    """SECRET_KEY absent -> construction fails closed (CWE-798/CWE-259)."""
    base_env.delenv("SECRET_KEY", raising=False)
    base_env.setenv("CORS_ALLOW_ORIGINS", "http://localhost:3000")
    with pytest.raises(pydantic.ValidationError):
        config_module.Settings()


def test_secret_too_short_rejected(base_env):
    """A SECRET_KEY shorter than 32 characters is rejected (CWE-798/CWE-259)."""
    base_env.setenv("SECRET_KEY", "x" * 8)
    base_env.setenv("CORS_ALLOW_ORIGINS", "http://localhost:3000")
    with pytest.raises(pydantic.ValidationError):
        config_module.Settings()


def test_config_module_reload_is_safe(base_env, restore_config):
    """Reloading the settings module must not raise a duplicate-validator error.

    The ``_split_cors_origins`` validator carries ``allow_reuse=True``; without it,
    ``importlib.reload`` raises ``ConfigError: duplicate validator`` that would mask
    the real missing-secret diagnostic on a misconfigured deployment.
    """
    os.environ["CORS_ALLOW_ORIGINS"] = "http://localhost:3000"
    importlib.reload(config_module)
    assert config_module.settings.cors_origins == ["http://localhost:3000"]


def test_missing_secret_on_reload_is_clean_error(base_env, restore_config):
    """With a secret missing, reload surfaces the missing-secret ValidationError.

    Regression guard for the previously-observed ``ConfigError: duplicate
    validator`` that obscured the real cause when secrets were absent.
    """
    os.environ.pop("SECRET_KEY", None)
    os.environ["CORS_ALLOW_ORIGINS"] = "http://localhost:3000"
    with pytest.raises(pydantic.ValidationError) as exc_info:
        importlib.reload(config_module)
    assert "secret_key" in str(exc_info.value).lower()
