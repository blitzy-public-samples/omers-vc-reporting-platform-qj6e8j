"""
This file is responsible for initializing and setting up the routing logic for the API Gateway component of the backend platform.
It imports and configures the necessary routes for the FastAPI application, ensuring that all endpoints are correctly registered and accessible.

Requirements addressed:
- API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
  Develop the FastAPI-based RESTful API to facilitate secure and efficient data ingestion and retrieval from the PostgreSQL database.
"""

from fastapi import FastAPI
from src.backend.api_gateway.app.routers.routes import setup_routes
from src.backend.api_gateway.config import Settings

def initialize_routes(app: FastAPI) -> None:
    """
    Sets up and initializes the API routes for the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.

    Returns:
        None: This function does not return a value.
    """
    # Import the setup_routes function from the routes module
    setup_routes(app)

# No application is instantiated at import time: doing so created a circular
# import with main.py (F-GW-1). The application is built by create_app() in
# main.py, which wires routes via setup_routes(); initialize_routes above
# remains available for callers that construct the app explicitly.