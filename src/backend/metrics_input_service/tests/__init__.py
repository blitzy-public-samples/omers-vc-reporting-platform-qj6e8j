"""
This file initializes the test suite for the Metrics Input Service, organizing and preparing
the test environment for executing unit tests related to financial metrics input.

Requirements addressed:
- Automated Testing and Quality Assurance (Technical Requirements/Feature 13: Automated Testing and Quality Assurance)
  Description: Develop unit tests for all critical components of the FastAPI application using pytest.

Dependencies:
- pytest (version 6.2.4): Used for writing and executing unit tests.
- test_create_metrics (from src/backend/metrics_input_service/tests/test_metrics.py):
  Tests the creation of new financial metrics data entries via the API.
- test_get_metrics (from src/backend/metrics_input_service/tests/test_metrics.py):
  Tests the retrieval of financial metrics data based on specified query parameters.

This file integrates and organizes test cases for the Metrics Input Service by:
1. Importing test cases from test_metrics.py.
2. Ensuring that pytest recognizes the test cases for execution.
3. Preparing any necessary test fixtures or configurations.
"""

# Import pytest for test suite configuration
import pytest

# Import test cases from test_metrics.py
from .test_metrics import test_create_metrics, test_get_metrics

# Configure pytest to discover and run the imported test functions
pytest.register_assert_rewrite('src.backend.metrics_input_service.tests.test_metrics')

# Any additional test suite configuration or fixtures can be added here
# For example:
@pytest.fixture(scope="module")
def api_client():
    """
    Fixture to provide a test client for API requests.
    This fixture sets up the FastAPI test client for use in test cases.
    """
    from fastapi.testclient import TestClient
    from src.backend.metrics_input_service.main import create_app
    app = create_app()
    return TestClient(app)

# Note: The actual implementation of fixtures and additional configurations
# would depend on the specific needs of the Metrics Input Service tests.