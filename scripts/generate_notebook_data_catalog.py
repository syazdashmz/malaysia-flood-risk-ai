"""Generate notebook data catalog report."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

REPORT_PATH = PROJECT_ROOT / "reports" / "notebook_data_catalog_report.md"


def main() -> None:
    from floodrisk.notebooks.catalog import (
        build_notebook_data_catalog,
        write_notebook_data_catalog_report,
    )

    summary = build_notebook_data_catalog(PROJECT_ROOT)
    output_path = write_notebook_data_catalog_report(summary, REPORT_PATH)

    print(f"Generated notebook data catalog report: {output_path}")
    print(f"Assets cataloged: {summary.asset_count}")
    print(f"Available assets: {summary.available_count}")
    print(f"Explorable assets: {summary.explorable_count}")
    print(f"Missing assets: {summary.missing_count}")
    print(f"Blocking EDA assets: {summary.blocking_eda_count}")
    print(f"Ready for initial EDA: {summary.ready_for_eda}")


if __name__ == "__main__":
    main()
