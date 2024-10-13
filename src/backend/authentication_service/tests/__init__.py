# src/backend/authentication_service/tests/__init__.py

"""
Initialization module for the test suite of the authentication service, responsible for setting up the testing environment and importing necessary test modules.

This module addresses the following requirement:
- Authentication and Authorization Implementation (Technical Requirements/Feature 4: Authentication and Authorization Implementation)
  Implement secure authentication and authorization mechanisms to control access to the backend platform and its resources.

The __init__.py file sets up the testing environment for the authentication service by importing test modules and configuring pytest.
"""

# Import the test_authentication module to include its test cases in the test suite.
from src.backend.authentication_service.tests import test_authentication

# External dependency: pytest (version 6.2.5)
# Purpose: To provide a testing framework for writing and running test cases.
import pytest

# Configure pytest for the authentication service tests
def pytest_configure(config):
    """
    Configure pytest for the authentication service test suite.
    This function can be used to add custom markers, set up fixtures, or perform any other test suite configuration.
    """
    # Add custom markers if needed
    config.addinivalue_line(
        "markers", "auth: mark test as part of the authentication service test suite"
    )

# Optionally, you can define shared fixtures or helper functions here that can be used across multiple test files

# Example of a shared fixture (if needed):
# @pytest.fixture(scope="module")
# def auth_client():
#     # Set up a test client for authentication service
#     # This is just a placeholder and should be implemented based on your actual authentication service setup
#     from your_auth_service import create_test_client
#     client = create_test_client()
#     yield client
#     # Teardown code (if necessary)

# Ensure pytest discovers and runs the tests in the authentication service
pytest.main(["-v", "src/backend/authentication_service/tests"])