# src/backend/metrics_input_service/app/models/models.py
from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from uuid import UUID as PyUUID

# Base class for SQLAlchemy models
Base = declarative_base()

class MetricsInput(Base):
    """
    Represents the financial metrics input data model, defining the schema for storing metrics data in the database.
    
    This model addresses the following requirement:
    - Data Storage (Technical Requirements/Feature 1: Database Setup and Configuration):
      Ensures that the data models are properly defined to store financial metrics data in the PostgreSQL database.
    """
    __tablename__ = 'metrics_input'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    currency = Column(String, nullable=False)
    total_revenue = Column(Numeric, nullable=False)
    recurring_revenue = Column(Numeric, nullable=False)
    gross_profit = Column(Numeric, nullable=False)
    sales_marketing_expense = Column(Numeric, nullable=False)
    total_operating_expense = Column(Numeric, nullable=False)
    ebitda = Column(Numeric, nullable=False)
    net_income = Column(Numeric, nullable=False)
    cash_burn = Column(Numeric, nullable=False)
    cash_balance = Column(Numeric, nullable=False)
    debt_outstanding = Column(Numeric)
    employees = Column(Integer, nullable=False)
    customers = Column(Integer)
    fiscal_reporting_date = Column(Date, nullable=False)
    fiscal_reporting_quarter = Column(Integer, nullable=False)
    reporting_year = Column(Integer, nullable=False)
    reporting_quarter = Column(Integer, nullable=False)
    created_date = Column(DateTime, server_default=func.now(), nullable=False)
    created_by = Column(String, nullable=False)
    last_update_date = Column(DateTime, onupdate=func.now())
    last_updated_by = Column(String)

class MetricsInputSchema(BaseModel):
    """
    Pydantic schema for validating and serializing MetricsInput data.
    This schema is used for data validation when creating or updating MetricsInput records.
    """
    id: Optional[PyUUID] = Field(None, description="Unique identifier for the metrics input record")
    company_id: PyUUID = Field(..., description="Unique identifier of the company")
    currency: str = Field(..., description="Currency of the financial metrics")
    total_revenue: float = Field(..., description="Total revenue for the reporting period")
    recurring_revenue: float = Field(..., description="Recurring revenue for the reporting period")
    gross_profit: float = Field(..., description="Gross profit for the reporting period")
    sales_marketing_expense: float = Field(..., description="Sales and marketing expense for the reporting period")
    total_operating_expense: float = Field(..., description="Total operating expense for the reporting period")
    ebitda: float = Field(..., description="EBITDA for the reporting period")
    net_income: float = Field(..., description="Net income for the reporting period")
    cash_burn: float = Field(..., description="Cash burn for the reporting period")
    cash_balance: float = Field(..., description="Cash balance at the end of the reporting period")
    debt_outstanding: Optional[float] = Field(None, description="Outstanding debt at the end of the reporting period")
    employees: int = Field(..., description="Number of employees at the end of the reporting period")
    customers: Optional[int] = Field(None, description="Number of customers at the end of the reporting period")
    fiscal_reporting_date: date = Field(..., description="Fiscal reporting date")
    fiscal_reporting_quarter: int = Field(..., description="Fiscal reporting quarter")
    reporting_year: int = Field(..., description="Reporting year")
    reporting_quarter: int = Field(..., description="Reporting quarter")
    created_date: Optional[datetime] = Field(None, description="Date and time when the record was created")
    created_by: str = Field(..., description="User who created the record")
    last_update_date: Optional[datetime] = Field(None, description="Date and time when the record was last updated")
    last_updated_by: Optional[str] = Field(None, description="User who last updated the record")

    class Config:
        orm_mode = True

# Note: Ensure that the UUID generation function `uuid_generate_v4()` is available in your PostgreSQL database.
# If not, you may need to create an extension or use a different method for UUID generation.