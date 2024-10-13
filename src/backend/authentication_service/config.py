# src/backend/authentication_service/config.py

"""
Configuration module for the authentication service, responsible for loading and managing
environment variables and configuration settings required for the service's operation.

This module addresses the following requirement:
- Authentication and Authorization Implementation (Technical Requirements/Feature 4)

The configuration settings loaded here are essential for secure authentication and
authorization mechanisms to control access to the backend platform and its resources.
"""

import os
from dotenv import load_dotenv  # python-dotenv v0.19.2

# Load environment variables from .env file
load_dotenv()

def load_config():
    """
    Loads configuration settings from environment variables using python-dotenv.

    Returns:
        dict: A dictionary containing configuration settings such as SECRET_KEY,
              DATABASE_URL, TOKEN_EXPIRATION, and DEBUG.
    """
    config = {
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'DATABASE_URL': os.getenv('DATABASE_URL'),
        'TOKEN_EXPIRATION': int(os.getenv('TOKEN_EXPIRATION', 30)),  # Default to 30 minutes if not set
        'DEBUG': os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    }

    # Validate required configuration settings
    required_settings = ['SECRET_KEY', 'DATABASE_URL']
    for setting in required_settings:
        if not config[setting]:
            raise ValueError(f"Missing required configuration setting: {setting}")

    return config

# Global configuration variables
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
TOKEN_EXPIRATION = int(os.getenv('TOKEN_EXPIRATION', 30))  # In minutes
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

# Ensure critical configuration is set
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in environment variables")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set in environment variables")

# Additional configuration checks
if len(SECRET_KEY) < 32:
    raise ValueError("SECRET_KEY should be at least 32 characters long for security")

# Log configuration status (avoid logging sensitive information)
if DEBUG:
    print("Debug mode is enabled")
    print(f"Token expiration set to {TOKEN_EXPIRATION} minutes")
else:
    print("Running in production mode")

# Optionally, you can add more complex configuration logic here
# For example, loading different configurations based on the environment (dev, staging, prod)