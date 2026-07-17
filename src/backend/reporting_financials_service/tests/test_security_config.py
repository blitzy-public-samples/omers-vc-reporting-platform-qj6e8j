"""Security regression tests for reporting-financials configuration (CWE-798/CWE-259).

Verifies that ``JWT_SECRET_KEY`` is required from the environment with a 32-character
minimum and has no insecure default, and that the JWT algorithm stays restricted to
HS256. The settings class is instantiated directly (``Config(_env_file=None)``) so each
case is stateless and self-contained -- no module reload and no shared-environment mutation.
"""

import pytest
import pydantic

from src.backend.reporting_financials_service.config import Config

MIN_SECRET_LEN = 32
_VALID_DB_URL = "postgresql://testuser:testpass@localhost:5432/testdb"


def _make_config(**overrides):
    # Instantiate the settings class directly; no .env file, no module reload.
    return Config(_env_file=None, **overrides)


def test_jwt_algorithm_is_hs256():
    cfg = _make_config(JWT_SECRET_KEY="x" * MIN_SECRET_LEN, DATABASE_URL=_VALID_DB_URL)
    assert cfg.JWT_ALGORITHM == "HS256"


def test_secret_required_from_env_no_insecure_default(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "e" * MIN_SECRET_LEN)
    monkeypatch.setenv("DATABASE_URL", _VALID_DB_URL)
    cfg = _make_config()
    resolved = cfg.JWT_SECRET_KEY.get_secret_value()
    assert resolved == "e" * MIN_SECRET_LEN
    assert len(resolved) >= MIN_SECRET_LEN


def test_secret_absent_fails_closed(monkeypatch):
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
    monkeypatch.setenv("DATABASE_URL", _VALID_DB_URL)
    with pytest.raises(pydantic.ValidationError):
        _make_config()


def test_secret_too_short_fails_closed(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "x" * 8)
    monkeypatch.setenv("DATABASE_URL", _VALID_DB_URL)
    with pytest.raises(pydantic.ValidationError):
        _make_config()


def test_jwt_algorithm_restriction_regression():
    # PyJWT is not a dependency of this service; skip the round-trip when it is absent.
    jwt = pytest.importorskip("jwt")
    key = "x" * MIN_SECRET_LEN
    cfg = _make_config(JWT_SECRET_KEY=key, DATABASE_URL=_VALID_DB_URL)
    assert cfg.JWT_ALGORITHM == "HS256"

    token = jwt.encode({"sub": "user-1"}, key, algorithm=cfg.JWT_ALGORITHM)
    assert jwt.decode(token, key, algorithms=["HS256"]).get("sub") == "user-1"

    forged = jwt.encode({"sub": "attacker"}, key=None, algorithm="none")
    with pytest.raises(jwt.PyJWTError):
        jwt.decode(forged, key, algorithms=["HS256"])
