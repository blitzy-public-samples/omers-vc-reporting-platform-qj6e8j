from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel, Field

# Import the FinancialReport model from the models module
from src.backend.reporting_financials_service.app.models.models import FinancialReport

# Import the config instance from the config module. Pydantic v1 removes required fields
# (Field(...)) from the class namespace, so values must be read from the instance
# (config.DATABASE_URL), not the class (Config.DATABASE_URL) — the latter raised
# AttributeError at import and prevented the service from starting.
from src.backend.reporting_financials_service.config import config

# Import necessary SQLAlchemy components
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# FastAPI version 0.68.0
# SQLAlchemy version 1.4.22
# pydantic version 1.8.2

router = APIRouter()

# Create a database engine and session
engine = create_engine(str(config.DATABASE_URL))
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

# Pydantic response schema. FastAPI's response_model must be a Pydantic model, not the
# SQLAlchemy ORM class (FinancialReport); orm_mode=True lets FastAPI serialize ORM rows.
# Fields mirror the authoritative quarterly_reporting_financials columns.
class FinancialReportResponse(BaseModel):
    company_id: UUID
    currency: str
    exchange_rate_used: Optional[float] = None
    total_revenue: Optional[float] = None
    recurring_revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    debt_outstanding: Optional[float] = None
    sales_marketing_expense: Optional[float] = None
    total_operating_expense: Optional[float] = None
    ebitda: Optional[float] = None
    net_income: Optional[float] = None
    cash_burn: Optional[float] = None
    cash_balance: Optional[float] = None
    fiscal_reporting_date: Optional[date] = None
    fiscal_reporting_quarter: Optional[int] = None
    reporting_year: Optional[int] = None
    reporting_quarter: Optional[int] = None
    created_date: Optional[datetime] = None
    created_by: Optional[str] = None
    last_update_date: Optional[datetime] = None
    last_updated_by: Optional[str] = None

    class Config:
        orm_mode = True

# GET endpoint to retrieve financial reports
@router.get('/financial_reports/', response_model=List[FinancialReportResponse])
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
@router.post('/financial_reports/', response_model=FinancialReportResponse)
async def create_financial_report(report_data: FinancialReportCreate, db: Session = Depends(get_db)):
    """
    Creates a new financial report entry in the database.
    
    This endpoint addresses the requirement:
    - API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
    
    :param report_data: FinancialReportCreate object containing the report data
    :param db: Database session dependency
    :return: The newly created financial report entry
    """
    # employees/customers are accepted by the request model for backward compatibility
    # but are not columns of the authoritative quarterly_reporting_financials table, so
    # they are not persisted. created_date is populated by the DB default (CURRENT_TIMESTAMP).
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
        fiscal_reporting_date=report_data.fiscal_reporting_date,
        fiscal_reporting_quarter=report_data.fiscal_reporting_quarter,
        reporting_year=report_data.reporting_year,
        reporting_quarter=report_data.reporting_quarter,
        created_by="API"
    )
    
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

# NOTE: exception handlers and HTTP middleware are registered on the FastAPI application
# (see main.create_app), not on an APIRouter. APIRouter has no `.exception_handler` or
# `.middleware` decorators, so the previous `@router.exception_handler(HTTPException)` and
# `@router.middleware("http")` declarations raised AttributeError at import and prevented the
# service from starting. They are removed here; application-level logging is configured in main.py.