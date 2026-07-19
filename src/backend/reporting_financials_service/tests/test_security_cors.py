"""CORS security regression tests for the reporting-financials service.

Covers the wildcard-removal remediation (CWE-942, Overly Permissive CORS): the
configured origin allow-list must never contain the wildcard ``*``, must reject
empty or malformed origin lists (fail closed), and must accept only explicit
http(s) origins; and the application's CORS middleware must never combine
``Access-Control-Allow-Origin: *`` with ``Access-Control-Allow-Credentials: true``.

The security control under test is the ``CORS_ORIGINS`` validator on
``config.Config`` (the real allow-list the service consumes) plus the middleware
wiring in ``main.create_app``. The validator is exercised directly so the tests
fail if the control is weakened. The real application is built via
``main.create_app`` in the ``real_app`` fixture below, and
``test_real_app_cors_never_wildcard_with_credentials`` binds a ``TestClient`` to it
and asserts the middleware never returns ``Access-Control-Allow-Origin: *`` together
with ``Access-Control-Allow-Credentials: true`` and reflects only the configured
origin. Rationale detail lives in ``docs/security/decision-log.md``.
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


# --- Real application factory: middleware wiring ----------------------------------

@pytest.fixture
def real_app():
    """Construct the real application via ``main.create_app``.

    Imported lazily inside the fixture so the CORS assertions run against the real
    middleware wiring produced by the application factory.
    """
    from src.backend.reporting_financials_service.main import create_app

    return create_app()


def test_real_app_cors_never_wildcard_with_credentials(real_app):
    """The real app must reflect only the configured origin, never '*' with credentials.

    Kills the CWE-942 mutation (``allow_origins=['*']`` with ``allow_credentials=True``):
    under that mutation the untrusted-origin response carries
    ``Access-Control-Allow-Origin: *`` and the allowed-origin response stops reflecting
    the specific origin, so the assertions below fail.
    """
    client = TestClient(real_app)

    # An untrusted origin must never be answered with a wildcard nor reflected back,
    # and the wildcard-with-credentials combination must never appear.
    resp = client.get("/", headers={"Origin": UNTRUSTED_ORIGIN})
    acao = resp.headers.get("access-control-allow-origin")
    acac = resp.headers.get("access-control-allow-credentials")
    assert acao != "*"
    assert acao != UNTRUSTED_ORIGIN
    assert not (acao == "*" and acac == "true")

    # The configured origin must be reflected specifically (never "*"), even though
    # credentials are enabled for it.
    resp = client.get("/", headers={"Origin": ALLOWED_ORIGIN})
    acao = resp.headers.get("access-control-allow-origin")
    acac = resp.headers.get("access-control-allow-credentials")
    assert acao == ALLOWED_ORIGIN
    assert acao != "*"
    assert not (acao == "*" and acac == "true")
