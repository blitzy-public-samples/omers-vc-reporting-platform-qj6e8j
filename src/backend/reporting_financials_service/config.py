"""
This file provides configuration settings for the Reporting Financials Service, including database connection strings,
API keys, and other environment-specific variables necessary for the service's operation.

Requirements addressed:
- API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
  Develop and deploy the FastAPI-based RESTful API to facilitate secure and efficient data ingestion and retrieval
  from the PostgreSQL database.
"""

import os
from typing import List, Union
from pydantic import BaseSettings, PostgresDsn, SecretStr, Field, validator

class Config(BaseSettings):
    """
    Configuration class for the Reporting Financials Service.
    
    This class uses Pydantic's BaseSettings to automatically read environment variables
    and provide type checking and validation for configuration settings.
    """

    # Database configuration
    # Required from the environment; no default (a placeholder default would let the
    # service start with an unusable/misleading DSN). Fail closed if unset.
    DATABASE_URL: PostgresDsn = Field(..., env="DATABASE_URL")

    # API configuration
    API_KEY: SecretStr = os.getenv("API_KEY", "<your_api_key_here>")

    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Additional service-specific configurations can be added here
    SERVICE_NAME: str = "Reporting Financials Service"
    API_VERSION: str = "v1"

    # CORS settings
    # Union[str, List[str]] keeps Pydantic v1 from JSON-parsing the env var, so the
    # documented comma-separated CORS_ORIGINS string reaches the validator (see .env.sample / README).
    CORS_ORIGINS: Union[str, List[str]] = ["http://localhost:3000"]  # CWE-942: no wildcard; restrict origins

    # JWT settings for authentication
    JWT_SECRET_KEY: SecretStr = Field(..., min_length=32, env="JWT_SECRET_KEY")  # CWE-798/CWE-259: require from env, min length 32
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @validator('CORS_ORIGINS', pre=True, always=True, allow_reuse=True)  # allow_reuse: reload-safe under importlib.reload
    def _parse_and_validate_cors_origins(cls, v):
        # Accept comma-separated CORS_ORIGINS (see .env.sample / README) and reject
        # wildcard, empty, or malformed origins (CWE-942). Each entry must be a
        # serialized origin: http(s) scheme + host, optional valid port, and no
        # credentials, path, query, or fragment.
        if isinstance(v, str):
            v = [origin.strip() for origin in v.split(',') if origin.strip()]
        from urllib.parse import urlsplit
        if not v:
            raise ValueError("CORS_ORIGINS must be a non-empty explicit allow-list; wildcard '*' is not permitted.")
        for origin in v:
            if origin == '*':
                raise ValueError("Wildcard '*' CORS origin is not permitted with credentials (CWE-942).")
            parts = urlsplit(origin)
            try:
                parts.port  # accessing an invalid port raises ValueError
            except ValueError:
                raise ValueError(f"Invalid CORS origin (bad port): {origin}")
            if (parts.scheme not in ('http', 'https')
                    or not parts.hostname
                    or parts.username is not None
                    or parts.password is not None
                    or parts.path
                    or parts.query
                    or parts.fragment):
                raise ValueError(
                    f"Invalid CORS origin (expected scheme://host[:port] with no "
                    f"credentials/path/query/fragment): {origin}"
                )
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Instantiate the config object
config = Config()

# Constants derived from config
DATABASE_URL = config.DATABASE_URL
API_KEY = config.API_KEY.get_secret_value()
LOG_LEVEL = config.LOG_LEVEL
SERVICE_NAME = config.SERVICE_NAME
API_VERSION = config.API_VERSION
CORS_ORIGINS = config.CORS_ORIGINS
JWT_SECRET_KEY = config.JWT_SECRET_KEY.get_secret_value()
JWT_ALGORITHM = config.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES

# Additional constants and configurations can be defined here

# Example of a function to get a configuration value
def get_config_value(key: str) -> str:
    """
    Retrieve a configuration value by key.
    
    Args:
        key (str): The configuration key to retrieve.
    
    Returns:
        str: The value of the configuration key.
    
    Raises:
        AttributeError: If the key is not found in the configuration.
    """
    return getattr(config, key)

# Example usage:
# database_url = get_config_value("DATABASE_URL")