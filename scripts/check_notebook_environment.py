"""Check notebook environment readiness."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

REPORT_PATH = PROJECT_ROOT / "reports" / "notebook_environment_report.md"


def main() -> None:
    from floodrisk.notebooks.environment import (
        check_notebook_environment,
        write_notebook_environment_report,
    )

    summary = check_notebook_environment()
    output_path = write_notebook_environment_report(summary, REPORT_PATH)

    print(f"Generated notebook environment report: {output_path}")
    print(f"Dependencies checked: {summary.dependency_count}")
    print(f"Available dependencies: {summary.available_count}")
    print(f"Missing dependencies: {summary.missing_count}")
    print(f"Blocking dependencies: {summary.blocking_count}")
    print(f"Ready for notebook work: {summary.ready_for_notebook_work}")


if __name__ == "__main__":
    main()
