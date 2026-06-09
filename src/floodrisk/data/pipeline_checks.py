"""Validation helpers for generated data pipeline artifacts."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

WEATHER_PIPELINE_REQUIRED_OUTPUTS = [
    "data/raw/manifest.jsonl",
    "data/raw/weather/weather_forecast_sample.json",
    "data/raw/weather/weather_warning_sample.json",
    "data/interim/weather/weather_forecast_sample_flat.csv",
    "data/interim/weather/weather_warning_sample_flat.csv",
    "data/processed/weather/weather_sample_features.csv",
    "reports/weather_risk_signal_summary.json",
    "reports/weather_sample_profile.md",
]


VALID_WEATHER_SIGNALS = {
    "none",
    "advisory",
    "warning",
    "severe",
}


@dataclass(frozen=True)
class FileCheck:
    """Existence check for one expected file."""

    path: str
    exists: bool


@dataclass(frozen=True)
class WeatherPipelineValidation:
    """Validation result for the weather pipeline."""

    required_files: list[FileCheck]
    manifest_record_count: int
    risk_engine_weather_warning: str
    is_valid: bool

    @property
    def missing_paths(self) -> list[str]:
        """Return missing required file paths."""

        return [file_check.path for file_check in self.required_files if not file_check.exists]

    def as_dict(self) -> dict[str, Any]:
        """Return validation result as a JSON-serializable dictionary."""

        return asdict(self)


def check_required_files(
    project_root: Path,
    relative_paths: list[str],
) -> list[FileCheck]:
    """Check whether required files exist."""

    return [
        FileCheck(path=relative_path, exists=(project_root / relative_path).exists())
        for relative_path in relative_paths
    ]


def count_jsonl_records(input_path: Path) -> int:
    """Count non-empty JSON Lines records."""

    if not input_path.exists():
        return 0

    with input_path.open("r", encoding="utf-8") as file:
        return sum(1 for line in file if line.strip())


def load_json_object(input_path: Path) -> dict[str, Any]:
    """Load a JSON object from disk."""

    if not input_path.exists():
        return {}

    data = json.loads(input_path.read_text(encoding="utf-8"))

    if isinstance(data, dict):
        return data

    return {}


def validate_weather_pipeline(project_root: Path) -> WeatherPipelineValidation:
    """Validate expected weather pipeline artifacts."""

    required_files = check_required_files(
        project_root,
        WEATHER_PIPELINE_REQUIRED_OUTPUTS,
    )
    manifest_record_count = count_jsonl_records(
        project_root / "data/raw/manifest.jsonl",
    )
    risk_summary = load_json_object(
        project_root / "reports/weather_risk_signal_summary.json",
    )
    risk_engine_weather_warning = str(risk_summary.get("risk_engine_weather_warning", "none"))

    missing_paths = [file_check.path for file_check in required_files if not file_check.exists]

    is_valid = (
        not missing_paths
        and manifest_record_count >= 2
        and risk_engine_weather_warning in VALID_WEATHER_SIGNALS
    )

    return WeatherPipelineValidation(
        required_files=required_files,
        manifest_record_count=manifest_record_count,
        risk_engine_weather_warning=risk_engine_weather_warning,
        is_valid=is_valid,
    )


def render_weather_pipeline_validation(
    validation: WeatherPipelineValidation,
) -> str:
    """Render weather pipeline validation result as Markdown."""

    lines = [
        "# Weather Pipeline Validation",
        "",
        f"- Valid: {validation.is_valid}",
        f"- Manifest records: {validation.manifest_record_count}",
        f"- Risk engine weather warning: {validation.risk_engine_weather_warning}",
        "",
        "## Required Files",
        "",
    ]

    for file_check in validation.required_files:
        status = "OK" if file_check.exists else "MISSING"
        lines.append(f"- {status}: {file_check.path}")

    if validation.missing_paths:
        lines.extend(["", "## Missing Files", ""])
        lines.extend(f"- {path}" for path in validation.missing_paths)

    return "\n".join(lines).rstrip() + "\n"


def write_weather_pipeline_validation(
    validation: WeatherPipelineValidation,
    output_path: Path,
) -> Path:
    """Write weather pipeline validation result to Markdown."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_weather_pipeline_validation(validation),
        encoding="utf-8",
    )
    return output_path
