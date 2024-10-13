# File: src/backend/api_gateway/main.py
# Description: This file serves as the entry point for the API Gateway component of the backend platform.
# It initializes and configures the FastAPI application, sets up routing, and integrates necessary
# middleware and security features to handle incoming HTTP requests.

# Requirements addressed:
# - API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
#   Develop the FastAPI-based RESTful API to facilitate secure and efficient data ingestion and retrieval
#   from the PostgreSQL database.

import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # version 1.8.2
import jwt  # PyJWT version 2.3.0

from src.backend.api_gateway.app.models.models import ExampleModel, Company, MetricsInput, QuarterlyReportingFinancials, QuarterlyReportingMetrics
from src.backend.api_gateway.app.routers.routes import setup_routes
from src.backend.api_gateway.config import Settings
from src.backend.authentication_service.app.security import generate_token, validate_token

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """
    Initializes and configures the FastAPI application.

    Returns:
        FastAPI: An instance of the configured FastAPI application.
    """
    # Load configuration settings
    settings = Settings()

    # Initialize FastAPI application
    app = FastAPI(
        title="OMERS Ventures API Gateway",
        description="API Gateway for managing financial reporting metrics",
        version="1.0.0"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Set up API routes
    setup_routes(app)

    # Integrate JWT token generation and validation
    @app.post("/token")
    async def login_for_access_token(username: str, password: str):
        """
        Endpoint for generating JWT tokens for secure API access.
        """
        if not authenticate_user(username, password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = generate_token(username)
        return {"access_token": access_token, "token_type": "bearer"}

    async def get_current_user(token: str = Depends(validate_token)):
        """
        Dependency for validating JWT tokens to ensure secure API access.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        username = validate_token(token)
        if username is None:
            raise credentials_exception
        return username

    # Example protected route
    @app.get("/protected")
    async def protected_route(current_user: str = Depends(get_current_user)):
        return {"message": f"Hello, {current_user}"}

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    logger.info("FastAPI application initialized and configured successfully")
    return app

def authenticate_user(username: str, password: str) -> bool:
    """
    Placeholder function for user authentication.
    In a real-world scenario, this would validate against a user database.
    """
    # TODO: Implement actual user authentication logic
    return username == "test_user" and password == "test_password"

# Create the FastAPI application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)