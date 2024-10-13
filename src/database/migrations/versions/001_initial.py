"""
Initial migration

Revision ID: 001
Revises: 
Create Date: 2023-09-15 10:00:00.000000

This script sets up the initial database schema for the OMERS Ventures financial reporting platform.
It creates the necessary tables and constraints to store company data, input metrics, and calculated financial metrics.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    """
    Applies the initial database schema by creating tables and constraints.
    
    This function addresses the requirement:
    - Database Setup and Configuration (Technical Requirements/Feature 1: Database Setup and Configuration)
      Establishes the initial database schema by creating tables and constraints, ensuring that the database
      is ready to store financial reporting metrics.
    """
    # Create Companies table
    op.create_table('companies',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('reporting_status', sa.String(), nullable=False),
        sa.Column('reporting_currency', sa.String(), nullable=False),
        sa.Column('fund', sa.String(), nullable=False),
        sa.Column('location_country', sa.String(), nullable=False),
        sa.Column('customer_type', sa.String(), nullable=False),
        sa.Column('revenue_type', sa.String(), nullable=False),
        sa.Column('equity_raised', sa.Numeric(), nullable=True),
        sa.Column('post_money_valuation', sa.Numeric(), nullable=True),
        sa.Column('year_end_date', sa.Date(), nullable=False),
        sa.Column('created_date', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(), nullable=False),
        sa.Column('last_update_date', sa.DateTime(), nullable=True, onupdate=sa.func.now()),
        sa.Column('last_updated_by', sa.String(), nullable=True)
    )

    # Create Metrics Input table
    op.create_table('metrics_input',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('company_id', UUID(as_uuid=True), sa.ForeignKey('companies.id'), nullable=False),
        sa.Column('currency', sa.String(), nullable=False),
        sa.Column('total_revenue', sa.Numeric(), nullable=True),
        sa.Column('recurring_revenue', sa.Numeric(), nullable=True),
        sa.Column('gross_profit', sa.Numeric(), nullable=True),
        sa.Column('sales_marketing_expense', sa.Numeric(), nullable=True),
        sa.Column('total_operating_expense', sa.Numeric(), nullable=True),
        sa.Column('ebitda', sa.Numeric(), nullable=True),
        sa.Column('net_income', sa.Numeric(), nullable=True),
        sa.Column('cash_burn', sa.Numeric(), nullable=True),
        sa.Column('cash_balance', sa.Numeric(), nullable=True),
        sa.Column('debt_outstanding', sa.Numeric(), nullable=True),
        sa.Column('employees', sa.Integer(), nullable=True),
        sa.Column('customers', sa.Integer(), nullable=True),
        sa.Column('fiscal_reporting_date', sa.Date(), nullable=False),
        sa.Column('fiscal_reporting_quarter', sa.Integer(), nullable=False),
        sa.Column('reporting_year', sa.Integer(), nullable=False),
        sa.Column('reporting_quarter', sa.Integer(), nullable=False),
        sa.Column('created_date', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(), nullable=False),
        sa.Column('last_update_date', sa.DateTime(), nullable=True, onupdate=sa.func.now()),
        sa.Column('last_updated_by', sa.String(), nullable=True)
    )

    # Create Quarterly Reporting Financials table
    op.create_table('quarterly_reporting_financials',
        sa.Column('company_id', UUID(as_uuid=True), sa.ForeignKey('companies.id'), primary_key=True),
        sa.Column('currency', sa.String(), primary_key=True),
        sa.Column('exchange_rate_used', sa.Numeric(), nullable=False),
        sa.Column('total_revenue', sa.Numeric(), nullable=True),
        sa.Column('recurring_revenue', sa.Numeric(), nullable=True),
        sa.Column('gross_profit', sa.Numeric(), nullable=True),
        sa.Column('debt_outstanding', sa.Numeric(), nullable=True),
        sa.Column('sales_marketing_expense', sa.Numeric(), nullable=True),
        sa.Column('total_operating_expense', sa.Numeric(), nullable=True),
        sa.Column('ebitda', sa.Numeric(), nullable=True),
        sa.Column('net_income', sa.Numeric(), nullable=True),
        sa.Column('cash_burn', sa.Numeric(), nullable=True),
        sa.Column('cash_balance', sa.Numeric(), nullable=True),
        sa.Column('fiscal_reporting_date', sa.Date(), primary_key=True),
        sa.Column('fiscal_reporting_quarter', sa.Integer(), nullable=False),
        sa.Column('reporting_year', sa.Integer(), nullable=False),
        sa.Column('reporting_quarter', sa.Integer(), nullable=False),
        sa.Column('created_date', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(), nullable=False),
        sa.Column('last_update_date', sa.DateTime(), nullable=True, onupdate=sa.func.now()),
        sa.Column('last_updated_by', sa.String(), nullable=True)
    )

    # Create Quarterly Reporting Metrics table
    op.create_table('quarterly_reporting_metrics',
        sa.Column('company_id', UUID(as_uuid=True), sa.ForeignKey('companies.id'), primary_key=True),
        sa.Column('currency', sa.String(), primary_key=True),
        sa.Column('enterprise_value', sa.Numeric(), nullable=True),
        sa.Column('arr', sa.Numeric(), nullable=True),
        sa.Column('recurring_percentage_revenue', sa.Numeric(), nullable=True),
        sa.Column('revenue_per_fte', sa.Numeric(), nullable=True),
        sa.Column('gross_profit_per_fte', sa.Numeric(), nullable=True),
        sa.Column('employee_growth_rate', sa.Numeric(), nullable=True),
        sa.Column('change_in_cash', sa.Numeric(), nullable=True),
        sa.Column('revenue_growth', sa.Numeric(), nullable=True),
        sa.Column('monthly_cash_burn', sa.Numeric(), nullable=True),
        sa.Column('runway_months', sa.Numeric(), nullable=True),
        sa.Column('ev_by_equity_raised_plus_debt', sa.Numeric(), nullable=True),
        sa.Column('sales_marketing_percentage_revenue', sa.Numeric(), nullable=True),
        sa.Column('total_operating_percentage_revenue', sa.Numeric(), nullable=True),
        sa.Column('gross_profit_margin', sa.Numeric(), nullable=True),
        sa.Column('valuation_to_revenue', sa.Numeric(), nullable=True),
        sa.Column('yoy_growth_revenue', sa.Numeric(), nullable=True),
        sa.Column('yoy_growth_profit', sa.Numeric(), nullable=True),
        sa.Column('yoy_growth_employees', sa.Numeric(), nullable=True),
        sa.Column('yoy_growth_ltm_revenue', sa.Numeric(), nullable=True),
        sa.Column('ltm_total_revenue', sa.Numeric(), nullable=True),
        sa.Column('ltm_gross_profit', sa.Numeric(), nullable=True),
        sa.Column('ltm_sales_marketing_expense', sa.Numeric(), nullable=True),
        sa.Column('ltm_gross_margin', sa.Numeric(), nullable=True),
        sa.Column('ltm_operating_expense', sa.Numeric(), nullable=True),
        sa.Column('ltm_ebitda', sa.Numeric(), nullable=True),
        sa.Column('ltm_net_income', sa.Numeric(), nullable=True),
        sa.Column('ltm_ebitda_margin', sa.Numeric(), nullable=True),
        sa.Column('ltm_net_income_margin', sa.Numeric(), nullable=True),
        sa.Column('fiscal_reporting_date', sa.Date(), primary_key=True),
        sa.Column('fiscal_reporting_quarter', sa.Integer(), nullable=False),
        sa.Column('reporting_year', sa.Integer(), nullable=False),
        sa.Column('reporting_quarter', sa.Integer(), nullable=False),
        sa.Column('created_date', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(), nullable=False),
        sa.Column('last_update_date', sa.DateTime(), nullable=True, onupdate=sa.func.now()),
        sa.Column('last_updated_by', sa.String(), nullable=True)
    )

    # Create indexes for improved query performance
    op.create_index('ix_companies_name', 'companies', ['name'])
    op.create_index('ix_metrics_input_company_id_fiscal_reporting_date', 'metrics_input', ['company_id', 'fiscal_reporting_date'])
    op.create_index('ix_quarterly_reporting_financials_company_id_fiscal_reporting_date', 'quarterly_reporting_financials', ['company_id', 'fiscal_reporting_date'])
    op.create_index('ix_quarterly_reporting_metrics_company_id_fiscal_reporting_date', 'quarterly_reporting_metrics', ['company_id', 'fiscal_reporting_date'])

def downgrade():
    """
    Reverts the initial database schema by dropping tables and constraints.
    
    This function does not return a value but reverts the schema changes in the database.
    """
    # Drop tables in reverse order of creation to avoid foreign key constraint violations
    op.drop_table('quarterly_reporting_metrics')
    op.drop_table('quarterly_reporting_financials')
    op.drop_table('metrics_input')
    op.drop_table('companies')