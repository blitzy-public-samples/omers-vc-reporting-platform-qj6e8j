"""Pytest environment provisioning for the reporting-financials test suite.

Security remediation (CWE-798/CWE-259): after the fix, ``config.py`` requires
``JWT_SECRET_KEY`` (min length 32) from the environment and fails closed if it is
absent or too short. ``config.py`` also types ``DATABASE_URL`` as ``PostgresDsn``.
Provision both here so the package's modules import cleanly during collection.

The package initializer ``tests/__init__.py`` now provisions the same variables at
the very top of package import (before pytest collects any test module), so the
security regression tests import ``config`` and collect cleanly. This conftest
remains as a redundant, idempotent safety net (``setdefault`` never overrides a
value already set by the environment or by the package initializer). Rationale
detail lives in ``docs/security/decision-log.md``.
"""

import os

# Fail-closed JWT signing key required by config.py (>= 32 chars).
os.environ.setdefault("JWT_SECRET_KEY", "x" * 32)

# DATABASE_URL is typed PostgresDsn in config.py, so it MUST be a valid postgres DSN.
# A sqlite URL is rejected by PostgresDsn validation ("URL scheme not permitted").
os.environ.setdefault(
    "DATABASE_URL", "postgresql://testuser:testpass@localhost:5432/testdb"
)

# CORS_ORIGINS intentionally left to the safe non-wildcard default in config.py.
