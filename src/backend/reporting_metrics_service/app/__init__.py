"""
This file initializes the Reporting Metrics Service application, setting up the FastAPI instance
and integrating necessary components such as models, routers, and configurations for handling
reporting metrics.

Requirements addressed:
- API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
  Develop the FastAPI-based RESTful API to facilitate secure and efficient data ingestion and
  retrieval from the PostgreSQL database.
"""

# External imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Internal imports
from src.backend.reporting_metrics_service.main import app as main_app
from src.backend.reporting_metrics_service.app.models.models import ReportingMetrics
from src.backend.reporting_metrics_service.config import settings

# Version information for third-party libraries (for reference)
# fastapi==0.68.0
# sqlalchemy==1.4.22

# Initialize the FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for managing and retrieving reporting metrics data",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # Adjust this in production to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from the main application
app.include_router(main_app.router, prefix=settings.API_V1_STR + "/metrics", tags=["metrics"])

# Configure application settings based on the ENVIRONMENT variable
if settings.ENVIRONMENT == "development":
    # Development-specific configurations
    app.debug = True
elif settings.ENVIRONMENT == "production":
    # Production-specific configurations
    app.debug = False

# Startup event to initialize database connection
@app.on_event("startup")
async def startup_event():
    """
    Perform any necessary startup operations
    """
    print(f"Starting Reporting Metrics Service in {settings.ENVIRONMENT} environment")
    # Initialize database connection
    # This is a placeholder and should be replaced with actual database initialization code
    pass

# Shutdown event to close database connection
@app.on_event("shutdown")
async def shutdown_event():
    """
    Perform any necessary cleanup operations
    """
    print("Shutting down Reporting Metrics Service")
    # Close database connection
    # This is a placeholder and should be replaced with actual database cleanup code
    pass

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {"status": "healthy", "environment": settings.ENVIRONMENT}

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint to verify service is running
    """
    return {"message": "Welcome to the Reporting Metrics Service API"}

# Make the ReportingMetrics model available for use in other parts of the application
app.state.reporting_metrics_model = ReportingMetrics

# Export the app instance for use in other modules
__all__ = ["app"]

# Note: Ensure that the database is properly initialized and migrated before running the service.
# This includes creating necessary tables and applying any pending migrations.
# Additionally, ensure that environment variables are set correctly, especially for sensitive information.