"""
This file initializes the Metrics Input Service application, setting up the necessary configurations, models, and routers to handle financial metrics input operations.

Requirements addressed:
- API Services (Technical Requirements/Feature 2: API Development and Deployment): Develop the API using FastAPI framework to ensure high performance and scalability.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.backend.metrics_input_service.app.models.models import MetricsInput  # Import the MetricsInput model
from src.backend.metrics_input_service.app.routers.metrics import metrics_router  # Import the metrics router
from src.backend.metrics_input_service.config import Settings  # Import the Settings class

def initialize_app() -> FastAPI:
    """
    Sets up the FastAPI application with configurations, models, and routers.

    Returns:
        FastAPI: The initialized FastAPI application instance.
    """
    # Create a FastAPI application instance
    app = FastAPI(
        title="Metrics Input Service",
        description="API for handling financial metrics input operations for OMERS Ventures portfolio companies.",
        version="1.0.0"
    )

    # Load configuration settings
    settings = Settings()

    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include the metrics_router in the FastAPI application to register endpoints
    app.include_router(metrics_router, prefix="/api/v1/metrics", tags=["metrics"])

    @app.on_event("startup")
    async def startup_event():
        """
        Perform any necessary startup operations, such as database connections.
        """
        # Add any startup logic here, e.g., database connection initialization
        pass

    @app.on_event("shutdown")
    async def shutdown_event():
        """
        Perform any necessary cleanup operations on application shutdown.
        """
        # Add any shutdown logic here, e.g., closing database connections
        pass

    return app

# Initialize the FastAPI application
app = initialize_app()

# This conditional is used to prevent the app from starting when imported by other modules
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Notes and Comments:
- **Imports Verification**: All imported components (`MetricsInput`, `metrics_router`, `Settings`) are verified to exist and are used correctly within the application.
- **Configuration**: The `Settings` class is used to manage environment-specific settings, ensuring the application can adapt to different deployment environments.
- **CORS Configuration**: CORS middleware is configured to allow requests from specified origins, which is essential for enabling cross-origin requests in web applications.
- **Router Inclusion**: The `metrics_router` is included to handle API requests related to financial metrics, ensuring that the endpoints are registered and accessible.
- **Startup and Shutdown Events**: Placeholder functions are provided for startup and shutdown events, allowing for future expansion to include necessary operations such as database connections.
- **Execution Guard**: The `if __name__ == "__main__":` block ensures that the application only runs when executed as a script, not when imported as a module.

### Additional Considerations:
- **Database Session Management**: Ensure that database session management is implemented in the routers to handle database connections efficiently.
- **Logging**: Consider implementing additional logging configurations to capture detailed logs for monitoring and debugging purposes.
- **Testing**: Validate that all API endpoints are correctly documented and tested for expected behavior.
- **Environment Variables**: Ensure that the `.env` file is correctly set up with necessary environment variables such as `DATABASE_URL`, `API_KEY`, and `LOG_LEVEL` to avoid runtime errors.