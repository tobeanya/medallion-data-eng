with reference as (
  select study_id, scenario_id, zone_id, metric_name,
         cast(metric_value as double) as reference_value
  from read_csv_auto('data/generated/reference_results.csv', header=true)
), candidate as (
  select * from {{ ref('stg_model_results') }}
)
select c.study_id, c.scenario_id, c.zone_id, c.model_approach, c.metric_name,
       r.reference_value, c.metric_value as candidate_value,
       abs(c.metric_value - r.reference_value) as absolute_difference,
       abs(c.metric_value - r.reference_value) <= 0.001 as passed
from candidate c
join reference r using (study_id, scenario_id, zone_id, metric_name)
