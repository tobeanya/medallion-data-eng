"""Generate deterministic synthetic energy-planning source batches."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import json
import random
from pathlib import Path
from typing import Iterable, Mapping, Sequence


STUDY_ID = "study_001"
SCENARIOS = (
    ("baseline", "Baseline", 1.0),
    ("high_load", "High Load", 1.12),
    ("retire_units", "Retire Units", 1.04),
)
ZONES = (("north", "North Zone", 0.0), ("south", "South Zone", 180.0))
APPROACHES = ("approach_a", "approach_b", "approach_c")
METRICS = ("unserved_mwh", "capacity_added_mw", "production_cost_usd")
SCHEMA_VERSION = "1.0"
GENERATED_AT_UTC = "2026-01-01T00:00:00Z"


CSV_SCHEMAS: dict[str, tuple[str, ...]] = {
    "study.csv": ("study_id", "study_name", "planning_year"),
    "scenarios.csv": ("study_id", "scenario_id", "scenario_name", "load_multiplier"),
    "zones.csv": ("study_id", "zone_id", "zone_name"),
    "assets.csv": ("study_id", "asset_id", "zone_id", "asset_type", "nameplate_mw"),
    "model_runs.csv": (
        "study_id", "scenario_id", "model_approach", "run_id", "run_status"
    ),
    "hourly_operations.csv": (
        "study_id", "scenario_id", "zone_id", "period_id", "timestamp_utc",
        "load_mw", "dispatch_mw", "unserved_mwh", "capacity_added_mw",
    ),
    "load_forecasts.csv": (
        "study_id", "scenario_id", "zone_id", "model_name", "horizon_hours",
        "period_id", "forecast_mw", "actual_mw",
    ),
    "battery_bids.csv": (
        "study_id", "scenario_id", "asset_id", "market", "period_id",
        "bid_price_usd_mwh",
    ),
    "battery_dispatch.csv": (
        "study_id", "scenario_id", "asset_id", "period_id", "dispatched_mwh",
        "ancillary_service_mw", "market_price_usd_mwh",
    ),
    "reference_results.csv": (
        "study_id", "scenario_id", "zone_id", "metric_name", "metric_value",
    ),
    "candidate_results.csv": (
        "study_id", "scenario_id", "zone_id", "model_approach", "metric_name",
        "metric_value",
    ),
}


def _write_csv(path: Path, fieldnames: Sequence[str], rows: Iterable[Mapping[str, object]]) -> int:
    materialized = list(rows)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, extrasaction="raise")
        writer.writeheader()
        writer.writerows(materialized)
    return len(materialized)


def _metric_value(scenario_id: str, zone_id: str, metric: str) -> float:
    scenario_factor = {"baseline": 1.0, "high_load": 1.35, "retire_units": 1.18}[scenario_id]
    zone_factor = 1.0 if zone_id == "north" else 1.22
    base = {
        "unserved_mwh": 0.0 if scenario_id == "baseline" else 2.5,
        "capacity_added_mw": 120.0,
        "production_cost_usd": 125_000.0,
    }[metric]
    return round(base * scenario_factor * zone_factor, 3)


def generate_sample_data(
    output_dir: str | Path,
    *,
    periods: int = 24,
    seed: int = 41,
    inject_defect: str = "none",
) -> dict[str, object]:
    """Write a reproducible source batch and return its manifest.

    ``inject_defect`` is intended for quality-gate exercises. Supported values
    are ``none``, ``candidate_mismatch``, and ``duplicate_operation_key``.
    """
    if periods < 1:
        raise ValueError("periods must be at least 1")
    if inject_defect not in {"none", "candidate_mismatch", "duplicate_operation_key"}:
        raise ValueError(f"unsupported defect: {inject_defect}")

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)

    rows: dict[str, list[dict[str, object]]] = {name: [] for name in CSV_SCHEMAS}
    rows["study.csv"] = [{
        "study_id": STUDY_ID,
        "study_name": "Synthetic Regional Resource Plan",
        "planning_year": 2035,
    }]
    rows["scenarios.csv"] = [
        {"study_id": STUDY_ID, "scenario_id": sid, "scenario_name": name,
         "load_multiplier": multiplier}
        for sid, name, multiplier in SCENARIOS
    ]
    rows["zones.csv"] = [
        {"study_id": STUDY_ID, "zone_id": zid, "zone_name": name}
        for zid, name, _ in ZONES
    ]
    rows["assets.csv"] = [
        {"study_id": STUDY_ID, "asset_id": f"battery_{zid}", "zone_id": zid,
         "asset_type": "battery", "nameplate_mw": 100}
        for zid, _, _ in ZONES
    ] + [
        {"study_id": STUDY_ID, "asset_id": f"thermal_{zid}", "zone_id": zid,
         "asset_type": "thermal", "nameplate_mw": 900}
        for zid, _, _ in ZONES
    ]
    rows["model_runs.csv"] = [
        {"study_id": STUDY_ID, "scenario_id": sid, "model_approach": approach,
         "run_id": f"{sid}_{approach}_001", "run_status": "succeeded"}
        for sid, _, _ in SCENARIOS for approach in APPROACHES
    ]

    weather: list[dict[str, object]] = []
    start_time = datetime(2035, 1, 1, tzinfo=timezone.utc)
    for zid, _, _ in ZONES:
        for period in range(periods):
            timestamp = (start_time + timedelta(hours=period)).isoformat().replace("+00:00", "Z")
            weather.append({
                "study_id": STUDY_ID, "zone_id": zid,
                "period_id": f"p{period:04d}", "timestamp_utc": timestamp,
                "temperature_c": round(12 + 10 * rng.random(), 3),
                "wind_speed_mps": round(2 + 8 * rng.random(), 3),
            })

    for sid, _, load_multiplier in SCENARIOS:
        for zid, _, zone_load_offset in ZONES:
            for period in range(periods):
                timestamp = (start_time + timedelta(hours=period)).isoformat().replace("+00:00", "Z")
                base_load = (900 + zone_load_offset + 110 * (period % 24 >= 17))
                actual_load = round(base_load * load_multiplier, 3)
                shortage = round(max(0.0, actual_load - (base_load + 160)), 3)
                rows["hourly_operations.csv"].append({
                    "study_id": STUDY_ID, "scenario_id": sid, "zone_id": zid,
                    "period_id": f"p{period:04d}", "timestamp_utc": timestamp,
                    "load_mw": actual_load,
                    "dispatch_mw": round(actual_load - shortage, 3),
                    "unserved_mwh": shortage,
                    "capacity_added_mw": 40 if period == 0 and sid != "baseline" else 0,
                })
                forecast = round(actual_load * (1 + rng.uniform(-0.04, 0.04)), 3)
                rows["load_forecasts.csv"].append({
                    "study_id": STUDY_ID, "scenario_id": sid, "zone_id": zid,
                    "model_name": "baseline_nn", "horizon_hours": 1,
                    "period_id": f"p{period:04d}", "forecast_mw": forecast,
                    "actual_mw": actual_load,
                })
                asset_id = f"battery_{zid}"
                price = round(25 + 75 * ((period % 24) / 23), 3)
                rows["battery_bids.csv"].append({
                    "study_id": STUDY_ID, "scenario_id": sid, "asset_id": asset_id,
                    "market": "energy", "period_id": f"p{period:04d}",
                    "bid_price_usd_mwh": price,
                })
                rows["battery_dispatch.csv"].append({
                    "study_id": STUDY_ID, "scenario_id": sid, "asset_id": asset_id,
                    "period_id": f"p{period:04d}",
                    "dispatched_mwh": round(20 if period in range(17, 22) else 0, 3),
                    "ancillary_service_mw": round(15 if period not in range(17, 22) else 0, 3),
                    "market_price_usd_mwh": price,
                })

    for sid, _, _ in SCENARIOS:
        for zid, _, _ in ZONES:
            for metric in METRICS:
                reference_value = _metric_value(sid, zid, metric)
                rows["reference_results.csv"].append({
                    "study_id": STUDY_ID, "scenario_id": sid, "zone_id": zid,
                    "metric_name": metric, "metric_value": reference_value,
                })
                for approach_index, approach in enumerate(APPROACHES):
                    value = reference_value
                    if metric == "production_cost_usd":
                        value += approach_index * 125.0
                    rows["candidate_results.csv"].append({
                        "study_id": STUDY_ID, "scenario_id": sid, "zone_id": zid,
                        "model_approach": approach, "metric_name": metric,
                        "metric_value": round(value, 3),
                    })

    if inject_defect == "candidate_mismatch":
        target = rows["candidate_results.csv"][0]
        target["metric_value"] = round(float(target["metric_value"]) + 999.0, 3)
    elif inject_defect == "duplicate_operation_key":
        rows["hourly_operations.csv"].append(dict(rows["hourly_operations.csv"][0]))

    file_rows: dict[str, int] = {}
    for filename, records in rows.items():
        file_rows[filename] = _write_csv(destination / filename, CSV_SCHEMAS[filename], records)

    weather_path = destination / "weather.json"
    weather_path.write_text(json.dumps(weather, indent=2) + "\n", encoding="utf-8")
    file_rows["weather.json"] = len(weather)

    file_manifest = []
    for filename, count in sorted(file_rows.items()):
        digest = hashlib.sha256((destination / filename).read_bytes()).hexdigest()
        file_manifest.append({
            "file": filename,
            "format": "json" if filename.endswith(".json") else "csv",
            "schema_version": SCHEMA_VERSION,
            "row_count": count,
            "sha256": digest,
        })
    manifest: dict[str, object] = {
        "source_batch_id": f"demo-{seed}-{periods}",
        "source_system": "synthetic_energy_planning",
        "generated_at_utc": GENERATED_AT_UTC,
        "schema_version": SCHEMA_VERSION,
        "periods": periods,
        "seed": seed,
        "injected_defect": inject_defect,
        "files": file_manifest,
    }
    (destination / "batch_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="data/generated", help="Output directory")
    parser.add_argument("--periods", type=int, default=24, help="Number of hourly periods")
    parser.add_argument("--seed", type=int, default=41, help="Deterministic random seed")
    parser.add_argument(
        "--inject-defect", choices=("none", "candidate_mismatch", "duplicate_operation_key"),
        default="none", help="Seed a defect to exercise downstream quality checks",
    )
    args = parser.parse_args()
    manifest = generate_sample_data(
        args.output_dir, periods=args.periods, seed=args.seed, inject_defect=args.inject_defect
    )
    print(json.dumps({
        "source_batch_id": manifest["source_batch_id"],
        "output_dir": str(Path(args.output_dir)),
        "file_count": len(manifest["files"]),
        "row_counts": {item["file"]: item["row_count"] for item in manifest["files"]},
    }, indent=2))


if __name__ == "__main__":
    main()
