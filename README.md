# Data Engineering Portfolio

One repository with separate projects for data engineering, modeling, and pipeline operations. Each project has its own domain folder and design documents; shared repository files stay at the root.

## Projects

### Customer Analytics Lakehouse
Path: [`projects/customer-analytics-lakehouse/`](projects/customer-analytics-lakehouse/)

A medallion-architecture learning project for customer, product, transaction, and event data. The folder contains its architecture notes, runbook, and study curriculum.

### Energy Planning Data Platform
Path: [`projects/energy-planning-dbt-platform/`](projects/energy-planning-dbt-platform/)

A dbt-centered project design for synthetic grid-planning data. It maps prior pipeline experience in reliability analysis, reconciliation, forecasting, battery optimization, GCP ETL, Spark, and Dagster into a concrete MVP. Its current contents are the MVP and architecture design; implementation and benchmark results will be added as they are built and measured.

## Repository conventions

- Use synthetic or public sample data. Do not commit employer data, code, schemas, or confidential business logic.
- Keep each project's setup, models, tests, and documentation inside its folder unless a dependency or standard is deliberately shared.
- Keep performance claims tied to reproducible measurements from the project that produced them.
