"""
This file contains the configuration settings for the Metrics Input Service.
It is responsible for managing environment-specific settings and configurations
that are used throughout the service.

Requirements addressed:
- Configuration Management (Technical Requirements/Feature 2: API Development and Deployment)
  Ensure the API supports configuration management to handle different environments and settings.
"""

from pydantic import BaseSettings  # version 1.8.2

class Settings(BaseSettings):
    """
    Represents the configuration settings for the Metrics Input Service.
    
    Attributes:
        database_url (str): The URL for connecting to the PostgreSQL database.
        api_key (str): The API key for authenticating with external services.
        log_level (str): The logging level for the application.
    """

    database_url: str
    api_key: str
    log_level: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def load_settings() -> Settings:
    """
    Loads and validates the configuration settings for the Metrics Input Service.

    Returns:
        Settings: The validated configuration settings instance.

    Steps:
    1. Define a Pydantic BaseSettings class to represent the configuration schema.
    2. Load environment variables and default values into the Settings class.
    3. Validate the loaded settings using Pydantic's validation mechanisms.
    4. Return the validated Settings instance for use throughout the service.
    """
    return Settings()

# Global instance of the settings
settings = load_settings()

# Note: Ensure that the .env file is correctly set up with the necessary environment variables
# such as DATABASE_URL, API_KEY, and LOG_LEVEL to avoid runtime errors.

# Imports from related modules
from src.backend.metrics_input_service.app.models.models import MetricsInput
from src.backend.metrics_input_service.app.routers.metrics import router as metrics_router

# Ensure that all imported modules and components are correctly utilized within the service
# and that any unused imports are removed to maintain code cleanliness and efficiency.

# Comments for potential changes in other files:
# - Ensure that the database session management is implemented in the routers to handle
#   database connections efficiently.
# - Validate that all API endpoints are correctly documented and tested for expected behavior.
# - Consider implementing additional logging configurations to capture detailed logs
#   for monitoring and debugging purposes.