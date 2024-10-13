"""
This file serves as the initializer for the database models package, facilitating the import of ORM models that represent the database tables for financial reporting metrics.

Requirements addressed:
- Database Setup and Configuration (Technical Requirements/Feature 1: Database Setup and Configuration)
  Ensures that all ORM models are accessible for database operations, maintaining consistency between the application's data model and the database schema.
"""

# External dependencies
from sqlalchemy import create_engine  # SQLAlchemy v1.4.22
from sqlalchemy.orm import sessionmaker  # SQLAlchemy v1.4.22
from pydantic import BaseModel  # Pydantic v1.8.2

# Internal dependencies
from src.database.models.models import (
    Company,
    MetricsInput,
    QuarterlyReportingFinancials,
    QuarterlyReportingMetrics,
    CompanyBase,
    MetricsInputBase,
    QuarterlyReportingFinancialsBase,
    QuarterlyReportingMetricsBase
)

# Create a database engine and session
engine = create_engine('postgresql://user:password@localhost/dbname')  # Replace with actual database URL
Session = sessionmaker(bind=engine)

# Export models for easy access
__all__ = [
    'Company', 'MetricsInput', 'QuarterlyReportingFinancials', 'QuarterlyReportingMetrics',
    'CompanyBase', 'MetricsInputBase', 'QuarterlyReportingFinancialsBase', 'QuarterlyReportingMetricsBase',
    'Session'
]

# Pydantic models for data validation (if needed)
class CompanyModel(BaseModel):
    name: str
    reporting_status: str
    reporting_currency: str
    fund: str
    location_country: str
    customer_type: str
    revenue_type: str
    equity_raised: float
    post_money_valuation: float
    year_end_date: date

    class Config:
        orm_mode = True

class MetricsInputModel(BaseModel):
    company_id: uuid.UUID
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
    debt_outstanding: Optional[float]
    employees: int
    customers: Optional[int]
    fiscal_reporting_date: date
    fiscal_reporting_quarter: int
    reporting_year: int
    reporting_quarter: int

    class Config:
        orm_mode = True

class QuarterlyReportingFinancialsModel(BaseModel):
    company_id: uuid.UUID
    currency: str
    exchange_rate_used: float
    total_revenue: float
    recurring_revenue: float
    gross_profit: float
    debt_outstanding: float
    sales_marketing_expense: float
    total_operating_expense: float
    ebitda: float
    net_income: float
    cash_burn: float
    cash_balance: float
    fiscal_reporting_date: date
    fiscal_reporting_quarter: int
    reporting_year: int
    reporting_quarter: int

    class Config:
        orm_mode = True

class QuarterlyReportingMetricsModel(BaseModel):
    company_id: uuid.UUID
    currency: str
    enterprise_value: float
    arr: float
    recurring_percentage_revenue: float
    revenue_per_fte: float
    gross_profit_per_fte: float
    employee_growth_rate: float
    change_in_cash: float
    revenue_growth: float
    monthly_cash_burn: float
    runway_months: float
    ev_by_equity_raised_plus_debt: float
    sales_marketing_percentage_revenue: float
    total_operating_percentage_revenue: float
    gross_profit_margin: float
    valuation_to_revenue: float
    yoy_growth_revenue: float
    yoy_growth_profit: float
    yoy_growth_employees: float
    yoy_growth_ltm_revenue: float
    ltm_total_revenue: float
    ltm_gross_profit: float
    ltm_sales_marketing_expense: float
    ltm_gross_margin: float
    ltm_operating_expense: float
    ltm_ebitda: float
    ltm_net_income: float
    ltm_ebitda_margin: float
    ltm_net_income_margin: float
    fiscal_reporting_date: date
    fiscal_reporting_quarter: int
    reporting_year: int
    reporting_quarter: int

    class Config:
        orm_mode = True

# Export Pydantic models
__all__ += [
    'CompanyModel', 'MetricsInputModel', 'QuarterlyReportingFinancialsModel', 'QuarterlyReportingMetricsModel'
]