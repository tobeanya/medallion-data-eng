select
    study_id,
    scenario_id,
    zone_id,
    sum(load_mw) as load_mwh,
    sum(dispatch_mw) as dispatch_mwh,
    sum(unserved_mwh) as unserved_mwh,
    sum(capacity_added_mw) as capacity_added_mw,
    case when sum(load_mw) = 0 then 0
         else sum(unserved_mwh) / sum(load_mw) end as unserved_energy_rate
from {{ ref('stg_hourly_operations') }}
group by study_id, scenario_id, zone_id
