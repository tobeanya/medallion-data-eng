# Medallion Data Engineering

A production-style lakehouse project for mastering Medallion Architecture at a Senior Data Engineer level.

## Business scenario

Build a Customer Analytics Lakehouse that ingests customers, products, transactions, and event data and turns them into trusted datasets for revenue reporting, retention analysis, customer health, product analytics, and dashboards.

## Architecture

Source systems → Bronze → Silver → Gold → BI / ML / APIs

### Bronze
Raw, append-oriented ingestion with source fidelity, ingestion metadata, schema capture, replayability, and quarantine.

### Silver
Validated, typed, deduplicated, conformed data with CDC handling, SCD Type 2, referential integrity, late-arriving data handling, and data-quality enforcement.

### Gold
Business-ready dimensional and aggregate models including:
- dim_customer
- dim_product
- fact_transactions
- customer_360
- monthly_revenue
- retention_cohorts
- customer_health

## Target stack

- Python
- PySpark
- Delta Lake
- Databricks
- dbt
- Dagster
- Great Expectations or Soda
- Terraform
- GitHub Actions

See `docs/two_week_curriculum.md` for the full learning plan.
