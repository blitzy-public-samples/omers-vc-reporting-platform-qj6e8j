# Authentication Service

## Overview

The Authentication Service is a component of the backend platform responsible for issuing and validating JSON Web Tokens (JWT). It implements JWT (HS256) token-based authentication and extracts bearer tokens using FastAPI's `OAuth2PasswordBearer` scheme. **Note:** the login handler's credential check is currently a placeholder for demonstration, and Azure Active Directory integration is not yet wired; a full authentication implementation (replacing the placeholder check and wiring a real identity source) is a documented follow-up (see the root [`SECURITY.md`](../../../SECURITY.md)).

## Setup Instructions

1. Clone the repository and navigate to the authentication service directory:
   ```bash
   git clone <repository-url>
   cd src/backend/authentication_service
   ```

2. Copy the `.env.sample` file to `.env` and fill in the necessary environment variables:
   ```bash
   cp .env.sample .env
   ```
   Edit the `.env` file and provide values for:
   - `SECRET_KEY`: A secret key used for JWT token signing. Required (no default); must be at least 32 characters. Must be kept secret.
   - `DATABASE_URL`: Connection string for the PostgreSQL database. Required (no default).
   - `CORS_ORIGINS`: Comma-separated list of explicit allowed origins (no wildcard `*`); defaults to `http://localhost:3000` if unset.
   - `TOKEN_EXPIRATION`: JWT token expiration time in minutes.
   - `DEBUG`: Set to 'True' for development environments, 'False' for production.

3. Build the Docker image using the provided Dockerfile:
   ```bash
   docker build -t authentication-service .
   ```

4. Run the Docker container, ensuring the environment variables are correctly set:
   ```bash
   docker run -p 8000:8000 --env-file .env authentication-service
   ```

   **Note:** The container image runs as a dedicated non-root user (uid 1000) on the `python:3.10-slim` base image.

   > **Known limitation:** a default `docker run` of this image currently exits with `ModuleNotFoundError: No module named 'src'` because the image is built with the service directory as the build context (`COPY . .`) while the application uses absolute `src.backend.*` imports. The in-scope container hardening (non-root uid 1000, supported base image) is in place; packaging the namespace correctly for the build context is a pre-existing, out-of-scope defect and a documented follow-up (see the root [`SECURITY.md`](../../../SECURITY.md)).

5. Access the FastAPI application through the specified host and port (default: http://localhost:8000).

## Usage

### Token Generation

Use the `POST /token` endpoint to obtain a JWT. The endpoint currently accepts `username` and `password` as **query parameters** (its credential check is a placeholder for demonstration only — see the note in the Overview):

```http
POST /token?username=<username>&password=<password>
```

On success it returns a JSON body of the form `{"access_token": "<jwt>", "token_type": "bearer"}`.

### Accessing a Protected Route

The `GET /protected` endpoint requires a valid bearer token; an invalid or expired token returns `401 Unauthorized`:

```http
GET /protected
Authorization: Bearer <your_jwt_token>
```

### API Documentation

Refer to the Swagger documentation at `/docs` for detailed API usage and endpoint specifications.

## Configuration

The service uses environment variables for configuration. Key variables include:

- `SECRET_KEY`: Used for JWT token signing. **Required** (no default) and must be **at least 32 characters** long, or the service fails to start. Must be kept secret.
- `DATABASE_URL`: Connection string for the PostgreSQL database. **Required** (no default).
- `CORS_ORIGINS`: Comma-separated list of explicit allowed origins for CORS (for example, `https://app.example.com`). Must **not** be a wildcard (`*`); defaults to `http://localhost:3000` if unset.
- `TOKEN_EXPIRATION`: JWT token expiration time in minutes.
- `DEBUG`: Set to 'True' for development environments, 'False' for production.

## Dependencies

This service targets **Python 3.10+** (matching the service container's `python:3.10-slim` base image) and relies on the following key dependencies:

- `python-dotenv (1.2.2)`: For loading environment variables from a .env file.
- `PyJWT (2.13.0)`: For encoding and decoding JSON Web Tokens.
- `FastAPI (0.125.0)`: The web framework used for creating the API.
- `Uvicorn (0.15.0)`: ASGI server for running the FastAPI application.
- `pytest (6.2.5)`: Testing framework for writing and running test cases.

For a complete list of dependencies, refer to the `requirements.txt` file.

## Testing

Run tests using pytest to ensure the functionality of token generation and validation:

```bash
pytest
```

Ensure all tests pass before deploying the service to production.

## Notes

This README provides essential information for setting up and using the Authentication Service. Ensure all dependencies are installed and environment variables are correctly configured for optimal operation. The service is designed to address the Authentication and Authorization Implementation requirement as specified in the Technical Requirements/Feature 4 of the project documentation.

For any issues or further information, please contact the development team.