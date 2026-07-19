"""Test-suite package initializer for the Reporting Financials Service.

Security remediation (CWE-798 / CWE-259, fail-closed configuration): this
initializer provisions the environment required by ``config.py`` — ``JWT_SECRET_KEY``
(>= 32 chars, required with no insecure default), ``DATABASE_URL`` (typed
``PostgresDsn``), and ``API_KEY`` (required, no placeholder default) — at the very
top of package import, before any test module in
this package is collected. Provisioning here (rather than only in ``conftest.py``)
is what makes the CORS and configuration security regression tests import
``config`` and collect cleanly: pytest imports this package initializer while
resolving the fully-qualified test module names, before the ``conftest.py`` body
runs, so the environment must be present at this point.

This initializer is intentionally side-effect-free beyond environment
provisioning. It does NOT import the application factory (``main.create_app``) or
any module under the ``app`` package; it exists only to make ``config`` importable
during collection for the configuration and CORS security regression tests. The
earlier configuration-import defect is resolved — ``app/routers/financials.py``
reads the settings **instance** (``config.DATABASE_URL``), not the class attribute,
so ``main.create_app`` now imports and starts cleanly. Any remaining collection
error in the non-security ``test_financials.py`` suite is a separate pre-existing
test defect (it imports a ``financials_router`` symbol the router module does not
export), unrelated to this security remediation and tracked separately (AAP §0.8.2).
Rationale detail lives in ``docs/security/decision-log.md``.
"""

import os

# Fail-closed JWT signing key required by config.py (Field(..., min_length=32)).
# CWE-798 / CWE-259: no insecure default is permitted; a real key must be supplied.
os.environ.setdefault("JWT_SECRET_KEY", "x" * 32)

# DATABASE_URL is typed PostgresDsn in config.py, so it MUST be a valid postgres
# DSN (a sqlite URL, or the placeholder default, is rejected by PostgresDsn
# validation with "URL host invalid"). Provide a syntactically valid DSN so the
# settings object constructs during collection.
os.environ.setdefault(
    "DATABASE_URL", "postgresql://testuser:testpass@localhost:5432/testdb"
)

# API_KEY is now required from the environment (CWE-798 / CWE-259: no predictable
# placeholder default). Provide a non-placeholder value so the settings object
# constructs during collection.
os.environ.setdefault("API_KEY", "test-api-key-value")
