# Use the official Python 3.8 slim image as the base image
FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container at /app
COPY . .

# Expose the port that the FastAPI application will run on
EXPOSE 8000

# Define the command to run the FastAPI application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Add comments about requirements addressed and their location in the documentation
# Requirement: API Development and Deployment
# Location: Technical Requirements/Feature 2: API Development and Deployment
# Description: This Dockerfile implements Docker containers for consistent deployment environments across development and production.

# Add version comments for third-party imports
# FastAPI version: 0.68.0
# SQLAlchemy version: 1.4.22
# Pytest version: 6.2.4
# Uvicorn version: 0.15.0
# Pydantic version: 1.8.2
# Databases version: 0.5.2
# Asyncpg version: 0.24.0
# Python-dotenv version: 0.19.0
# Requests version: 2.26.0
# Alembic version: 1.7.3
# Psycopg2-binary version: 2.9.1
# Dependency injector version: 4.39.1
# Loguru version: 0.5.3
# Prometheus client version: 0.11.0
# Azure Identity version: 1.7.0
# Azure Key Vault version: 4.3.0
# Tenacity version: 8.0.1
# Gunicorn version: 20.1.0

# Note: Ensure that the application code includes a 'main.py' file with a FastAPI app instance named 'app'.