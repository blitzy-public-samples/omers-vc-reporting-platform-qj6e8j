"""
This file serves as the entry point for the Reporting Financials Service.
It initializes the FastAPI application, configures routes, and sets up the necessary
middleware and database connections to handle financial report data.

Requirements addressed:
- API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
  Develop and deploy the FastAPI-based RESTful API to facilitate secure and efficient
  data ingestion and retrieval from the PostgreSQL database.
"""

import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Internal imports
from src.backend.reporting_financials_service.app.models.models import FinancialReport
from src.backend.reporting_financials_service.app.routers.financials import financials_router
from src.backend.reporting_financials_service.config import Config

# External imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Global variable for the FastAPI application
app = FastAPI()

def create_app() -> FastAPI:
    """
    Initializes the FastAPI application, sets up routes, and configures middleware.

    Returns:
        FastAPI: The initialized FastAPI application instance.
    """
    # Load configuration
    config = Config()

    # Create FastAPI application
    app = FastAPI(
        title=config.SERVICE_NAME,
        description="API for managing and retrieving financial reports",
        version=config.API_VERSION
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Set up database connection
    engine = create_engine(config.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Dependency to get database session
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    # Include routers
    app.include_router(
        financials_router,
        prefix="/api/v1/financials",
        tags=["financials"],
        dependencies=[Depends(get_db)]
    )

    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting up Reporting Financials Service")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down Reporting Financials Service")

    return app

# Create the FastAPI application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)