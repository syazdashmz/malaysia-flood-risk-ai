import csv
from pathlib import Path

from floodrisk.data.profile import (
    CsvProfile,
    profile_csv,
    render_profiles_markdown,
    write_profiles_markdown,
)


def test_profile_csv_counts_rows_columns_and_missing_values(tmp_path: Path):
    input_path = tmp_path / "sample.csv"

    with input_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["location", "rainfall"])
        writer.writeheader()
        writer.writerow({"location": "Kuala Lumpur", "rainfall": "12"})
        writer.writerow({"location": "Shah Alam", "rainfall": ""})

    profile = profile_csv(input_path)

    assert profile.file_name == "sample.csv"
    assert profile.row_count == 2
    assert profile.column_count == 2
    assert profile.missing_counts["rainfall"] == 1


def test_render_profiles_markdown():
    markdown = render_profiles_markdown(
        [
            CsvProfile(
                file_name="sample.csv",
                row_count=2,
                column_count=1,
                columns=["location"],
                missing_counts={"location": 0},
            )
        ],
        title="Example Profile",
    )

    assert "# Example Profile" in markdown
    assert "sample.csv" in markdown
    assert "Rows: 2" in markdown
    assert "location" in markdown


def test_write_profiles_markdown(tmp_path: Path):
    output_path = tmp_path / "profile.md"

    saved_path = write_profiles_markdown(
        [
            CsvProfile(
                file_name="sample.csv",
                row_count=1,
                column_count=1,
                columns=["status"],
                missing_counts={"status": 0},
            )
        ],
        output_path,
    )

    assert saved_path.exists()
    assert "sample.csv" in saved_path.read_text(encoding="utf-8")
