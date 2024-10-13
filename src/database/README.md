# Database Setup and Management Guide

This README provides an overview and instructions for setting up and managing the database components of the financial reporting metrics platform. It includes details on the database schema, migration processes, and seeding procedures to ensure a consistent and reliable database environment.

## Table of Contents

1. [Overview](#overview)
2. [Database Schema](#database-schema)
3. [Setup Instructions](#setup-instructions)
4. [Migration Process](#migration-process)
5. [Seeding Data](#seeding-data)
6. [Maintenance and Best Practices](#maintenance-and-best-practices)

## Overview

The financial reporting metrics platform utilizes PostgreSQL 13 as its primary database management system. The database is structured to efficiently store and manage financial data from portfolio companies, supporting the core functionalities of data ingestion, transformation, and reporting.

## Database Schema

The database consists of four main tables:

1. **Companies**: Stores information about portfolio companies.
2. **Metrics Input**: Contains raw financial metrics submitted by companies.
3. **Quarterly Reporting Financials**: Holds currency-adjusted financial metrics.
4. **Quarterly Reporting Metrics**: Stores calculated derivative financial metrics.

For detailed schema information, refer to `src/database/schemas/create_tables.sql`.

## Setup Instructions

1. Ensure PostgreSQL 13 is installed and running on your system or Azure Database for PostgreSQL is provisioned.
2. Create a new database for the project:
   ```bash
   createdb financial_reporting_metrics
   ```
3. Set up the database connection in the project's configuration file (usually found in `src/backend/config.py` or `.env` file).

## Migration Process

We use Alembic for database migrations to manage schema changes over time.

1. To create a new migration:
   ```bash
   alembic revision -m "description of the change"
   ```
2. To apply migrations:
   ```bash
   alembic upgrade head
   ```
3. To revert migrations:
   ```bash
   alembic downgrade -1
   ```

For more details on the migration setup, refer to `src/database/migrations/env.py` and `src/database/migrations/alembic.ini`.

## Seeding Data

Initial data seeding is crucial for testing and development. To seed the database:

1. Ensure your database is up-to-date with migrations.
2. Run the seeding script:
   ```bash
   python src/database/seeds/seed_data.py
   ```

The seeding data is defined in `src/database/seeds/seed_data.sql`.

## Maintenance and Best Practices

1. **Regular Backups**: Configure automated backups in Azure Database for PostgreSQL.
2. **Performance Monitoring**: Use Azure Monitor to track database performance metrics.
3. **Index Optimization**: Regularly review and optimize indexes based on query patterns.
4. **Data Validation**: Implement strict data validation rules in the API layer and database constraints.

For any issues or questions regarding the database setup, please contact the database administration team.

---

This README addresses the requirement "Database Setup and Configuration" as specified in the Technical Requirements/Feature 1 section of the project documentation. It provides guidance on establishing and configuring the PostgreSQL database, including schema creation, migrations, and seeding procedures.