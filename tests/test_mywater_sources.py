from pathlib import Path

from floodrisk.data.mywater_sources import (
    classify_mywater_file,
    clean_mywater_dataframe,
    normalize_mywater_column_name,
    profile_mywater_file,
    summarize_mywater_profiles,
)


def test_normalize_mywater_column_name_returns_snake_case():
    assert normalize_mywater_column_name("Station Name") == "station_name"
    assert normalize_mywater_column_name("Flood Cause (%)") == "flood_cause"
    assert normalize_mywater_column_name("") == "unnamed_column"


def test_classify_mywater_file_matches_known_exports():
    assert (
        classify_mywater_file(
            Path("Summary List of Location and Cause of Flood - 20260610_114539.xls")
        )
        == "flood_location_cause"
    )
    assert (
        classify_mywater_file(
            Path("Summary Status List of Flood Monitoring Station - 20260610_114543.xls")
        )
        == "flood_monitoring_station_status"
    )
    assert (
        classify_mywater_file(Path("Total Operation Modes By Year - 20260610_114547.xls"))
        == "operation_modes_by_year"
    )
    assert (
        classify_mywater_file(Path("Total Zone By Status - 20260610_114551.xls"))
        == "zone_by_status"
    )


def test_clean_mywater_dataframe_removes_empty_rows_and_columns():
    import pandas as pd

    df = pd.DataFrame(
        {
            "Station Name": ["Station A", None],
            "Status": ["Normal", None],
            "Empty": [None, None],
        }
    )

    cleaned = clean_mywater_dataframe(df)

    assert list(cleaned.columns) == ["station_name", "status"]
    assert len(cleaned) == 1


def test_profile_mywater_file_reads_html_style_xls(tmp_path):
    html_export = tmp_path / "Summary List of Location and Cause of Flood - sample.xls"
    html_export.write_text(
        """
        <table>
            <tr><th>Location</th><th>Cause</th></tr>
            <tr><td>Kuala Lumpur</td><td>Heavy rain</td></tr>
            <tr><td>Selangor</td><td>River overflow</td></tr>
        </table>
        """,
        encoding="utf-8",
    )

    profiles = profile_mywater_file(html_export)

    assert len(profiles) == 1
    assert profiles[0].source_kind == "flood_location_cause"
    assert profiles[0].row_count == 2
    assert profiles[0].columns == ["location", "cause"]


def test_summarize_mywater_profiles_counts_files_and_rows(tmp_path):
    html_export = tmp_path / "Total Zone By Status - sample.xls"
    html_export.write_text(
        """
        <table>
            <tr><th>Zone</th><th>Status</th></tr>
            <tr><td>North</td><td>Normal</td></tr>
        </table>
        """,
        encoding="utf-8",
    )

    profiles = profile_mywater_file(html_export)
    summary = summarize_mywater_profiles(profiles)

    assert summary["source_id"] == "mywater_did_exports"
    assert summary["source_file_count"] == 1
    assert summary["table_count"] == 1
    assert summary["total_rows"] == 1


def test_parse_mywater_script_exists():
    script_path = Path("scripts/parse_mywater_sources.py")
    content = script_path.read_text(encoding="utf-8")

    assert script_path.exists()
    assert "profile_mywater_sources" in content
    assert "mywater_parse_summary.json" in content
