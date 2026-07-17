# API Gateway

This README provides an overview and instructions for setting up and running the API Gateway component of the backend platform. The API Gateway is responsible for handling incoming HTTP requests, routing them to appropriate services, and managing authentication and authorization.

## Overview

The API Gateway is built using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints. It serves as the entry point for all client requests to the backend services, providing a unified interface for data ingestion and retrieval from the PostgreSQL database.

## Features

- RESTful API endpoints for data ingestion and retrieval
- JWT (HS256) bearer-token validation for request authentication (delegated to the Authentication Service)
- Automatic API documentation with Swagger/OpenAPI
- Integration with other backend services (Metrics Input, Reporting Financials, Reporting Metrics)

> **Note:** Azure Active Directory integration and role-based access control (RBAC) are **not** implemented in this gateway; see [Security Considerations](#security-considerations).

## Requirements

Versions below reflect this service's pinned `requirements.txt` and its container base image (`python:3.9-slim`).

- Python 3.9 (container base `python:3.9-slim`)
- FastAPI 0.125.0
- Pydantic 1.10.13 (v1 line — `BaseSettings`)
- PyJWT 2.13.0
- pytest 6.2.4 (for testing)
- httpx 0.27.0 (for testing)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd src/backend/api_gateway
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

## Configuration

1. Copy the `.env.sample` file to `.env` and update the environment variables:
   ```bash
   cp .env.sample .env
   ```

2. Edit the `.env` file with your specific configuration (these are the variables `config.py` actually reads):
   ```plaintext
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   SECRET_KEY=<a-strong-secret-at-least-32-characters-long>
   API_KEY=<your-api-key>
   CORS_ALLOW_ORIGINS=http://localhost:3000
   ```

### Required environment variables

The following environment variables are read by `config.py`. The service **fails to start** if a required variable is missing:

- `DATABASE_URL` — **required** (no default); PostgreSQL connection string.
- `SECRET_KEY` — **required** (no default), **minimum 32 characters** (the service fails to start if it is shorter); used for JWT signing.
- `API_KEY` — **required** (no default); API key value loaded into service configuration.
- `CORS_ALLOW_ORIGINS` — comma-separated list of **explicit allowed origins** for CORS (e.g. `http://localhost:3000,https://app.omersventures.com`); **must NOT be a wildcard `*`**. Defaults to `http://localhost:3000` if unset. (Variable name is `CORS_ALLOW_ORIGINS`, matching `.env.sample`.)

## Running the API

To start the API Gateway:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`. You can access the Swagger documentation at `http://localhost:8000/docs`.

## Testing

To run the tests:

```bash
pytest
```

## API Endpoints

- `/input/`: POST and GET endpoints for metrics input data
- `/reporting/`: GET endpoint for quarterly reporting financials
- `/metrics/`: GET endpoint for quarterly reporting metrics
- `/company/`: POST endpoint for creating or updating company records

For detailed API documentation, refer to the Swagger UI at `/docs` when the application is running.

## Docker

A Dockerfile is provided for containerization. To build and run the Docker container:

```bash
docker build -t api-gateway .
docker run -p 8000:8000 api-gateway
```

## Deployment

The API Gateway is designed to be deployed on Azure App Service. Refer to the Azure deployment documentation for detailed instructions on deploying FastAPI applications to Azure App Service.

## Security Considerations

- API requests are authenticated with JWT (HS256) bearer tokens; token validation is delegated to the Authentication Service. Azure Active Directory integration and role-based access control (RBAC) are **not** implemented here and are documented follow-ups (see the root [`SECURITY.md`](../../../SECURITY.md)).
- HTTPS termination is expected to be provided by the Azure App Service / ingress layer in front of the gateway; it is not enforced in application code.
- CORS is restricted to an explicit, non-wildcard origin allow-list (`CORS_ALLOW_ORIGINS`; CWE-942).
- Input validation is performed via the API's Pydantic request models.

## Troubleshooting

If you encounter any issues, please check the following:

1. Ensure all required environment variables (`DATABASE_URL`, `SECRET_KEY`, `API_KEY`) are correctly set in the `.env` file; the service fails closed if any is missing or if `SECRET_KEY` is shorter than 32 characters.
2. Verify that the PostgreSQL database is accessible and the connection string is correct.
3. For authentication issues, verify the bearer token is valid and unexpired and that `SECRET_KEY` is consistent with the Authentication Service that issued the token.

For further assistance, please contact the development team.

## Contributing

Please refer to the project's contribution guidelines for information on how to contribute to this component.

## License

This project is licensed under [LICENSE_TYPE]. See the LICENSE file for details.