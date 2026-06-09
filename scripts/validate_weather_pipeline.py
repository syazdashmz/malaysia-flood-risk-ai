"""Validate local weather pipeline outputs."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


REPORT_PATH = PROJECT_ROOT / "reports" / "weather_pipeline_validation.md"


def main() -> None:
    from floodrisk.data.pipeline_checks import (
        validate_weather_pipeline,
        write_weather_pipeline_validation,
    )

    validation = validate_weather_pipeline(PROJECT_ROOT)
    output_path = write_weather_pipeline_validation(validation, REPORT_PATH)

    print(f"Generated weather pipeline validation report: {output_path}")
    print(f"Weather pipeline valid: {validation.is_valid}")

    if not validation.is_valid:
        missing = ", ".join(validation.missing_paths)
        raise SystemExit(f"Weather pipeline validation failed. Missing: {missing}")


if __name__ == "__main__":
    main()
