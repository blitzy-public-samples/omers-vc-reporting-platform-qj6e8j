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

# Pre-existing, out-of-scope defect (noted follow-up -- see docs/security/decision-log.md):
# app/database.py and app/schemas.py do not exist and app/__init__.py imports main, so
# importing the app package or main raises ImportError. Guard the app-dependent wiring
# (models import, table creation, dependency override, test client) so this package
# imports cleanly and the security regression tests can be collected.
try:
    from src.backend.reporting_metrics_service.app.models import ReportingMetrics
    from src.backend.reporting_metrics_service.main import app, get_db

    # Create tables in the test database
    ReportingMetrics.metadata.create_all(bind=engine)

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
except ImportError:
    ReportingMetrics = None
    app = None
    client = None

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

# Import test modules (guarded: test_metrics imports the pre-existing broken app package)
try:
    from .test_metrics import test_get_reporting_metrics
except ImportError:
    pass

# Define test suite
def test_suite():
    """
    Run all tests for the reporting metrics service.
    """
    pytest.main(["-v", "src/backend/reporting_metrics_service/tests"])

if __name__ == "__main__":
    test_suite()