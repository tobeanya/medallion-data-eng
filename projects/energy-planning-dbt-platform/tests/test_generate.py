import csv
import json
import tempfile
import unittest
from pathlib import Path

from energy_data.generate import generate_sample_data


class GenerateSampleDataTests(unittest.TestCase):
    def test_generation_is_deterministic_and_writes_manifest(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_manifest = generate_sample_data(first, periods=4, seed=7)
            second_manifest = generate_sample_data(second, periods=4, seed=7)

            self.assertEqual(first_manifest, second_manifest)
            self.assertEqual(
                sorted(p.name for p in Path(first).iterdir()),
                sorted(p.name for p in Path(second).iterdir()),
            )
            self.assertEqual(
                (Path(first) / "batch_manifest.json").read_bytes(),
                (Path(second) / "batch_manifest.json").read_bytes(),
            )
            self.assertEqual(first_manifest["source_batch_id"], "demo-7-4")
            self.assertEqual(len(first_manifest["files"]), 12)

    def test_model_results_are_scenario_scoped_and_cover_three_approaches(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            generate_sample_data(temp_dir, periods=2)
            with (Path(temp_dir) / "candidate_results.csv").open(newline="") as stream:
                candidates = list(csv.DictReader(stream))

            self.assertEqual(len(candidates), 54)
            keys = [
                (row["study_id"], row["scenario_id"], row["zone_id"],
                 row["model_approach"], row["metric_name"])
                for row in candidates
            ]
            self.assertEqual(len(keys), len(set(keys)))
            self.assertEqual({row["model_approach"] for row in candidates},
                             {"approach_a", "approach_b", "approach_c"})

    def test_weather_is_shared_across_scenarios_and_unique_by_zone_and_period(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = generate_sample_data(temp_dir, periods=5)
            weather_entry = next(item for item in manifest["files"] if item["file"] == "weather.json")
            self.assertEqual(weather_entry["row_count"], 10)
            weather = json.loads((Path(temp_dir) / "weather.json").read_text())
            keys = [(row["study_id"], row["zone_id"], row["period_id"]) for row in weather]
            self.assertEqual(len(keys), len(set(keys)))

    def test_defect_modes_change_generated_rows(self):
        with tempfile.TemporaryDirectory() as clean_dir, tempfile.TemporaryDirectory() as mismatch_dir, tempfile.TemporaryDirectory() as duplicate_dir:
            generate_sample_data(clean_dir, periods=1)
            mismatch_manifest = generate_sample_data(
                mismatch_dir, periods=1, inject_defect="candidate_mismatch"
            )
            duplicate_manifest = generate_sample_data(
                duplicate_dir, periods=1, inject_defect="duplicate_operation_key"
            )
            self.assertEqual(mismatch_manifest["injected_defect"], "candidate_mismatch")
            self.assertEqual(duplicate_manifest["injected_defect"], "duplicate_operation_key")

            with (Path(clean_dir) / "candidate_results.csv").open(newline="") as stream:
                clean_first = next(csv.DictReader(stream))
            with (Path(mismatch_dir) / "candidate_results.csv").open(newline="") as stream:
                mismatch_first = next(csv.DictReader(stream))
            self.assertNotEqual(clean_first["metric_value"], mismatch_first["metric_value"])

            with (Path(duplicate_dir) / "hourly_operations.csv").open(newline="") as stream:
                operations = list(csv.DictReader(stream))
            keys = [(row["study_id"], row["scenario_id"], row["zone_id"], row["period_id"])
                    for row in operations]
            self.assertLess(len(set(keys)), len(keys))

    def test_invalid_period_count_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(ValueError, "periods must be at least 1"):
                generate_sample_data(temp_dir, periods=0)


if __name__ == "__main__":
    unittest.main()
