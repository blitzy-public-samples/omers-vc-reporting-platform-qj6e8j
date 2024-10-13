"""
This file initializes the Reporting Financials Service application, setting up the necessary
configurations, models, and routers for handling financial report data.

Requirements addressed:
- API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
  Develop and deploy the FastAPI-based RESTful API to facilitate secure and efficient data ingestion
  and retrieval from the PostgreSQL database.
"""

# External dependencies
from fastapi import FastAPI  # version 0.68.0
from sqlalchemy import create_engine  # version 1.4.22
from sqlalchemy.orm import sessionmaker

# Internal dependencies
from .models.models import FinancialReport
from ..config import Config
from .routers.financials import router as financials_router

# Initialize the FastAPI application
app = FastAPI(
    title="Reporting Financials Service",
    description="API for managing and retrieving financial reports for OMERS Ventures portfolio companies.",
    version="1.0.0"
)

# Create database engine and session
engine = create_engine(Config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Include routers
app.include_router(financials_router, prefix="/api/v1", tags=["financials"])

@app.on_event("startup")
async def startup_event():
    """
    Perform any necessary startup operations, such as initializing database connections.
    """
    # You can add any startup logic here, e.g., creating database tables if they don't exist
    FinancialReport.metadata.create_all(bind=engine)

@app.on_event("shutdown")
async def shutdown_event():
    """
    Perform any necessary cleanup operations on application shutdown.
    """
    # You can add any cleanup logic here, e.g., closing database connections

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Make the database session available to the application
app.dependency_overrides[get_db] = get_db

# Additional configuration and middleware can be added here
# For example, adding CORS middleware, authentication middleware, etc.

# Example of adding CORS middleware (uncomment if needed):
# from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )

# Example of adding custom middleware for logging (uncomment if needed):
# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     # Log request details
#     response = await call_next(request)
#     # Log response details
#     return response