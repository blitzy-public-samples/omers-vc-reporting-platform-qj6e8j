from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import date

# Version comments for external libraries
# fastapi==0.68.0
# sqlalchemy==1.4.22

from src.backend.reporting_metrics_service.app.models.models import ReportingMetrics
from src.backend.reporting_metrics_service.app.database import get_db
from src.backend.reporting_metrics_service.app.schemas import ReportingMetricsResponse

router = APIRouter()

@router.get('/metrics', response_model=List[ReportingMetricsResponse])
async def get_reporting_metrics(
    company_id: UUID = Query(..., description="UUID of the company"),
    reporting_year: int = Query(..., description="Reporting year"),
    reporting_quarter: Optional[int] = Query(None, description="Reporting quarter (optional)"),
    db: Session = Depends(get_db)
):
    """
    Handles HTTP GET requests to retrieve reporting metrics data based on specified query parameters.
    
    This endpoint addresses the requirement:
    - API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
    
    Args:
        company_id (UUID): The unique identifier of the company.
        reporting_year (int): The year for which to retrieve metrics.
        reporting_quarter (Optional[int]): The specific quarter to retrieve metrics for (optional).
        db (Session): The database session dependency.
    
    Returns:
        List[ReportingMetricsResponse]: A JSON response containing the requested reporting metrics data.
    
    Raises:
        HTTPException: If no data is found for the given parameters.
    """
    # Step 1: Validate the incoming query parameters
    if reporting_quarter and not 1 <= reporting_quarter <= 4:
        raise HTTPException(status_code=400, detail="Invalid reporting quarter. Must be between 1 and 4.")

    # Step 2: Query the ReportingMetrics model using SQLAlchemy to fetch data matching the specified parameters
    query = db.query(ReportingMetrics).filter(
        ReportingMetrics.company_id == company_id,
        ReportingMetrics.reporting_year == reporting_year
    )

    if reporting_quarter:
        query = query.filter(ReportingMetrics.reporting_quarter == reporting_quarter)

    metrics = query.all()

    # Step 3: Check if any data was found
    if not metrics:
        raise HTTPException(status_code=404, detail="No reporting metrics found for the given parameters.")

    # Step 4: Format the retrieved data into a JSON response
    response_data = [ReportingMetricsResponse.from_orm(metric) for metric in metrics]

    # Step 5: Return the JSON response to the client
    return response_data

# Additional endpoints can be added here as needed, following the same pattern
# For example, endpoints for creating, updating, or deleting reporting metrics

# Example of an additional endpoint for creating a new reporting metric
@router.post('/metrics', response_model=ReportingMetricsResponse, status_code=201)
async def create_reporting_metric(
    metric: ReportingMetricsResponse,
    db: Session = Depends(get_db)
):
    """
    Handles HTTP POST requests to create a new reporting metric.
    
    This endpoint addresses the requirement:
    - API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
    
    Args:
        metric (ReportingMetricsResponse): The reporting metric data to be created.
        db (Session): The database session dependency.
    
    Returns:
        ReportingMetricsResponse: A JSON response containing the created reporting metric data.
    
    Raises:
        HTTPException: If there's an error creating the metric.
    """
    db_metric = ReportingMetrics(**metric.dict())
    db.add(db_metric)
    try:
        db.commit()
        db.refresh(db_metric)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating metric: {str(e)}")
    return ReportingMetricsResponse.from_orm(db_metric)