"""
Package initializer for the Reporting Metrics Service application package.

Requirements addressed:
- API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
  Develop the FastAPI-based RESTful API to facilitate secure and efficient data ingestion and
  retrieval from the PostgreSQL database.

This package initializer is intentionally free of import-time side effects. The FastAPI
application is constructed in ``main`` (the container entrypoint runs ``uvicorn main:app``).
The previous version imported ``main.app`` here (``from ...main import app``) while ``main``
imports ``app.routers`` — a circular import that crashed the service at startup — and it built
a second, redundant FastAPI application. Because importing any ``app.*`` submodule (models,
routers, database, schemas) executes this module first, it must remain importable without
building an application, importing ``main``, or requiring environment variables. All of that
now lives in ``main``.
"""
