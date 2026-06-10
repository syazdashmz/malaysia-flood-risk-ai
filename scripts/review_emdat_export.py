"""Review a local EM-DAT export without approving it for training."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


def main() -> None:
    from floodrisk.sources.emdat import (
        build_emdat_export_review,
        write_emdat_export_review_outputs,
    )

    review = build_emdat_export_review(PROJECT_ROOT)
    interim_path, summary_path, report_path = write_emdat_export_review_outputs(
        review,
        project_root=PROJECT_ROOT,
    )

    print(f"Raw export exists: {review.raw_exists}")
    print(f"Malaysia flood rows: {review.malaysia_flood_rows}")
    print(f"Rows with latitude/longitude: {review.rows_with_lat_lon}")
    print(f"Rows with admin units: {review.rows_with_admin_units}")
    print(f"Ready for training: {review.ready_for_training}")
    print(f"Wrote interim review table: {interim_path}")
    print(f"Wrote review summary: {summary_path}")
    print(f"Wrote review report: {report_path}")


if __name__ == "__main__":
    main()
