-- Seed data for OMERS Ventures Financial Reporting Metrics Backend Platform
-- This SQL script populates the database tables with sample data for testing and development purposes.
-- Requirements addressed: Database Setup and Configuration (Technical Requirements/Feature 1: Database Setup and Configuration)

-- Disable foreign key checks temporarily to allow for easier data insertion
SET session_replication_role = 'replica';

-- Seed data for Companies table
INSERT INTO "companies" (id, name, reporting_status, reporting_currency, fund, location_country, customer_type, revenue_type, equity_raised, post_money_valuation, year_end_date, created_date, created_by, last_update_date, last_updated_by)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'TechCorp', 'Active', 'USD', 'Fund I', 'United States', 'B2B', 'Recurring', 10000000.00, 50000000.00, '2023-12-31', CURRENT_TIMESTAMP, 'Seed Script', NULL, NULL),
    ('22222222-2222-2222-2222-222222222222', 'DataSoft', 'Active', 'CAD', 'Fund II', 'Canada', 'B2C', 'Subscription', 5000000.00, 25000000.00, '2023-12-31', CURRENT_TIMESTAMP, 'Seed Script', NULL, NULL),
    ('33333333-3333-3333-3333-333333333333', 'AIInnovate', 'Inactive', 'EUR', 'Fund III', 'Germany', 'B2B', 'Recurring', 15000000.00, 75000000.00, '2023-12-31', CURRENT_TIMESTAMP, 'Seed Script', NULL, NULL);

-- Seed data for Metrics Input table
INSERT INTO "metrics_input" (id, company_id, currency, total_revenue, recurring_revenue, gross_profit, sales_marketing_expense, total_operating_expense, ebitda, net_income, cash_burn, cash_balance, debt_outstanding, employees, customers, fiscal_reporting_date, fiscal_reporting_quarter, reporting_year, reporting_quarter, created_date, created_by, last_update_date, last_updated_by)
VALUES
    ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-1111-1111-1111-111111111111', 'USD', 1000000.00, 800000.00, 600000.00, 200000.00, 700000.00, 300000.00, 250000.00, 50000.00, 2000000.00, 0.00, 50, 1000, '2023-03-31', 1, 2023, 1, CURRENT_TIMESTAMP, 'Seed Script', NULL, NULL),
    ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '22222222-2222-2222-2222-222222222222', 'CAD', 750000.00, 600000.00, 450000.00, 150000.00, 500000.00, 250000.00, 200000.00, 50000.00, 1500000.00, 100000.00, 30, 500, '2023-03-31', 1, 2023, 1, CURRENT_TIMESTAMP, 'Seed Script', NULL, NULL),
    ('cccccccc-cccc-cccc-cccc-cccccccccccc', '33333333-3333-3333-3333-333333333333', 'EUR', 1200000.00, 1000000.00, 800000.00, 250000.00, 900000.00, 300000.00, 250000.00, 100000.00, 3000000.00, 500000.00, 75, 2000, '2023-03-31', 1, 2023, 1, CURRENT_TIMESTAMP, 'Seed Script', NULL, NULL);

-- Seed data for Quarterly Reporting Financials table
INSERT INTO "quarterly_reporting_financials" (company_id, currency, exchange_rate_used, total_revenue, recurring_revenue, gross_profit, debt_outstanding, sales_marketing_expense, total_operating_expense, ebitda, net_income, cash_burn, cash_balance, fiscal_reporting_date, fiscal_reporting_quarter, reporting_year, reporting_quarter, created_date, created_by, last_update_date, last_updated_by)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'USD', 1.00, 1000000.00, 800000.00, 600000.00, 0.00, 200000.00, 700000.00, 300000.00, 250000.00, 50000.00, 2000000.00, '2023-03-31', 1, 2023, 1, CURRENT_TIMESTAMP, 'Seed Script', NULL, NULL),
    ('22222222-2222-2222-2222-222222222222', 'USD', 0.75, 562500.00, 450000.00, 337500.00, 75000.00, 112500.00, 375000.00, 187500.00, 150000.00, 37500.00, 1125000.00, '2023-03-31', 1, 2023, 1, CURRENT_TIMESTAMP, 'Seed Script', NULL, NULL),
    ('33333333-3333-3333-3333-333333333333', 'USD', 1.10, 1320000.00, 1100000.00, 880000.00, 550000.00, 275000.00, 990000.00, 330000.00, 275000.00, 110000.00, 3300000.00, '2023-03-31', 1, 2023, 1, CURRENT_TIMESTAMP, 'Seed Script', NULL, NULL);

