# This file serves as the initializer for the models package within the API Gateway component.
# It imports and exposes the data models defined in the models.py file, facilitating their use
# throughout the API Gateway application.

# Requirement Addressed:
# API Development and Deployment
# Location: Technical Requirements/Feature 2: API Development and Deployment
# Description: Develop the FastAPI-based RESTful API to facilitate secure and efficient data
# ingestion and retrieval from the PostgreSQL database.

from .models import ExampleModel, Company, MetricsInput, QuarterlyReportingFinancials, QuarterlyReportingMetrics

# Expose the models for easy import by other modules
__all__ = [
    'ExampleModel',
    'Company',
    'MetricsInput',
    'QuarterlyReportingFinancials',
    'QuarterlyReportingMetrics'
]

# Note: As more models are added to the models.py file, they should be imported and added to
# the __all__ list to make them available for import from the models package.