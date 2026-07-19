# Metrics Input Service

## Overview

The Metrics Input Service is a crucial component of the OMERS Ventures backend platform, responsible for managing the ingestion and storage of financial metrics data from portfolio companies. This service provides a RESTful API for submitting and retrieving metrics data, ensuring data integrity and facilitating the transformation process for reporting purposes.

## Features

- RESTful API endpoints for submitting and retrieving financial metrics data
- Request-body validation via Pydantic schemas (integrity checks on submitted data)
- CORS hardening: an explicit, non-wildcard origin allow-list (CWE-942)
- Integration point for Azure Functions automated data transformation
- Runs as a non-root container user for least-privilege execution

> **Note on authentication:** the metrics routes in this service are **not** authenticated at the service level today (see [Security Considerations](#security-considerations)). Service-level authentication/authorization is a documented follow-up, not a delivered feature.

## Requirements

Versions below reflect this service's pinned `requirements.txt` and its container base image (`python:3.9-slim`).

- Python 3.9 (container base `python:3.9-slim`)
- FastAPI 0.125.0
- SQLAlchemy 1.4.22
- Pydantic 1.10.13 (v1 line — `BaseSettings`)
- pytest 6.2.4
- httpx 0.27.0

## Setup Instructions

1. Ensure Python 3.9 is installed on your system (the service ships on the `python:3.9-slim` base image).
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
6. Run the FastAPI application using Uvicorn. This service uses repository-root absolute imports (`src.backend.metrics_input_service...`), so run it **from the repository root** with the repository root on `PYTHONPATH` (`main.py` exposes the ASGI app instance as `app = create_app()`):
   ```bash
   # from the repository root
   PYTHONPATH=. uvicorn src.backend.metrics_input_service.main:app --host 0.0.0.0 --port 8000 --reload
   ```
7. Run the test suite (also **from the repository root**) to ensure everything is set up correctly:
   ```bash
   # from the repository root
   PYTHONPATH=. python -m pytest src/backend/metrics_input_service/tests
   ```

## Environment Variables

Configure these variables in your `.env` file (copy from `.env.sample`, per Setup step 5) or in the deployment environment. The service's `Settings` class (`config.py`) requires `DATABASE_URL`, `API_KEY`, and `LOG_LEVEL` — the service fails to start if any required variable is unset.

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL SQLAlchemy connection string. No default; the service fails to start if unset. |
| `API_KEY` | Yes | API key for authenticating with external services. No default. |
| `LOG_LEVEL` | Yes | Application logging level (e.g. `info`). No default. |
| `CORS_ORIGINS` | No | Explicit, non-wildcard list of browser origins allowed to call this API (CWE-942 CORS hardening). `config.py` supplies a safe localhost default (`http://localhost:3000,https://localhost:3000`), so it is optional. Override per environment using a **comma-separated list** of origins — the convention shared with the API gateway and reporting-financials services — e.g. `CORS_ORIGINS=https://app.example.com,https://admin.example.com`. A JSON array (e.g. `["https://app.example.com"]`) is also accepted. Never use `*`. |

The `Settings` class (`config.py`) defines exactly these four fields — `database_url`, `api_key`, `log_level` (all required), and `CORS_ORIGINS` (optional, with a safe default). It does **not** define a JWT signing key or any OAuth/RBAC setting; this service performs no JWT handling of its own.

The local development template is `.env.sample` — copy it to `.env` (see Setup step 5) and fill in real values per environment. Never commit real secrets to version control.

## Usage Instructions

1. Access the API documentation at `http://localhost:8000/docs` to view available endpoints and their specifications.
2. Use the POST `/api/v1/metrics/metrics/` endpoint to submit new financial metrics data.
3. Use the GET `/api/v1/metrics/metrics/` endpoint to retrieve financial metrics data based on query parameters such as company ID and reporting period.

> These routes are mounted under the `/api/v1/metrics` prefix (see `main.py`'s `include_router`) and the router defines `/metrics/`, so the full paths are `POST /api/v1/metrics/metrics/` and `GET /api/v1/metrics/metrics/`. A request to the bare `/metrics/` path returns 404.

## Deployment Instructions

1. Build the Docker image using the provided Dockerfile:
   ```bash
   docker build -t metrics-input-service .
   ```
2. Push the Docker image to your preferred container registry (e.g., Azure Container Registry).
3. Deploy the Docker container to your chosen environment (e.g., Azure App Service, Azure Kubernetes Service).
4. Ensure the environment variables consumed by this service's `Settings` class (`config.py`) are configured in your deployment environment:
   - `DATABASE_URL` (required): Connection string for the PostgreSQL database
   - `API_KEY` (required): API key for authenticating with external services
   - `LOG_LEVEL` (required): Application logging level
   - `CORS_ORIGINS` (optional): JSON array of allowed browser origins (see [Environment Variables](#environment-variables))

   Any `AZURE_*` values (for example an Azure Function URL or Azure AD identifiers) belong to the broader platform data-transformation integration and are **not** read by this service's `Settings` class; they are not required for the service to start and should be configured only where that integration is actually wired.

## API Endpoints

- `POST /api/v1/metrics/metrics/`: Submit new financial metrics data
- `GET /api/v1/metrics/metrics/`: Retrieve financial metrics data based on query parameters

These are the full mounted paths (the `/api/v1/metrics` router prefix plus the router's own `/metrics/` route). For detailed API documentation, refer to the Swagger UI available at `/docs` when running the service.

## Security Considerations

- **Service-level authentication is not enforced on the metrics routes today.** The routes in `app/routers/metrics.py` declare no authentication dependency; access control is expected to be provided by the API gateway / network boundary in front of this service. Adding service-level authentication and authorization (for example OAuth 2.0 and role-based access control) is a documented follow-up and is **not** implemented here — do not rely on this service to authenticate callers on its own.
- CORS is hardened with an explicit, non-wildcard origin allow-list (`CORS_ORIGINS`, validated in `config.py`; CWE-942). The wildcard `*` is rejected.
- Input validation is performed on submitted data via the Pydantic request schema (`MetricsInputSchema`), reducing malformed-input risk.
- The service container runs as a non-root user (`USER myuser` in the Dockerfile) for least-privilege execution (CWE-250).

## Troubleshooting

- If you encounter database connection issues, ensure the `DATABASE_URL` environment variable is correctly set and the PostgreSQL server is accessible.
- If browser requests are blocked by CORS, confirm the calling origin is listed in `CORS_ORIGINS` (a JSON array; the wildcard `*` is rejected by design).
- Check the application logs for detailed error messages and stack traces.

## Contributing

Please refer to the main project repository for contribution guidelines and coding standards.

## License

This project is proprietary and confidential. Unauthorized copying, transferring, or reproduction of the contents of this file, via any medium, is strictly prohibited.

## Contact

For any questions or support, please contact the OMERS Ventures development team.

---

This README addresses the requirement for "Documentation and Knowledge Management" as specified in the Technical Requirements/Feature 14, providing an updated setup guide for developers to facilitate onboarding and local development.