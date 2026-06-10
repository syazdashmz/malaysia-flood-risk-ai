"""Generate feature table generation plan report."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

REPORT_PATH = PROJECT_ROOT / "reports" / "feature_table_plan.md"


def main() -> None:
    from floodrisk.ml.feature_table_plan import (
        build_feature_table_plan,
        write_feature_table_plan_report,
    )

    plan_items = build_feature_table_plan()
    output_path = write_feature_table_plan_report(plan_items, REPORT_PATH)

    ready_count = sum(1 for item in plan_items if item.ready_now)
    missing_count = len(plan_items) - ready_count

    print(f"Generated feature table plan report: {output_path}")
    print(f"Planned columns: {len(plan_items)}")
    print(f"Columns ready now: {ready_count}")
    print(f"Columns requiring future data work: {missing_count}")
    print("Real ML training allowed now: False")


if __name__ == "__main__":
    main()
