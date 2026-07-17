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

import pydantic
import pytest

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
