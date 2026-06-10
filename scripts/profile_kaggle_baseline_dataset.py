from __future__ import annotations

import csv
from collections import Counter
from datetime import date
from pathlib import Path

RAW_PATH = Path("data/raw/kaggle/malaysia_flood_master.csv")
REPORT_PATH = Path("reports/kaggle_baseline_profile.md")


def clean(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def as_int(value: object) -> int:
    text = clean(value)
    if not text:
        return 0
    return int(float(text))


def parse_date(value: object) -> date | None:
    text = clean(value)
    if not text:
        return None

    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            import datetime as dt

            return dt.datetime.strptime(text, fmt).date()
        except ValueError:
            continue

    return None


def main() -> None:
    if not RAW_PATH.exists():
        raise SystemExit(f"Missing raw dataset: {RAW_PATH}")

    with RAW_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    columns = reader.fieldnames or []

    date_values = [parsed for row in rows if (parsed := parse_date(row.get("DATE")))]

    city_counts = Counter(clean(row.get("City")) for row in rows)
    flood_positive = sum(as_int(row.get("Flood")) == 1 for row in rows)
    flash_positive = sum(as_int(row.get("Flash_Flood")) == 1 for row in rows)
    flash_without_flood = sum(
        as_int(row.get("Flash_Flood")) == 1 and as_int(row.get("Flood")) != 1 for row in rows
    )

    missing_by_column = {
        column: sum(clean(row.get(column)) == "" for row in rows) for column in columns
    }

    report = [
        "# Kaggle Experimental Baseline Dataset Profile",
        "",
        "## Summary",
        "",
        "- Source role: experimental proxy baseline dataset",
        "- Official verified target source: False",
        "- Experimental training allowed: True",
        f"- Raw path: `{RAW_PATH.as_posix()}`",
        f"- Rows: {len(rows)}",
        f"- Columns: {len(columns)}",
        f"- Date range: {min(date_values).isoformat()} to {max(date_values).isoformat()}",
        f"- Cities: {len(city_counts)}",
        f"- Flood positive rows: {flood_positive}",
        f"- Flash flood positive rows: {flash_positive}",
        f"- Flash flood rows without Flood=1: {flash_without_flood}",
        "",
        "## Columns",
        "",
    ]

    report.extend(f"- `{column}`" for column in columns)

    report.extend(
        [
            "",
            "## City Counts",
            "",
        ]
    )

    report.extend(f"- {city}: {count}" for city, count in city_counts.most_common())

    report.extend(
        [
            "",
            "## Missing Values",
            "",
        ]
    )

    report.extend(f"- `{column}`: {count}" for column, count in missing_by_column.items())

    report.extend(
        [
            "",
            "## Decision",
            "",
            "Use this dataset for experimental baseline ML training only.",
            "Do not present it as the final official verified target source.",
            "",
        ]
    )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")

    print(f"Generated Kaggle baseline profile: {REPORT_PATH}")
    print(f"Rows: {len(rows)}")
    print(f"Columns: {len(columns)}")
    print(f"Flood positives: {flood_positive}")
    print(f"Flash flood positives: {flash_positive}")
    print(f"Cities: {len(city_counts)}")


if __name__ == "__main__":
    main()
