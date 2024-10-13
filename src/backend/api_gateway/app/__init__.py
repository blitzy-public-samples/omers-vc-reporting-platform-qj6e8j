"""
This module initializes the API Gateway component of the backend platform.
It sets up the necessary configurations, imports, and components required
for the FastAPI application to function correctly. This includes loading
configuration settings, initializing routes, and integrating security features.

Requirements addressed:
- API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
  Develop the FastAPI-based RESTful API to facilitate secure and efficient data ingestion
  and retrieval from the PostgreSQL database.
"""

import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # version 1.8.2
import jwt  # PyJWT version 2.3.0

# Internal imports
from src.backend.api_gateway.app.models.models import ExampleModel, Company, MetricsInput, QuarterlyReportingFinancials, QuarterlyReportingMetrics
from src.backend.api_gateway.app.routers.routes import setup_routes
from src.backend.api_gateway.config import Settings
from src.backend.authentication_service.app.security import generate_token, validate_token

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_api_gateway() -> FastAPI:
    """
    Sets up the API Gateway by configuring routes, loading settings,
    and integrating security features.

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

    # Integrate JWT token generation and validation for secure endpoints
    @app.middleware("http")
    async def authenticate_request(request, call_next):
        token = request.headers.get("Authorization")
        if token:
            try:
                payload = validate_token(token.split(" ")[1])
                request.state.user = payload
            except jwt.PyJWTError:
                # Handle invalid token
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        response = await call_next(request)
        return response

    # Example protected route
    @app.get("/protected")
    async def protected_route(current_user: str = Depends(validate_token)):
        return {"message": f"Hello, {current_user}"}

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    logger.info("FastAPI application initialized and configured successfully")
    return app

# Initialize the API Gateway
api_gateway = initialize_api_gateway()