"""
Pydantic schemas for the Reporting Metrics Service.

Requirements addressed:
- API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
  Provide the request/response serialization model used by the reporting-metrics API routers.

The routers import ``ReportingMetricsResponse`` from this module
(``from ...app.schemas import ReportingMetricsResponse``). The module previously did not exist,
which raised ModuleNotFoundError at import and prevented the service from starting. FastAPI's
``response_model`` must be a Pydantic model (not the SQLAlchemy ORM class), and ``orm_mode = True``
enables ``ReportingMetricsResponse.from_orm(metric)`` to serialize ORM rows. Fields mirror the
authoritative ``quarterly_reporting_metrics`` columns; company_id and currency are required while
the derived metrics and audit columns are optional.
"""

from typing import Optional
from uuid import UUID
from datetime import date, datetime

from pydantic import BaseModel


class ReportingMetricsResponse(BaseModel):
    company_id: UUID
    currency: str
    enterprise_value: Optional[float] = None
    arr: Optional[float] = None
    recurring_percentage_revenue: Optional[float] = None
    revenue_per_fte: Optional[float] = None
    gross_profit_per_fte: Optional[float] = None
    employee_growth_rate: Optional[float] = None
    change_in_cash: Optional[float] = None
    revenue_growth: Optional[float] = None
    monthly_cash_burn: Optional[float] = None
    runway_months: Optional[float] = None
    ev_by_equity_raised_plus_debt: Optional[float] = None
    sales_marketing_percentage_revenue: Optional[float] = None
    total_operating_percentage_revenue: Optional[float] = None
    gross_profit_margin: Optional[float] = None
    valuation_to_revenue: Optional[float] = None
    yoy_growth_revenue: Optional[float] = None
    yoy_growth_profit: Optional[float] = None
    yoy_growth_employees: Optional[float] = None
    yoy_growth_ltm_revenue: Optional[float] = None
    ltm_total_revenue: Optional[float] = None
    ltm_gross_profit: Optional[float] = None
    ltm_sales_marketing_expense: Optional[float] = None
    ltm_gross_margin: Optional[float] = None
    ltm_operating_expense: Optional[float] = None
    ltm_ebitda: Optional[float] = None
    ltm_net_income: Optional[float] = None
    ltm_ebitda_margin: Optional[float] = None
    ltm_net_income_margin: Optional[float] = None
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
