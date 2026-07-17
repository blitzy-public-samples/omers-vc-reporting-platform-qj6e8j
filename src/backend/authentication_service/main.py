"""
Main entry point for the authentication service, responsible for initializing the FastAPI application,
setting up routes, and configuring middleware for handling authentication requests.

This module addresses the following requirement:
- Authentication and Authorization Implementation (Technical Requirements/Feature 4)
"""

# Import FastAPI and necessary modules
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

# Import internal dependencies
from src.backend.authentication_service.config import load_config
from src.backend.authentication_service.app.security import (
    generate_token,
    validate_token,
    log_security_event,
    get_correlation_id,
    pseudonymize,
    install_security_logging,
)

# FastAPI version: 0.68.1
# Uvicorn version: 0.15.0

# Structured security-event logging (FR-8.5 / FR-10.6): configure the root
# handler so security records carry timestamp, level, and logger name instead
# of the bare last-resort format. force=True guarantees this format even if an
# imported module already configured root logging.
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s", force=True)

def create_app() -> FastAPI:
    """
    Initializes the FastAPI application, sets up routes, and configures middleware.

    Returns:
        FastAPI: The initialized FastAPI application instance.
    """
    # Load configuration settings
    config = load_config()

    # Initialize the FastAPI application
    app = FastAPI(
        title="Authentication Service",
        description="API for handling authentication and token generation",
        version="1.0.0",
        debug=config['DEBUG']
    )

    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config['CORS_ORIGINS'],  # CORS allow-list (CWE-942)
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Correlation-id propagation + scoped CORS-rejection security events (CWE-942)
    install_security_logging(app, service="authentication_service", allowed_origins=config['CORS_ORIGINS'])

    # Initialize OAuth2 password bearer for token authentication
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    @app.post("/token")
    async def login_for_access_token(request: Request, username: str, password: str):
        """
        Endpoint for user authentication and token generation.

        Args:
            request (Request): The inbound request (used for correlation-id propagation).
            username (str): The user's username.
            password (str): The user's password.

        Returns:
            dict: A dictionary containing the access token and token type.

        Raises:
            HTTPException: If authentication fails.
        """
        # TODO: Implement actual user authentication logic here
        # For demonstration purposes, we'll use a dummy check
        if username == "testuser" and password == "testpassword":
            token = generate_token(username)
            return {"access_token": token, "token_type": "bearer"}
        else:
            # Security-event logging: authentication failure (FR-8.5 / FR-10.6)
            # Username is pseudonymized (CWE-532 / CWE-117); one event per failure.
            log_security_event(
                service="authentication_service",
                event="authentication_failure",
                outcome="denied",
                correlation_id=get_correlation_id(request),
                subject=pseudonymize(username),
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @app.get("/protected")
    async def protected_route(request: Request, token: str = Depends(oauth2_scheme)):
        """
        A protected route that requires a valid token for access.

        Args:
            request (Request): The inbound request (used for correlation-id propagation).
            token (str): The JWT token provided in the request header.

        Returns:
            dict: A message indicating successful authentication.

        Raises:
            HTTPException: If the token is invalid or expired.
        """
        correlation_id = get_correlation_id(request)
        try:
            user_id = validate_token(token)
        except Exception as e:
            # Security-event logging: token validation failure (FR-8.5 / FR-10.6)
            log_security_event(
                service="authentication_service",
                event="token_validation_failure",
                outcome="denied",
                correlation_id=correlation_id,
                reason=type(e).__name__,
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if user_id is None:
            # Security-event logging: token validation failure (FR-8.5 / FR-10.6)
            # Raised outside the try above so it is not re-caught and double-logged.
            log_security_event(
                service="authentication_service",
                event="token_validation_failure",
                outcome="denied",
                correlation_id=correlation_id,
                reason="missing_subject",
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"message": f"Hello, {user_id}! This is a protected route."}

    return app

# Entry point
if __name__ == "__main__":
    app = create_app()
    # Run the FastAPI application using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)