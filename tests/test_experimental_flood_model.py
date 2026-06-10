import json
from pathlib import Path

import joblib

from floodrisk.ml.experimental_flood_model import (
    MODEL_METADATA_RELATIVE_PATH,
    MODEL_RELATIVE_PATH,
    THRESHOLD_METRICS_RELATIVE_PATH,
    build_experimental_feature_frame,
    load_experimental_model_status,
    predict_experimental_flood,
    warning_level_for_probability,
)
from floodrisk.schemas import ExperimentalFloodPredictionInput


class FixedProbabilityModel:
    def __init__(self, probability: float):
        self.probability = probability

    def predict_proba(self, _features):
        return [[1 - self.probability, self.probability]]


def example_payload() -> ExperimentalFloodPredictionInput:
    return ExperimentalFloodPredictionInput(
        city="Kuala Lumpur",
        temperature_c=29.5,
        humidity_pct=86,
        wind_speed_ms=4.2,
        rainfall_3day_mm=120,
        rainfall_7day_mm=180,
        rainfall_14day_mm=260,
        rainfall_cumsum7_mm=180,
        month=12,
        is_monsoon=1,
    )


def write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_experimental_model_status_reports_missing_artifact(tmp_path: Path):
    status = load_experimental_model_status(tmp_path)

    assert status.available is False
    assert status.model_path == MODEL_RELATIVE_PATH.as_posix()
    assert status.threshold > 0
    assert status.official_verified_target_source is False


def test_experimental_model_status_reads_metadata_and_threshold(tmp_path: Path):
    write_json(
        tmp_path / MODEL_METADATA_RELATIVE_PATH,
        {
            "source_id": "kaggle_malaysia_flood_master",
            "training_mode": "experimental_baseline",
            "target_column": "Flood",
            "feature_columns": ["City", "Rainfall_3day"],
            "official_verified_target_source": False,
            "guardrail": "experimental only",
        },
    )
    write_json(
        tmp_path / THRESHOLD_METRICS_RELATIVE_PATH,
        {"best_high_recall": {"threshold": 0.7}},
    )
    model_path = tmp_path / MODEL_RELATIVE_PATH
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model_path.write_bytes(b"placeholder")

    status = load_experimental_model_status(tmp_path)

    assert status.available is True
    assert status.threshold == 0.7
    assert status.threshold_source == "best_high_recall"
    assert status.feature_columns == ["City", "Rainfall_3day"]


def test_build_experimental_feature_frame_maps_api_fields():
    frame = build_experimental_feature_frame(example_payload())

    assert list(frame.columns) == [
        "City",
        "Temperature_C",
        "Humidity_pct",
        "Wind_Speed_ms",
        "Rainfall_3day",
        "Rainfall_7day",
        "Rainfall_14day",
        "Rainfall_cumsum7",
        "Month",
        "Is_Monsoon",
    ]
    assert frame.loc[0, "City"] == "Kuala Lumpur"
    assert frame.loc[0, "Rainfall_3day"] == 120


def test_predict_experimental_flood_uses_saved_model(tmp_path: Path):
    model_path = tmp_path / MODEL_RELATIVE_PATH
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(FixedProbabilityModel(0.82), model_path)

    write_json(
        tmp_path / MODEL_METADATA_RELATIVE_PATH,
        {
            "source_id": "kaggle_malaysia_flood_master",
            "training_mode": "experimental_baseline",
            "target_column": "Flood",
            "feature_columns": ["City"],
            "official_verified_target_source": False,
            "guardrail": "experimental only",
        },
    )
    write_json(
        tmp_path / THRESHOLD_METRICS_RELATIVE_PATH,
        {"best_high_recall": {"threshold": 0.75}},
    )

    prediction = predict_experimental_flood(example_payload(), tmp_path)

    assert prediction.model_available is True
    assert prediction.flood_probability == 0.82
    assert prediction.predicted_flood is True
    assert prediction.warning_level == "warning"
    assert prediction.official_verified_target_source is False


def test_warning_level_for_probability():
    assert warning_level_for_probability(0.8, 0.75) == "warning"
    assert warning_level_for_probability(0.5, 0.75) == "watch"
    assert warning_level_for_probability(0.1, 0.75) == "low"
