# src/backend/reporting_metrics_service/app/models/__init__.py

"""
This module serves as the initializer for the models package within the reporting metrics service.
It facilitates the import of data models used for ORM with the PostgreSQL database.

Requirements addressed:
- Data Consistency and Integrity (Technical Requirements/Feature 12: Data Consistency and Integrity)
  Ensures the consistency and integrity of financial data across all database tables and during all data processing operations.
"""

# Import the ReportingMetrics model from the models.py file
from src.backend.reporting_metrics_service.app.models.models import ReportingMetrics

# Import SQLAlchemy for ORM functionality
# SQLAlchemy version 1.4.22 is used for ORM to define database models and interact with the PostgreSQL database.
from sqlalchemy import __version__ as sqlalchemy_version

# Print SQLAlchemy version for debugging purposes
print(f"SQLAlchemy version: {sqlalchemy_version}")

# Export the ReportingMetrics model to make it available when importing from this package
__all__ = ['ReportingMetrics']