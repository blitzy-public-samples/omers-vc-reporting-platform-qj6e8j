# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# Comment: Using --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME ReportingFinancialsService

# Run main.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Health check to ensure the application is running
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Label the image with metadata
LABEL maintainer="OMERS Ventures DevOps Team <devops@omersventures.com>"
LABEL version="1.0"
LABEL description="Dockerfile for the Reporting Financials Service, responsible for containerizing the FastAPI application that manages and retrieves financial reports."

# Multi-stage build to reduce final image size
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Comments addressing requirements:
# This Dockerfile addresses the requirement for "API Development and Deployment" as specified in
# Technical Requirements/Feature 2: API Development and Deployment. It containerizes the FastAPI
# application, ensuring that it can be deployed consistently across different environments.

# The use of multi-stage builds and a non-root user enhances security and reduces the final image size,
# which are best practices for containerized applications in production environments.

# The HEALTHCHECK instruction ensures that the container's health can be monitored, which is crucial
# for maintaining high availability in a production setting.

# The LABEL instructions provide metadata about the image, which is useful for image management and
# documentation purposes in a production environment.