We are building a backend platform to store and retrieve financial reporting metrics from companies a VC firm has invested in.

Key Assets:
- Database to store quarterly reporting metrics received from companies the firm has invested in
- The database will be made up of four tables: Company Table, Input Metrics, Reporting Financials and Reporting Metrics
- A REST API service to add and retrieve data from the database
- A data transformation process which a) retrieves fx rates from an API service & calculates derivative metrics from the input table, into the reporting and metrics tables

Environment/technology Notes:
Ideally use:
- A Postgres SQL database
- FastAPI service
- You choose the technology to calculate derivative metrics (from input table to financials & metrics tables)
- Note that this will be hosted on standard Azure products

Database Table Structure:

1. Companies Table:
The main table that stores descriptive information on OV Portcos
| Field                | Notes                                                         |
|----------------------|---------------------------------------------------------------|
| id                   | Assigned UUID of the OV Portfolio Company |
| name                 | Name of the portfolio company|
| reporting_status     | Indicator of whether or not we are actively reporting on this company. Status: Active vs. Inactive |
| reporting_currency   | Currency currently used by the company (follow ISO 4217 standard) |
| fund                 | OV fund(s) invested in this company |
| location_country     | Country location of this company (use full country name) |
| customer_type        | Select: Enterprise/Mid-Market, SMB, Consumer |
| revenue_type         | Select: Subscription, Usage Pricing, Transactional, Marketplace |
| equity_raised        | Total equity raised to date |
| post_money_valuation | Last post money valuation |
| year_end_date        | Fiscal year end of the company |
| created_date         | Date the company record was created |
| created_by           | Person who created the record |
| last_update_date     | Date the record was last updated |
| last_updated_by      | Person who last updated the record |

2. Metrics Input Table:
The table which contains the metrics & values that we receive from the portfolio company, in their reporting currency
| Input                   | Notes                              |
|-------------------------|------------------------------------|
| id                      | Primary Key |
| company_id              | The id of the company (OV Portco DB UUID) |
| currency                | The base currency the metrics are being input in |
| total_revenue           | Input: Quarterly total revenue |
| recurring_revenue       | Input: Quarterly Recurring Revenue |
| gross_profit            | Input: Quarterly Gross Profit |
| sales_marketing_expense | Input: Quarterly Sales Marketing Expense |
| total_operating_expense | Input: Quarterly Total Operating Expense |
| ebitda                  | Input: Quarterly EBITDA |
| net_income              | Input: Quarterly Net Income |
| cash_burn               | Input: Quarterly Cash Burn |
| cash_balance            | Input: Quarter end Cash Balance |
| debt_outstanding        | Input: Quarter end total debt outstanding (including convertible) |
| employees               | Input: Quarter end number of employees |
| customers               | Input: Quarter end number of customers |
| fiscal_reporting_date   | Portfolio company quarter ending date this data is from |
| fiscal_reporting_quarter| Portfolio company quarter ending that this data is from |
| reporting_year          | OMERS Ventures reporting year this data relates to |
| reporting_quarter       | OMERS Ventures reporting quarter this data relates to |
| created_date            | Date this record was created |
| created_by              | Person who created the record (passed via API) |
| last_update_date        | Date the record was last updated |
| last_updated_by         | The person who last updated the record (passed via API)|

3. Quarterly Reporting Financials:
The table which contains the main financial metrics for each Portfolio Company. Taken from the Input Table & then stored in Local, USD & CAD for each quarter.
| Field                   | Notes                                                         |
|-------------------------|---------------------------------------------------------------|
| company_id              |                                    |
| currency                | Currency code of the this data (ISO 4217)|
| exchange_rate_used      | Foreign exchange rate used for this data|
| total_revenue           | Currency adjusted Quarterly Total Revenue|
| recurring_revenue       | Currency adjusted Quarterly Recurring Revenue|                                                              
| gross_profit            | Currency adjusted Quarterly Gross Profit|
| debt_outstanding        | Currency adjusted Quarter end total debt outstanding (including convertible) |
| sales_marketing_expense | Currency adjusted Quarterly Sales & Marketing Expense|
| total_operating_expense | Currency adjusted Quarterly Total Operating Expense |
| ebitda                  | Currency adjusted Quarterly EBITDA |
| net_income              | Currency adjusted Quarterly Net Income |
| cash_burn               | Currency adjusted Quarterly Cash Burn |
| cash_balance            | Currency adjusted Quarter End Cash Balance |
| fiscal_reporting_date   | Portfolio company quarter ending date this data is from |
| fiscal_reporting_quarter| Portfolio company quarter ending that this data is from |
| reporting_year          | OMERS Ventures reporting year this data relates to |
| reporting_quarter       | OMERS Ventures reporting quarter this data relates to |
| created_date            | The date the record was created |
| created_by              | The person who created the record |
| last_update_date        | The date the record was last updated |
| last_updated_by         | The person who last updated the record |

