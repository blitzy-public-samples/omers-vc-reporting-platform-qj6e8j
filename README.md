# OMERS Ventures Backend Platform

## Overview

This backend platform is designed to manage financial reporting metrics for OMERS Ventures' portfolio companies. It includes services for data ingestion, transformation, and retrieval, leveraging Azure's cloud infrastructure for scalability and security.

## Components

- **Authentication Service:** Manages user authentication and authorization.
- **API Gateway:** Centralized entry point for API requests, routing them to appropriate services.
- **Metrics Input Service:** Handles the ingestion and management of financial metrics data.
- **Reporting Financials Service:** Provides access to currency-adjusted financial metrics.
- **Reporting Metrics Service:** Serves derived financial metrics for analysis.
- **Data Transformation:** Automates the calculation of derivative metrics using Azure Functions.
- **Infrastructure:** Defined using Terraform for consistent and repeatable deployments.

## Setup Instructions

1. Clone the repository to your local machine.
2. Follow the setup instructions in each service's README file to configure and run the individual components:
   - [Authentication Service README](src/backend/authentication_service/README.md)
   - [API Gateway README](src/backend/api_gateway/README.md)
   - [Metrics Input Service README](src/backend/metrics_input_service/README.md)
   - [Reporting Financials Service README](src/backend/reporting_financials_service/README.md)
   - [Reporting Metrics Service README](src/backend/reporting_metrics_service/README.md)
   - [Data Transformation README](src/functions/data_transformation/README.md)
3. Ensure all environment variables are correctly set as per the `.env.sample` files provided in each service directory.
4. Use Docker to containerize and deploy services where applicable, following the Dockerfile instructions in each service.

## Security Configuration

The following environment variables are **required** for secure operation and must be provided per service via that service's `.env` file (see each service's `.env.sample`). Missing or weak values now cause services to fail closed at startup.

### CORS Origins

Wildcard CORS (`*`) is no longer permitted; every service validates its origin allow-list and fails closed on `*`, an empty list, or a malformed origin. **The variable name and value format differ per service** (matching each service's `.env.sample` and `config.py`), so use the exact form listed below:

| Service | Variable | Format | Default |
|---------|----------|--------|---------|
| Authentication Service (`src/backend/authentication_service`) | `CORS_ORIGINS` | Comma-separated, e.g. `http://localhost:3000,https://app.omersventures.com` | `http://localhost:3000` |
| API Gateway (`src/backend/api_gateway`) | `CORS_ALLOW_ORIGINS` | Comma-separated | `http://localhost:3000` (the code binds this name to match `.env.sample`; the previous `CORS_ORIGINS` mismatch was corrected) |
| Reporting Financials Service (`src/backend/reporting_financials_service`) | `CORS_ORIGINS` | Comma-separated | `http://localhost:3000` |
| Metrics Input Service (`src/backend/metrics_input_service`) | `CORS_ORIGINS` | **JSON array**, e.g. `["https://app.example.com"]` | `["http://localhost:3000","https://localhost:3000"]` |
| Reporting Metrics Service (`src/backend/reporting_metrics_service`) | `BACKEND_CORS_ORIGINS` | **JSON array** | `["http://localhost:3000","https://localhost:3000","http://localhost","https://localhost"]` |

All five services ship a safe non-wildcard default, so `CORS`/`BACKEND_CORS_ORIGINS` is optional for local development but must be set to the real front-end origins before deploying to any browser-facing environment.

### Secrets

Signing keys and database URLs are required from the environment (no fallback defaults; a minimum length is enforced where noted):

- **Authentication Service** (`src/backend/authentication_service`): `SECRET_KEY` (required, **minimum 32 characters**), `DATABASE_URL` (required).
- **API Gateway** (`src/backend/api_gateway`): `SECRET_KEY` (required, **minimum 32 characters**), `DATABASE_URL` (required), `API_KEY` (required).
- **Reporting Financials Service** (`src/backend/reporting_financials_service`): `JWT_SECRET_KEY` (required, **minimum 32 characters** — no `"your-secret-key"` default), `DATABASE_URL` (required, must be a `postgresql://` DSN).
- **Reporting Metrics Service** (`src/backend/reporting_metrics_service`): `SECRET_KEY` (required, **minimum 32 characters** — no `"your-secret-key-here"` default), `DATABASE_URL` (required, must be a `postgresql://` DSN — no credential-bearing localhost default).
- **Metrics Input Service** (`src/backend/metrics_input_service`): `DATABASE_URL` (required), `API_KEY` (required), `LOG_LEVEL` (required). This service defines **no** JWT/signing-key setting and performs no JWT handling of its own.

Signing keys must be strong, unique, and provided via the environment. Services will raise and fail to start if a required secret is absent or, where a minimum is enforced, shorter than 32 characters.

### Container Runtime

All service containers run as a **dedicated non-root user**. The Authentication Service and Reporting Metrics Service Dockerfiles were hardened to add a non-root `USER` and to advance off the end-of-life `python:3.8-slim` base image. No action is required from operators beyond building the updated images.

For the full security policy, disclosure process, and remediation summary, see [`SECURITY.md`](SECURITY.md).

## Usage Instructions

- Refer to the API documentation generated by FastAPI for details on available endpoints and their usage.
- Use the Swagger UI available at `/docs` for interactive API exploration and testing.
- Ensure authentication is configured correctly to access secured endpoints.

## Deployment Instructions

1. Use the [infrastructure README](infrastructure/README.md) to set up the necessary Azure resources using Terraform.
2. Deploy each service using the provided Dockerfiles and ensure they are correctly configured to communicate with each other.
3. Monitor the deployment using Azure Monitor and set up alerts for any anomalies.

**Note:** The PostgreSQL administrator password is no longer stored in Terraform source; it must be supplied at apply time via the sensitive Terraform variable `postgresql_admin_password` (for example, as a pipeline secret). This is a one-time deployment-coordination step; see the [infrastructure README](infrastructure/README.md) for operational detail.

## Notes

This README serves as the central documentation hub for the backend platform. Ensure all related service READMEs are kept up-to-date to reflect any changes in setup or usage instructions.

## Requirements Addressed

This README addresses the following requirement:

- **Documentation and Knowledge Management**
  - Location: Technical Requirements/Feature 14: Documentation and Knowledge Management
  - Description: Create and maintain comprehensive documentation to support the development, deployment, and maintenance of the backend platform.

By providing an overview of the project, setup instructions, and references to key components and services, this README fulfills the requirement for comprehensive documentation to support the development, deployment, and maintenance of the backend platform.