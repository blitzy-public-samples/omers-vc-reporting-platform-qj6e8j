"""Security regression tests for reporting-financials configuration.

Covers the weak-secret remediation (CWE-798 / CWE-259): JWT_SECRET_KEY must be
required from the environment with a >= 32 char minimum and no insecure default,
and the JWT algorithm must remain restricted to HS256 (guards the
algorithm-confusion class, CVE-2022-29217).
"""

import os
import importlib

import pytest
import pydantic

import src.backend.reporting_financials_service.config as config_module

MIN_SECRET_LEN = 32


def test_jwt_algorithm_is_hs256():
    # Always-available config invariant (no PyJWT dependency in this service).
    from src.backend.reporting_financials_service.config import JWT_ALGORITHM

    assert JWT_ALGORITHM == "HS256"


def test_secret_required_from_env_no_insecure_default():
    # With a valid key present (provisioned by conftest), config resolves to the
    # env-supplied value and NOT to any weak built-in default.
    importlib.reload(config_module)
    resolved = config_module.config.JWT_SECRET_KEY.get_secret_value()
    assert resolved == os.environ["JWT_SECRET_KEY"]
    assert len(resolved) >= MIN_SECRET_LEN


@pytest.fixture
def restore_config():
    # Restore a valid config for subsequent tests/modules after a negative case.
    yield
    os.environ["JWT_SECRET_KEY"] = "x" * MIN_SECRET_LEN
    importlib.reload(config_module)


def test_secret_absent_fails_closed(monkeypatch, restore_config):
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
    with pytest.raises((pydantic.ValidationError, ValueError)):
        importlib.reload(config_module)


def test_secret_too_short_fails_closed(monkeypatch, restore_config):
    monkeypatch.setenv("JWT_SECRET_KEY", "x" * 8)
    with pytest.raises((pydantic.ValidationError, ValueError)):
        importlib.reload(config_module)


def test_jwt_algorithm_restriction_regression():
    # This service has no PyJWT dependency and no decode call site of its own, so
    # skip the round-trip when PyJWT is absent; the config invariant above always runs.
    jwt = pytest.importorskip("jwt")
    importlib.reload(config_module)
    key = config_module.config.JWT_SECRET_KEY.get_secret_value()
    algorithm = config_module.JWT_ALGORITHM

    assert algorithm == "HS256"

    token = jwt.encode({"sub": "user-1"}, key, algorithm=algorithm)
    assert jwt.decode(token, key, algorithms=["HS256"]).get("sub") == "user-1"

    forged = jwt.encode({"sub": "attacker"}, key=None, algorithm="none")
    with pytest.raises(jwt.PyJWTError):
        jwt.decode(forged, key, algorithms=["HS256"])
