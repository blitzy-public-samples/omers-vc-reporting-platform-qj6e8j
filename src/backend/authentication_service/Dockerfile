# Use a base image with Python 3.8 or higher
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies specified in requirements.txt using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables necessary for the application
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV APP_MODULE=main:app

# Expose the port that the FastAPI application will run on
EXPOSE 8000

# Define the command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Comments for requirements addressed and their location in the documentation
# This Dockerfile addresses the following requirement:
# Requirement: Authentication and Authorization Implementation
# Location: Technical Requirements/Feature 4: Authentication and Authorization Implementation
# Description: This Dockerfile sets up the containerized environment for the Authentication Service,
# which is responsible for implementing secure authentication and authorization mechanisms to control
# access to the backend platform and its resources.

# Additional comments for a junior developer:
# - The base image python:3.8-slim is used to ensure a minimal image size while providing Python 3.8+.
# - We set the working directory to /app to keep our application code organized within the container.
# - Dependencies are installed first (before copying the app code) to leverage Docker's layer caching.
# - Environment variables are set to optimize Python's behavior in a containerized environment.
# - The application is exposed on port 8000, which should match the port in your FastAPI configuration.
# - Uvicorn is used as the ASGI server to run the FastAPI application.

# Note on external dependencies (versions are specified in requirements.txt):
# - python-dotenv: For loading environment variables from a .env file.
# - PyJWT: For encoding and decoding JSON Web Tokens.
# - FastAPI: The web framework used for creating the API.
# - Uvicorn: The ASGI server used to run the FastAPI application.