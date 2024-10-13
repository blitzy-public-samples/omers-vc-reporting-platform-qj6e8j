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
from pydantic import BaseSettings, Field

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

    # Secret key for JWT token encoding/decoding
    secret_key: str = Field(..., env='SECRET_KEY')

    # CORS origins
    cors_origins: list = Field(default_factory=lambda: ["*"], env='CORS_ORIGINS')

    # JWT algorithm
    algorithm: str = Field(default="HS256", env='ALGORITHM')

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