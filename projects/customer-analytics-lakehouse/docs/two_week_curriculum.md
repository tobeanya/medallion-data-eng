# Two-Week Senior Data Engineer Medallion Curriculum

## Day 1 — Architecture and environment
Learn lakehouse vs warehouse vs data lake, Medallion responsibilities, replayability, and source fidelity.

Build:
- Spark/Delta development environment
- Sample customer, product, transaction, and event data
- Ingestion metadata: timestamp, source file, source system, batch_id

Interview drill:
- Why not clean before Bronze?
- Why is Bronze commonly append-only?
- When could Bronze contain duplicates?
- What is the danger of business logic in Bronze?

## Day 2 — Bronze ingestion
Build raw ingestion for CSV, JSON, and Parquet sources.

Requirements:
- preserve raw values
- capture metadata
- quarantine corrupt records
- rerunnable ingestion
- deterministic batch IDs

Test:
- duplicate batch
- malformed record
- missing file
- unexpected column
- empty source

## Day 3 — Silver cleansing and data contracts
Create:
- silver_customers
- silver_products
- silver_transactions
- silver_events

Implement:
- explicit schemas
- type conversion
- null handling
- duplicate resolution
- business-key validation
- referential integrity
- quarantine

## Day 4 — Incremental processing and CDC
Implement INSERT, UPDATE, DELETE handling with Delta MERGE.

Test:
- duplicate CDC event
- out-of-order update
- update after delete
- replay same batch

Senior concepts:
- log-based CDC vs timestamp extraction
- tombstones vs hard deletes
- ordering guarantees
- idempotent merges

## Day 5 — SCD Type 2
Track customer history for region, membership tier, and account manager.

Fields:
- surrogate_key
- customer_id
- effective_from
- effective_to
- is_current
- attribute_hash

## Day 6 — Gold dimensional modeling
Build:
- dim_customer
- dim_product
- dim_date
- fact_transactions
- monthly_revenue
- customer_360

Document grain, keys, measures, and dimensional choices.

## Day 7 — dbt transformations
Use:
- sources
- ref()
- tests
- macros
- incremental models
- snapshots
- docs and lineage

Week 1 checkpoint: explain the full architecture without notes.

## Day 8 — Late-arriving data and backfills
Simulate transactions arriving three days late.

Build:
- watermark strategy
- late-event detection
- affected-partition recomputation
- safe historical backfill

## Day 9 — Schema evolution
Add new customer fields, then introduce a breaking schema change.

Build:
- schema detection
- compatibility policy
- additive evolution
- breaking-change handling
- contract versioning

## Day 10 — Performance engineering
Benchmark:
- full scans
- filtered scans
- joins
- aggregations

Experiment with:
- partitioning
- clustering / Z-order style strategies
- predicate pushdown
- compaction
- caching
- broadcast joins

Record before/after metrics in `docs/performance_report.md`.

## Day 11 — Orchestration and recovery
Build a Dagster pipeline:
1. ingest_bronze
2. validate_bronze
3. build_silver
4. validate_silver
5. build_gold
6. validate_gold

Add retries, partitions, backfills, and failure hooks.

Failure exercise:
- break Silver
- identify the failure
- repair it
- rerun safely
- verify Gold is not corrupted

## Day 12 — Observability and reliability
Track:
- rows read/written
- rejected rows
- duplicates
- pipeline duration
- freshness
- null-rate changes
- schema changes
- failed expectations
- Bronze → Silver reconciliation
- Silver → Gold reconciliation

Define SLA, SLO, freshness target, and escalation thresholds.

## Day 13 — Governance, security, and IaC
Design:
- RBAC
- masking
- least privilege
- PII separation
- audit logs
- retention/deletion

Create Terraform skeletons for storage, compute, identities, roles, and environments.

## Day 14 — Production review and mock system design
Design for:
- 2 TB/day
- batch + near-real-time events
- 50 source systems
- 200 analysts
- 10 downstream ML jobs
- PII
- 5-year retention

Defend:
- storage format
- Medallion boundaries
- CDC
- batch vs streaming
- partitioning
- backfills
- schema evolution
- monitoring
- governance
- cost controls
- disaster recovery

## Final interview checklist
You should be able to answer:
1. What belongs in Bronze, Silver, and Gold?
2. Why retain raw data?
3. How do you guarantee idempotency?
4. How do you implement CDC?
5. What happens when CDC events arrive out of order?
6. How do you support deletes?
7. How do you handle schema drift?
8. How do you implement SCD Type 2?
9. How do you handle late-arriving facts?
10. How do you backfill safely?
11. How do you reconcile layers?
12. How do you test data pipelines?
13. How do you monitor freshness?
14. How do you reduce the small-file problem?
15. How do you select partition columns?
16. When would you use streaming?
17. What is the grain of your Gold fact table?
18. Why use surrogate keys?
19. How do you protect PII?
20. How do you recover from partial pipeline failures?
