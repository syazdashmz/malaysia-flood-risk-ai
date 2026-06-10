"""Experimental Kaggle flood model serving utilities.

This module serves only the experimental proxy baseline. It does not replace
the official target-source readiness gate for real supervised ML training.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from floodrisk.schemas import (
    ExperimentalFloodPredictionInput,
    ExperimentalFloodPredictionOutput,
)

DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_RELATIVE_PATH = Path("models/kaggle_flood_baseline.joblib")
MODEL_METADATA_RELATIVE_PATH = Path("models/kaggle_flood_baseline_metadata.json")
TRAINING_METRICS_RELATIVE_PATH = Path("reports/kaggle_flood_baseline_training_metrics.json")
THRESHOLD_METRICS_RELATIVE_PATH = Path("reports/kaggle_flood_threshold_tuning_metrics.json")

DEFAULT_SERVING_THRESHOLD = 0.75
DEFAULT_GUARDRAIL = (
    "Experimental proxy baseline only. Do not present as final official verified flood model."
)


@dataclass(frozen=True)
class ExperimentalModelStatus:
    """Status summary for the experimental flood model artifact."""

    available: bool
    model_path: str
    metadata_path: str
    source_id: str
    training_mode: str
    target_column: str
    feature_columns: list[str]
    threshold: float
    threshold_source: str
    official_verified_target_source: bool
    guardrail: str

    def as_dict(self) -> dict[str, Any]:
        """Return status as a JSON-serializable dictionary."""

        return asdict(self)


def _load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from disk when available."""

    if not path.exists():
        return {}

    data = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(data, dict):
        return data

    return {}


def _selected_threshold(project_root: Path) -> tuple[float, str]:
    """Return the serving threshold and its source."""

    threshold_metrics = _load_json(project_root / THRESHOLD_METRICS_RELATIVE_PATH)
    best_high_recall = threshold_metrics.get("best_high_recall", {})

    if isinstance(best_high_recall, dict) and "threshold" in best_high_recall:
        return round(float(best_high_recall["threshold"]), 4), "best_high_recall"

    return DEFAULT_SERVING_THRESHOLD, "default_high_recall"


def load_experimental_model_status(
    project_root: Path = DEFAULT_PROJECT_ROOT,
) -> ExperimentalModelStatus:
    """Load experimental model artifact status for app/API display."""

    model_path = project_root / MODEL_RELATIVE_PATH
    metadata_path = project_root / MODEL_METADATA_RELATIVE_PATH
    metadata = _load_json(metadata_path)
    training_metrics = _load_json(project_root / TRAINING_METRICS_RELATIVE_PATH)
    threshold, threshold_source = _selected_threshold(project_root)

    feature_columns = (
        metadata.get("feature_columns") or training_metrics.get("feature_columns") or []
    )

    return ExperimentalModelStatus(
        available=model_path.exists() and metadata_path.exists(),
        model_path=MODEL_RELATIVE_PATH.as_posix(),
        metadata_path=MODEL_METADATA_RELATIVE_PATH.as_posix(),
        source_id=str(
            metadata.get("source_id")
            or training_metrics.get("source_id")
            or "kaggle_malaysia_flood_master"
        ),
        training_mode=str(
            metadata.get("training_mode")
            or training_metrics.get("training_mode")
            or "experimental_baseline"
        ),
        target_column=str(
            metadata.get("target_column") or training_metrics.get("target_column") or "Flood"
        ),
        feature_columns=[str(column) for column in feature_columns],
        threshold=threshold,
        threshold_source=threshold_source,
        official_verified_target_source=bool(
            metadata.get("official_verified_target_source", False)
        ),
        guardrail=str(
            metadata.get("guardrail") or training_metrics.get("guardrail") or DEFAULT_GUARDRAIL
        ),
    )


def build_experimental_feature_frame(
    payload: ExperimentalFloodPredictionInput,
) -> pd.DataFrame:
    """Map API input into the training feature columns."""

    return pd.DataFrame(
        [
            {
                "City": payload.city,
                "Temperature_C": payload.temperature_c,
                "Humidity_pct": payload.humidity_pct,
                "Wind_Speed_ms": payload.wind_speed_ms,
                "Rainfall_3day": payload.rainfall_3day_mm,
                "Rainfall_7day": payload.rainfall_7day_mm,
                "Rainfall_14day": payload.rainfall_14day_mm,
                "Rainfall_cumsum7": payload.rainfall_cumsum7_mm,
                "Month": payload.month,
                "Is_Monsoon": payload.is_monsoon,
            }
        ]
    )


def warning_level_for_probability(probability: float, threshold: float) -> str:
    """Return a compact warning level for experimental model output."""

    if probability >= threshold:
        return "warning"
    if probability >= max(0.4, threshold * 0.6):
        return "watch"
    return "low"


def predict_experimental_flood(
    payload: ExperimentalFloodPredictionInput,
    project_root: Path = DEFAULT_PROJECT_ROOT,
) -> ExperimentalFloodPredictionOutput:
    """Run the experimental flood baseline model for one observation."""

    status = load_experimental_model_status(project_root)

    if not status.available:
        msg = (
            "Experimental model artifact is missing. "
            "Run scripts/train_kaggle_flood_baseline.py first."
        )
        raise FileNotFoundError(msg)

    import joblib

    model = joblib.load(project_root / MODEL_RELATIVE_PATH)
    feature_frame = build_experimental_feature_frame(payload)
    probability = round(float(model.predict_proba(feature_frame)[0][1]), 4)
    predicted_flood = probability >= status.threshold

    return ExperimentalFloodPredictionOutput(
        model_available=True,
        flood_probability=probability,
        predicted_flood=predicted_flood,
        threshold=status.threshold,
        warning_level=warning_level_for_probability(probability, status.threshold),
        source_id=status.source_id,
        training_mode=status.training_mode,
        official_verified_target_source=status.official_verified_target_source,
        guardrail=status.guardrail,
        disclaimer=(
            "Experimental model output for research only. "
            "Always follow official Malaysian flood warnings and emergency instructions."
        ),
    )
