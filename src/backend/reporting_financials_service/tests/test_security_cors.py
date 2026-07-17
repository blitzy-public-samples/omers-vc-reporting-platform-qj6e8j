"""CORS security regression tests for the reporting-financials service.

Covers the wildcard-removal remediation (CWE-942, Overly Permissive CORS): a CORS
response must never combine ``Access-Control-Allow-Origin: *`` with
``Access-Control-Allow-Credentials: true``; only configured origins are reflected;
and an unlisted origin is never reflected.

The app's CORS middleware is wired here with the real ``config.CORS_ORIGINS`` value,
mirroring exactly how ``main.py`` configures ``CORSMiddleware`` (allow_credentials
enabled, wildcard methods/headers). This exercises the actual security control (the
restricted origin allow-list) while avoiding an import of the application factory
``main.create_app``: its import chain has a pre-existing, out-of-scope defect
(``app/routers/financials.py`` accesses ``Config.DATABASE_URL`` as a class attribute,
invalid under Pydantic v1) that is unrelated to CORS. Binding this test directly to
``create_app`` is therefore deferred until that unrelated app defect is fixed;
rationale detail lives in ``docs/security/decision-log.md``.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

from src.backend.reporting_financials_service.config import CORS_ORIGINS


def _build_cors_app():
    app = FastAPI()
    # Mirrors main.py CORSMiddleware wiring; origins are the restricted config list.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/probe")
    def probe():
        return {"ok": True}

    return app


def test_config_cors_not_wildcard():
    # The configured origin list must not be a wildcard (CWE-942).
    assert "*" not in CORS_ORIGINS
    assert len(CORS_ORIGINS) >= 1


def test_allowed_origin_reflected_never_wildcard_with_credentials():
    allowed = CORS_ORIGINS[0]
    client = TestClient(_build_cors_app())
    response = client.options(
        "/probe",
        headers={
            "Origin": allowed,
            "Access-Control-Request-Method": "GET",
        },
    )
    # A well-formed preflight for an allowed origin must succeed; guards against
    # route/middleware-wiring drift that would silently skip the header checks.
    assert response.status_code == 200
    acao = response.headers.get("access-control-allow-origin")
    acac = response.headers.get("access-control-allow-credentials")

    # Only the configured origin is reflected, never "*".
    assert acao == allowed
    assert acao != "*"
    # Credentials are enabled for the listed origin. Asserted unconditionally so the
    # test is mutation-sensitive to allow_credentials=False; combined with acao != "*"
    # it proves the response never combines a wildcard origin with credentials (CWE-942).
    assert acac == "true"


def test_unlisted_origin_not_reflected():
    client = TestClient(_build_cors_app())
    response = client.get("/probe", headers={"Origin": "http://evil.com"})
    # The endpoint must exist and respond (guards route drift); the origin must not
    # be reflected regardless.
    assert response.status_code == 200
    acao = response.headers.get("access-control-allow-origin")

    assert acao != "http://evil.com"
    assert acao != "*"
