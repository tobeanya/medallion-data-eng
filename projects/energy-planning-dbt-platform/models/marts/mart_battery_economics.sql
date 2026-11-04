select study_id, scenario_id, asset_id,
       sum(dispatched_mwh) as energy_dispatched_mwh,
       sum(ancillary_service_mw) as ancillary_capacity_mw_hours,
       sum(dispatched_mwh * market_price_usd_mwh) as energy_value_usd
from {{ ref('stg_battery_dispatch') }}
group by study_id, scenario_id, asset_id
