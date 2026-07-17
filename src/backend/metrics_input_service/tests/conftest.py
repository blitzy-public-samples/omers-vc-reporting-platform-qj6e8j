"""Pytest environment provisioning for the metrics-input test suite.

``config.py`` constructs a module-level ``settings = load_settings()`` at import
time, and ``Settings`` requires ``database_url``, ``api_key``, and ``log_level``
(no defaults). Provision those three here so the package's application modules
(imported by ``test_metrics.py`` through ``main.create_app``) import cleanly during
collection instead of aborting the whole suite with a ``ValidationError``.

Values are supplied with ``setdefault`` so an externally supplied value (for
example from CI or the developer's environment) is always preserved. This mirrors
the env-provisioning conftest pattern already used by the reporting-financials and
authentication services. ``CORS_ORIGINS`` is intentionally left to the safe,
non-wildcard default in ``config.py``.
"""

import os

# Non-security settings required by config.Settings (no defaults); provisioned so
# the application import chain resolves during test collection.
os.environ.setdefault("database_url", "postgresql://user:pass@localhost:5432/testdb")
os.environ.setdefault("api_key", "test-api-key")
os.environ.setdefault("log_level", "INFO")
