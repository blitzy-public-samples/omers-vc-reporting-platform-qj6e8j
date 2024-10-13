# Authentication Service

## Overview

The Authentication Service is a critical component of the backend platform, responsible for implementing secure authentication and authorization mechanisms to control access to the backend platform and its resources. This service is designed to work seamlessly with Azure Active Directory (AAD) and implements OAuth 2.0 for robust token-based authentication.

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
   - `SECRET_KEY`: A secret key used for JWT token signing. Must be kept secret.
   - `DATABASE_URL`: Connection string for the PostgreSQL database.
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

5. Access the FastAPI application through the specified host and port (default: http://localhost:8000).

## Usage

### Token Generation

Use the `/token` endpoint to generate JWT tokens for authenticated users:

```http
POST /token
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "securepassword"
}
```

### Token Validation

Secure API endpoints by validating tokens using the `/validate` endpoint:

```http
GET /validate
Authorization: Bearer <your_jwt_token>
```

### API Documentation

Refer to the Swagger documentation at `/docs` for detailed API usage and endpoint specifications.

## Configuration

The service uses environment variables for configuration. Key variables include:

- `SECRET_KEY`: Used for JWT token signing. Must be kept secret.
- `DATABASE_URL`: Connection string for the PostgreSQL database.
- `TOKEN_EXPIRATION`: JWT token expiration time in minutes.
- `DEBUG`: Set to 'True' for development environments, 'False' for production.

## Dependencies

This service relies on the following key dependencies:

- `python-dotenv (0.19.2)`: For loading environment variables from a .env file.
- `PyJWT (2.3.0)`: For encoding and decoding JSON Web Tokens.
- `FastAPI (0.68.1)`: The web framework used for creating the API.
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