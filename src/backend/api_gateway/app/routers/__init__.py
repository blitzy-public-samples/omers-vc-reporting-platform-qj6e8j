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
from src.backend.api_gateway.main import create_app

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

# The following code is not typically included in an __init__.py file,
# but is added here to demonstrate how the initialize_routes function would be used.

# Create the FastAPI application instance
app = create_app()

# Initialize the routes
initialize_routes(app)

# Note: In a real-world scenario, the app creation and route initialization
# would typically be done in the main.py file or a separate application factory function.