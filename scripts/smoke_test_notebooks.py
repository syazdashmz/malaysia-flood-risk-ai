"""Smoke test notebook execution without saving outputs."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

NOTEBOOK_DIR = PROJECT_ROOT / "notebooks"
REPORT_PATH = PROJECT_ROOT / "reports" / "notebook_execution_report.md"


def main() -> None:
    from floodrisk.notebooks.execution import (
        smoke_test_notebook_directory,
        write_notebook_execution_report,
    )

    summary = smoke_test_notebook_directory(
        notebook_dir=NOTEBOOK_DIR,
        project_root=PROJECT_ROOT,
    )
    output_path = write_notebook_execution_report(summary, REPORT_PATH)

    print(f"Generated notebook smoke execution report: {output_path}")
    print(f"Notebooks checked: {summary.notebook_count}")
    print(f"Successful notebooks: {summary.successful_count}")
    print(f"Failed notebooks: {summary.failed_count}")
    print(f"Ready for notebook EDA: {summary.ready_for_notebook_eda}")

    if not summary.ready_for_notebook_eda:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