4. Quarterly Reporting Metrics:
The table which contains all calculated financial metrics for each Portfolio Company. Taken from the Input Table, calculated and then stored in Local, USD & CAD for each quarter.
| Field                            | Notes                                                       |
|----------------------------------|-------------------------------------------------------------|
| company_id                        |                                           |
| currency                          | Currency code of the this data (ISO 4217) |
| enterprise_value                  | Calculation: post_money_valuation + debt_outstanding |
| arr                               | (Annual Recurring Revenue). Calculation: recurring_revenue * 4 |
| recurring_percentage_revenue      | Calculation: recurring_revenue / total_revenue |
| revenue_per_fte                   | Revenue Per Employee. Calculation: (total_revenue * 12) / employees |
| gross_profit_per_fte              | Gross Profit Per Employee. Calculation: (gross_profit * 12) / employees |
| employee_growth_rate              | Calculation: current period employees / last period employees |
| change_in_cash                    | Calculation: current period cash balance - last period quarter end cash balance |
| revenue_growth                    | Calculation: current period revenue / last period revenue |
| monthly_cash_burn                 | Calculation: cash_burn / 3 |
| runway_months                     | Months of 'runway' left with business. Calculation: monthly_cash_burn / cash_balance |
| ev_by_equity_raised_plus_debt     | Calculation: enterprise_value / (companies.equity_raised + debt_outstanding)|
| sales_marketing_percentage_revenue| Calculation: sales_marketing_expense / total_revenue |
| total_operating_percentage_revenue| Calculation: total_operating_expense / total_revenue |
| gross_profit_margin               | Calculation: gross_profit / total_revenue |
| valuation_to_revenue              | Calculation: company.post_money_valuation / total_revenue |
| yoy_growth_revenue                | Calculation: current period total_revenue / last period total_revenue |
| yoy_growth_profit                 | Calculation: current period gross_profit / last period gross_profit |
| yoy_growth_employees              | Calculation: current period employees / last period employees |
| yoy_growth_ltm_revenue            | Calculation: current period ltm_revenue / last period ltm_revenue |
| ltm_total_revenue                 | Calculation: SUM of total_revenue from last 4 quarters |
| ltm_gross_profit                  | Calculation: SUM of gross_profit from last 4 quarters |
| ltm_sales_marketing_expense       | Calculation: SUM of sales_marketing_expense from last 4 quarters |
| ltm_gross_margin                  | Calculation: SUM of gross_margin from last 4 quarters |
| ltm_operating_expense             | Calculation: SUM of operating_expense from last 4 quarters |
| ltm_ebitda                        | Calculation: SUM of ebitda from last 4 quarters |
| ltm_net_income                    | Calculation: SUM of net_income from last 4 quarters |
| ltm_ebitda_margin                 | Calculation: ltm_ebitda / ltm_revenue |
| ltm_net_income_margin             | Calculation: ltm_net_income / ltm_revenue |
| fiscal_reporting_date   | Portfolio company quarter ending date this data is from |
| fiscal_reporting_quarter| Portfolio company quarter ending that this data is from |
| reporting_year                    | OMERS Ventures reporting year this data relates to |
| reporting_quarter                 | OMERS Ventures reporting quarter this data relates to |
| created_date                      | The date the record was created |
| created_by                        | The person who created the record |
| last_update_date                  | The date the record was last updated |
| last_updated_by                   | The person who last updated the record |

API Structure:
The API has two basic functions. GET data and POST data.

GET Input Metrics:
GET function to retrieve data from the database tables.
The endpoint requires a company_id and a reporting time frame start and end date example.
Endpoints -
/input/ (pull data from the input table)
/reporting/ (pull data from the reporting table)
/metrics/ (pull data from the metrics table)
(https://api.omersventures.com/v1/input_metrics?company_id=reciLI8sBuJE9vEAv&fiscal_reporting_date=2022-12-31)
URL Parameters:
    company_id=reciLI8sBuJE9vEAv
    end_reporting_date=2022-12-31
    start_reporting_date=2023-12-31
Example result:
{
    "company_id": "reciLI8sBuJE9vEAv",
    "reporting_year": 2022,
    "reporting_quarter": 4,
    "currency": "USD",
    "total_revenue": 4194199.0,
    "recurring_revenue": 3912138.0,
    "gross_profit": 2730244.0,
    "sales_marketing_expense": 1470828.0,
    "total_operating_expense": 7195136.0,
    "ebitda": -4464892.0,
    "net_income": -4339102.0,
    "cash_burn": -4464892.0,
    "cash_balance": 32407138.0,
    "debt_outstanding": null,
    "employees": 1,
    "customers": null,
    "fiscal_reporting_quarter": 4,
    "fiscal_reporting_date": "2022-12-31 00:00:00",
    "created_date": "2023-08-24 15:25:11",
    "created_by": "ManualTest",
    "last_update_date": null,
    "last_updated_by": null
}

PUT Company:
Endpoint -
/input/ (push data into the input table)
/company/ (push data to the company table)
Post a body to create a company:
{
  "company_id": "reciLI8sBuJE9vEAv",
  "company_name": "WorkRamp",
  "reporting_status": "Active",
  "reporting_currency": "USD",
  "fund": "Fund IV",
  "customer_type": "B2B",
  "location_country": "United States",
  "revenue_type": "Recurring",
  "equity_raised": 67.20,
  "post_money_valuation": 215.0,
  "year_end_date": "2022-12-31"
}
Same for input
Update vs insert:
If company_id exists in the table, the other fields will be updated.
If company_id is new, all fields in the body will be inserted.

Create the derivative metrics from the input metrics:
Whenever a new input metrics file is uploaded, automatically calculate the reporting and derivative metrics in multiple currencies.
Formulas are in the database table descriptions above.