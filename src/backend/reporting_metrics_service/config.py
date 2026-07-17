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
        # Require a non-empty PostgreSQL DSN using the 'postgresql' scheme the
        # SQLAlchemy/databases consumer actually supports. The bare 'postgres://' scheme
        # is rejected because SQLAlchemy 1.4 raises NoSuchModuleError for it. Fail closed.
        from urllib.parse import urlsplit
        parts = urlsplit(v or '')
        if not ((parts.scheme == 'postgresql' or parts.scheme.startswith('postgresql+')) and parts.netloc):
            raise ValueError(
                "DATABASE_URL must be a non-empty PostgreSQL DSN using the 'postgresql://' "
                "scheme (e.g. postgresql://user:pass@host:port/db); 'postgres://' is not supported."
            )
        return v

    @validator('BACKEND_CORS_ORIGINS', pre=True, always=True)
    def _validate_cors_origins(cls, v):
        # CWE-942: fail closed. Reject wildcard, empty, or malformed origins in a Pydantic
        # validator (the validation failure is NOT swallowed). The env value is a JSON
        # array; a comma-separated string is also accepted. Each entry must be a serialized
        # origin: http(s) scheme + host, optional valid port, no credentials/path/query/fragment.
        if isinstance(v, str):
            s = v.strip()
            if s.startswith('['):
                import json
                v = json.loads(s)
            else:
                v = [origin.strip() for origin in s.split(',') if origin.strip()]
        from urllib.parse import urlsplit
        if not v:
            raise ValueError("BACKEND_CORS_ORIGINS must be a non-empty explicit allow-list; wildcard '*' is not permitted.")
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
        case_sensitive = True
        env_file = '.env'

# Initialize settings
settings = Settings()

# Global variable for environment, as specified in the JSON specification
ENVIRONMENT = settings.ENVIRONMENT

# Note: Ensure that the environment variables are correctly set in the .env file or the system environment.
# This includes sensitive information such as DATABASE_URL and SECRET_KEY, which should be kept secure.

# CORS origins are validated fail-closed by the BACKEND_CORS_ORIGINS Pydantic validator
# on the Settings class above (CWE-942); no separate, swallowed post-initialization check.