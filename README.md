# Data Engineering Portfolio

One repository with separate projects for data engineering, modeling, and pipeline operations. Each project has its own domain folder; shared repository files stay at the root.

## Projects

### Customer Analytics Lakehouse
Path: [`projects/customer-analytics-lakehouse/`](projects/customer-analytics-lakehouse/)

A medallion-architecture learning project for customer, product, transaction, and event data. Its folder contains architecture notes, a runbook, and a study curriculum.

### Energy Planning Data Platform
Path: [`projects/energy-planning-dbt-platform/`](projects/energy-planning-dbt-platform/)

A dbt project built from synthetic energy-planning sources. It includes source contracts, deterministic CSV/JSON generation, staging models, reliability, forecasting, battery, and reconciliation marts, plus data-quality tests. The local dbt build passes; Dagster orchestration is a later milestone.

## Repository conventions

- Use synthetic or public sample data. Do not commit employer data, code, schemas, or confidential business logic.
- Keep each project's setup, models, tests, and documentation inside its folder unless a dependency or standard is deliberately shared.
- Keep performance claims tied to reproducible measurements from the project that produced them.
