# src/backend/metrics_input_service/main.py

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Internal imports
from src.backend.metrics_input_service.app.models.models import MetricsInput
from src.backend.metrics_input_service.app.routers.metrics import router as metrics_router
from src.backend.metrics_input_service.config import Settings

# External library imports
# FastAPI version 0.68.0
# SQLAlchemy version 1.4.22
# Pydantic version 1.8.2

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """
    Initializes and configures the FastAPI application for the Metrics Input Service.

    Returns:
        FastAPI: The configured FastAPI application instance.

    This function addresses the following requirements:
    - API Services (Technical Requirements/Feature 2: API Development and Deployment)
    - Develop the API using FastAPI framework to ensure high performance and scalability.
    """
    # Create a FastAPI application instance
    app = FastAPI(
        title="Metrics Input Service",
        description="API for managing financial metrics input data for OMERS Ventures portfolio companies.",
        version="1.0.0"
    )

    # Load configuration settings
    settings = Settings()

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Create database engine and session
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Dependency to get database session
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    # Include the router in the FastAPI application instance
    app.include_router(metrics_router, prefix="/api/v1/metrics", tags=["metrics"])

    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting up Metrics Input Service")
        # Perform any necessary startup tasks, such as database connections or cache warming

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down Metrics Input Service")
        # Perform any necessary cleanup tasks

    return app

# Create the FastAPI application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Comments for potential changes in other files:
# - Ensure that the database session management is implemented in the routers to handle
#   database connections efficiently.
# - Validate that all API endpoints are correctly documented and tested for expected behavior.
# - Consider implementing additional logging configurations to capture detailed logs
#   for monitoring and debugging purposes.