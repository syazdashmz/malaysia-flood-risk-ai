"""Fetch Public InfoBanjir water-level table data."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from floodrisk.data.infobanjir_water_level import (  # noqa: E402
    fetch_water_level_records_for_state,
    save_json,
    summarize_water_level_records,
    water_level_records_to_dicts,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch public InfoBanjir river water-level station rows."
    )
    parser.add_argument(
        "--state-code",
        default="SEL",
        help="Public InfoBanjir state code, e.g. SEL.",
    )
    parser.add_argument(
        "--state-name",
        default="Selangor",
        help="Human-readable state name.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "data" / "processed" / "infobanjir" / "water_level_latest.json",
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=PROJECT_ROOT / "reports" / "infobanjir_water_level_summary.json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    records = fetch_water_level_records_for_state(
        state_code=args.state_code,
        state_name=args.state_name,
    )

    rows = water_level_records_to_dicts(records)
    summary = summarize_water_level_records(records)

    save_json(rows, args.output)
    save_json(summary, args.summary_output)

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
