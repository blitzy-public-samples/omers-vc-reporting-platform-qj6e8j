-- create_tables.sql
-- This SQL script defines the schema for the PostgreSQL database used to store financial reporting metrics.
-- It includes the creation of tables such as Companies, Metrics Input, Quarterly Reporting Financials,
-- and Quarterly Reporting Metrics, along with their respective constraints and indexes.

-- Requirements addressed:
-- Database Setup and Configuration (Technical Requirements/Feature 1: Database Setup and Configuration)
-- Establishes the database schema by creating the necessary tables and constraints to store financial reporting metrics,
-- ensuring alignment with ORM models and migration scripts.

-- Note: This script is designed for PostgreSQL 13

-- Create Companies table
CREATE TABLE IF NOT EXISTS Companies (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    reporting_status VARCHAR(50) NOT NULL,
    reporting_currency VARCHAR(3) NOT NULL,
    fund VARCHAR(100) NOT NULL,
    location_country VARCHAR(100) NOT NULL,
    customer_type VARCHAR(50) NOT NULL,
    revenue_type VARCHAR(50) NOT NULL,
    equity_raised DECIMAL,
    post_money_valuation DECIMAL,
    year_end_date DATE,
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100) NOT NULL,
    last_update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated_by VARCHAR(100)
);

-- Create Metrics Input table
CREATE TABLE IF NOT EXISTS Metrics_Input (
    id UUID PRIMARY KEY,
    company_id UUID NOT NULL,
    currency VARCHAR(3) NOT NULL,
    total_revenue DECIMAL,
    recurring_revenue DECIMAL,
    gross_profit DECIMAL,
    sales_marketing_expense DECIMAL,
    total_operating_expense DECIMAL,
    ebitda DECIMAL,
    net_income DECIMAL,
    cash_burn DECIMAL,
    cash_balance DECIMAL,
    debt_outstanding DECIMAL,
    employees INTEGER,
    customers INTEGER,
    fiscal_reporting_date DATE,
    fiscal_reporting_quarter INTEGER,
    reporting_year INTEGER,
    reporting_quarter INTEGER,
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100) NOT NULL,
    last_update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated_by VARCHAR(100),
    FOREIGN KEY (company_id) REFERENCES Companies(id)
);

-- Create Quarterly Reporting Financials table
CREATE TABLE IF NOT EXISTS Quarterly_Reporting_Financials (
    company_id UUID NOT NULL,
    currency VARCHAR(3) NOT NULL,
    exchange_rate_used DECIMAL,
    total_revenue DECIMAL,
    recurring_revenue DECIMAL,
    gross_profit DECIMAL,
    debt_outstanding DECIMAL,
    sales_marketing_expense DECIMAL,
    total_operating_expense DECIMAL,
    ebitda DECIMAL,
    net_income DECIMAL,
    cash_burn DECIMAL,
    cash_balance DECIMAL,
    fiscal_reporting_date DATE,
    fiscal_reporting_quarter INTEGER,
    reporting_year INTEGER,
    reporting_quarter INTEGER,
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100) NOT NULL,
    last_update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated_by VARCHAR(100),
    FOREIGN KEY (company_id) REFERENCES Companies(id)
);

