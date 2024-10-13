"""
This file initializes the routing components for the Metrics Input Service,
integrating the defined API endpoints to facilitate operations related to financial metrics data.

Requirements addressed:
- API Services (Technical Requirements/Feature 2: API Development and Deployment):
  Develop the API using FastAPI framework to ensure high performance and scalability.
"""

from fastapi import APIRouter  # FastAPI version 0.68.0
from .metrics import router as metrics_router

# Create a main router for the Metrics Input Service
router = APIRouter()

# Include the metrics router
router.include_router(metrics_router, prefix="/metrics", tags=["metrics"])

# This router can be imported and included in the main FastAPI application
# to register all the endpoints defined in the metrics module.