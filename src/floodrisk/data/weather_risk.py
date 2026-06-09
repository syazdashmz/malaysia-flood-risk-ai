"""Summarize weather feature tables into risk-engine weather signals."""

from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

SIGNAL_SEVERITY = {
    "none": 0,
    "advisory": 1,
    "warning": 2,
    "severe": 3,
}


@dataclass(frozen=True)
class WeatherRiskSummary:
    """Compact weather risk summary for downstream use."""

    record_count: int
    forecast_count: int
    warning_count: int
    max_weather_signal: str
    risk_engine_weather_warning: str
    signal_counts: dict[str, int]

    def as_dict(self) -> dict[str, object]:
        """Return the summary as a JSON-serializable dictionary."""

        return asdict(self)


def normalize_weather_signal(signal: str | None) -> str:
    """Normalize a weather signal value."""

    normalized = (signal or "").strip().lower()

    if normalized in SIGNAL_SEVERITY:
        return normalized

    return "none"


def select_max_weather_signal(signals: list[str | None]) -> str:
    """Select the strongest weather signal from a list."""

    if not signals:
        return "none"

    normalized_signals = [normalize_weather_signal(signal) for signal in signals]

    return max(normalized_signals, key=lambda signal: SIGNAL_SEVERITY[signal])


def load_weather_feature_records(input_path: Path) -> list[dict[str, str]]:
    """Load weather feature CSV records."""

    with input_path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def summarize_weather_features(
    records: list[dict[str, str]],
) -> WeatherRiskSummary:
    """Summarize weather feature records."""

    signals = [normalize_weather_signal(record.get("weather_signal")) for record in records]

    signal_counts = Counter(signals)
    max_weather_signal = select_max_weather_signal(signals)

    forecast_count = sum(1 for record in records if record.get("source_type") == "forecast")
    warning_count = sum(1 for record in records if record.get("source_type") == "warning")

    return WeatherRiskSummary(
        record_count=len(records),
        forecast_count=forecast_count,
        warning_count=warning_count,
        max_weather_signal=max_weather_signal,
        risk_engine_weather_warning=max_weather_signal,
        signal_counts={signal: signal_counts.get(signal, 0) for signal in SIGNAL_SEVERITY},
    )


def summarize_weather_feature_file(input_path: Path) -> WeatherRiskSummary:
    """Summarize one weather feature CSV file."""

    records = load_weather_feature_records(input_path)
    return summarize_weather_features(records)


def write_weather_risk_summary(
    summary: WeatherRiskSummary,
    output_path: Path,
) -> Path:
    """Write a weather risk summary JSON file."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(summary.as_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return output_path
