"""
This file provides configuration settings for the Reporting Financials Service, including database connection strings,
API keys, and other environment-specific variables necessary for the service's operation.

Requirements addressed:
- API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
  Develop and deploy the FastAPI-based RESTful API to facilitate secure and efficient data ingestion and retrieval
  from the PostgreSQL database.
"""

import os
from pydantic import BaseSettings, PostgresDsn, SecretStr

class Config(BaseSettings):
    """
    Configuration class for the Reporting Financials Service.
    
    This class uses Pydantic's BaseSettings to automatically read environment variables
    and provide type checking and validation for configuration settings.
    """

    # Database configuration
    DATABASE_URL: PostgresDsn = os.getenv("DATABASE_URL", "postgresql://<username>:<password>@<host>:<port>/<database_name>")

    # API configuration
    API_KEY: SecretStr = os.getenv("API_KEY", "<your_api_key_here>")

    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Additional service-specific configurations can be added here
    SERVICE_NAME: str = "Reporting Financials Service"
    API_VERSION: str = "v1"

    # CORS settings
    CORS_ORIGINS: list = ["*"]  # In production, specify allowed origins

    # JWT settings for authentication
    JWT_SECRET_KEY: SecretStr = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

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