select * from {{ ref('mart_model_reconciliation') }} where not passed
