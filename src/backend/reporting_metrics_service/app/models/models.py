from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# SQLAlchemy version 1.4.22
# Used for ORM to define database models and interact with the PostgreSQL database.

Base = declarative_base()

class ReportingMetrics(Base):
    """
    ORM model for a quarterly reporting-metrics entry.

    This model addresses the requirement:
    - Data Consistency and Integrity (Technical Requirements/Feature 12: Data Consistency and Integrity)
      Ensures the consistency and integrity of financial data across all database tables and during all
      data processing operations.
    """
    # The authoritative table is `quarterly_reporting_metrics` (database/schemas/create_tables.sql),
    # not `reporting_metrics`. Aligning the ORM mapping to the real table is what enables the
    # API -> PostgreSQL round trip.
    __tablename__ = 'quarterly_reporting_metrics'

    # The authoritative table declares no surrogate `id` and no single-column primary key; its
    # natural business key is (company_id, reporting_year, reporting_quarter). Declaring that
    # composite key as the ORM primary key gives SQLAlchemy the row identity it needs for
    # SELECT/INSERT without altering the database schema. Referential integrity to companies(id)
    # is enforced by the DB-level constraint (quarterly_reporting_metrics_company_id_fkey); no
    # ORM-level ForeignKey is declared because the companies table is not mapped in this microservice.
    company_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    currency = Column(String, nullable=False)
    enterprise_value = Column(Numeric)
    arr = Column(Numeric)
    recurring_percentage_revenue = Column(Numeric)
    revenue_per_fte = Column(Numeric)
    gross_profit_per_fte = Column(Numeric)
    employee_growth_rate = Column(Numeric)
    change_in_cash = Column(Numeric)
    revenue_growth = Column(Numeric)
    monthly_cash_burn = Column(Numeric)
    runway_months = Column(Numeric)
    ev_by_equity_raised_plus_debt = Column(Numeric)
    sales_marketing_percentage_revenue = Column(Numeric)
    total_operating_percentage_revenue = Column(Numeric)
    gross_profit_margin = Column(Numeric)
    valuation_to_revenue = Column(Numeric)
    yoy_growth_revenue = Column(Numeric)
    yoy_growth_profit = Column(Numeric)
    yoy_growth_employees = Column(Numeric)
    yoy_growth_ltm_revenue = Column(Numeric)
    ltm_total_revenue = Column(Numeric)
    ltm_gross_profit = Column(Numeric)
    ltm_sales_marketing_expense = Column(Numeric)
    ltm_gross_margin = Column(Numeric)
    ltm_operating_expense = Column(Numeric)
    ltm_ebitda = Column(Numeric)
    ltm_net_income = Column(Numeric)
    ltm_ebitda_margin = Column(Numeric)
    ltm_net_income_margin = Column(Numeric)
    fiscal_reporting_date = Column(Date)
    fiscal_reporting_quarter = Column(Integer)
    reporting_year = Column(Integer, primary_key=True)
    reporting_quarter = Column(Integer, primary_key=True)
    # created_date / last_update_date carry a DB-side DEFAULT CURRENT_TIMESTAMP; declaring
    # server_default lets SQLAlchemy omit them on INSERT and read the DB-generated value back
    # via refresh, matching the authoritative schema.
    created_date = Column(DateTime, server_default=func.now(), nullable=False)
    created_by = Column(String, nullable=False)
    last_update_date = Column(DateTime, server_default=func.now())
    last_updated_by = Column(String)

    def __repr__(self):
        return (f"<ReportingMetrics(company_id={self.company_id}, "
                f"reporting_year={self.reporting_year}, reporting_quarter={self.reporting_quarter})>")

# Note: referential integrity to companies(id) is enforced by the database foreign key, not by an
# ORM-level relationship, because the companies table is not mapped inside this microservice.
