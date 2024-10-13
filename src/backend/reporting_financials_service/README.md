# Reporting Financials Service

## Overview

The Reporting Financials Service is a critical component of the OMERS Ventures backend platform, responsible for managing and retrieving currency-adjusted financial metrics. This service provides a RESTful API built with FastAPI to facilitate secure and efficient data retrieval from the PostgreSQL database.

## Features

- Retrieval of currency-adjusted financial metrics
- Support for multiple currencies (Local, USD, CAD)
- Integration with Azure Active Directory for authentication
- Role-Based Access Control (RBAC) for authorization
- Scalable and performant API design

## Requirements

- Python 3.8+
- FastAPI 0.68.0
- SQLAlchemy 1.4.22
- Pydantic 1.8.2
- Azure SDK for Python
- Docker (for containerization)

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd src/backend/reporting_financials_service
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Copy the `.env.sample` file to `.env` and fill in the required values:
   ```bash
   cp .env.sample .env
   ```
   Edit the `.env` file with your specific configuration:
   ```plaintext
   DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>
   API_KEY=<your_api_key_here>
   LOG_LEVEL=INFO
   ```

5. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t reporting-financials-service .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 --env-file .env reporting-financials-service
   ```

## API Endpoints

- `GET /financials/`: Retrieve a list of financial reports
- `GET /financials/{company_id}`: Retrieve financial reports for a specific company
- `GET /financials/{company_id}/{reporting_period}`: Retrieve a specific financial report

For detailed API documentation, visit `/docs` when the service is running.

## Authentication and Authorization

This service uses OAuth 2.0 with Azure Active Directory for authentication. Ensure you have the necessary Azure AD configurations set up and the correct permissions to access the API.

## Testing

Run the tests using pytest:

```bash
pytest
```

## Monitoring and Logging

The service integrates with Azure Monitor for performance tracking and log analysis. Logs are configured to be sent to Azure Log Analytics for centralized monitoring.

## Compliance and Security

- Data encryption at rest and in transit
- Adherence to GDPR and CCPA regulations
- Regular security audits and vulnerability assessments

## Contributing

Please refer to the main project's CONTRIBUTING.md file for guidelines on how to contribute to this service.

## License

This project is licensed under the [LICENSE] - see the LICENSE file for details.

## Contact

For any queries or support, please contact the OMERS Ventures IT team.

---

This README addresses the API Development and Deployment requirement as specified in the Technical Requirements/Feature 2 section of the project documentation. It provides comprehensive setup instructions and details about the Reporting Financials Service within the backend platform.