from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# SQLAlchemy version 1.4.22 is used for ORM operations
Base = declarative_base()

class FinancialReport(Base):
    """
    ORM model for a quarterly financial report entry.
    This model addresses the 'Data Storage' requirement as specified in
    Technical Specification/Feature 1: Database Setup and Configuration.
    It ensures efficient storage and retrieval of financial data in the PostgreSQL database.
    """
    # The authoritative table is `quarterly_reporting_financials` (database/schemas/
    # create_tables.sql), not `financial_reports`. Aligning the ORM mapping to the real
    # table is what enables the API -> PostgreSQL round trip.
    __tablename__ = 'quarterly_reporting_financials'

    # The authoritative table declares no surrogate `id` and no single-column primary key.
    # Its natural business key is (company_id, reporting_year, reporting_quarter); declaring
    # that composite key as the ORM primary key gives SQLAlchemy the row identity it needs
    # for SELECT/INSERT without altering the database schema. Referential integrity to
    # companies(id) is enforced by the DB-level constraint
    # (quarterly_reporting_financials_company_id_fkey); no ORM-level ForeignKey is declared
    # because the companies table is not mapped inside this microservice.
    company_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    currency = Column(String, nullable=False)
    exchange_rate_used = Column(Numeric)
    total_revenue = Column(Numeric)
    recurring_revenue = Column(Numeric)
    gross_profit = Column(Numeric)
    debt_outstanding = Column(Numeric)
    sales_marketing_expense = Column(Numeric)
    total_operating_expense = Column(Numeric)
    ebitda = Column(Numeric)
    net_income = Column(Numeric)
    cash_burn = Column(Numeric)
    cash_balance = Column(Numeric)
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
        """
        Returns a string representation of the FinancialReport instance.
        """
        return (f"<FinancialReport(company_id={self.company_id}, "
                f"reporting_year={self.reporting_year}, reporting_quarter={self.reporting_quarter})>")
