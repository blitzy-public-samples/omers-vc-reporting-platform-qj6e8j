import os
from pydantic import BaseSettings, Field, validator

# Requirements addressed:
# - API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
#   This configuration file supports the development of the FastAPI-based RESTful API
#   by providing necessary environment variables and settings.

class Settings(BaseSettings):
    """
    Configuration settings for the Reporting Metrics Service.
    
    This class uses Pydantic's BaseSettings to manage environment variables
    and provide default values where necessary.
    """
    
    # Environment setting
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')
    
    # Database configuration
    DATABASE_URL: str = Field(..., env='DATABASE_URL')
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Reporting Metrics Service"
    
    # Security settings
    # Required from environment; no insecure default (CWE-798/CWE-259)
    SECRET_KEY: str = Field(..., min_length=32, env='SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list = ['http://localhost:3000', 'https://localhost:3000', 'http://localhost', 'https://localhost']
    
    # Logging configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # Azure Active Directory settings
    AZURE_AD_CLIENT_ID: str = os.getenv('AZURE_AD_CLIENT_ID')
    AZURE_AD_TENANT_ID: str = os.getenv('AZURE_AD_TENANT_ID')

    @validator('DATABASE_URL')
    def _validate_database_url(cls, v):
        # Require a non-empty PostgreSQL DSN; reject empty/malformed values (fail closed).
        from urllib.parse import urlparse
        parsed = urlparse(v or '')
        if not (parsed.scheme in ('postgresql', 'postgres') and parsed.netloc):
            raise ValueError("DATABASE_URL must be a non-empty PostgreSQL DSN (e.g. postgresql://user:pass@host:port/db).")
        return v
    
    class Config:
        case_sensitive = True
        env_file = '.env'

# Initialize settings
settings = Settings()

# Global variable for environment, as specified in the JSON specification
ENVIRONMENT = settings.ENVIRONMENT

# Note: Ensure that the environment variables are correctly set in the .env file or the system environment.
# This includes sensitive information such as DATABASE_URL and SECRET_KEY, which should be kept secure.

# Additional configuration or helper functions can be added here if needed.
# For example, functions to validate certain settings or to initialize logging configurations.

# Example of a helper function to validate CORS origins
def validate_cors_origins(origins: list):
    """
    Validates the list of CORS origins to ensure they are properly formatted URLs.
    
    Args:
        origins (list): List of CORS origin URLs.
    
    Raises:
        ValueError: If any of the origins are not valid URLs.
    """
    from urllib.parse import urlparse
    
    for origin in origins:
        result = urlparse(origin)
        if not all([result.scheme, result.netloc]):
            raise ValueError(f"Invalid CORS origin URL: {origin}")

# Validate CORS origins during initialization
try:
    validate_cors_origins(settings.BACKEND_CORS_ORIGINS)
except ValueError as e:
    print(f"Configuration Error: {e}")
    # Handle the error appropriately, such as logging or raising an exception