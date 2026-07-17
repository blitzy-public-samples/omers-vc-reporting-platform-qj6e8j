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

    @validator('CORS_ORIGINS', pre=True, always=True)
    def _validate_cors_origins(cls, v):
        # CWE-942: reject wildcard, empty, or malformed origins (fail closed). The env
        # value is a JSON array (canonical, see .env.sample); a comma-separated string is
        # also accepted. Each entry must be a serialized origin: http(s) scheme + host,
        # optional valid port, and no credentials, path, query, or fragment.
        if isinstance(v, str):
            s = v.strip()
            if s.startswith('['):
                import json
                v = json.loads(s)
            else:
                v = [origin.strip() for origin in s.split(',') if origin.strip()]
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