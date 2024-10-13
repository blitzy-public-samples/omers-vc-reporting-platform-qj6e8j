# src/backend/reporting_metrics_service/app/routers/__init__.py

from fastapi import APIRouter
from .metrics import router as metrics_router

# Initialize the main router for the reporting metrics service
router = APIRouter()

# Include the metrics router to handle requests related to reporting metrics
router.include_router(metrics_router, prefix="/metrics", tags=["Reporting Metrics"])

# This file initializes the routing for the reporting metrics service,
# integrating the defined API endpoints into the FastAPI application.
# It addresses the following requirement:
# - API Development and Deployment (Technical Requirements/Feature 2)
#   Develop the FastAPI-based RESTful API to facilitate secure and efficient
#   data ingestion and retrieval from the PostgreSQL database.

# The router defined here can be imported and included in the main FastAPI
# application to enable routing of requests to the appropriate endpoint handlers.

# Note: Ensure that all imported modules and functions are correctly implemented
# and available in the specified paths. The metrics router should define all
# necessary endpoints for managing reporting metrics.