"""
This file contains the configuration settings for the API Gateway component of the backend platform.
It manages environment-specific settings, such as database connections, API keys, and other
configuration parameters necessary for the operation of the FastAPI application.

Requirements addressed:
- API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
  Develop the FastAPI-based RESTful API to facilitate secure and efficient data ingestion and
  retrieval from the PostgreSQL database.
"""

import os
from typing import List, Union
from pydantic import BaseSettings, Field, validator

# Define the path to the .env file
ENV_FILE = '.env'

class Settings(BaseSettings):
    """
    A Pydantic BaseSettings class that defines the configuration settings for the API Gateway.
    
    This class uses Pydantic's BaseSettings to automatically load environment variables
    and provide type checking and validation for configuration values.
    """

    # Database connection string
    database_url: str = Field(..., env='DATABASE_URL')

    # API key for authentication
    api_key: str = Field(..., env='API_KEY')

    # Secret key for JWT token encoding/decoding (CWE-798/CWE-259: min length 32)
    secret_key: str = Field(..., min_length=32, env='SECRET_KEY')

    # CORS allow-list (CWE-942): explicit non-wildcard origins from CORS_ALLOW_ORIGINS
    cors_origins: Union[str, List[str]] = Field(default_factory=lambda: ["http://localhost:3000"], env='CORS_ALLOW_ORIGINS')

    # JWT algorithm
    algorithm: str = Field(default="HS256", env='ALGORITHM')

    @validator('cors_origins', pre=True, always=True, allow_reuse=True)  # allow_reuse: reload-safe under importlib.reload
    def _split_cors_origins(cls, v):
        # Accept comma-separated CORS_ALLOW_ORIGINS (see .env.sample) as an explicit list
        if isinstance(v, str):
            v = [origin.strip() for origin in v.split(',') if origin.strip()]
        # Reject wildcard, empty, or malformed origins (CWE-942). Each entry must be a
        # serialized origin: http(s) scheme + host, optional valid port, and no
        # credentials, path, query, or fragment.
        from urllib.parse import urlsplit
        if not v:
            raise ValueError("CORS_ALLOW_ORIGINS must be a non-empty explicit allow-list; wildcard '*' is not permitted.")
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
        env_file = ENV_FILE
        env_file_encoding = 'utf-8'

def load_settings() -> Settings:
    """
    Loads and validates configuration settings using Pydantic.

    This function creates an instance of the Settings class, which automatically
    loads values from environment variables and the .env file.

    Returns:
        Settings: An instance of the Settings class containing the loaded configuration.

    Raises:
        ValidationError: If any required settings are missing or invalid.
    """
    try:
        settings = Settings()
        print("Configuration loaded successfully.")
        return settings
    except Exception as e:
        print(f"Error loading configuration: {str(e)}")
        raise

# Create a global instance of Settings to be used throughout the application
settings = load_settings()

# Note: Ensure that all environment variables are correctly set in the .env file
# and that the file is located in the root directory of the project.