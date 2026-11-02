# MVP Specification

## Goal

Create a working, reviewable dbt project that starts with ad hoc energy study files and source tables and grows into a tested, documented, orchestrated data modeling layer. The project should demonstrate the owner's design decisions and tradeoffs, not just a collection of dbt models.

## Users and decisions

The primary users are planning analysts and model engineers who need to compare study scenarios, inspect forecast performance, understand battery economics, and identify model-output inconsistencies. They need traceable data from each published metric back to its source batch, study, scenario, model run, and input version.

## MVP input data

Generate deterministic, synthetic batches for:

1. Study, scenario, zone, asset, and model-run metadata.
2. Hourly load, weather, dispatch, capacity additions, and unserved-energy results.
3. Forecast values and actual load, with model, weather-year, zone, and horizon keys.
4. Battery bids, market prices, dispatch, and ancillary-service allocations.
5. Reference outputs and candidate outputs for three modeling approaches, including deliberately injected defects for validation demonstrations.

Support CSV and JSON input so the ingestion path exercises structured and semi-structured sources. Keep raw source payloads and a batch manifest with source name, schema version, batch ID, ingestion time, file checksum, and record count.

## MVP pipelines

### 1. Batch ingestion

Python ingestion assets load source batches into raw warehouse tables. Replaying the same batch must not duplicate rows. Invalid records go to a quarantine table with the source batch, record key, validation error, and original payload. Dagster assets expose dependencies, retries, and batch-level run metadata.

### 2. dbt medallion models

- **Bronze/raw:** source-faithful records with ingestion metadata.
- **Silver/staging and intermediate:** typed values, canonical units and timestamps, deduplicated records, conformed identifiers, and scenario-scoped keys.
- **Gold/marts:** reliability economics, forecast accuracy, battery outcomes, and model reconciliation.

### 3. Reconciliation and quality gates

Compare candidate and reference results at explicit business keys. Critical failures include duplicate natural keys, missing required relationships, invalid scenario references, and mismatched control totals. Warnings include late data and non-critical optional fields. A failure summary lists the failing model/test, batch, scenario, affected key count, and a small safe sample of keys.

### 4. Orchestration and delivery

Dagster runs ingestion followed by `dbt build`, captures run metadata, and supports retries and partitioned reprocessing. GitHub Actions runs formatting/lint checks, Python tests, sample ingestion, and dbt build on a small local dataset.

## dbt model scope

### Dimensions and core facts

- `dim_study`, `dim_scenario`, `dim_zone`, `dim_asset`, `dim_model`, `dim_weather_year`
- `fct_hourly_dispatch`, `fct_load_forecast`, `fct_battery_dispatch`, `fct_expansion_candidate`
- `fct_model_run_result`, `fct_reference_result`

### Gold marts

- `mart_reliability_summary`: reliability and economic measures by study, scenario, zone, and planning year.
- `mart_forecast_accuracy`: error metrics by zone, model, weather year, and forecast horizon.
- `mart_battery_economics`: energy and ancillary-service outcomes by scenario, asset, and period.
- `mart_model_reconciliation`: row counts, control totals, absolute/relative differences, and pass/fail status by scenario and approach.

## MVP acceptance criteria

- A clean local setup can generate data and execute the full sample workflow without cloud credentials.
- Ingestion is idempotent; rerunning the same batch leaves raw and modeled record counts unchanged.
- Source freshness, uniqueness, non-null, accepted-value, and relationship checks are declared in dbt.
- Scenario identifiers are scoped so records from different scenarios cannot silently overwrite or cross-join.
- Reconciliation compares exact business keys and surfaces injected defects with an actionable failure summary.
- Every Gold model has a description, grain, owner, and documented metric definitions.
- `dbt build` passes for valid sample data and fails at the expected test when seeded with a critical defect.
- Dagster run history shows the source-to-mart dependency graph and failed asset/test details.
- Pull-request CI runs the same small correctness checks without requiring secrets.
- README documents setup, architecture, tradeoffs, and a verified run path; no performance claim is published before measurement.

## Out of scope for MVP

- Live utility or market feeds.
- Employer datasets, code, schemas, or exact proprietary business logic.
- Production cloud deployment, Terraform, and cost optimization.
- Distributed Spark processing and large-scale performance claims.
- Forecast or optimization model training; the MVP models their inputs and outputs.
- A production API or dashboard.

## Delivery milestones

1. **Contracts and sample data:** define grains, keys, schema versions, and deterministic generators.
2. **Ingestion:** create batch manifests, raw loading, idempotency, quarantine, and Dagster assets.
3. **dbt foundation:** configure environments, sources, staging/intermediate layers, tests, docs, and naming conventions.
4. **Gold models:** publish the four marts and their business definitions.
5. **Reconciliation and operations:** add defect injection, failure summaries, retry/backfill behavior, and run metrics.
6. **CI and evidence:** implement pull-request checks, capture verified screenshots/logs, and document actual results and tradeoffs.

## Key design decisions to document

- Why local DuckDB is used for reproducible development while BigQuery is the cloud target.
- Which models are views, tables, or incremental and how late-arriving corrections are handled.
- Which data-quality failures block publication versus land in quarantine or warnings.
- How source schema versions and backward-compatible changes are managed.
- How reconciliation balances exact comparisons with tolerances for floating-point measures.
- How retry, replay, and backfill preserve idempotency and lineage.
