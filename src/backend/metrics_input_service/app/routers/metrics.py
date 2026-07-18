from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from datetime import date
from uuid import UUID

from src.backend.metrics_input_service.app.models.models import MetricsInput, MetricsInputSchema
from src.backend.metrics_input_service.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Version information for external libraries
# fastapi==0.68.0

router = APIRouter()

# Lazily-initialized SQLAlchemy session factory. The engine is built on first use
# (not at import time) from settings.database_url, so importing this router never opens
# a database connection. The postgresql:// engine loads the psycopg2 driver declared in
# requirements.txt (psycopg2-binary).
_SessionLocal = None


def _get_session_local():
    """Build the module-level SQLAlchemy sessionmaker once and return it."""
    global _SessionLocal
    if _SessionLocal is None:
        engine = create_engine(settings.database_url)
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _SessionLocal


# Dependency to get database session
def get_db():
    """
    FastAPI dependency that yields a real SQLAlchemy session bound to the configured
    PostgreSQL database (settings.database_url), closing it when the request completes.

    Yields:
        Session: An active SQLAlchemy session object.
    """
    db = _get_session_local()()
    try:
        yield db
    finally:
        db.close()

@router.post('/metrics/', response_model=dict)
async def create_metrics(metrics_data: MetricsInputSchema, db: Session = Depends(get_db)):
    """
    Handles the creation of new financial metrics data entries.
    
    This endpoint is responsible for validating incoming metrics data,
    inserting it into the PostgreSQL database, and returning a confirmation message.
    
    Args:
        metrics_data (MetricsInputSchema): The metrics data to be inserted.
        db (Session): Database session dependency.
    
    Returns:
        dict: A confirmation message indicating successful creation.
    
    Raises:
        HTTPException: If there's an error during data insertion.
    """
    try:
        # Convert Pydantic model to SQLAlchemy model. exclude_none omits unsupplied optional
        # fields so that server-side column defaults apply (id -> uuid_generate_v4(),
        # created_date -> now()) instead of attempting to insert NULL into NOT NULL columns.
        metrics_instance = MetricsInput(**metrics_data.dict(exclude_none=True))

        # Insert the validated data into the PostgreSQL database
        db.add(metrics_instance)
        db.commit()
        db.refresh(metrics_instance)

        return {"message": "Metrics data created successfully", "metrics_id": str(metrics_instance.id)}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while creating metrics: {str(e)}")

@router.get('/metrics/', response_model=List[MetricsInputSchema])
async def get_metrics(
    company_id: UUID,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieves financial metrics data based on specified query parameters.
    
    This endpoint queries the PostgreSQL database for metrics entries matching
    the provided company_id, start_date, and end_date parameters.
    
    Args:
        company_id (UUID): The unique identifier of the company.
        start_date (date, optional): The start date for the query range.
        end_date (date, optional): The end date for the query range.
        db (Session): Database session dependency.
    
    Returns:
        List[MetricsInputSchema]: A list of financial metrics entries matching the query parameters.
    
    Raises:
        HTTPException: If there's an error during data retrieval or if no data is found.
    """
    try:
        # Validate the query parameters
        if start_date and end_date and start_date > end_date:
            raise HTTPException(status_code=400, detail="start_date must be before or equal to end_date")

        # Query the PostgreSQL database for metrics entries matching the parameters
        query = db.query(MetricsInput).filter(MetricsInput.company_id == company_id)
        if start_date:
            query = query.filter(MetricsInput.fiscal_reporting_date >= start_date)
        if end_date:
            query = query.filter(MetricsInput.fiscal_reporting_date <= end_date)
        metrics = query.all()

        if not metrics:
            raise HTTPException(status_code=404, detail="No metrics found for the given parameters")

        return metrics
    except HTTPException as he:
        raise he
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving metrics: {str(e)}")

# This section demonstrates how the router would be included in the main FastAPI application
# app = FastAPI()
# app.include_router(router, prefix="/api/v1", tags=["metrics"])

"""
This module defines the API endpoints for managing financial metrics input within the Metrics Input Service.
It handles the routing of HTTP requests related to metrics data, facilitating operations such as data submission,
retrieval, and validation.

Requirements addressed:
- API Services (Technical Requirements/Feature 2: API Development and Deployment):
  Develop the API using FastAPI framework to ensure high performance and scalability.

The module uses FastAPI to create API endpoints, leveraging its high performance and built-in features for request
validation and documentation generation. It integrates with the MetricsInput model from the models module to ensure
data consistency and with the Settings from the config module for any configuration-specific needs.

Note: This module assumes the existence of a database session management system, which should be implemented
separately. The placeholder 'get_db' function should be replaced with the actual database session retrieval logic.
"""