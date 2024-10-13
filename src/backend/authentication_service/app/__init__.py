"""
Initialization module for the authentication service.

This module sets up necessary configurations and security utilities for the authentication service.
It imports required functions from the config and security modules to initialize the service.

Requirements addressed:
- Authentication and Authorization Implementation (Technical Requirements/Feature 4)
"""

# Third-party imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Internal imports
from src.backend.authentication_service.config import load_config
from src.backend.authentication_service.app.security import generate_token, validate_token

# Initialize FastAPI application
app = FastAPI(
    title="Authentication Service",
    description="API for handling authentication and authorization",
    version="1.0.0"
)

# Load configuration
config = load_config()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config['CORS_ORIGINS'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize security utilities
token_generator = generate_token
token_validator = validate_token

# Make config and security utilities available to other modules
app.state.config = config
app.state.generate_token = token_generator
app.state.validate_token = token_validator

# Import and include routers
# Note: Import statements are placed here to avoid circular imports
try:
    from src.backend.authentication_service.app.routers import auth
    app.include_router(auth.router, prefix="/auth", tags=["authentication"])
except ImportError:
    # Log or handle the error as needed
    print("Error importing authentication routers. Ensure the module exists and is accessible.")

@app.on_event("startup")
async def startup_event():
    """
    Perform any necessary startup operations for the authentication service.
    """
    # TODO: Add any additional startup operations if needed
    pass

@app.on_event("shutdown")
async def shutdown_event():
    """
    Perform any necessary cleanup operations when shutting down the authentication service.
    """
    # TODO: Add any cleanup operations if needed
    pass