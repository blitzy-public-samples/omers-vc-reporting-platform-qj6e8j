"""
This module serves as the initialization for the test suite of the Reporting Financials Service.
It sets up the necessary test configurations and imports required for running unit and integration
tests on the financial reporting functionalities.

Requirements Addressed:
    - Automated Testing and Quality Assurance
      Location: Technical Requirements/Feature 13: Automated Testing and Quality Assurance
      Description: Implement automated testing frameworks and quality assurance processes to ensure
                   the reliability and robustness of the backend platform.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Import the FastAPI app instance for testing
from src.backend.reporting_financials_service.main import create_app
from src.backend.reporting_financials_service.app.models.models import FinancialReport
from src.backend.reporting_financials_service.app.routers.financials import financials_router

# Create a test database URL (use an in-memory SQLite database for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create an async engine for the test database
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)

# Create a sessionmaker for creating test database sessions
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
    class_=AsyncSession
)

# Create a test FastAPI application
test_app = create_app()

@pytest.fixture
async def test_client():
    """
    Fixture to create a test client for making requests to the FastAPI application.
    
    Returns:
        AsyncClient: An asynchronous test client for the FastAPI application.
    """
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def test_db():
    """
    Fixture to set up and tear down a test database session.
    
    Yields:
        AsyncSession: An asynchronous database session for testing.
    """
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture(autouse=True)
async def setup_test_database():
    """
    Fixture to set up the test database before running tests and clean up after.
    This fixture runs automatically for all tests.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(FinancialReport.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(FinancialReport.metadata.drop_all)

# Import test modules here to ensure they are discovered by pytest
from . import test_financials

# Optionally, you can add more configuration or setup code for the test suite here