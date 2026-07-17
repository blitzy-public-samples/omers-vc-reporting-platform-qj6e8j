# src/backend/authentication_service/app/security.py

import hashlib
import logging
import uuid
import jwt
from datetime import datetime, timedelta
from typing import Optional

# PyJWT version 2.3.0
from jwt import PyJWTError

from src.backend.authentication_service.config import load_config

# Load configuration settings
config = load_config()

# Dedicated logger for structured security-event records (FR-8.5 / FR-10.6).
# Reuses the standard-library logging already present; no new monitoring dependency.
_security_logger = logging.getLogger("omers.security")

def generate_token(user_id: str) -> str:
    """
    Generates a JWT token for a given user ID, encoding it with a secret key and setting an expiration time.

    This function addresses the requirement:
    'Authentication and Authorization Implementation' located in 'Technical Requirements/Feature 4: Authentication and Authorization Implementation'
    which states: 'Implement secure authentication and authorization mechanisms to control access to the backend platform and its resources.'

    Args:
        user_id (str): The unique identifier of the user.

    Returns:
        str: A JWT token encoded with the user ID and expiration time.
    """
    # Load configuration settings
    secret_key = config['SECRET_KEY']
    token_expiration = config['TOKEN_EXPIRATION']

    # Create a payload containing the user_id and expiration time
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=token_expiration)
    }

    # Encode the payload using PyJWT with the SECRET_KEY
    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return token

def validate_token(token: str) -> Optional[str]:
    """
    Validates a given JWT token, ensuring it is correctly signed and not expired, and extracts the user ID.

    This function addresses the requirement:
    'Authentication and Authorization Implementation' located in 'Technical Requirements/Feature 4: Authentication and Authorization Implementation'
    which states: 'Implement secure authentication and authorization mechanisms to control access to the backend platform and its resources.'

    Args:
        token (str): The JWT token to validate.

    Returns:
        Optional[str]: The user ID extracted from the token if valid, None otherwise.
    """
    # Load configuration settings
    secret_key = config['SECRET_KEY']

    try:
        # Decode the token using PyJWT with the SECRET_KEY
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        
        # Extract and return the user ID from the token payload
        return payload.get("sub")
    except PyJWTError:
        # If the token is invalid or expired, return None
        return None


def pseudonymize(value: Optional[str]) -> str:
    """
    Return a bounded, non-reversible pseudonym for a sensitive identifier (CWE-532).

    Attacker-controlled identifiers (e.g. a submitted username) are never logged in the
    clear; a short SHA-256-derived token is emitted instead so failures remain correlatable
    without exposing PII or enabling log forging.
    """
    if not value:
        return "anonymous"
    digest = hashlib.sha256(str(value).encode("utf-8", "replace")).hexdigest()
    return "sub_" + digest[:16]


def sanitize(value: Optional[str], max_len: int = 128) -> str:
    """
    Strip control characters and bound length of a value before it enters a log record (CWE-117).
    """
    if value is None:
        return ""
    text = str(value).replace("\r", "").replace("\n", "")
    text = "".join(ch for ch in text if ch.isprintable())
    return text[:max_len]


def log_security_event(service: str, event: str, outcome: str, correlation_id: str, **fields) -> None:
    """
    Emit exactly one normalized, structured security-event log record.

    Every record carries the emitting ``service``, the ``event`` type, an ``outcome``, and the
    request-level ``correlation_id``; any additional non-sensitive fields are sanitized. This is
    the single event contract consumed by the security-observability dashboard panels.
    """
    parts = [
        f"security_event={event}",
        f"service={service}",
        f"outcome={outcome}",
        f"correlation_id={correlation_id}",
    ]
    for key, value in fields.items():
        parts.append(f"{key}={sanitize(str(value))}")
    _security_logger.warning(" ".join(parts))


def get_correlation_id(request) -> str:
    """
    Resolve one correlation identifier per request, propagated (not regenerated per failure).

    Prefers an inbound ``X-Correlation-ID``/``X-Request-ID`` header, otherwise generates a UUID,
    and caches it on ``request.state`` so every event for the same request shares one id (M-05).
    """
    correlation_id = getattr(request.state, "correlation_id", None)
    if not correlation_id:
        correlation_id = (
            request.headers.get("X-Correlation-ID")
            or request.headers.get("X-Request-ID")
            or str(uuid.uuid4())
        )
        request.state.correlation_id = correlation_id
    return correlation_id


def install_security_logging(app, service: str, allowed_origins) -> None:
    """
    Install the shared security-event contract on a FastAPI app (used by every construction path).

    Adds one HTTP middleware that (1) assigns/propagates a request correlation id and (2) emits a
    scoped ``cors_rejection`` security event when a request carries an ``Origin`` header that is not
    in the configured allow-list (CWE-942). The middleware never alters the response status or body;
    it only adds the correlation id to the response headers and emits observability signals.
    """
    normalized_origins = set(allowed_origins or [])

    @app.middleware("http")
    async def _security_logging_middleware(request, call_next):
        correlation_id = get_correlation_id(request)
        origin = request.headers.get("origin")
        if origin and origin not in normalized_origins:
            log_security_event(
                service=service,
                event="cors_rejection",
                outcome="denied",
                correlation_id=correlation_id,
                origin=origin,
            )
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response


# Additional helper functions can be added here as needed for enhanced security features