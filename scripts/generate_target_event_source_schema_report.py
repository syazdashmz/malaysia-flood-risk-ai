"""Generate target event source schema report."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

REPORT_PATH = PROJECT_ROOT / "reports" / "target_event_source_schema_report.md"


def main() -> None:
    from floodrisk.ml.target_event_schema import (
        validate_target_event_source_schema,
        write_target_event_source_schema_report,
    )

    validation = validate_target_event_source_schema(PROJECT_ROOT)
    output_path = write_target_event_source_schema_report(validation, REPORT_PATH)

    print(f"Generated target event source schema report: {output_path}")
    print(f"Exists: {validation.exists}")
    print(f"Rows: {validation.row_count}")
    print(f"Schema valid: {validation.is_schema_valid}")
    print(f"Ready for target generation: {validation.is_ready_for_target_generation}")


if __name__ == "__main__":
    main()
