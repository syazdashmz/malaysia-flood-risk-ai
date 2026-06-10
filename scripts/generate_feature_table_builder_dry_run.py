"""Generate feature table builder dry-run report."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

REPORT_PATH = PROJECT_ROOT / "reports" / "feature_table_builder_dry_run.md"


def main() -> None:
    from floodrisk.ml.feature_table_builder import (
        build_feature_table_preview,
        write_feature_table_builder_report,
    )

    preview = build_feature_table_preview(PROJECT_ROOT, output_allowed=False)
    output_path = write_feature_table_builder_report(preview, REPORT_PATH)

    print(f"Generated feature table builder dry-run report: {output_path}")
    print(f"Source exists: {preview.source_exists}")
    print(f"Source rows: {preview.source_row_count}")
    print(f"Mapped training columns: {len(preview.mapped_training_columns)}")
    print(f"Missing training columns: {len(preview.missing_training_columns)}")
    print(f"Target available: {preview.target_available}")
    print(f"Can create real training table: {preview.can_create_real_training_table}")


if __name__ == "__main__":
    main()
