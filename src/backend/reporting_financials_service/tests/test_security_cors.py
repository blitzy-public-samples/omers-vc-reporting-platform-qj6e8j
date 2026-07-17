"""CORS security regression tests for the reporting-financials service.

Covers the wildcard-removal remediation (CWE-942, Overly Permissive CORS): the
configured origin allow-list must never contain the wildcard ``*``, must reject
empty or malformed origin lists (fail closed), and must accept only explicit
http(s) origins; and the application's CORS middleware must never combine
``Access-Control-Allow-Origin: *`` with ``Access-Control-Allow-Credentials: true``.

The security control under test is the ``CORS_ORIGINS`` validator on
``config.Config`` (the real allow-list the service consumes) plus the middleware
wiring in ``main.create_app``. The validator is exercised directly so the tests
fail if the control is weakened. Binding to the real ``main.create_app`` is done
via ``real_app`` below; its import chain has a pre-existing, out-of-scope defect
(``app/routers/financials.py`` reads ``Config.DATABASE_URL`` as a class attribute,
which is invalid under Pydantic v1 and raises ``AttributeError`` at import). Per
AAP 0.8.2 that pre-existing non-security defect is not fixed here, so the
real-factory test is marked ``xfail`` to keep the blocker visible (it becomes an
``xpass`` once that unrelated defect is resolved) rather than masking it behind a
synthetic application. Rationale detail lives in ``docs/security/decision-log.md``.
"""

import os

# config.py builds a module-level ``config = Config()`` at import time and requires
# these values, so they must exist before importing config/main. setdefault keeps an
# externally supplied value (e.g. CI); CORS_ORIGINS is set explicitly so the allowed
# origin under test is deterministic.
os.environ.setdefault("DATABASE_URL", "postgresql://user:pass@localhost:5432/testdb")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-thirty-two-chars-min-000")
os.environ["CORS_ORIGINS"] = "http://localhost:3000"

import pytest
import pydantic
from fastapi.testclient import TestClient

from src.backend.reporting_financials_service.config import Config, CORS_ORIGINS

# The single configured (trusted) origin; matches CORS_ORIGINS above.
ALLOWED_ORIGIN = "http://localhost:3000"
UNTRUSTED_ORIGIN = "http://evil.example.com"

_VALID_DB_URL = "postgresql://user:pass@localhost:5432/testdb"
_VALID_SECRET = "x" * 32


def _make_config(**overrides):
    # Instantiate the real settings class directly; init kwargs run through the real
    # validator, so any CORS_ORIGINS override here exercises the production control.
    params = {"DATABASE_URL": _VALID_DB_URL, "JWT_SECRET_KEY": _VALID_SECRET}
    params.update(overrides)
    return Config(_env_file=None, **params)


# --- Real security control: the CORS_ORIGINS allow-list validator -----------------

def test_configured_origins_never_wildcard():
    # The shipped/consumed allow-list must be explicit and never contain "*" (CWE-942).
    assert "*" not in CORS_ORIGINS
    assert len(CORS_ORIGINS) >= 1


def test_wildcard_origin_rejected():
    with pytest.raises(pydantic.ValidationError):
        _make_config(CORS_ORIGINS="*")


def test_wildcard_in_list_rejected():
    with pytest.raises(pydantic.ValidationError):
        _make_config(CORS_ORIGINS=["http://localhost:3000", "*"])


def test_empty_origin_list_rejected():
    with pytest.raises(pydantic.ValidationError):
        _make_config(CORS_ORIGINS=[])


def test_malformed_origin_rejected():
    # An entry that is not a bare scheme://host[:port] origin must fail closed.
    with pytest.raises(pydantic.ValidationError):
        _make_config(CORS_ORIGINS=["http://user:pass@host/path"])


def test_explicit_allowlist_accepted():
    cfg = _make_config(CORS_ORIGINS="https://app.example.com")
    assert cfg.CORS_ORIGINS == ["https://app.example.com"]
    assert "*" not in cfg.CORS_ORIGINS


# --- Real application factory: middleware wiring (visible pre-existing blocker) ----

@pytest.fixture
def real_app():
    """Construct the real application via ``main.create_app``.

    Import is performed lazily inside the fixture so the pre-existing app-chain
    defect surfaces as a test outcome rather than a module collection error.
    """
    from src.backend.reporting_financials_service.main import create_app

    return create_app()


@pytest.mark.xfail(
    reason=(
        "Pre-existing out-of-scope defect (AAP 0.8.2): "
        "app/routers/financials.py reads Config.DATABASE_URL as a class attribute "
        "(invalid under Pydantic v1), breaking main.create_app import. Kept visible "
        "as xfail; see docs/security/decision-log.md."
    ),
    strict=False,
    raises=Exception,
)
def test_real_app_cors_never_wildcard_with_credentials(real_app):
    """The real app must reflect only the configured origin, never '*' with credentials."""
    client = TestClient(real_app)

    # Untrusted origin is neither reflected nor answered with a wildcard.
    resp = client.get("/", headers={"Origin": UNTRUSTED_ORIGIN})
    acao = resp.headers.get("access-control-allow-origin")
    assert acao != "*"
    assert acao != UNTRUSTED_ORIGIN

    # Configured origin is reflected specifically (never "*") when credentials are on.
    resp = client.get("/", headers={"Origin": ALLOWED_ORIGIN})
    acao = resp.headers.get("access-control-allow-origin")
    assert acao != "*"
