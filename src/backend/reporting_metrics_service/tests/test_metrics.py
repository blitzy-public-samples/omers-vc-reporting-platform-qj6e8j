import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal

# Import necessary modules and functions from the reporting_metrics_service
from src.backend.reporting_metrics_service.app.routers.metrics import get_reporting_metrics
from src.backend.reporting_metrics_service.app.models.models import ReportingMetrics
from src.backend.reporting_metrics_service.main import app

# Import the version of FastAPI used in the project
# FastAPI version: 0.68.0
from fastapi import FastAPI

# Import the version of SQLAlchemy used in the project
# SQLAlchemy version: 1.4.22
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Pytest version: 6.2.4 (as specified in the JSON)

# Create a test database engine and session
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a test client
client = TestClient(app)

@pytest.fixture
def db_session():
    """
    Fixture to create a new database session for each test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

def create_test_reporting_metrics(db: Session):
    """
    Helper function to create test reporting metrics data.
    """
    test_metrics = ReportingMetrics(
        company_id=UUID("12345678-1234-5678-1234-567812345678"),
        currency="USD",
        enterprise_value=Decimal("1000000.00"),
        arr=Decimal("100000.00"),
        recurring_percentage_revenue=Decimal("0.8"),
        revenue_per_fte=Decimal("50000.00"),
        gross_profit_per_fte=Decimal("30000.00"),
        employee_growth_rate=Decimal("0.1"),
        change_in_cash=Decimal("50000.00"),
        revenue_growth=Decimal("0.2"),
        monthly_cash_burn=Decimal("10000.00"),
        runway_months=12,
        ev_by_equity_raised_plus_debt=Decimal("2.5"),
        sales_marketing_percentage_revenue=Decimal("0.3"),
        total_operating_percentage_revenue=Decimal("0.7"),
        gross_profit_margin=Decimal("0.6"),
        valuation_to_revenue=Decimal("10.0"),
        yoy_growth_revenue=Decimal("0.25"),
        yoy_growth_profit=Decimal("0.15"),
        yoy_growth_employees=Decimal("0.05"),
        yoy_growth_ltm_revenue=Decimal("0.3"),
        ltm_total_revenue=Decimal("500000.00"),
        ltm_gross_profit=Decimal("300000.00"),
        ltm_sales_marketing_expense=Decimal("100000.00"),
        ltm_gross_margin=Decimal("0.6"),
        ltm_operating_expense=Decimal("350000.00"),
        ltm_ebitda=Decimal("150000.00"),
        ltm_net_income=Decimal("100000.00"),
        ltm_ebitda_margin=Decimal("0.3"),
        ltm_net_income_margin=Decimal("0.2"),
        fiscal_reporting_date=date(2022, 12, 31),
        fiscal_reporting_quarter=4,
        reporting_year=2022,
        reporting_quarter=4,
        created_date=datetime.utcnow(),
        created_by="test_user",
        last_update_date=None,
        last_updated_by=None
    )
    db.add(test_metrics)
    db.commit()
    db.refresh(test_metrics)
    return test_metrics

@pytest.mark.asyncio
async def test_get_reporting_metrics(db_session: Session):
    """
    Test the API endpoint for retrieving reporting metrics to ensure it returns the correct data.
    
    This test addresses the requirement:
    - Automated Testing and Quality Assurance
    Location: Technical Requirements/Feature 13: Automated Testing and Quality Assurance
    Description: Implement automated testing frameworks and quality assurance processes to ensure
    the reliability and robustness of the backend platform.
    """
    # Create test data
    test_metrics = create_test_reporting_metrics(db_session)
    
    # Set up a test client using FastAPI's TestClient
    client = TestClient(app)
    
    # Send a GET request to the /metrics endpoint with test query parameters
    response = client.get(f"/reporting-metrics/metrics?company_id={test_metrics.company_id}&reporting_year={test_metrics.reporting_year}&reporting_quarter={test_metrics.reporting_quarter}")
    
    # Assert that the response status code is 200
    assert response.status_code == 200
    
    # Validate that the response data matches the expected test data
    data = response.json()
    assert data[0]["company_id"] == str(test_metrics.company_id)
    assert data[0]["currency"] == test_metrics.currency
    assert float(data[0]["enterprise_value"]) == float(test_metrics.enterprise_value)
    assert float(data[0]["arr"]) == float(test_metrics.arr)
    assert float(data[0]["recurring_percentage_revenue"]) == float(test_metrics.recurring_percentage_revenue)
    assert float(data[0]["revenue_per_fte"]) == float(test_metrics.revenue_per_fte)
    assert float(data[0]["gross_profit_per_fte"]) == float(test_metrics.gross_profit_per_fte)
    assert float(data[0]["employee_growth_rate"]) == float(test_metrics.employee_growth_rate)
    assert float(data[0]["change_in_cash"]) == float(test_metrics.change_in_cash)
    assert float(data[0]["revenue_growth"]) == float(test_metrics.revenue_growth)
    assert float(data[0]["monthly_cash_burn"]) == float(test_metrics.monthly_cash_burn)
    assert data[0]["runway_months"] == test_metrics.runway_months
    assert float(data[0]["ev_by_equity_raised_plus_debt"]) == float(test_metrics.ev_by_equity_raised_plus_debt)
    assert float(data[0]["sales_marketing_percentage_revenue"]) == float(test_metrics.sales_marketing_percentage_revenue)
    assert float(data[0]["total_operating_percentage_revenue"]) == float(test_metrics.total_operating_percentage_revenue)
    assert float(data[0]["gross_profit_margin"]) == float(test_metrics.gross_profit_margin)
    assert float(data[0]["valuation_to_revenue"]) == float(test_metrics.valuation_to_revenue)
    assert float(data[0]["yoy_growth_revenue"]) == float(test_metrics.yoy_growth_revenue)
    assert float(data[0]["yoy_growth_profit"]) == float(test_metrics.yoy_growth_profit)
    assert float(data[0]["yoy_growth_employees"]) == float(test_metrics.yoy_growth_employees)
    assert float(data[0]["yoy_growth_ltm_revenue"]) == float(test_metrics.yoy_growth_ltm_revenue)
    assert float(data[0]["ltm_total_revenue"]) == float(test_metrics.ltm_total_revenue)
    assert float(data[0]["ltm_gross_profit"]) == float(test_metrics.ltm_gross_profit)
    assert float(data[0]["ltm_sales_marketing_expense"]) == float(test_metrics.ltm_sales_marketing_expense)
    assert float(data[0]["ltm_gross_margin"]) == float(test_metrics.ltm_gross_margin)
    assert float(data[0]["ltm_operating_expense"]) == float(test_metrics.ltm_operating_expense)
    assert float(data[0]["ltm_ebitda"]) == float(test_metrics.ltm_ebitda)
    assert float(data[0]["ltm_net_income"]) == float(test_metrics.ltm_net_income)
    assert float(data[0]["ltm_ebitda_margin"]) == float(test_metrics.ltm_ebitda_margin)
    assert float(data[0]["ltm_net_income_margin"]) == float(test_metrics.ltm_net_income_margin)
    assert data[0]["fiscal_reporting_date"] == test_metrics.fiscal_reporting_date.isoformat()
    assert data[0]["fiscal_reporting_quarter"] == test_metrics.fiscal_reporting_quarter
    assert data[0]["reporting_year"] == test_metrics.reporting_year
    assert data[0]["reporting_quarter"] == test_metrics.reporting_quarter

@pytest.mark.asyncio
async def test_get_reporting_metrics_not_found(db_session: Session):
    """
    Test the API endpoint for retrieving reporting metrics when the data is not found.
    
    This test addresses the requirement:
    - Automated Testing and Quality Assurance
    Location: Technical Requirements/Feature 13: Automated Testing and Quality Assurance
    Description: Implement automated testing frameworks and quality assurance processes to ensure
    the reliability and robustness of the backend platform.
    """
    # Set up a test client using FastAPI's TestClient
    client = TestClient(app)
    
    # Send a GET request to the /metrics endpoint with non-existent data
    response = client.get("/reporting-metrics/metrics?company_id=00000000-0000-0000-0000-000000000000&reporting_year=2022&reporting_quarter=4")
    
    # Assert that the response status code is 404 (Not Found)
    assert response.status_code == 404
    
    # Validate the error message
    data = response.json()
    assert data["detail"] == "No reporting metrics found for the given parameters."

@pytest.mark.asyncio
async def test_get_reporting_metrics_invalid_params(db_session: Session):
    """
    Test the API endpoint for retrieving reporting metrics with invalid parameters.
    
    This test addresses the requirement:
    - Automated Testing and Quality Assurance
    Location: Technical Requirements/Feature 13: Automated Testing and Quality Assurance
    Description: Implement automated testing frameworks and quality assurance processes to ensure
    the reliability and robustness of the backend platform.
    """
    # Set up a test client using FastAPI's TestClient
    client = TestClient(app)
    
    # Send a GET request to the /metrics endpoint with invalid parameters
    response = client.get("/reporting-metrics/metrics?company_id=invalid-uuid&reporting_year=invalid&reporting_quarter=invalid")
    
    # Assert that the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 422
    
    # Validate the error messages
    data = response.json()
    assert "detail" in data
    errors = data["detail"]
    assert any(error["loc"] == ["query", "company_id"] for error in errors)
    assert any(error["loc"] == ["query", "reporting_year"] for error in errors)
    assert any(error["loc"] == ["query", "reporting_quarter"] for error in errors)

# Add more test cases as needed to cover different scenarios and edge cases