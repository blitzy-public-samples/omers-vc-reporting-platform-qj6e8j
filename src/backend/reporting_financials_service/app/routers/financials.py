from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel, Field

# Import the FinancialReport model from the models module
from src.backend.reporting_financials_service.app.models.models import FinancialReport

# Import the Config from the config module
from src.backend.reporting_financials_service.config import Config

# Import necessary SQLAlchemy components
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# FastAPI version 0.68.0
# SQLAlchemy version 1.4.22
# pydantic version 1.8.2

router = APIRouter()

# Create a database engine and session
engine = create_engine(Config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for financial report creation
class FinancialReportCreate(BaseModel):
    company_id: UUID
    currency: str
    total_revenue: float
    recurring_revenue: float
    gross_profit: float
    sales_marketing_expense: float
    total_operating_expense: float
    ebitda: float
    net_income: float
    cash_burn: float
    cash_balance: float
    debt_outstanding: Optional[float] = None
    employees: int
    customers: Optional[int] = None
    fiscal_reporting_date: date
    fiscal_reporting_quarter: int
    reporting_year: int
    reporting_quarter: int

    class Config:
        schema_extra = {
            "example": {
                "company_id": "123e4567-e89b-12d3-a456-426614174000",
                "currency": "USD",
                "total_revenue": 1000000.00,
                "recurring_revenue": 900000.00,
                "gross_profit": 700000.00,
                "sales_marketing_expense": 200000.00,
                "total_operating_expense": 800000.00,
                "ebitda": 200000.00,
                "net_income": 150000.00,
                "cash_burn": 50000.00,
                "cash_balance": 500000.00,
                "debt_outstanding": 100000.00,
                "employees": 50,
                "customers": 1000,
                "fiscal_reporting_date": "2023-03-31",
                "fiscal_reporting_quarter": 1,
                "reporting_year": 2023,
                "reporting_quarter": 1
            }
        }

# GET endpoint to retrieve financial reports
@router.get('/financial_reports/', response_model=List[FinancialReport])
async def get_financial_reports(
    company_id: Optional[UUID] = Query(None, description="Filter by company ID"),
    reporting_year: Optional[int] = Query(None, description="Filter by reporting year"),
    reporting_quarter: Optional[int] = Query(None, description="Filter by reporting quarter"),
    db: Session = Depends(get_db)
):
    """
    Retrieves financial reports from the database based on query parameters.
    
    This endpoint addresses the requirement:
    - API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
    
    :param company_id: Optional UUID to filter reports by company
    :param reporting_year: Optional integer to filter reports by year
    :param reporting_quarter: Optional integer to filter reports by quarter
    :param db: Database session dependency
    :return: A list of financial report entries matching the query parameters
    """
    query = db.query(FinancialReport)
    
    if company_id:
        query = query.filter(FinancialReport.company_id == company_id)
    if reporting_year:
        query = query.filter(FinancialReport.reporting_year == reporting_year)
    if reporting_quarter:
        query = query.filter(FinancialReport.reporting_quarter == reporting_quarter)
    
    reports = query.all()
    return reports

# POST endpoint to create a new financial report
@router.post('/financial_reports/', response_model=FinancialReport)
async def create_financial_report(report_data: FinancialReportCreate, db: Session = Depends(get_db)):
    """
    Creates a new financial report entry in the database.
    
    This endpoint addresses the requirement:
    - API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
    
    :param report_data: FinancialReportCreate object containing the report data
    :param db: Database session dependency
    :return: The newly created financial report entry
    """
    new_report = FinancialReport(
        company_id=report_data.company_id,
        currency=report_data.currency,
        total_revenue=report_data.total_revenue,
        recurring_revenue=report_data.recurring_revenue,
        gross_profit=report_data.gross_profit,
        sales_marketing_expense=report_data.sales_marketing_expense,
        total_operating_expense=report_data.total_operating_expense,
        ebitda=report_data.ebitda,
        net_income=report_data.net_income,
        cash_burn=report_data.cash_burn,
        cash_balance=report_data.cash_balance,
        debt_outstanding=report_data.debt_outstanding,
        employees=report_data.employees,
        customers=report_data.customers,
        fiscal_reporting_date=report_data.fiscal_reporting_date,
        fiscal_reporting_quarter=report_data.fiscal_reporting_quarter,
        reporting_year=report_data.reporting_year,
        reporting_quarter=report_data.reporting_quarter,
        created_date=datetime.utcnow(),
        created_by="API"
    )
    
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

# Error handling for common exceptions
@router.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {"detail": str(exc.detail), "status_code": exc.status_code}

# Logging configuration
import logging
logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Log all requests
@router.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Note: Ensure that the 'Company' model is defined in the models module or imported if needed.