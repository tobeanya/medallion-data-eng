select study_id, scenario_id, zone_id, model_approach, metric_name,
       cast(metric_value as double) as metric_value
from read_csv_auto('data/generated/candidate_results.csv', header=true)
