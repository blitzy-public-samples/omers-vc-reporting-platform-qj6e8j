"""
This module serves as the initializer for the test suite of the API Gateway component.
It ensures that all necessary test modules and configurations are properly set up,
allowing for the execution of unit and integration tests to validate the functionality
and reliability of the API Gateway.

Requirements Addressed:
- Automated Testing and Quality Assurance
  Location: Technical Requirements/Feature 13: Automated Testing and Quality Assurance
  Description: Implement automated testing frameworks and quality assurance processes
               to ensure the reliability and robustness of the backend platform.
"""

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient

# Import the necessary components for testing
from src.backend.api_gateway.main import create_app
from src.backend.api_gateway.app.routers.routes import setup_routes

# pytest version 6.2.4
# httpx version 0.18.2

def pytest_configure(config):
    """
    Pytest configuration hook to set up the test environment.
    This function is called once at the beginning of a test run.
    """
    # You can add any global test configurations here if needed
    pass

@pytest.fixture(scope="module")
def test_app():
    """
    Fixture to create a test instance of the FastAPI application.
    This fixture is scoped to the module level, meaning it's created once per test module.
    
    Returns:
        TestClient: A test client for the FastAPI application.
    """
    app = create_app()
    setup_routes(app)
    client = TestClient(app)
    yield client

@pytest.fixture(scope="module")
async def async_test_client():
    """
    Fixture to create an asynchronous test client for the FastAPI application.
    This fixture is useful for testing asynchronous endpoints.
    
    Yields:
        AsyncClient: An asynchronous test client for the FastAPI application.
    """
    app = create_app()
    setup_routes(app)
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# Add any additional fixtures or setup code needed for your tests here