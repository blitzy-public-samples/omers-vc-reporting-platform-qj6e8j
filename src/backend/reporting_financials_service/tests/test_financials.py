import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from src.backend.reporting_financials_service.main import create_app
from src.backend.reporting_financials_service.app.models.models import FinancialReport
from src.backend.reporting_financials_service.app.routers.financials import financials_router

# Import the database URL from your config
from src.backend.reporting_financials_service.config import DATABASE_URL

# Create an async engine for testing
test_engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)

# Override the dependency in your FastAPI app
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app = create_app()
app.dependency_overrides[financials_router.get_db] = override_get_db

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_get_financial_reports(async_client):
    """
    Test the retrieval of financial reports from the API.
    
    This test verifies that the GET request to '/financial_reports/' endpoint
    returns the expected financial report entries.
    
    Requirements addressed:
    - Automated Testing and Quality Assurance
    Location: Technical Requirements/Feature 13: Automated Testing and Quality Assurance
    """
    # Prepare test data
    test_company_id = "test-company-123"
    test_reporting_year = 2023
    test_reporting_quarter = 2
    
    # Send GET request to the endpoint
    response = await async_client.get(
        f"/financial_reports/?company_id={test_company_id}&reporting_year={test_reporting_year}&reporting_quarter={test_reporting_quarter}"
    )
    
    # Assert response status code
    assert response.status_code == 200
    
    # Parse response data
    data = response.json()
    
    # Verify that the response data matches the expected structure
    assert isinstance(data, list)
    if len(data) > 0:
        assert "company_id" in data[0]
        assert "reporting_year" in data[0]
        assert "reporting_quarter" in data[0]
        assert "currency" in data[0]
        assert "total_revenue" in data[0]
        # Add more assertions for other expected fields

@pytest.mark.asyncio
async def test_create_financial_report(async_client):
    """
    Test the creation of a new financial report entry via the API.
    
    This test verifies that a POST request to '/financial_reports/' endpoint
    successfully creates a new financial report entry.
    
    Requirements addressed:
    - Automated Testing and Quality Assurance
    Location: Technical Requirements/Feature 13: Automated Testing and Quality Assurance
    """
    # Prepare test data
    test_financial_report = {
        "company_id": "test-company-456",
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
        "fiscal_reporting_date": "2023-09-30",
        "fiscal_reporting_quarter": 3,
        "reporting_year": 2023,
        "reporting_quarter": 3,
        "employees": 100,
        "customers": 1000
    }
    
    # Send POST request to create a new financial report
    response = await async_client.post("/financial_reports/", json=test_financial_report)
    
    # Assert response status code
    assert response.status_code == 201
    
    # Parse response data
    data = response.json()
    
    # Verify that the response data contains the newly created financial report entry
    assert data["company_id"] == test_financial_report["company_id"]
    assert data["reporting_year"] == test_financial_report["reporting_year"]
    assert data["reporting_quarter"] == test_financial_report["reporting_quarter"]
    assert data["currency"] == test_financial_report["currency"]
    assert data["total_revenue"] == test_financial_report["total_revenue"]
    # Add more assertions for other fields

@pytest.mark.asyncio
async def test_update_financial_report(async_client):
    """
    Test the update of an existing financial report entry via the API.
    
    This test verifies that a PUT request to '/financial_reports/{report_id}' endpoint
    successfully updates an existing financial report entry.
    
    Requirements addressed:
    - Automated Testing and Quality Assurance
    Location: Technical Requirements/Feature 13: Automated Testing and Quality Assurance
    """
    # Prepare test data
    test_report_id = "test-report-789"
    update_data = {
        "total_revenue": 1100000.00,
        "recurring_revenue": 900000.00,
        "gross_profit": 650000.00
    }
    
    # Send PUT request to update the financial report
    response = await async_client.put(f"/financial_reports/{test_report_id}", json=update_data)
    
    # Assert response status code
    assert response.status_code == 200
    
    # Parse response data
    data = response.json()
    
    # Verify that the response data contains the updated financial report entry
    assert data["id"] == test_report_id
    assert data["total_revenue"] == update_data["total_revenue"]
    assert data["recurring_revenue"] == update_data["recurring_revenue"]
    assert data["gross_profit"] == update_data["gross_profit"]

@pytest.mark.asyncio
async def test_delete_financial_report(async_client):
    """
    Test the deletion of a financial report entry via the API.
    
    This test verifies that a DELETE request to '/financial_reports/{report_id}' endpoint
    successfully deletes an existing financial report entry.
    
    Requirements addressed:
    - Automated Testing and Quality Assurance
    Location: Technical Requirements/Feature 13: Automated Testing and Quality Assurance
    """
    # Prepare test data
    test_report_id = "test-report-101"
    
    # Send DELETE request to remove the financial report
    response = await async_client.delete(f"/financial_reports/{test_report_id}")
    
    # Assert response status code
    assert response.status_code == 204
    
    # Verify that the report no longer exists
    get_response = await async_client.get(f"/financial_reports/{test_report_id}")
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_get_financial_report_by_id(async_client):
    """
    Test the retrieval of a specific financial report by ID from the API.
    
    This test verifies that a GET request to '/financial_reports/{report_id}' endpoint
    returns the expected financial report entry.
    
    Requirements addressed:
    - Automated Testing and Quality Assurance
    Location: Technical Requirements/Feature 13: Automated Testing and Quality Assurance
    """
    # Prepare test data
    test_report_id = "test-report-202"
    
    # Send GET request to retrieve the specific financial report
    response = await async_client.get(f"/financial_reports/{test_report_id}")
    
    # Assert response status code
    assert response.status_code == 200
    
    # Parse response data
    data = response.json()
    
    # Verify that the response data matches the expected structure
    assert data["id"] == test_report_id
    assert "company_id" in data
    assert "reporting_year" in data
    assert "reporting_quarter" in data
    assert "currency" in data
    assert "total_revenue" in data
    # Add more assertions for other expected fields

# Add more test cases as needed to cover edge cases, error handling, etc.