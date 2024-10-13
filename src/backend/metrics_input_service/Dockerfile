# Use an official Python runtime as the base image
# This image is compatible with FastAPI and other dependencies
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port that the FastAPI application will run on
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Metadata
LABEL maintainer="OMERS Ventures"
LABEL version="1.0"
LABEL description="Dockerfile for the Metrics Input Service"

# Health check to ensure the application is running
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Additional security measures
RUN useradd -m myuser
USER myuser

# Comments for requirements addressed
# This Dockerfile addresses the following requirement:
# Requirement: Containerization
# Location: Technical Requirements/Feature 2: API Development and Deployment
# Description: Implement Docker containers for consistent deployment environments across development and production.

# The Dockerfile ensures a consistent environment for the Metrics Input Service,
# including all necessary dependencies and configurations. It uses a slim Python image
# to minimize container size while providing all required functionality.

# Note: Make sure to have a requirements.txt file in the same directory as this Dockerfile,
# containing all the necessary Python packages, including:
# sqlalchemy==1.4.22
# pydantic==1.8.2
# pytest==6.2.4
# httpx==0.18.2
# uvicorn (for running the FastAPI application)

# The Dockerfile copies all files from the current directory, ensuring that
# main.py, config.py, and the app directory with models and routers are included.

# The exposed port 8000 should match the port configured in your FastAPI application.

# The health check ensures the application is running and responsive.

# Environment variables are set to improve Python behavior in a containerized environment.

# A non-root user is created and used for improved security.