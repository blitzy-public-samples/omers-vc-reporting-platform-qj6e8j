import pytest
from fastapi.testclient import TestClient
from datetime import date, datetime
from uuid import uuid4
from decimal import Decimal

# Import the create_app function from the main module
from src.backend.metrics_input_service.main import create_app

# Import the MetricsInput model
from src.backend.metrics_input_service.app.models.models import MetricsInput

# pytest.mark.asyncio decorator for asynchronous tests
pytestmark = pytest.mark.asyncio

# Create a test client using the create_app function
@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)

# Test function for creating new metrics
async def test_create_metrics(client):
    """
    Test the creation of new financial metrics data entries via the API.
    This test ensures that the POST /metrics/ endpoint behaves as expected,
    validating data submission and response.

    Requirements addressed:
    - Automated Testing and Quality Assurance
    Location: Technical Requirements/Feature 13: Automated Testing and Quality Assurance
    Description: Develop unit tests for all critical components of the FastAPI application using pytest.
    """
    # Define a sample payload representing valid financial metrics data
    sample_metrics = {
        "id": str(uuid4()),
        "company_id": str(uuid4()),
        "currency": "USD",
        "total_revenue": 1000000.00,
        "recurring_revenue": 800000.00,
        "gross_profit": 600000.00,
        "sales_marketing_expense": 200000.00,
        "total_operating_expense": 700000.00,
        "ebitda": 300000.00,
        "net_income": 250000.00,
        "cash_burn": 50000.00,
        "cash_balance": 2000000.00,
        "debt_outstanding": 500000.00,
        "employees": 50,
        "customers": 100,
        "fiscal_reporting_date": str(date.today()),
        "fiscal_reporting_quarter": 2,
        "reporting_year": 2023,
        "reporting_quarter": 2,
        "created_date": str(datetime.now()),
        "created_by": "test_user",
        "last_update_date": None,
        "last_updated_by": None
    }

    # Send a POST request to the '/metrics/' endpoint with the sample payload
    response = client.post("/api/v1/metrics/", json=sample_metrics)

    # Assert that the response status code is 200, indicating success
    assert response.status_code == 200

    # Assert that the response contains a confirmation message
    assert "message" in response.json()
    assert "successfully created" in response.json()["message"]

# Test function for retrieving metrics
async def test_get_metrics(client):
    """
    Test the retrieval of financial metrics data based on specified query parameters.
    This test ensures that the GET /metrics/ endpoint behaves as expected,
    validating data retrieval and response format.

    Requirements addressed:
    - Automated Testing and Quality Assurance
    Location: Technical Requirements/Feature 13: Automated Testing and Quality Assurance
    Description: Develop unit tests for all critical components of the FastAPI application using pytest.
    """
    # Generate a sample company_id
    company_id = str(uuid4())

    # Define query parameters for retrieving metrics
    params = {
        "company_id": company_id,
        "start_date": str(date(2023, 1, 1)),
        "end_date": str(date(2023, 12, 31))
    }

    # Send a GET request to the '/metrics/' endpoint with query parameters
    response = client.get("/api/v1/metrics/", params=params)

    # Assert that the response status code is 200, indicating success
    assert response.status_code == 200

    # Assert that the response contains a list of financial metrics entries
    assert isinstance(response.json(), list)

    # If the list is not empty, check the structure of the first item
    if response.json():
        first_item = response.json()[0]
        assert "id" in first_item
        assert "company_id" in first_item
        assert "currency" in first_item
        assert "total_revenue" in first_item
        # Add more assertions for other fields as needed

# Additional test cases can be added here to cover more scenarios,
# such as testing with invalid data, edge cases, or specific error conditions.