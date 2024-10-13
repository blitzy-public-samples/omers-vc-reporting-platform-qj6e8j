# src/backend/reporting_financials_service/app/models/__init__.py

"""
This file serves as the package initializer for the models module within the Reporting Financials Service.
It is responsible for importing and exposing the data models used in the service, facilitating their use
in other parts of the application.

Requirements addressed:
- Data Storage (Technical Specification/Feature 1: Database Setup and Configuration):
  Ensures that the data models for storing financial report entries are accessible throughout
  the Reporting Financials Service.
"""

from .models import FinancialReport

__all__ = ['FinancialReport']