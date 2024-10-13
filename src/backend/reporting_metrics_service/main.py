# File: src/backend/reporting_metrics_service/main.py
# Description: This file serves as the entry point for the Reporting Metrics Service,
# initializing the FastAPI application, setting up routes, and configuring the service
# to handle HTTP requests related to reporting metrics.

# Requirements addressed:
# - API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
#   Develop the FastAPI-based RESTful API to facilitate secure and efficient data ingestion
#   and retrieval from the PostgreSQL database.

import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Internal imports
from src.backend.reporting_metrics_service.app.routers import metrics
from src.backend.reporting_metrics_service.app.models.models import ReportingMetrics
from src.backend.reporting_metrics_service.config import settings

# Initialize the database engine and session
DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize the FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for retrieving and managing reporting metrics data",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include routers
app.include_router(metrics.router, prefix=settings.API_V1_STR + "/reporting-metrics", tags=["reporting-metrics"])

@app.on_event("startup")
async def startup_event():
    """
    Perform any necessary startup operations
    """
    print(f"Starting Reporting Metrics Service in {settings.ENVIRONMENT} environment")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Perform any necessary cleanup operations
    """
    print("Shutting down Reporting Metrics Service")

@app.get("/")
async def root():
    """
    Root endpoint to verify service is running
    """
    return {"message": "Reporting Metrics Service is operational"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {"status": "healthy", "environment": settings.ENVIRONMENT}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Note: Ensure that the database is properly initialized and migrated before running the service.
# This includes creating necessary tables and applying any pending migrations.
# Additionally, ensure that environment variables are set correctly, especially for sensitive information.