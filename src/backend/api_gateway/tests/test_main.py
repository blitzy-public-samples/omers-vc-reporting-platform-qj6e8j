import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from src.backend.api_gateway.main import create_app
from src.backend.api_gateway.app.routers.routes import setup_routes
from src.backend.api_gateway.app.models.models import ExampleModel, Company, MetricsInput, QuarterlyReportingFinancials, QuarterlyReportingMetrics

# This file contains unit tests for the main functionalities of the API Gateway component.
# It ensures that the FastAPI application is correctly initialized, routes are properly set up,
# and the API endpoints function as expected.

# Requirement addressed: Automated Testing and Quality Assurance
# Location: Technical Requirements/Feature 13: Automated Testing and Quality Assurance
# Description: Implement automated testing frameworks and quality assurance processes to ensure
# the reliability and robustness of the backend platform.

@pytest.fixture
def app():
    """
    Fixture to create a FastAPI application instance for testing.
    """
    return create_app()

@pytest.fixture
def client(app):
    """
    Fixture to create a test client for the FastAPI application.
    """
    return TestClient(app)

@pytest.mark.asyncio
async def test_create_app():
    """
    Test the initialization of the FastAPI application.
    """
    app = create_app()
    assert app is not None
    assert isinstance(app, FastAPI)

@pytest.mark.asyncio
async def test_setup_routes(app):
    """
    Test the setup of API routes in the FastAPI application.
    """
    setup_routes(app)
    routes = [route.path for route in app.routes]
    assert "/v1/input_metrics/" in routes
    assert "/v1/reporting_financials/" in routes
    assert "/v1/reporting_metrics/" in routes
    assert "/v1/company/" in routes

@pytest.mark.asyncio
async def test_example_endpoint(client):
    """
    Test a specific API endpoint to ensure it returns the expected response.
    """
    response = client.get("/v1/input_metrics/?company_id=test_id&start_reporting_date=2022-01-01&end_reporting_date=2022-12-31")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_example_model():
    """
    Test the ExampleModel to ensure it correctly handles data.
    """
    example = ExampleModel(name="Test", value=42)
    assert example.name == "Test"
    assert example.value == 42
    assert example.to_dict() == {"name": "Test", "value": 42}

@pytest.mark.asyncio
async def test_async_client():
    """
    Test asynchronous client requests to the API.
    """
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v1/input_metrics/?company_id=test_id&start_reporting_date=2022-01-01&end_reporting_date=2022-12-31")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_error_handling():
    """
    Test error handling in the API.
    """
    app = create_app()
    client = TestClient(app)
    response = client.get("/non_existent_endpoint")
    assert response.status_code == 404

# Additional tests can be added here to cover more specific functionalities
# of the API Gateway, such as authentication, rate limiting, etc.

if __name__ == "__main__":
    pytest.main(["-v", "test_main.py"])