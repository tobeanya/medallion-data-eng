# Energy Planning Data Platform

An end-to-end dbt project for turning raw grid-planning and market-simulation outputs into trusted reliability, forecasting, battery, and expansion-planning datasets.

The project demonstrates ownership of a data platform from an initially ad hoc set of files and source tables through source contracts, ingestion, medallion modeling, reconciliation, documentation, orchestration, and CI. All project data is synthetic. No employer code or confidential data is included.

## MVP scope

The first release will support one synthetic study with multiple zones, weather years, scenarios, model runs, and battery dispatch periods. It will ingest CSV and JSON source batches, preserve raw records, standardize them into conformed models, and publish four dbt marts:

- Reliability and economic study results
- Load forecast accuracy by zone, model, weather year, and horizon
- Battery bidding and ancillary-service outcomes
- Cross-model scenario reconciliation

The build will make key decisions visible: stable source contracts, scenario-scoped identifiers, incremental versus full-refresh models, critical versus warning-level quality gates, and run-level failure summaries.

## Planned stack

- Python for synthetic data generation, source ingestion, and reconciliation utilities
- Dagster for asset orchestration, retries, backfills, and run-level observability
- dbt Core for the owned modeling layer, tests, documentation, and lineage
- BigQuery as the target warehouse, with a local DuckDB profile for reproducible development
- GitHub Actions for pull-request validation

PySpark is a scale-out extension after the MVP passes end-to-end correctness checks. The initial release will not require a paid cloud resource to run locally.

## Start here

- [MVP specification](docs/MVP.md)
- [Architecture and modeling design](docs/architecture.md)
- [Prior pipeline experience mapped to the project](docs/pipeline-inventory.md)

## Success criteria

From a clean checkout, a developer can generate the sample data, ingest it idempotently, run the Dagster job, run `dbt build`, inspect generated documentation and lineage, and see a useful summary when a deliberately introduced data-quality failure blocks a critical model.

## Project status

This repository begins with the MVP design. Implementation results and performance measurements will be added only after the corresponding pipeline is built and run.
