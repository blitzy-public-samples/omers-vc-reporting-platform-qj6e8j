"""
Package initializer for the Metrics Input Service application package.

Requirements addressed:
- API Services (Technical Requirements/Feature 2: API Development and Deployment):
  Develop the API using the FastAPI framework to ensure high performance and scalability.

This package initializer is intentionally free of import-time side effects. The
FastAPI application is constructed by ``main.create_app`` (the container entrypoint
runs ``uvicorn main:app``). Because importing any ``app.*`` submodule (models,
routers) executes this module first, it must remain importable without building the
application or requiring environment variables.
"""