-- Create Quarterly Reporting Metrics table
CREATE TABLE IF NOT EXISTS Quarterly_Reporting_Metrics (
    company_id UUID NOT NULL,
    currency VARCHAR(3) NOT NULL,
    enterprise_value DECIMAL,
    arr DECIMAL,
    recurring_percentage_revenue DECIMAL,
    revenue_per_fte DECIMAL,
    gross_profit_per_fte DECIMAL,
    employee_growth_rate DECIMAL,
    change_in_cash DECIMAL,
    revenue_growth DECIMAL,
    monthly_cash_burn DECIMAL,
    runway_months DECIMAL,
    ev_by_equity_raised_plus_debt DECIMAL,
    sales_marketing_percentage_revenue DECIMAL,
    total_operating_percentage_revenue DECIMAL,
    gross_profit_margin DECIMAL,
    valuation_to_revenue DECIMAL,
    yoy_growth_revenue DECIMAL,
    yoy_growth_profit DECIMAL,
    yoy_growth_employees DECIMAL,
    yoy_growth_ltm_revenue DECIMAL,
    ltm_total_revenue DECIMAL,
    ltm_gross_profit DECIMAL,
    ltm_sales_marketing_expense DECIMAL,
    ltm_gross_margin DECIMAL,
    ltm_operating_expense DECIMAL,
    ltm_ebitda DECIMAL,
    ltm_net_income DECIMAL,
    ltm_ebitda_margin DECIMAL,
    ltm_net_income_margin DECIMAL,
    fiscal_reporting_date DATE,
    fiscal_reporting_quarter INTEGER,
    reporting_year INTEGER,
    reporting_quarter INTEGER,
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100) NOT NULL,
    last_update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated_by VARCHAR(100),
    FOREIGN KEY (company_id) REFERENCES Companies(id)
);

-- Create indexes for improved query performance
CREATE INDEX idx_companies_name ON Companies(name);
CREATE INDEX idx_metrics_input_company_id ON Metrics_Input(company_id);
CREATE INDEX idx_metrics_input_fiscal_reporting_date ON Metrics_Input(fiscal_reporting_date);
CREATE INDEX idx_quarterly_reporting_financials_company_id ON Quarterly_Reporting_Financials(company_id);
CREATE INDEX idx_quarterly_reporting_financials_reporting_year_quarter ON Quarterly_Reporting_Financials(reporting_year, reporting_quarter);
CREATE INDEX idx_quarterly_reporting_metrics_company_id ON Quarterly_Reporting_Metrics(company_id);
CREATE INDEX idx_quarterly_reporting_metrics_reporting_year_quarter ON Quarterly_Reporting_Metrics(reporting_year, reporting_quarter);

-- Add comments to tables for documentation
COMMENT ON TABLE Companies IS 'Stores descriptive information about OMERS Ventures portfolio companies';
COMMENT ON TABLE Metrics_Input IS 'Contains raw financial metrics submitted by portfolio companies in their reporting currency';
COMMENT ON TABLE Quarterly_Reporting_Financials IS 'Holds currency-adjusted financial metrics derived from the Metrics Input table';
COMMENT ON TABLE Quarterly_Reporting_Metrics IS 'Stores calculated derivative financial metrics based on the transformed financials data';

-- Add comments to columns for documentation (example for Companies table)
COMMENT ON COLUMN Companies.id IS 'Unique identifier for the company';
COMMENT ON COLUMN Companies.name IS 'Name of the company';
COMMENT ON COLUMN Companies.reporting_status IS 'Current reporting status of the company';
COMMENT ON COLUMN Companies.reporting_currency IS 'Primary currency used for reporting by the company';
COMMENT ON COLUMN Companies.fund IS 'OMERS Ventures fund associated with the company';
COMMENT ON COLUMN Companies.location_country IS 'Country where the company is located';
COMMENT ON COLUMN Companies.customer_type IS 'Type of customers the company serves (e.g., B2B, B2C)';
COMMENT ON COLUMN Companies.revenue_type IS 'Primary type of revenue for the company (e.g., Recurring, Non-recurring)';
COMMENT ON COLUMN Companies.equity_raised IS 'Total equity raised by the company';
COMMENT ON COLUMN Companies.post_money_valuation IS 'Post-money valuation of the company';
COMMENT ON COLUMN Companies.year_end_date IS 'Financial year end date for the company';
COMMENT ON COLUMN Companies.created_date IS 'Date and time when the company record was created';
COMMENT ON COLUMN Companies.created_by IS 'User who created the company record';
COMMENT ON COLUMN Companies.last_update_date IS 'Date and time of the last update to the company record';
COMMENT ON COLUMN Companies.last_updated_by IS 'User who last updated the company record';

-- Note: Similar comments should be added for columns in other tables as well