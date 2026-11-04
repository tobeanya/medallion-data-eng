select study_id, scenario_id, zone_id, model_name, horizon_hours,
       count(*) as forecast_count,
       avg(abs(forecast_mw - actual_mw)) as mae_mw,
       avg(abs(forecast_mw - actual_mw) / nullif(actual_mw, 0)) as mape
from {{ ref('stg_load_forecasts') }}
group by study_id, scenario_id, zone_id, model_name, horizon_hours
