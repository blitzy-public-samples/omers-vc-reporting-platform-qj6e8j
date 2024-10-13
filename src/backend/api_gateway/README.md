# API Gateway

This README provides an overview and instructions for setting up and running the API Gateway component of the backend platform. The API Gateway is responsible for handling incoming HTTP requests, routing them to appropriate services, and managing authentication and authorization.

## Overview

The API Gateway is built using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints. It serves as the entry point for all client requests to the backend services, providing a unified interface for data ingestion and retrieval from the PostgreSQL database.

## Features

- RESTful API endpoints for data ingestion and retrieval
- OAuth 2.0 authentication integration with Azure Active Directory
- Role-Based Access Control (RBAC) for authorization
- Automatic API documentation with Swagger/OpenAPI
- Integration with other backend services (Metrics Input, Reporting Financials, Reporting Metrics)

## Requirements

- Python 3.8+
- FastAPI 0.70.0
- Pydantic 1.8.2
- PyJWT 2.3.0
- pytest 6.2.4 (for testing)
- httpx 0.18.2 (for testing)

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

2. Edit the `.env` file with your specific configuration:
   ```plaintext
   DATABASE_URL=postgresql://user:password@localhost/dbname
   AZURE_AD_TENANT_ID=your_tenant_id
   AZURE_AD_CLIENT_ID=your_client_id
   AZURE_AD_CLIENT_SECRET=your_client_secret
   ```

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

- All API endpoints are secured with OAuth 2.0 authentication.
- HTTPS is enforced for all communications.
- Role-Based Access Control (RBAC) is implemented to restrict access based on user roles.
- Input validation is performed on all incoming data to prevent injection attacks.

## Troubleshooting

If you encounter any issues, please check the following:

1. Ensure all environment variables are correctly set in the `.env` file.
2. Verify that the PostgreSQL database is accessible and the connection string is correct.
3. Check the Azure AD configuration for authentication issues.

For further assistance, please contact the development team.

## Contributing

Please refer to the project's contribution guidelines for information on how to contribute to this component.

## License

This project is licensed under [LICENSE_TYPE]. See the LICENSE file for details.