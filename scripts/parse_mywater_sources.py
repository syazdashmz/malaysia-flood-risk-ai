"""Parse MyWater/DID spreadsheet exports into lightweight table profiles."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from floodrisk.data.mywater_sources import (  # noqa: E402
    DEFAULT_MYWATER_RAW_DIR,
    discover_mywater_files,
    profile_mywater_sources,
    save_mywater_profiles,
    summarize_mywater_profiles,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse MyWater/DID exported spreadsheet files.")
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=DEFAULT_MYWATER_RAW_DIR,
        help="Directory containing MyWater/DID .xls/.xlsx exports.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "data" / "processed" / "mywater" / "mywater_table_profiles.json",
        help="Output JSON file for parsed table profiles.",
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=PROJECT_ROOT / "reports" / "mywater_parse_summary.json",
        help="Output JSON file for parse summary.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    files = discover_mywater_files(args.raw_dir)
    profiles = profile_mywater_sources(files)

    save_mywater_profiles(profiles, args.output)

    summary = summarize_mywater_profiles(profiles)
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
