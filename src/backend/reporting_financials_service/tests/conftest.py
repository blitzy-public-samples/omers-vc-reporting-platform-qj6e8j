"""Pytest environment provisioning for the reporting-financials test suite.

Security remediation (CWE-798/CWE-259): after the fix, ``config.py`` requires
``JWT_SECRET_KEY`` (min length 32) from the environment and fails closed if it is
absent or too short. ``config.py`` also types ``DATABASE_URL`` as ``PostgresDsn``.
Provision both here so the package's modules import cleanly during collection.

NOTE (pre-existing, out of scope): ``tests/__init__.py`` executes on package import
(it calls ``create_app()``), and because this ``tests/`` directory is a package,
pytest imports it before this conftest body runs. A service-level
``reporting_financials_service/conftest.py`` (a namespace dir without ``__init__.py``)
would be required to provision the environment strictly before ``tests/__init__.py``.
Creating that file is outside this folder's scope; it is recommended to the owner of
the parent service folder. Rationale detail lives in ``docs/security/decision-log.md``.
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
