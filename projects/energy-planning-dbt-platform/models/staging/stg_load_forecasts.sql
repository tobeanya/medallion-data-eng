select study_id, scenario_id, zone_id, model_name,
       cast(horizon_hours as integer) as horizon_hours,
       period_id, cast(forecast_mw as double) as forecast_mw,
       cast(actual_mw as double) as actual_mw
from read_csv_auto('data/generated/load_forecasts.csv', header=true)
