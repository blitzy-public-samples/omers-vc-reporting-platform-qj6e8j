# src/backend/authentication_service/conftest.py

"""Pytest environment provisioning for the authentication-service test suite.

``config.py`` validates required settings at import time (``SECRET_KEY`` of at
least 32 characters and ``DATABASE_URL``) and ``main.py`` imports it, so the
environment must exist before the tests package is imported. The service
directory is a namespace package (no ``__init__.py``), so this conftest is
imported before ``tests/__init__.py`` runs, and it restores the exact prior
process environment at session end so no shared state leaks to other suites.
"""

import os

import pytest

# Deterministic values the CORS tests assert against.
_TEST_ENV = {
    "SECRET_KEY": "test-secret-key-thirty-two-chars-min-000",
    "DATABASE_URL": "postgresql://user:pass@localhost:5432/testdb",
    "CORS_ORIGINS": "http://localhost:3000",
}

# Snapshot prior values (None means previously unset) for exact restoration.
_PRIOR_ENV = {key: os.environ.get(key) for key in _TEST_ENV}

# SECRET_KEY and DATABASE_URL honour an externally supplied value (e.g. CI);
# CORS_ORIGINS is set explicitly so the configured origin under test is fixed.
os.environ.setdefault("SECRET_KEY", _TEST_ENV["SECRET_KEY"])
os.environ.setdefault("DATABASE_URL", _TEST_ENV["DATABASE_URL"])
os.environ["CORS_ORIGINS"] = _TEST_ENV["CORS_ORIGINS"]


@pytest.fixture(scope="session", autouse=True)
def _restore_environment():
    """Restore the exact prior process environment after the session."""
    yield
    for key, prior in _PRIOR_ENV.items():
        if prior is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = prior
