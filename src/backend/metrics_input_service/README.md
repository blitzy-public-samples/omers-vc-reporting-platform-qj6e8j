# Metrics Input Service

## Overview

The Metrics Input Service is a crucial component of the OMERS Ventures backend platform, responsible for managing the ingestion and storage of financial metrics data from portfolio companies. This service provides a RESTful API for submitting and retrieving metrics data, ensuring data integrity and facilitating the transformation process for reporting purposes.

## Features

- Secure API endpoints for submitting and retrieving financial metrics data
- Data validation and integrity checks
- Integration with Azure Functions for automated data transformation
- Role-Based Access Control (RBAC) for secure data access
- Scalable architecture using Azure App Service and Azure Database for PostgreSQL

## Requirements

- Python 3.8+
- FastAPI 0.68.0
- SQLAlchemy 1.4.22
- Pydantic 1.8.2
- pytest 6.2.4
- httpx 0.18.2

## Setup Instructions

1. Ensure Python 3.8+ is installed on your system.
2. Clone the repository and navigate to the `src/backend/metrics_input_service` directory.
3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Copy the `.env.sample` file to `.env` and configure the environment variables:
   ```bash
   cp .env.sample .env
   ```
   Edit the `.env` file to set the appropriate values for your development environment.
6. Run the FastAPI application using Uvicorn:
   ```bash
   uvicorn main:create_app --host 0.0.0.0 --port 8000 --reload
   ```
7. Run the test suite to ensure everything is set up correctly:
   ```bash
   pytest
   ```

## Usage Instructions

1. Access the API documentation at `http://localhost:8000/docs` to view available endpoints and their specifications.
2. Use the POST `/metrics/` endpoint to submit new financial metrics data. Ensure you have the necessary authentication token.
3. Use the GET `/metrics/` endpoint to retrieve financial metrics data based on query parameters such as company ID and reporting period.

## Deployment Instructions

1. Build the Docker image using the provided Dockerfile:
   ```bash
   docker build -t metrics-input-service .
   ```
2. Push the Docker image to your preferred container registry (e.g., Azure Container Registry).
3. Deploy the Docker container to your chosen environment (e.g., Azure App Service, Azure Kubernetes Service).
4. Ensure the following environment variables are correctly configured in your deployment environment:
   - `DATABASE_URL`: Connection string for the PostgreSQL database
   - `AZURE_FUNCTION_URL`: URL of the Azure Function for data transformation
   - `AZURE_AD_TENANT_ID`: Azure Active Directory tenant ID for authentication
   - `AZURE_AD_CLIENT_ID`: Client ID for the Metrics Input Service application in Azure AD
   - `AZURE_AD_CLIENT_SECRET`: Client secret for the Metrics Input Service application in Azure AD

## API Endpoints

- `POST /metrics/`: Submit new financial metrics data
- `GET /metrics/`: Retrieve financial metrics data based on query parameters

For detailed API documentation, refer to the Swagger UI available at `/docs` when running the service.

## Security Considerations

- All API endpoints are secured using OAuth 2.0 authentication.
- Role-Based Access Control (RBAC) is implemented to restrict data access based on user roles.
- Sensitive data is encrypted at rest and in transit.
- Input validation is performed on all submitted data to prevent injection attacks.

## Troubleshooting

- If you encounter database connection issues, ensure the `DATABASE_URL` environment variable is correctly set and the PostgreSQL server is accessible.
- For authentication problems, verify that the Azure AD configuration is correct and that you're using a valid OAuth token.
- Check the application logs for detailed error messages and stack traces.

## Contributing

Please refer to the main project repository for contribution guidelines and coding standards.

## License

This project is proprietary and confidential. Unauthorized copying, transferring, or reproduction of the contents of this file, via any medium, is strictly prohibited.

## Contact

For any questions or support, please contact the OMERS Ventures development team.

---

This README addresses the requirement for "Documentation and Knowledge Management" as specified in the Technical Requirements/Feature 14, providing an updated setup guide for developers to facilitate onboarding and local development.