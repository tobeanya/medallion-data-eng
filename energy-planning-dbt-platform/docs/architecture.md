# Architecture and Modeling Design

## Data flow

```text
Synthetic CSV / JSON batches
          |
          v
Python ingestion + batch manifest
          |
          v
Dagster assets and run metadata
          |
          v
Raw source tables (Bronze)
          |
          v
dbt staging and intermediate models (Silver)
          |
          +--> dbt tests and reconciliation gates
          |
          v
Gold reliability, forecasting, battery, and reconciliation marts
          |
          v
Analyst-ready tables and generated dbt docs
```

## Ownership boundary

The project owner defines source contracts, table grains, identifiers, naming, layer boundaries, tests, failure behavior, and mart metrics. Ingestion owns transport and source preservation; dbt owns canonical transformation and analytical semantics; Dagster owns execution dependencies and run orchestration. Reconciliation validates that modeled outputs agree with independent reference results.

## Initial source contracts

Every source declares a schema version, natural key, event or effective timestamp, and required columns. Each ingested row carries `source_system`, `source_batch_id`, `ingested_at_utc`, and `record_hash`. Batch manifests record source file checksums and expected/observed row counts. Raw tables preserve the original payload for replay and audit.

Scenario and run identifiers must be composite or explicitly namespaced. The modeling layer must never assume that an identifier is globally unique when it is only unique within a study, scenario, or run.

## Layer responsibilities

### Bronze

Persist source values with minimal alteration. Add ingestion metadata, retain JSON payloads where appropriate, and quarantine records that cannot be parsed. Do not apply business definitions here.

### Silver

Cast types, normalize UTC timestamps and engineering units, deduplicate by declared source keys, standardize scenario and asset identifiers, and resolve relationships. Place reusable calculations in intermediate models. Keep model grain explicit in descriptions and tests.

### Gold

Publish the four user-facing marts. Each metric has a documented definition, units, aggregation grain, and source lineage. Avoid embedding competing definitions of reliability or battery economics across downstream marts.

## Quality and release behavior

Critical tests block Gold publication: unique keys, required fields, referential integrity, valid scenario scope, and reconciliation control totals. Non-critical quality issues are quarantined or reported as warnings with counts and sample keys. The Dagster run summary includes source batch, model/test, scenario, affected count, and next troubleshooting pointer.

## Incremental strategy

Start with full-refresh models on the small local fixture to keep correctness transparent. Introduce incremental materialization only where event or run volume warrants it. Define the merge key and correction window first; verify duplicate replay, late-arriving updates, and full-refresh equivalence before switching.

## Local and cloud environments

Local development uses DuckDB and deterministic fixtures. A BigQuery target profile is included as a documented deployment option; credentials are supplied by the developer through environment configuration and are never committed. CI uses local DuckDB and synthetic data so pull requests do not require cloud secrets.

## Scale extension

After MVP correctness is established, add a PySpark ingestion/transformation path and a configurable large-data benchmark. Compare results against the same dbt reconciliation contracts. Publish measured runtime, resource use, and output equivalence only after the benchmark is actually run.
