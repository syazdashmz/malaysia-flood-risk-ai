from datetime import datetime

from floodrisk.data.infobanjir_water_level import (
    build_station_options_url,
    build_water_level_result_url,
    build_water_level_url,
    compute_water_level_status,
    parse_district_options_from_html,
    parse_float,
    parse_infobanjir_last_updated,
    parse_station_options_from_html,
    parse_water_level_records_from_html,
    summarize_water_level_records,
)

SAMPLE_STATE_HTML = """
<select id="district" name="district">
  <option value="ALL">ALL</option>
  <option value="Gombak">Gombak</option>
  <option value="Hulu Langat">Hulu Langat</option>
  <option value="Hulu Selangor">Hulu Selangor</option>
</select>
"""

SAMPLE_STATION_OPTIONS_HTML = """
<option value='ALL'>ALL</option>
<option value='3516026_'>Sg. Kerling di Kerling</option>
<option value='3018103_'>Sg. Semenyih di Kg. Pasir</option>
"""

SAMPLE_HTML = """
<table>
  <tr>
    <th>No.</th><th>Station ID</th><th>Station Name</th><th>District</th>
    <th>Main Basin</th><th>Sub River Basin</th><th>Last Updated</th>
    <th>Water Level (m)</th><th>Normal</th><th>Alert</th><th>Warning</th><th>Danger</th>
  </tr>
  <tr>
    <td>1</td><td>3516423</td><td>Sg. Kerling di Kerling</td><td>Hulu Selangor</td>
    <td>Sungai Selangor</td><td>Sg. Kerling</td><td>11/06/2026 07:15</td>
    <td>44.04</td><td>45.00</td><td>47.60</td><td>47.90</td><td>48.30</td>
  </tr>
  <tr>
    <td>2</td><td>3018401</td><td>Sg. Semenyih di Kg. Pasir</td><td>Hulu Langat</td>
    <td>Sungai Langat</td><td>Sg. Semenyih</td><td>11/06/2026 07:00</td>
    <td>49.70</td><td>48.30</td><td>48.80</td><td>49.80</td><td>50.30</td>
  </tr>
</table>
"""


def test_build_water_level_url_uses_public_infobanjir_pattern():
    url = build_water_level_url(state_code="SEL")

    assert url.startswith("https://publicinfobanjir.water.gov.my")
    assert "/aras-air/data-paras-air/" in url
    assert "state=SEL" in url
    assert "lang=en" in url


def test_build_station_options_url_uses_public_endpoint():
    url = build_station_options_url(district="Hulu Selangor")

    assert "searchstationwl.php" in url
    assert "name=Hulu+Selangor" in url
    assert "lang=en" in url


def test_build_water_level_result_url_uses_station_specific_endpoint():
    url = build_water_level_result_url(
        state_code="SEL",
        district="Hulu Selangor",
        station_id="3516026_",
    )

    assert "searchresultwaterlevel.php" in url
    assert "state=SEL" in url
    assert "district=Hulu+Selangor" in url
    assert "station=3516026_" in url


def test_parse_district_options_from_html_excludes_all():
    districts = parse_district_options_from_html(SAMPLE_STATE_HTML)

    assert districts == ["Gombak", "Hulu Langat", "Hulu Selangor"]


def test_parse_station_options_from_html_excludes_all():
    stations = parse_station_options_from_html(
        SAMPLE_STATION_OPTIONS_HTML,
        district="Hulu Selangor",
    )

    assert len(stations) == 2
    assert stations[0].district == "Hulu Selangor"
    assert stations[0].station_id == "3516026_"
    assert stations[0].station_name == "Sg. Kerling di Kerling"


def test_parse_float_treats_invalid_sensor_value_as_none():
    assert parse_float("44.04") == 44.04
    assert parse_float("-9999.00") is None
    assert parse_float("not available") is None


def test_compute_water_level_status_from_thresholds():
    assert (
        compute_water_level_status(
            water_level_m=44.0,
            alert_threshold_m=47.6,
            warning_threshold_m=47.9,
            danger_threshold_m=48.3,
        )
        == "normal"
    )
    assert (
        compute_water_level_status(
            water_level_m=49.0,
            alert_threshold_m=47.6,
            warning_threshold_m=47.9,
            danger_threshold_m=50.0,
        )
        == "warning"
    )
    assert (
        compute_water_level_status(
            water_level_m=51.0,
            alert_threshold_m=47.6,
            warning_threshold_m=47.9,
            danger_threshold_m=50.0,
        )
        == "danger"
    )


def test_parse_water_level_records_from_html_extracts_station_rows():
    records = parse_water_level_records_from_html(
        SAMPLE_HTML,
        source_url="https://example.test",
        state_code="SEL",
        state_name="Selangor",
    )

    assert len(records) == 2
    assert records[0].station_id == "3516423"
    assert records[0].station_name == "Sg. Kerling di Kerling"
    assert records[0].district == "Hulu Selangor"
    assert records[0].computed_status == "normal"
    assert records[1].computed_status == "alert"


def test_summarize_water_level_records_counts_statuses():
    records = parse_water_level_records_from_html(
        SAMPLE_HTML,
        source_url="https://example.test",
        state_code="SEL",
        state_name="Selangor",
    )

    summary = summarize_water_level_records(records)

    assert summary["source_id"] == "public_infobanjir_water_level"
    assert summary["record_count"] == 2
    assert summary["states"] == ["Selangor"]
    assert summary["status_counts"] == {"normal": 1, "alert": 1}
    assert summary["alert_or_worse_count"] == 1


def test_fetch_infobanjir_water_level_script_exists():
    from pathlib import Path

    script_path = Path("scripts/fetch_infobanjir_water_level.py")
    content = script_path.read_text(encoding="utf-8")

    assert script_path.exists()
    assert "fetch_water_level_records_for_state" in content
    assert "infobanjir_water_level_summary.json" in content


def test_parse_infobanjir_last_updated_parses_source_timestamp():
    parsed = parse_infobanjir_last_updated("16/10/2018 15:45")

    assert parsed == datetime(2018, 10, 16, 15, 45)


def test_summarize_water_level_records_marks_stale_data():
    stale_html = """
    <table>
      <tr>
        <td>1</td><td>3516026</td><td>Sg.Kerling di Kerling</td>
        <td>Hulu Selangor</td><td>Sg.Selangor</td><td>Not Available</td>
        <td>16/10/2018 15:45</td><td>44.44</td><td>45.00</td>
        <td>47.60</td><td>47.81</td><td>48.30</td>
      </tr>
    </table>
    """
    records = parse_water_level_records_from_html(
        stale_html,
        source_url="https://example.test",
        state_code="SEL",
        state_name="Selangor",
    )

    summary = summarize_water_level_records(
        records,
        reference_datetime=datetime(2026, 6, 11, 8, 0),
    )

    assert summary["parseable_last_updated_count"] == 1
    assert summary["oldest_last_updated"] == "16/10/2018 15:45"
    assert summary["latest_last_updated"] == "16/10/2018 15:45"
    assert summary["data_freshness_status"] == "stale"
    assert summary["is_current"] is False
