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
ENV NAME World

# Run app.py when the container launches
# Comment: Using uvicorn to run the FastAPI application
CMD ["uvicorn", "main:create_app", "--host", "0.0.0.0", "--port", "8000"]

# Health check to ensure the application is running
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Label the image with metadata
LABEL maintainer="OMERS Ventures <tech@omersventures.com>"
LABEL version="1.0"
LABEL description="API Gateway for OMERS Ventures Financial Reporting Platform"

# Multi-stage build to reduce final image size
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
# Run as non-root user for better security (CWE-250 least privilege)
RUN adduser --disabled-password --gecos '' appuser

# Relocate pip --user packages into the non-root user's HOME so they stay
# reachable after dropping privileges (/root/.local is mode 700 and cannot be
# traversed by appuser, which prevented uvicorn from launching).
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local
COPY . .
ENV PATH=/home/appuser/.local/bin:$PATH

USER appuser

# Command to run the application
CMD ["uvicorn", "main:create_app", "--host", "0.0.0.0", "--port", "8000"]

# Note: Ensure all imported modules and dependencies are correctly installed and available in the requirements.txt file.
# Note: Verify that the main:create_app function exists and is correctly defined in the main.py file.
# Note: Ensure that all environment variables and configurations are correctly set up in the config.py file.
# Note: The health check endpoint /health should be implemented in the main.py file to return a healthy status.