"""CORS security regression tests for the reporting-financials service.

Covers the wildcard-removal remediation (CWE-942, Overly Permissive CORS): a CORS
response must never combine ``Access-Control-Allow-Origin: *`` with
``Access-Control-Allow-Credentials: true``; only configured origins are reflected;
and an unlisted origin is never reflected.

The app's CORS middleware is wired here with the real ``config.CORS_ORIGINS`` value,
mirroring exactly how ``main.py`` configures ``CORSMiddleware`` (allow_credentials
enabled, wildcard methods/headers). This avoids importing the application factory,
whose import chain has pre-existing, out-of-scope defects unrelated to CORS.
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
    acao = response.headers.get("access-control-allow-origin")
    acac = response.headers.get("access-control-allow-credentials")

    # Only the configured origin is reflected, never "*".
    assert acao == allowed
    # Never wildcard-with-credentials.
    assert not (acao == "*" and acac == "true")


def test_unlisted_origin_not_reflected():
    client = TestClient(_build_cors_app())
    response = client.get("/probe", headers={"Origin": "http://evil.com"})
    acao = response.headers.get("access-control-allow-origin")

    assert acao != "http://evil.com"
    assert acao != "*"
