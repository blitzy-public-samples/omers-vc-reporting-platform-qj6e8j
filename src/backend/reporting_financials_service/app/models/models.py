from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

# SQLAlchemy version 1.4.22 is used for ORM operations
Base = declarative_base()

class FinancialReport(Base):
    """
    A data model representing a financial report entry in the database.
    This model addresses the 'Data Storage' requirement as specified in
    Technical Specification/Feature 1: Database Setup and Configuration.
    It ensures efficient storage and retrieval of financial data in the PostgreSQL database.
    """
    __tablename__ = 'financial_reports'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    currency = Column(String, nullable=False)
    total_revenue = Column(Numeric(precision=18, scale=2), nullable=False)
    recurring_revenue = Column(Numeric(precision=18, scale=2), nullable=False)
    gross_profit = Column(Numeric(precision=18, scale=2), nullable=False)
    sales_marketing_expense = Column(Numeric(precision=18, scale=2), nullable=False)
    total_operating_expense = Column(Numeric(precision=18, scale=2), nullable=False)
    ebitda = Column(Numeric(precision=18, scale=2), nullable=False)
    net_income = Column(Numeric(precision=18, scale=2), nullable=False)
    cash_burn = Column(Numeric(precision=18, scale=2), nullable=False)
    cash_balance = Column(Numeric(precision=18, scale=2), nullable=False)
    debt_outstanding = Column(Numeric(precision=18, scale=2))
    employees = Column(Integer, nullable=False)
    customers = Column(Integer)
    fiscal_reporting_date = Column(Date, nullable=False)
    fiscal_reporting_quarter = Column(Integer, nullable=False)
    reporting_year = Column(Integer, nullable=False)
    reporting_quarter = Column(Integer, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(String, nullable=False)
    last_update_date = Column(DateTime, onupdate=datetime.utcnow)
    last_updated_by = Column(String)

    # Relationship to the Company model (assuming it exists in the same file or is imported)
    company = relationship("Company", back_populates="financial_reports")

    def __init__(self, company_id, currency, total_revenue, recurring_revenue, gross_profit,
                 sales_marketing_expense, total_operating_expense, ebitda, net_income, cash_burn,
                 cash_balance, debt_outstanding, employees, customers, fiscal_reporting_date,
                 fiscal_reporting_quarter, reporting_year, reporting_quarter, created_by, last_updated_by=None):
        """
        Initializes a new instance of the FinancialReport model with the provided attributes.
        """
        self.company_id = company_id
        self.currency = currency
        self.total_revenue = total_revenue
        self.recurring_revenue = recurring_revenue
        self.gross_profit = gross_profit
        self.sales_marketing_expense = sales_marketing_expense
        self.total_operating_expense = total_operating_expense
        self.ebitda = ebitda
        self.net_income = net_income
        self.cash_burn = cash_burn
        self.cash_balance = cash_balance
        self.debt_outstanding = debt_outstanding
        self.employees = employees
        self.customers = customers
        self.fiscal_reporting_date = fiscal_reporting_date
        self.fiscal_reporting_quarter = fiscal_reporting_quarter
        self.reporting_year = reporting_year
        self.reporting_quarter = reporting_quarter
        self.created_date = datetime.utcnow()
        self.created_by = created_by
        self.last_updated_by = last_updated_by

    def __repr__(self):
        """
        Returns a string representation of the FinancialReport instance.
        """
        return (f"<FinancialReport(id={self.id}, company_id={self.company_id}, "
                f"reporting_year={self.reporting_year}, reporting_quarter={self.reporting_quarter})>")

# Note: The Company model is not defined here as it's not mentioned in the provided specification.
# If needed, it should be imported or defined in this file to complete the relationship.