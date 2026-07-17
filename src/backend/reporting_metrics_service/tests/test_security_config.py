"""Security regression tests for reporting-metrics configuration (CWE-798 / CWE-259).

Verifies that ``SECRET_KEY`` is required from the environment with a 32-character
minimum and has no insecure default, and that ``DATABASE_URL`` is required and
validated as a PostgreSQL DSN (fail closed). The settings class is instantiated
directly (``Settings(_env_file=None, ...)``) so each case is stateless and
self-contained -- no application import (the reporting-metrics ``app`` package has a
pre-existing, out-of-scope import-time defect) and no module reload.

These tests fail if the required-secret / minimum-length / required-DSN controls in
``config.py`` are removed, which is what makes them a regression gate for the
remediation.
"""

import os

import pydantic
import pytest

# config.py builds a module-level ``settings = Settings()`` at import time and requires
# these values, so they must exist before importing the config module. setdefault keeps
# an externally supplied value (e.g. CI); BACKEND_CORS_ORIGINS is removed so the shipped
# default is used at import (each case sets its own via init kwargs) and to avoid a
# Pydantic complex-field env JSON-parse error on a non-JSON ambient value.
os.environ.setdefault("SECRET_KEY", "test-secret-key-thirty-two-chars-min-000")
os.environ.setdefault("DATABASE_URL", "postgresql://user:pass@localhost:5432/testdb")
os.environ.pop("BACKEND_CORS_ORIGINS", None)

from src.backend.reporting_metrics_service.config import Settings

MIN_SECRET_LEN = 32
_VALID_DB_URL = "postgresql://testuser:testpass@localhost:5432/testdb"


def _make_settings(**overrides):
    # Instantiate the settings class directly; no .env file, no module reload.
    return Settings(_env_file=None, **overrides)


def test_valid_secret_and_db_url_accepted():
    cfg = _make_settings(SECRET_KEY="e" * MIN_SECRET_LEN, DATABASE_URL=_VALID_DB_URL)
    assert cfg.SECRET_KEY == "e" * MIN_SECRET_LEN
    assert len(cfg.SECRET_KEY) >= MIN_SECRET_LEN
    assert cfg.DATABASE_URL == _VALID_DB_URL


def test_secret_absent_fails_closed(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.setenv("DATABASE_URL", _VALID_DB_URL)
    with pytest.raises(pydantic.ValidationError):
        _make_settings()


def test_secret_empty_fails_closed(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", _VALID_DB_URL)
    with pytest.raises(pydantic.ValidationError):
        _make_settings(SECRET_KEY="")


def test_secret_too_short_fails_closed(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", _VALID_DB_URL)
    with pytest.raises(pydantic.ValidationError):
        _make_settings(SECRET_KEY="x" * (MIN_SECRET_LEN - 1))


def test_no_insecure_secret_default_resolvable(monkeypatch):
    # CWE-798: no insecure hard-coded default may be resolvable. SECRET_KEY is a
    # required field, so with it absent, construction fails closed.
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.setenv("DATABASE_URL", _VALID_DB_URL)
    assert Settings.__fields__["SECRET_KEY"].required is True
    with pytest.raises(pydantic.ValidationError):
        _make_settings()


def test_database_url_absent_fails_closed(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("SECRET_KEY", "x" * MIN_SECRET_LEN)
    with pytest.raises(pydantic.ValidationError):
        _make_settings()


def test_database_url_non_postgres_rejected(monkeypatch):
    # DATABASE_URL must be a PostgreSQL DSN; a sqlite URL is rejected (fail closed).
    monkeypatch.setenv("SECRET_KEY", "x" * MIN_SECRET_LEN)
    with pytest.raises(pydantic.ValidationError):
        _make_settings(DATABASE_URL="sqlite:///./test.db")


def test_database_url_bare_postgres_scheme_rejected(monkeypatch):
    # MJ-03: the bare 'postgres://' scheme is not supported by the SQLAlchemy/databases
    # consumer; only 'postgresql://' (or 'postgresql+driver://') is accepted (fail closed).
    monkeypatch.setenv("SECRET_KEY", "x" * MIN_SECRET_LEN)
    with pytest.raises(pydantic.ValidationError):
        _make_settings(DATABASE_URL="postgres://user:pass@localhost:5432/db")


def test_database_url_postgresql_driver_scheme_accepted(monkeypatch):
    # A 'postgresql+asyncpg://' DSN is a supported SQLAlchemy/databases scheme.
    monkeypatch.setenv("SECRET_KEY", "x" * MIN_SECRET_LEN)
    dsn = "postgresql+asyncpg://user:pass@localhost:5432/db"
    cfg = _make_settings(DATABASE_URL=dsn)
    assert cfg.DATABASE_URL == dsn


# --- CORS allow-list fail-close boundaries (CWE-942, CR-16 fail-closed validator) --

def test_backend_cors_default_not_wildcard():
    # The shipped default allow-list must be explicit and never contain "*".
    cfg = _make_settings(SECRET_KEY="x" * MIN_SECRET_LEN, DATABASE_URL=_VALID_DB_URL)
    assert "*" not in cfg.BACKEND_CORS_ORIGINS
    assert len(cfg.BACKEND_CORS_ORIGINS) >= 1


def test_backend_cors_wildcard_rejected():
    # A wildcard-only allow-list must fail closed rather than be silently accepted.
    with pytest.raises(pydantic.ValidationError):
        _make_settings(
            SECRET_KEY="x" * MIN_SECRET_LEN,
            DATABASE_URL=_VALID_DB_URL,
            BACKEND_CORS_ORIGINS=["*"],
        )


def test_backend_cors_empty_rejected():
    # An empty allow-list must fail closed.
    with pytest.raises(pydantic.ValidationError):
        _make_settings(
            SECRET_KEY="x" * MIN_SECRET_LEN,
            DATABASE_URL=_VALID_DB_URL,
            BACKEND_CORS_ORIGINS=[],
        )


def test_backend_cors_explicit_allowlist_accepted():
    cfg = _make_settings(
        SECRET_KEY="x" * MIN_SECRET_LEN,
        DATABASE_URL=_VALID_DB_URL,
        BACKEND_CORS_ORIGINS=["https://app.example.com"],
    )
    assert cfg.BACKEND_CORS_ORIGINS == ["https://app.example.com"]
    assert "*" not in cfg.BACKEND_CORS_ORIGINS
