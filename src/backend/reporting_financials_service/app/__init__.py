"""
Package initializer for the Reporting Financials Service application package.

Requirements addressed:
- API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
  Develop and deploy the FastAPI-based RESTful API to facilitate secure and efficient data
  ingestion and retrieval from the PostgreSQL database.

This package initializer is intentionally free of import-time side effects. The FastAPI
application is constructed by ``main.create_app`` (the container entrypoint runs
``uvicorn main:app``). Because importing any ``app.*`` submodule (models, routers) executes
this module first, it must remain importable without building a second application or
requiring environment variables. The previous version built a duplicate FastAPI app,
created a database engine from ``Config.DATABASE_URL`` (an AttributeError under Pydantic v1,
which prevented the service from starting), and ran ``create_all`` on startup; all of that
is owned by ``main.create_app`` and has been removed here.
"""
