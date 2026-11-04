# Data Engineering Portfolio

One repository with separate projects for data engineering, modeling, and pipeline operations. Each project has its own domain folder; shared repository files stay at the root.

## Projects

### Customer Analytics Lakehouse
Path: [`projects/customer-analytics-lakehouse/`](projects/customer-analytics-lakehouse/)

A medallion-architecture learning project for customer, product, transaction, and event data. Its folder contains architecture notes, a runbook, and a study curriculum.

### Energy Planning Data Platform
Path: [`projects/energy-planning-dbt-platform/`](projects/energy-planning-dbt-platform/)

A dbt-centered project for synthetic grid-planning data, built around source contracts, reliability analysis, model reconciliation, load forecasting, battery optimization, GCP ETL, Spark, and Dagster. Its first working slice generates deterministic CSV/JSON source batches and a checksum manifest. The dbt models and orchestration are the next implementation stages.

## Repository conventions

- Use synthetic or public sample data. Do not commit employer data, code, schemas, or confidential business logic.
- Keep each project's setup, models, tests, and documentation inside its folder unless a dependency or standard is deliberately shared.
- Keep performance claims tied to reproducible measurements from the project that produced them.
