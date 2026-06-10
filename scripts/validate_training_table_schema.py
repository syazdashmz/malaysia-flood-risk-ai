"""Validate model-training table schema."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

TRAINING_TABLE_PATH = (
    PROJECT_ROOT / "data" / "processed" / "model_training" / "training_features.csv"
)
REPORT_PATH = PROJECT_ROOT / "reports" / "training_table_schema_report.md"


def main() -> None:
    from floodrisk.ml.training_schema import (
        validate_training_table_schema,
        write_training_table_schema_report,
    )

    validation = validate_training_table_schema(TRAINING_TABLE_PATH)
    output_path = write_training_table_schema_report(validation, REPORT_PATH)

    print(f"Generated training table schema report: {output_path}")
    print(f"Training table exists: {validation.exists}")
    print(f"Schema valid: {validation.is_schema_valid}")
    print(f"Training ready: {validation.is_training_ready}")
    print(f"Missing required columns: {len(validation.missing_required_columns)}")


if __name__ == "__main__":
    main()
