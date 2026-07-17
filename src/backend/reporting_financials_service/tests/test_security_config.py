"""Security regression tests for reporting-financials configuration.

Covers the configuration-layer controls this remediation established:
- ``JWT_SECRET_KEY`` required from the environment with a 32-character minimum and no
  insecure default (CWE-798/CWE-259);
- ``DATABASE_URL`` required from the environment with no credential-bearing default
  (CWE-798);
- ``CORS_ORIGINS`` an explicit, non-wildcard, well-formed allow-list (CWE-942); and
- ``JWT_ALGORITHM`` pinned to HS256 (guarding the algorithm-confusion class at the
  config level; this service does not depend on PyJWT, so the control is the pinned
  algorithm value the token consumers read -- the full decode round-trip is owned by
  the authentication service, which depends on PyJWT).

The settings class is instantiated directly (``Config(_env_file=None, ...)``) so each
case is stateless and self-contained -- no module reload and no shared-environment
mutation. These tests fail if any of the above controls is removed, which is what
makes them a regression gate for the remediation.
"""

import os

# config.py builds a module-level ``config = Config()`` at import time and requires
# these values, so they must exist before importing the config module. setdefault keeps
# an externally supplied value (e.g. CI).
os.environ.setdefault("DATABASE_URL", "postgresql://user:pass@localhost:5432/testdb")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-thirty-two-chars-min-000")
os.environ.setdefault("CORS_ORIGINS", "http://localhost:3000")

import pytest
import pydantic

from src.backend.reporting_financials_service.config import Config

MIN_SECRET_LEN = 32
_VALID_DB_URL = "postgresql://testuser:testpass@localhost:5432/testdb"
_VALID_SECRET = "x" * MIN_SECRET_LEN


def _make_config(**overrides):
    # Instantiate the settings class directly; no .env file, no module reload. Required
    # fields are supplied so a single control can be isolated per test.
    params = {"JWT_SECRET_KEY": _VALID_SECRET, "DATABASE_URL": _VALID_DB_URL}
    params.update(overrides)
    return Config(_env_file=None, **params)


# --- JWT signing key + algorithm --------------------------------------------------

def test_jwt_algorithm_is_hs256():
    assert _make_config().JWT_ALGORITHM == "HS256"


def test_jwt_algorithm_field_default_is_hs256():
    # Mutation-sensitive to the pinned algorithm: the field default must be HS256, so a
    # regression to an attacker-influenced or "none" algorithm is caught here.
    assert Config.__fields__["JWT_ALGORITHM"].default == "HS256"


def test_secret_required_from_env_no_insecure_default(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "e" * MIN_SECRET_LEN)
    monkeypatch.setenv("DATABASE_URL", _VALID_DB_URL)
    cfg = Config(_env_file=None)
    resolved = cfg.JWT_SECRET_KEY.get_secret_value()
    assert resolved == "e" * MIN_SECRET_LEN
    assert len(resolved) >= MIN_SECRET_LEN
    # No insecure default is resolvable: the field is required.
    assert Config.__fields__["JWT_SECRET_KEY"].required is True


def test_secret_absent_fails_closed(monkeypatch):
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
    monkeypatch.setenv("DATABASE_URL", _VALID_DB_URL)
    with pytest.raises(pydantic.ValidationError):
        Config(_env_file=None)


def test_secret_too_short_fails_closed(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "x" * 8)
    monkeypatch.setenv("DATABASE_URL", _VALID_DB_URL)
    with pytest.raises(pydantic.ValidationError):
        Config(_env_file=None)


# --- DATABASE_URL (DSN) required, no credential-bearing default -------------------

def test_database_url_required_no_default():
    # CWE-798: DATABASE_URL is a required field, so no credential-bearing default is
    # resolvable.
    assert Config.__fields__["DATABASE_URL"].required is True


def test_database_url_absent_fails_closed(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("JWT_SECRET_KEY", _VALID_SECRET)
    with pytest.raises(pydantic.ValidationError):
        Config(_env_file=None)


def test_database_url_valid_postgres_accepted():
    cfg = _make_config(DATABASE_URL=_VALID_DB_URL)
    assert str(cfg.DATABASE_URL) == _VALID_DB_URL


# --- CORS allow-list fail-close boundaries (CWE-942) ------------------------------

def test_cors_wildcard_rejected():
    with pytest.raises(pydantic.ValidationError):
        _make_config(CORS_ORIGINS="*")


def test_cors_wildcard_in_list_rejected():
    with pytest.raises(pydantic.ValidationError):
        _make_config(CORS_ORIGINS=["http://localhost:3000", "*"])


def test_cors_empty_rejected():
    with pytest.raises(pydantic.ValidationError):
        _make_config(CORS_ORIGINS=[])


def test_cors_malformed_rejected():
    with pytest.raises(pydantic.ValidationError):
        _make_config(CORS_ORIGINS=["http://user:pass@host/path"])


def test_cors_explicit_allowlist_accepted():
    cfg = _make_config(CORS_ORIGINS="https://app.example.com")
    assert cfg.CORS_ORIGINS == ["https://app.example.com"]
    assert "*" not in cfg.CORS_ORIGINS
