# Reporting Metrics Service

This README provides an overview and instructions for the Reporting Metrics Service, detailing how to set up, configure, and run the service, as well as how to interact with its API endpoints.

## Overview

The Reporting Metrics Service is a crucial component of the OMERS Ventures backend platform, responsible for managing and providing access to derived financial metrics for portfolio companies. This service calculates and stores various financial metrics based on the input data and makes them available through a RESTful API.

## Features

- Retrieval of derived financial metrics for portfolio companies
- Calculation of metrics such as ARR, recurring revenue percentage, and various growth rates
- Integration with the PostgreSQL database for data storage and retrieval
- Secure API endpoints with OAuth 2.0 authentication
- Scalable FastAPI-based architecture

## Requirements

- Python 3.8+
- FastAPI 0.68.0
- SQLAlchemy 1.4.22
- pytest 6.2.4 (for running tests)
- Other dependencies as listed in `requirements.txt`

## Setup Instructions

1. Clone the repository to your local machine:
   ```bash
   git clone <repository_url>
   ```

2. Navigate to the `src/backend/reporting_metrics_service` directory:
   ```bash
   cd src/backend/reporting_metrics_service
   ```

3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the environment variables:
   - Copy the `.env.sample` file to `.env`
   - Edit the `.env` file and fill in the necessary configuration values

6. Run the FastAPI application:
   ```bash
   uvicorn main:app --reload
   ```

## Usage Instructions

To interact with the Reporting Metrics Service API:

1. Ensure that the API is running and accessible at the specified host and port.

2. Use the `/metrics` endpoint to retrieve reporting metrics data. For example:
   ```http
   GET /metrics?company_id=<company_id>&reporting_year=<year>&reporting_quarter=<quarter>
   ```

3. Authenticate using OAuth 2.0 to access secured endpoints. Include the bearer token in the Authorization header of your requests.

4. Refer to the Swagger documentation at `/docs` for detailed API usage, including available endpoints, request parameters, and response schemas.

## Configuration

The service uses environment variables for configuration. Key configuration options include:

- `ENVIRONMENT`: The current running environment (e.g., 'development', 'production')
- `DATABASE_URL`: The connection string for the PostgreSQL database
- `SECRET_KEY`: Secret key for JWT token generation
- `ALGORITHM`: The algorithm used for JWT token encoding/decoding

Refer to the `config.py` file for a complete list of configuration options.

## Testing

To run the test suite:

1. Ensure you're in the `src/backend/reporting_metrics_service` directory
2. Run the following command:
   ```bash
   pytest
   ```

## API Documentation

Detailed API documentation is available through Swagger UI. Once the service is running, you can access the documentation at:

```
http://<host>:<port>/docs
```

This interactive documentation allows you to explore and test the API endpoints directly from your browser.

## Troubleshooting

If you encounter any issues:

1. Check that all environment variables are correctly set
2. Ensure the database is accessible and properly configured
3. Verify that all dependencies are installed correctly
4. Check the application logs for any error messages

For further assistance, please contact the development team.

## Contributing

Please refer to the project's contribution guidelines for information on how to contribute to this service.

## License

This project is licensed under [LICENSE_TYPE]. See the LICENSE file for details.

---

This README addresses the requirement for comprehensive documentation as specified in the Technical Requirements/Feature 14: Documentation and Knowledge Management. It provides clear instructions for setting up, configuring, and using the Reporting Metrics Service, supporting the development, deployment, and maintenance of the backend platform.