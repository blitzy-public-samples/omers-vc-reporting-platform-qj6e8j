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


def _validate_cors_origins(origins):
    """Reject wildcard, empty, or malformed CORS origins (CWE-942).

    Each entry must be a serialized origin: an http(s) scheme and host with an
    optional valid port and no credentials, path, query, or fragment.
    """
    from urllib.parse import urlsplit
    if not origins:
        raise ValueError("CORS origins must be a non-empty explicit allow-list; wildcard '*' is not permitted.")
    for origin in origins:
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
    return origins


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
        # CORS allow-list from environment; explicit non-wildcard origins (CWE-942)
        'CORS_ORIGINS': _validate_cors_origins(
            [o.strip() for o in os.getenv('CORS_ORIGINS', os.getenv('CORS_ALLOW_ORIGINS', 'http://localhost:3000')).split(',') if o.strip()]
        ),
        'TOKEN_EXPIRATION': int(os.getenv('TOKEN_EXPIRATION', 30)),  # Default to 30 minutes if not set
        'DEBUG': os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    }

    # Validate required configuration settings
    required_settings = ['SECRET_KEY', 'DATABASE_URL']
    for setting in required_settings:
        if not config[setting]:
            raise ValueError(f"Missing required configuration setting: {setting}")

    # CORS origins (including wildcard rejection) are validated by
    # _validate_cors_origins when the list is built above (CWE-942).
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