"""
This file contains the configuration settings for the Metrics Input Service.
It is responsible for managing environment-specific settings and configurations
that are used throughout the service.

Requirements addressed:
- Configuration Management (Technical Requirements/Feature 2: API Development and Deployment)
  Ensure the API supports configuration management to handle different environments and settings.
"""

from pydantic import BaseSettings, validator  # version 1.8.2

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

    # CWE-942: explicit non-wildcard CORS allow-list (never "*"); overridable via env
    CORS_ORIGINS: list = ['http://localhost:3000', 'https://localhost:3000']

    @validator('CORS_ORIGINS', always=True)
    def _validate_cors_origins(cls, value):
        # CWE-942: fail closed on any invalid entry; only explicit http(s) origins are allowed.
        from urllib.parse import urlparse
        if not value:
            raise ValueError("CORS_ORIGINS must define at least one explicit origin")
        for origin in value:
            if not isinstance(origin, str) or "*" in origin:
                raise ValueError("CORS_ORIGINS must not contain wildcard entries")
            parsed = urlparse(origin)
            if parsed.scheme not in ("http", "https"):
                raise ValueError("CORS_ORIGINS entries must use the http or https scheme")
            if not parsed.netloc:
                raise ValueError("CORS_ORIGINS entries must include a host")
            if parsed.username or parsed.password:
                raise ValueError("CORS_ORIGINS entries must not include userinfo")
            if parsed.path or parsed.query or parsed.fragment:
                raise ValueError("CORS_ORIGINS entries must be bare origins (no path, query, or fragment)")
        return value

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