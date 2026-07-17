"""
This file initializes the test suite for the reporting metrics service, ensuring that all test modules are correctly imported and executed. It sets up the necessary environment for running unit tests on the reporting metrics service components.

Requirements addressed:
- Automated Testing and Quality Assurance (Technical Requirements/Feature 13: Automated Testing and Quality Assurance)
  Description: Implement automated testing frameworks and quality assurance processes to ensure the reliability and robustness of the backend platform.

Dependencies:
- pytest (version 6.2.4): Framework for writing and executing test cases.
- test_get_reporting_metrics (from src/backend/reporting_metrics_service/tests/test_metrics.py): To test the functionality of the API endpoint for retrieving reporting metrics data.
"""

import os

# Required from environment; config.Settings() fails closed without them (CWE-798/CWE-259).
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-ci-only-0123456789")  # >= 32 chars
os.environ.setdefault(
    "DATABASE_URL", "postgresql://testuser:testpass@localhost:5432/testdb"
)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Create a test database in memory
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# The reporting-metrics application package has a pre-existing, out-of-scope import-time
# defect: app/models/models.py does `from sqlalchemy import ... UUID`, which SQLAlchemy
# 1.4.x does not provide (no top-level UUID), and app/database.py / app/schemas.py are
# absent. Per the checkpoint's security-test-quality requirement, this application import
# is deliberately NOT wrapped in a masking `except ImportError` guard: a broken app import
# must surface as a loud collection/runtime error, never be swallowed into
# app=None/client=None (which would present a false-green suite). The underlying app
# defect is separately tracked in docs/security/decision-log.md.
from src.backend.reporting_metrics_service.app.models import ReportingMetrics
from src.backend.reporting_metrics_service.main import app, get_db

# Create tables in the test database
ReportingMetrics.metadata.create_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Setup function to initialize test data
@pytest.fixture(scope="module")
def setup_test_data():
    # Insert test data into the database to simulate real-world scenarios
    db = TestingSessionLocal()
    try:
        # Add test data here
        # Example:
        # test_metrics = ReportingMetrics(company_id="test_company_id", currency="USD", ...)
        # db.add(test_metrics)
        # db.commit()
        pass
    finally:
        db.close()

# Teardown function to clean up after tests
@pytest.fixture(scope="module")
def teardown_test_data():
    yield
    # Clean up test data after all tests have run
    db = TestingSessionLocal()
    try:
        # Remove test data here
        # Example:
        # db.query(ReportingMetrics).filter(ReportingMetrics.company_id == "test_company_id").delete()
        # db.commit()
        pass
    finally:
        db.close()

# Import test modules for discovery. Deliberately NOT wrapped in a masking guard: if
# test_metrics (which imports the application chain) fails to import, that failure must
# surface loudly rather than being silently swallowed.
from .test_metrics import test_get_reporting_metrics

# Define test suite
def test_suite():
    """
    Run all tests for the reporting metrics service.
    """
    pytest.main(["-v", "src/backend/reporting_metrics_service/tests"])

if __name__ == "__main__":
    test_suite()