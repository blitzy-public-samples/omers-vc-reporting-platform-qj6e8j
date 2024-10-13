# Data Transformation Function

This README provides documentation for the data transformation function implemented in Azure Functions. It outlines the purpose, setup instructions, dependencies, and usage guidelines for automating the retrieval of foreign exchange rates and calculation of derivative financial metrics.

## Purpose

The data transformation function is designed to automate the retrieval of foreign exchange rates and calculation of derivative financial metrics. This automation enhances data accuracy and reduces manual intervention in the financial reporting process for OMERS Ventures' portfolio companies.

This function addresses the following requirement:
- **Data Transformation Processes** (Technical Requirements/Feature 3: Data Transformation Processes): Automate the retrieval of foreign exchange rates and calculation of derivative financial metrics to enhance data accuracy and reduce manual intervention.

## Dependencies

### Internal Dependencies
- `transform_data` from `src/functions/data_transformation/main.py`: This module contains the core data transformation logic, including currency conversion and derivative calculations.

### External Dependencies
- Azure Functions (azure-functions): Latest version
  - Purpose: To execute serverless data transformation scripts triggered by data ingestion events.
- requests: Latest version
  - Purpose: Used for making HTTP requests to external APIs, such as fetching foreign exchange rates.
- pandas: Latest version
  - Purpose: Facilitates data manipulation and transformation tasks, particularly for handling financial metrics.
- numpy: Latest version
  - Purpose: Supports numerical operations and calculations required for derivative metric computations.

## Setup Instructions

To set up the data transformation function, follow these steps:

1. Ensure that Azure Functions is configured in your Azure account.
2. Install the necessary Python dependencies listed in requirements.txt.
3. Configure environment variables using the .env.sample file as a reference.
4. Deploy the function to Azure Functions using the Azure CLI or Azure Portal.

## Usage Guidelines

To use the data transformation function:

1. Trigger the function manually via HTTP requests or automatically using the configured timer trigger.
2. Monitor the output queue for transformed data results.
3. Verify the accuracy of currency conversions and derivative calculations through logs and test cases.

## Testing Procedures

To test the data transformation function:

1. Run unit tests using pytest to validate the transformation logic.
2. Ensure all test cases in test_main.py pass successfully.
3. Review test coverage and address any gaps in testing.

## Notes

This README should be updated with any changes to the function's logic, dependencies, or configuration to ensure accurate and up-to-date documentation.