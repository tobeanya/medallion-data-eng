# Prior Pipeline Experience Mapped to This Project

This page records the user's prior work as project requirements and design inputs. The metrics below describe that prior work, not results of this portfolio repository. The new project's results will be measured and reported separately.

| Prior work | Recorded ownership and result | Project module |
|---|---|---|
| ComboCurve Python and Google Cloud extraction/transformation | Ingested structured and unstructured data into SQL and NoSQL systems; 99.5% accuracy and 25% higher throughput. | Python batch ingestion, schema contracts, raw tables, batch manifests, and validation. |
| Apache Spark transformation pipelines | Designed Python/Spark backend transformations; about 50% efficiency improvement. | Scale-out transformation extension after the local MVP is correct. |
| Dagster table-family imports | Built orchestrated imports across eight SQL Server table families, with idempotency, key mapping, UTC normalization, referential/orphan checks, retries, and migration validation. | Dagster assets and ingestion reliability patterns. |
| PowerGEM SQL reliability workflow | Owned a 70,960,464-row, 93-measure workflow; reduced runtime from 101.6 to 20.9 minutes and retained exact agreement across 160,704 values. | Large-data benchmark pattern, Gold reliability mart, and equivalence checks. |
| PowerGEM Python reconciliation framework | Built 45 scripts and 12,000+ lines across seven scenario families and three modeling approaches, comparing 160,704 reference cells. | Reusable scenario comparison models, reconciliation tests, and failure summaries. |
| PowerGEM defect investigation | Traced silent corruption across 230 rows, 79 identifiers, and 19 scenarios to an identifier map shared across scenarios; fixed with scenario-specific mapping and row-level validation. | Composite scenario keys, seeded defect, and regression tests. |
| PowerGEM expansion planning | Productionized scenario execution with checkpoint/restart, failed-case resubmission, multi-scenario comparison, and reliability gates. | Study-run metadata, orchestration behavior, retries, partitions, and publication gates. |
| Reliability and economic metrics | Developed reliability/economic measures, including unserved-energy cost and capacity-addition reporting for planning decisions. | `mart_reliability_summary` and shared metric definitions. |
| Astrapé load and energy forecasting | Developed neural-network forecasting from historical load and weather data. | Forecast, actual, weather-year, and horizon models in `mart_forecast_accuracy`. |
| Astrapé battery co-optimization | Worked on battery bidding and ancillary-service co-optimization. | Bid, price, dispatch, service allocation, and economics models. |
| Python/C#/.NET/SQL Server workflows and data access | Built production workflows and APIs across reliability, forecasting, optimization, and reporting; improved database performance through SQL/schema work. | Source interfaces, queryable Gold marts, and measured materialization choices. |
| Test-driven CI/CD | Implemented test-driven delivery practices associated with about 30% less debugging time. | Python/dbt CI checks and defect regression suite. |

## Evidence discipline

- Do not put employer data, source code, customer names, or proprietary model logic in this repository.
- Do not present prior-work performance metrics as portfolio-project results.
- Add project performance numbers only after running a reproducible benchmark and storing its configuration and outputs.
- If the role asks about dbt ownership before this repository is implemented, describe the repository as a current personal project and distinguish it from prior production ownership.
