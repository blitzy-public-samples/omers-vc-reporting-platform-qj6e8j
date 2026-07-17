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
module under the ``app`` package. Those imports have a pre-existing, out-of-scope
import-time defect (``app/models/models.py`` does ``from sqlalchemy import UUID``,
which SQLAlchemy 1.4.x does not provide; ``app/database.py`` / ``app/schemas.py``
are absent) that is unrelated to the security remediation. Keeping this file free
of the application import chain is what lets the configuration security regression
test (``test_security_config.py``) import ``config`` and collect cleanly. The
broken application import is not masked: ``test_metrics.py`` still imports the
application chain directly, so that pre-existing defect continues to surface
loudly at its own collection. Rationale detail lives in
``docs/security/decision-log.md``.
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
