from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
import uuid

# SQLAlchemy Base Model
Base = declarative_base()

# Pydantic models for data validation
class CompanyBase(BaseModel):
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

class MetricsInputBase(BaseModel):
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

class QuarterlyReportingFinancialsBase(BaseModel):
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

class QuarterlyReportingMetricsBase(BaseModel):
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

# SQLAlchemy ORM models
class Company(Base):
    """
    Represents a company entity in the database, including fields for company details and financial information.
    
    This model addresses the requirement: 'Database Setup and Configuration'
    Location: Technical Requirements/Feature 1: Database Setup and Configuration
    """
    __tablename__ = 'companies'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    reporting_status = Column(String, nullable=False)
    reporting_currency = Column(String, nullable=False)
    fund = Column(String, nullable=False)
    location_country = Column(String, nullable=False)
    customer_type = Column(String, nullable=False)
    revenue_type = Column(String, nullable=False)
    equity_raised = Column(Numeric, nullable=False)
    post_money_valuation = Column(Numeric, nullable=False)
    year_end_date = Column(Date, nullable=False)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    last_update_date = Column(DateTime(timezone=True), onupdate=func.now())
    last_updated_by = Column(String)

class MetricsInput(Base):
    """
    Represents the financial metrics input data model.
    
    This model addresses the requirement: 'Database Setup and Configuration'
    Location: Technical Requirements/Feature 1: Database Setup and Configuration
    """
    __tablename__ = 'metrics_input'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    last_update_date = Column(DateTime(timezone=True), onupdate=func.now())
    last_updated_by = Column(String)

class QuarterlyReportingFinancials(Base):
    """
    Represents the quarterly financial reporting data model.
    
    This model addresses the requirement: 'Database Setup and Configuration'
    Location: Technical Requirements/Feature 1: Database Setup and Configuration
    """
    __tablename__ = 'quarterly_reporting_financials'

    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), primary_key=True)
    currency = Column(String, nullable=False)
    exchange_rate_used = Column(Numeric, nullable=False)
    total_revenue = Column(Numeric, nullable=False)
    recurring_revenue = Column(Numeric, nullable=False)
    gross_profit = Column(Numeric, nullable=False)
    debt_outstanding = Column(Numeric, nullable=False)
    sales_marketing_expense = Column(Numeric, nullable=False)
    total_operating_expense = Column(Numeric, nullable=False)
    ebitda = Column(Numeric, nullable=False)
    net_income = Column(Numeric, nullable=False)
    cash_burn = Column(Numeric, nullable=False)
    cash_balance = Column(Numeric, nullable=False)
    fiscal_reporting_date = Column(Date, nullable=False, primary_key=True)
    fiscal_reporting_quarter = Column(Integer, nullable=False)
    reporting_year = Column(Integer, nullable=False)
    reporting_quarter = Column(Integer, nullable=False)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    last_update_date = Column(DateTime(timezone=True), onupdate=func.now())
    last_updated_by = Column(String)

class QuarterlyReportingMetrics(Base):
    """
    Represents the quarterly reporting metrics data model.
    
    This model addresses the requirement: 'Database Setup and Configuration'
    Location: Technical Requirements/Feature 1: Database Setup and Configuration
    """
    __tablename__ = 'quarterly_reporting_metrics'

    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), primary_key=True)
    currency = Column(String, nullable=False)
    enterprise_value = Column(Numeric, nullable=False)
    arr = Column(Numeric, nullable=False)
    recurring_percentage_revenue = Column(Numeric, nullable=False)
    revenue_per_fte = Column(Numeric, nullable=False)
    gross_profit_per_fte = Column(Numeric, nullable=False)
    employee_growth_rate = Column(Numeric, nullable=False)
    change_in_cash = Column(Numeric, nullable=False)
    revenue_growth = Column(Numeric, nullable=False)
    monthly_cash_burn = Column(Numeric, nullable=False)
    runway_months = Column(Numeric, nullable=False)
    ev_by_equity_raised_plus_debt = Column(Numeric, nullable=False)
    sales_marketing_percentage_revenue = Column(Numeric, nullable=False)
    total_operating_percentage_revenue = Column(Numeric, nullable=False)
    gross_profit_margin = Column(Numeric, nullable=False)
    valuation_to_revenue = Column(Numeric, nullable=False)
    yoy_growth_revenue = Column(Numeric, nullable=False)
    yoy_growth_profit = Column(Numeric, nullable=False)
    yoy_growth_employees = Column(Numeric, nullable=False)
    yoy_growth_ltm_revenue = Column(Numeric, nullable=False)
    ltm_total_revenue = Column(Numeric, nullable=False)
    ltm_gross_profit = Column(Numeric, nullable=False)
    ltm_sales_marketing_expense = Column(Numeric, nullable=False)
    ltm_gross_margin = Column(Numeric, nullable=False)
    ltm_operating_expense = Column(Numeric, nullable=False)
    ltm_ebitda = Column(Numeric, nullable=False)
    ltm_net_income = Column(Numeric, nullable=False)
    ltm_ebitda_margin = Column(Numeric, nullable=False)
    ltm_net_income_margin = Column(Numeric, nullable=False)
    fiscal_reporting_date = Column(Date, nullable=False, primary_key=True)
    fiscal_reporting_quarter = Column(Integer, nullable=False)
    reporting_year = Column(Integer, nullable=False)
    reporting_quarter = Column(Integer, nullable=False)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    last_update_date = Column(DateTime(timezone=True), onupdate=func.now())
    last_updated_by = Column(String)