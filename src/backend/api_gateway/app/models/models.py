# src/backend/api_gateway/app/models/models.py

# This file defines the data models used within the API Gateway component of the backend platform.
# These models represent the structure of the data that will be processed and transferred through the API,
# ensuring consistency and integrity across the system.

# Requirements addressed:
# - API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
#   Develop the FastAPI-based RESTful API to facilitate secure and efficient data ingestion and retrieval
#   from the PostgreSQL database.

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from uuid import UUID

class ExampleModel(BaseModel):
    """
    A sample data model representing the structure of data entities processed by the API.
    This model serves as a template for defining specific data structures required by the API.
    """
    name: str = Field(..., description="The name of the example entity")
    value: int = Field(..., description="The numeric value associated with the example entity")

    class Config:
        schema_extra = {
            "example": {
                "name": "Example Entity",
                "value": 42
            }
        }

    def to_dict(self) -> dict:
        """
        Converts the model instance to a dictionary.

        Returns:
            dict: A dictionary representation of the model instance.
        """
        return {
            "name": self.name,
            "value": self.value
        }

class Company(BaseModel):
    """
    Represents a company in the OMERS Ventures portfolio.
    """
    id: UUID
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
    created_date: datetime
    created_by: str
    last_update_date: Optional[datetime] = None
    last_updated_by: Optional[str] = None

class MetricsInput(BaseModel):
    """
    Represents the input metrics for a company's financial reporting.
    """
    id: UUID
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
    created_date: datetime
    created_by: str
    last_update_date: Optional[datetime] = None
    last_updated_by: Optional[str] = None

class QuarterlyReportingFinancials(BaseModel):
    """
    Represents the quarterly reporting financials for a company.
    """
    company_id: UUID
    currency: str
    exchange_rate_used: float
    total_revenue: float
    recurring_revenue: float
    gross_profit: float
    debt_outstanding: Optional[float] = None
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
    created_date: datetime
    created_by: str
    last_update_date: Optional[datetime] = None
    last_updated_by: Optional[str] = None

class QuarterlyReportingMetrics(BaseModel):
    """
    Represents the quarterly reporting metrics for a company.
    """
    company_id: UUID
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
    created_date: datetime
    created_by: str
    last_update_date: Optional[datetime] = None
    last_updated_by: Optional[str] = None