from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, UUID, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
import uuid

# SQLAlchemy version 1.4.22
# Used for ORM to define database models and interact with the PostgreSQL database.

Base = declarative_base()

class ReportingMetrics(Base):
    """
    Represents the data model for reporting metrics, defining the schema for the reporting metrics table in the database.
    
    This model addresses the requirement:
    - Data Consistency and Integrity (Technical Requirements/Feature 12: Data Consistency and Integrity)
      Ensures the consistency and integrity of financial data across all database tables and during all data processing operations.
    """
    __tablename__ = 'reporting_metrics'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    currency = Column(String, nullable=False)
    enterprise_value = Column(Numeric, nullable=True)
    arr = Column(Numeric, nullable=True)
    recurring_percentage_revenue = Column(Numeric, nullable=True)
    revenue_per_fte = Column(Numeric, nullable=True)
    gross_profit_per_fte = Column(Numeric, nullable=True)
    employee_growth_rate = Column(Numeric, nullable=True)
    change_in_cash = Column(Numeric, nullable=True)
    revenue_growth = Column(Numeric, nullable=True)
    monthly_cash_burn = Column(Numeric, nullable=True)
    runway_months = Column(Numeric, nullable=True)
    ev_by_equity_raised_plus_debt = Column(Numeric, nullable=True)
    sales_marketing_percentage_revenue = Column(Numeric, nullable=True)
    total_operating_percentage_revenue = Column(Numeric, nullable=True)
    gross_profit_margin = Column(Numeric, nullable=True)
    valuation_to_revenue = Column(Numeric, nullable=True)
    yoy_growth_revenue = Column(Numeric, nullable=True)
    yoy_growth_profit = Column(Numeric, nullable=True)
    yoy_growth_employees = Column(Numeric, nullable=True)
    yoy_growth_ltm_revenue = Column(Numeric, nullable=True)
    ltm_total_revenue = Column(Numeric, nullable=True)
    ltm_gross_profit = Column(Numeric, nullable=True)
    ltm_sales_marketing_expense = Column(Numeric, nullable=True)
    ltm_gross_margin = Column(Numeric, nullable=True)
    ltm_operating_expense = Column(Numeric, nullable=True)
    ltm_ebitda = Column(Numeric, nullable=True)
    ltm_net_income = Column(Numeric, nullable=True)
    ltm_ebitda_margin = Column(Numeric, nullable=True)
    ltm_net_income_margin = Column(Numeric, nullable=True)
    fiscal_reporting_date = Column(Date, nullable=False)
    fiscal_reporting_quarter = Column(Integer, nullable=False)
    reporting_year = Column(Integer, nullable=False)
    reporting_quarter = Column(Integer, nullable=False)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(String, nullable=False)
    last_update_date = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    last_updated_by = Column(String, nullable=True)

    def __init__(self, company_id, currency, enterprise_value, arr, recurring_percentage_revenue,
                 revenue_per_fte, gross_profit_per_fte, employee_growth_rate, change_in_cash,
                 revenue_growth, monthly_cash_burn, runway_months, ev_by_equity_raised_plus_debt,
                 sales_marketing_percentage_revenue, total_operating_percentage_revenue,
                 gross_profit_margin, valuation_to_revenue, yoy_growth_revenue, yoy_growth_profit,
                 yoy_growth_employees, yoy_growth_ltm_revenue, ltm_total_revenue, ltm_gross_profit,
                 ltm_sales_marketing_expense, ltm_gross_margin, ltm_operating_expense, ltm_ebitda,
                 ltm_net_income, ltm_ebitda_margin, ltm_net_income_margin, fiscal_reporting_date,
                 fiscal_reporting_quarter, reporting_year, reporting_quarter, created_date,
                 created_by, last_update_date, last_updated_by):
        """
        Initializes a new instance of the ReportingMetrics model with the specified parameters.

        Args:
            company_id (UUID): Unique identifier for the company.
            currency (str): Currency used for the financial metrics.
            enterprise_value (Decimal): Enterprise value of the company.
            arr (Decimal): Annual Recurring Revenue.
            recurring_percentage_revenue (Decimal): Percentage of recurring revenue.
            revenue_per_fte (Decimal): Revenue per full-time equivalent employee.
            gross_profit_per_fte (Decimal): Gross profit per full-time equivalent employee.
            employee_growth_rate (Decimal): Growth rate of employees.
            change_in_cash (Decimal): Change in cash balance.
            revenue_growth (Decimal): Revenue growth rate.
            monthly_cash_burn (Decimal): Monthly cash burn rate.
            runway_months (Decimal): Number of months of runway.
            ev_by_equity_raised_plus_debt (Decimal): Enterprise value divided by equity raised plus debt.
            sales_marketing_percentage_revenue (Decimal): Sales and marketing expense as a percentage of revenue.
            total_operating_percentage_revenue (Decimal): Total operating expense as a percentage of revenue.
            gross_profit_margin (Decimal): Gross profit margin.
            valuation_to_revenue (Decimal): Valuation to revenue ratio.
            yoy_growth_revenue (Decimal): Year-over-year revenue growth.
            yoy_growth_profit (Decimal): Year-over-year profit growth.
            yoy_growth_employees (Decimal): Year-over-year employee growth.
            yoy_growth_ltm_revenue (Decimal): Year-over-year growth in last twelve months revenue.
            ltm_total_revenue (Decimal): Last twelve months total revenue.
            ltm_gross_profit (Decimal): Last twelve months gross profit.
            ltm_sales_marketing_expense (Decimal): Last twelve months sales and marketing expense.
            ltm_gross_margin (Decimal): Last twelve months gross margin.
            ltm_operating_expense (Decimal): Last twelve months operating expense.
            ltm_ebitda (Decimal): Last twelve months EBITDA.
            ltm_net_income (Decimal): Last twelve months net income.
            ltm_ebitda_margin (Decimal): Last twelve months EBITDA margin.
            ltm_net_income_margin (Decimal): Last twelve months net income margin.
            fiscal_reporting_date (Date): Fiscal reporting date.
            fiscal_reporting_quarter (int): Fiscal reporting quarter.
            reporting_year (int): Reporting year.
            reporting_quarter (int): Reporting quarter.
            created_date (DateTime): Date and time of record creation.
            created_by (str): User who created the record.
            last_update_date (DateTime): Date and time of last update.
            last_updated_by (str): User who last updated the record.
        """
        self.company_id = company_id
        self.currency = currency
        self.enterprise_value = enterprise_value
        self.arr = arr
        self.recurring_percentage_revenue = recurring_percentage_revenue
        self.revenue_per_fte = revenue_per_fte
        self.gross_profit_per_fte = gross_profit_per_fte
        self.employee_growth_rate = employee_growth_rate
        self.change_in_cash = change_in_cash
        self.revenue_growth = revenue_growth
        self.monthly_cash_burn = monthly_cash_burn
        self.runway_months = runway_months
        self.ev_by_equity_raised_plus_debt = ev_by_equity_raised_plus_debt
        self.sales_marketing_percentage_revenue = sales_marketing_percentage_revenue
        self.total_operating_percentage_revenue = total_operating_percentage_revenue
        self.gross_profit_margin = gross_profit_margin
        self.valuation_to_revenue = valuation_to_revenue
        self.yoy_growth_revenue = yoy_growth_revenue
        self.yoy_growth_profit = yoy_growth_profit
        self.yoy_growth_employees = yoy_growth_employees
        self.yoy_growth_ltm_revenue = yoy_growth_ltm_revenue
        self.ltm_total_revenue = ltm_total_revenue
        self.ltm_gross_profit = ltm_gross_profit
        self.ltm_sales_marketing_expense = ltm_sales_marketing_expense
        self.ltm_gross_margin = ltm_gross_margin
        self.ltm_operating_expense = ltm_operating_expense
        self.ltm_ebitda = ltm_ebitda
        self.ltm_net_income = ltm_net_income
        self.ltm_ebitda_margin = ltm_ebitda_margin
        self.ltm_net_income_margin = ltm_net_income_margin
        self.fiscal_reporting_date = fiscal_reporting_date
        self.fiscal_reporting_quarter = fiscal_reporting_quarter
        self.reporting_year = reporting_year
        self.reporting_quarter = reporting_quarter
        self.created_date = created_date
        self.created_by = created_by
        self.last_update_date = last_update_date
        self.last_updated_by = last_updated_by

# Note: Ensure that the 'companies' table exists in the database schema with a primary key 'id' of type UUID.