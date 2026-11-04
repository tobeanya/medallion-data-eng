with source as (
    select * from read_csv_auto('data/generated/hourly_operations.csv', header = true)
),
typed as (
    select
        study_id,
        scenario_id,
        zone_id,
        period_id,
        cast(timestamp_utc as timestamptz) as timestamp_utc,
        cast(load_mw as double) as load_mw,
        cast(dispatch_mw as double) as dispatch_mw,
        cast(unserved_mwh as double) as unserved_mwh,
        cast(capacity_added_mw as double) as capacity_added_mw
    from source
)
select * from typed
