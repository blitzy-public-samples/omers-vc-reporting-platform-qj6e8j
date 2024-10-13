# src/backend/metrics_input_service/app/models/__init__.py

# This file initializes the models for the Metrics Input Service, facilitating the import and integration
# of data models used for managing financial metrics input.

# Requirement addressed:
# Name: Data Storage
# Location: Technical Requirements/Feature 1: Database Setup and Configuration
# Description: Ensures that the data models are properly defined and accessible for storing financial metrics data in the PostgreSQL database.

# Import the MetricsInput model from the models module
from src.backend.metrics_input_service.app.models.models import MetricsInput

# Ensure that the MetricsInput model is accessible for use in routers and other application components
__all__ = ['MetricsInput']