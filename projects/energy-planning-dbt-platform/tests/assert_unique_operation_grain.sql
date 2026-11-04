select study_id, scenario_id, zone_id, period_id, count(*) as row_count
from {{ ref('stg_hourly_operations') }}
group by study_id, scenario_id, zone_id, period_id
having count(*) > 1
