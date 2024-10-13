# src/backend/reporting_financials_service/app/routers/__init__.py

"""
This file initializes the routers for the Reporting Financials Service, integrating various API endpoints
related to financial reports into the FastAPI application.

Requirements addressed:
- API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
  Develop and deploy the FastAPI-based RESTful API to facilitate secure and efficient data ingestion
  and retrieval from the PostgreSQL database.

Dependencies:
- FastAPI (version 0.68.0): Used to create the API application and manage HTTP requests.
- financials_router from src/backend/reporting_financials_service/app/routers/financials.py:
  Defines the API endpoints for managing and retrieving financial reports.
"""

from fastapi import APIRouter
from .financials import router as financials_router

# Create a main router for the Reporting Financials Service
router = APIRouter()

# Include the financials router
router.include_router(financials_router, prefix="/financials", tags=["financials"])

# Export the main router for use in the FastAPI application
__all__ = ["router"]