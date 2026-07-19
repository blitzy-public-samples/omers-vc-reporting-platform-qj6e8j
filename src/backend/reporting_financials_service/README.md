# Reporting Financials Service

## Overview

The Reporting Financials Service is a critical component of the OMERS Ventures backend platform, responsible for managing and retrieving currency-adjusted financial metrics. This service provides a RESTful API built with FastAPI to facilitate secure and efficient data retrieval from the PostgreSQL database.

## Features

- Retrieval of currency-adjusted financial metrics
- Support for multiple currencies (Local, USD, CAD)
- CORS hardening: an explicit, non-wildcard origin allow-list (CWE-942)
- Scalable and performant API design

## Requirements

Versions below reflect this service's pinned `requirements.txt` and its container base image (`python:3.10-slim`).

- Python 3.10 (container base `python:3.10-slim`)
- FastAPI 0.125.0
- SQLAlchemy 1.4.22
- Pydantic 1.10.13 (v1 line — `BaseSettings`)
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
   JWT_SECRET_KEY=<required - at least 32 characters>
   CORS_ORIGINS=http://localhost:3000
   ```

   **Required environment variables (security):**
   - `JWT_SECRET_KEY`: **required**, supplied from the environment (no built-in default) and must be **at least 32 characters**. The service fails to start if it is missing or shorter than 32 characters.
   - `CORS_ORIGINS`: comma-separated list of explicitly allowed browser origins; **must not be `*`**. Declare the real origins for each environment before deploying to a browser-facing environment (example: `CORS_ORIGINS=http://localhost:3000`).
   - `DATABASE_URL`: **required** PostgreSQL connection string; it is typed as a Pydantic `PostgresDsn`, so it must be a valid `postgresql://user:pass@host:port/db` URL.

5. Run the application. Because the service uses absolute `src.backend.*` imports, start it from the **repository root** (not the service directory) so those imports resolve:
   ```bash
   PYTHONPATH=. uvicorn src.backend.reporting_financials_service.main:app --reload
   ```
   The application imports and starts cleanly: `app/routers/financials.py` reads `config.DATABASE_URL` from the settings instance (the earlier class-attribute configuration-import defect has been resolved).

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

The service's routes currently declare no authentication dependency (they use only a database-session dependency); access control is expected to be provided by the API gateway / network boundary in front of the service. A JWT signing key (`JWT_SECRET_KEY`) is required as configuration, but Azure Active Directory integration and role-based access control are **not** implemented here and are documented follow-ups (see the root [`SECURITY.md`](../../../SECURITY.md)).

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