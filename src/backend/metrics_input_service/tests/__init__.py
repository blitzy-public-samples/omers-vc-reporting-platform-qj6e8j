"""
This file initializes the test suite for the Metrics Input Service, organizing and preparing
the test environment for executing unit tests related to financial metrics input.

Requirements addressed:
- Automated Testing and Quality Assurance (Technical Requirements/Feature 13: Automated Testing and Quality Assurance)
  Description: Develop unit tests for all critical components of the FastAPI application using pytest.

Dependencies:
- pytest (version 6.2.4): Used for writing and executing unit tests.

This package initializer is intentionally free of import-time side effects: pytest
discovers the test modules in this directory automatically, so no test module is
imported here. It only exposes optional shared fixtures for the test suite.
"""

# Import pytest for test suite configuration
import pytest

# Test modules are discovered automatically by pytest; this package __init__ must
# remain free of import-time side effects. A prior revision eagerly imported
# test_metrics here, which pulled in the application import chain (config.py imports
# app.models/app.routers, and app/__init__.py has a pre-existing, out-of-scope
# SyntaxError), aborting collection of every module in this package -- including the
# CORS security regression test. The eager import has been removed so
# test_security_cors.py collects; test_metrics.py still imports the application chain
# directly, so that pre-existing defect continues to surface at its own collection.

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