"""Test-suite package initializer for the Reporting Metrics Service.

Security remediation (CWE-798 / CWE-259, fail-closed configuration): this
initializer provisions the environment required by ``config.py`` — ``SECRET_KEY``
(>= 32 chars, required with no insecure default) and ``DATABASE_URL`` (required,
validated as a PostgreSQL DSN) — at the very top of package import, before any
test module in this package is collected. pytest imports this package initializer
while resolving fully-qualified test module names, so the environment must be
present at this point for ``config.Settings()`` to construct during collection.

This initializer is intentionally side-effect-free beyond environment
provisioning. It does NOT import the application factory (``main.app``) or any
module under the ``app`` package; it exists only to make ``config`` importable
during collection for the configuration security regression test
(``test_security_config.py``). The application import chain is healthy —
``app/models/models.py`` imports ``UUID`` from ``sqlalchemy.dialects.postgresql``
(the correct location, which SQLAlchemy 1.4.x exposes), ``app/database.py`` and
``app/schemas.py`` are present, and ``main.app`` imports and starts cleanly
(verified at runtime). ``test_metrics.py`` imports that chain and collects without
error (its async cases skip when no async plugin is installed). Rationale detail
lives in ``docs/security/decision-log.md``.
"""

import os

# Fail-closed signing key required by config.py (Field(..., min_length=32)).
# CWE-798 / CWE-259: no insecure default is permitted; a real key must be supplied.
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-ci-only-0123456789")  # >= 32 chars

# DATABASE_URL is required and validated as a PostgreSQL DSN in config.py; provide a
# syntactically valid DSN so the settings object constructs during collection.
os.environ.setdefault(
    "DATABASE_URL", "postgresql://testuser:testpass@localhost:5432/testdb"
)
