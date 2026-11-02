# Pipeline Runbook

## Failure triage
1. Identify failed asset/job.
2. Check source availability and schema.
3. Review row-count and quality metrics.
4. Determine last successful partition/batch.
5. Verify whether downstream assets ran.
6. Correct root cause.
7. Replay smallest safe partition.
8. Reconcile source → Bronze → Silver → Gold.
9. Document incident and prevention action.

## Rule
Never blindly rerun. Confirm idempotency and partition scope before replaying production data.
