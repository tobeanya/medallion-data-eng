select study_id, scenario_id, asset_id, period_id,
       cast(dispatched_mwh as double) as dispatched_mwh,
       cast(ancillary_service_mw as double) as ancillary_service_mw,
       cast(market_price_usd_mwh as double) as market_price_usd_mwh
from read_csv_auto('data/generated/battery_dispatch.csv', header=true)
