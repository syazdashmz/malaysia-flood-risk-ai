"""Validate project notebooks."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

NOTEBOOK_DIR = PROJECT_ROOT / "notebooks"
REPORT_PATH = PROJECT_ROOT / "reports" / "notebook_validation_report.md"


def main() -> None:
    from floodrisk.notebooks.validation import (
        validate_notebook_directory,
        write_notebook_validation_report,
    )

    validations = validate_notebook_directory(NOTEBOOK_DIR)
    output_path = write_notebook_validation_report(validations, REPORT_PATH)

    clean_count = sum(1 for validation in validations if validation.is_clean)

    print(f"Generated notebook validation report: {output_path}")
    print(f"Notebooks checked: {len(validations)}")
    print(f"Clean notebooks: {clean_count}")
    print(f"Notebooks requiring attention: {len(validations) - clean_count}")


if __name__ == "__main__":
    main()