-- Seed data for Quarterly Reporting Metrics table
INSERT INTO "quarterly_reporting_metrics" (company_id, currency, enterprise_value, arr, recurring_percentage_revenue, revenue_per_fte, gross_profit_per_fte, employee_growth_rate, change_in_cash, revenue_growth, monthly_cash_burn, runway_months, ev_by_equity_raised_plus_debt, sales_marketing_percentage_revenue, total_operating_percentage_revenue, gross_profit_margin, valuation_to_revenue, yoy_growth_revenue, yoy_growth_profit, yoy_growth_employees, yoy_growth_ltm_revenue, ltm_total_revenue, ltm_gross_profit, ltm_sales_marketing_expense, ltm_gross_margin, ltm_operating_expense, ltm_ebitda, ltm_net_income, ltm_ebitda_margin, ltm_net_income_margin, fiscal_reporting_date, fiscal_reporting_quarter, reporting_year, reporting_quarter, created_date, created_by, last_update_date, last_updated_by)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'USD', 50000000.00, 3200000.00, 80.00, 20000.00, 12000.00, 25.00, 500000.00, 20.00, 16666.67, 120, 5.00, 20.00, 70.00, 60.00, 50.00, 30.00, 25.00, 20.00, 35.00, 4000000.00, 2400000.00, 800000.00, 60.00, 2800000.00, 1200000.00, 1000000.00, 30.00, 25.00, '2023-03-31', 1, 2023, 1, CURRENT_TIMESTAMP, 'Seed Script', NULL, NULL),
    ('22222222-2222-2222-2222-222222222222', 'USD', 25000000.00, 1800000.00, 80.00, 18750.00, 11250.00, 20.00, 250000.00, 15.00, 12500.00, 90, 5.00, 20.00, 66.67, 60.00, 44.44, 25.00, 20.00, 15.00, 30.00, 2250000.00, 1350000.00, 450000.00, 60.00, 1500000.00, 750000.00, 600000.00, 33.33, 26.67, '2023-03-31', 1, 2023, 1, CURRENT_TIMESTAMP, 'Seed Script', NULL, NULL),
    ('33333333-3333-3333-3333-333333333333', 'USD', 75000000.00, 4400000.00, 83.33, 17600.00, 11733.33, 30.00, 750000.00, 25.00, 36666.67, 90, 5.00, 20.83, 75.00, 66.67, 56.82, 35.00, 30.00, 25.00, 40.00, 5280000.00, 3520000.00, 1100000.00, 66.67, 3960000.00, 1320000.00, 1100000.00, 25.00, 20.83, '2023-03-31', 1, 2023, 1, CURRENT_TIMESTAMP, 'Seed Script', NULL, NULL);

-- Re-enable foreign key checks
SET session_replication_role = 'origin';

-- Verify data insertion
SELECT 'companies' AS table_name, COUNT(*) AS row_count FROM "companies"
UNION ALL
SELECT 'metrics_input' AS table_name, COUNT(*) AS row_count FROM "metrics_input"
UNION ALL
SELECT 'quarterly_reporting_financials' AS table_name, COUNT(*) AS row_count FROM "quarterly_reporting_financials"
UNION ALL
SELECT 'quarterly_reporting_metrics' AS table_name, COUNT(*) AS row_count FROM "quarterly_reporting_metrics";