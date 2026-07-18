"""
Database engine and session wiring for the Reporting Metrics Service.

Requirements addressed:
- API Development and Deployment (Technical Requirements/Feature 2: API Development and Deployment)
  Provide the SQLAlchemy engine, session factory, and request-scoped session dependency used by
  the reporting-metrics API routers to read from and write to the PostgreSQL database.

The routers import ``get_db`` from this module (``from ...app.database import get_db``). The
module previously did not exist, which raised ModuleNotFoundError at import and prevented the
service from starting. The engine binds to ``settings.DATABASE_URL`` (validated as a
``postgresql://`` DSN in config.Settings); the PostgreSQL DBAPI driver (psycopg2) is provided by
the service's requirements.txt.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.backend.reporting_metrics_service.config import settings

# SQLAlchemy engine bound to the configured PostgreSQL DSN. create_engine is lazy about
# connecting but resolves the psycopg2 dialect at construction, so the driver must be installed.
engine = create_engine(settings.DATABASE_URL)

# Session factory. autocommit/autoflush disabled to match the explicit commit pattern used by
# the routers.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Yield a request-scoped SQLAlchemy session and ensure it is closed after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
