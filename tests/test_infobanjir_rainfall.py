from datetime import datetime
from pathlib import Path

from floodrisk.data.infobanjir_rainfall import (
    build_rainfall_result_url,
    build_rainfall_station_options_url,
    build_rainfall_url,
    compute_rainfall_status,
    extract_html_cells,
    extract_rainfall_date_headers,
    parse_district_options_from_html,
    parse_float,
    parse_infobanjir_rainfall_last_updated,
    parse_rainfall_records_from_html,
    parse_rainfall_station_options_from_html,
    summarize_rainfall_records,
)

SAMPLE_STATE_HTML = """
<select id="district" name="district">
  <option value="ALL">ALL</option>
  <option value="Gombak">Gombak</option>
  <option value="Hulu Langat">Hulu Langat</option>
</select>
"""

SAMPLE_STATION_OPTIONS_HTML = """
<option value='ALL'>ALL</option>
<option value='26557'>Kg. Kemensah</option>
<option value='3018103_'>Kg. Pasir</option>
"""

SAMPLE_RAINFALL_HTML = """
<table>
<thead>
<tr>
  <th></th><th></th><th></th><th></th><th></th>
  <th colspan='6'></th>
  <th>(11/06/2026)</th>
  <th>()</th>
</tr>
<tr>
  <th>05/06/2026</th>
  <th>06/06/2026</th>
  <th>07/06/2026</th>
  <th>08/06/2026</th>
  <th>09/06/2026</th>
  <th>10/06/2026</th>
</tr>
</thead>
<tbody>
<tr></tr></tr></tr>
<td data-th='No'>1</td>
<td data-th='Station ID'>3018103</td>
<td>Kg. Pasir</td>
<td>Hulu Langat</td>
<td>11/06/2026 08:00:00</td>
<td>36.5</td>
<td>0.0</td>
<td>2.0</td>
<td>1.5</td>
<td>15.0</td>
<td>0.0</td>
<td><a href='/index.php/rf-graph/?stationid=3018103_' target='_blank'>0.0</a></td>
<td class='info'>0.0</a></td>
</tbody>
</table>
"""


def test_build_rainfall_url_uses_public_infobanjir_pattern():
    url = build_rainfall_url(state_code="SEL")

    assert url.startswith("https://publicinfobanjir.water.gov.my")
    assert "/hujan/data-hujan/" in url
    assert "state=SEL" in url
    assert "lang=en" in url


def test_build_rainfall_station_options_url_uses_public_endpoint():
    url = build_rainfall_station_options_url(district="Hulu Langat")

    assert "searchstationRF.php" in url
    assert "name=Hulu+Langat" in url
    assert "lang=en" in url


def test_build_rainfall_result_url_uses_station_specific_endpoint():
    url = build_rainfall_result_url(
        state_code="SEL",
        district="Hulu Langat",
        station_id="3018103_",
    )

    assert "searchresultrainfall.php" in url
    assert "state=SEL" in url
    assert "district=Hulu+Langat" in url
    assert "station=3018103_" in url


def test_parse_district_options_from_html_excludes_all():
    districts = parse_district_options_from_html(SAMPLE_STATE_HTML)

    assert districts == ["Gombak", "Hulu Langat"]


def test_parse_rainfall_station_options_from_html_excludes_all():
    stations = parse_rainfall_station_options_from_html(
        SAMPLE_STATION_OPTIONS_HTML,
        district="Hulu Langat",
    )

    assert len(stations) == 2
    assert stations[0].district == "Hulu Langat"
    assert stations[0].station_id == "26557"
    assert stations[0].station_name == "Kg. Kemensah"


def test_extract_html_cells_handles_malformed_cells():
    cells = extract_html_cells(SAMPLE_RAINFALL_HTML, "td")

    assert len(cells) == 13
    assert cells[1] == "3018103"
    assert cells[2] == "Kg. Pasir"
    assert cells[11] == "0.0"


def test_extract_rainfall_date_headers_maps_historical_and_current_dates():
    historical_dates, current_day_date = extract_rainfall_date_headers(SAMPLE_RAINFALL_HTML)

    assert historical_dates == [
        "05/06/2026",
        "06/06/2026",
        "07/06/2026",
        "08/06/2026",
        "09/06/2026",
        "10/06/2026",
    ]
    assert current_day_date == "11/06/2026"


def test_parse_float_parses_rainfall_values():
    assert parse_float("36.5") == 36.5
    assert parse_float("0.0") == 0.0
    assert parse_float("not available") is None


def test_compute_rainfall_status_from_values():
    assert compute_rainfall_status([0.0, 0.0]) == "no_rain"
    assert compute_rainfall_status([0.0, 1.5]) == "rain_observed"
    assert compute_rainfall_status([None]) == "unknown"


def test_parse_infobanjir_rainfall_last_updated_parses_timestamp():
    parsed = parse_infobanjir_rainfall_last_updated("11/06/2026 08:00:00")

    assert parsed == datetime(2026, 6, 11, 8, 0, 0)


def test_parse_rainfall_records_from_html_extracts_station_row():
    records = parse_rainfall_records_from_html(
        SAMPLE_RAINFALL_HTML,
        source_url="https://example.test",
        state_code="SEL",
        state_name="Selangor",
    )

    assert len(records) == 1
    assert records[0].station_id == "3018103"
    assert records[0].station_name == "Kg. Pasir"
    assert records[0].district == "Hulu Langat"
    assert records[0].last_updated == "11/06/2026 08:00:00"
    assert records[0].daily_rainfall_mm[0] == {
        "date": "05/06/2026",
        "rainfall_mm": 36.5,
    }
    assert records[0].current_day_date == "11/06/2026"
    assert records[0].current_day_rainfall_mm == 0.0
    assert records[0].total_recent_rainfall_mm == 55.0
    assert records[0].max_recent_rainfall_mm == 36.5
    assert records[0].computed_status == "rain_observed"


def test_summarize_rainfall_records_marks_current_data():
    records = parse_rainfall_records_from_html(
        SAMPLE_RAINFALL_HTML,
        source_url="https://example.test",
        state_code="SEL",
        state_name="Selangor",
    )

    summary = summarize_rainfall_records(
        records,
        reference_datetime=datetime(2026, 6, 11, 9, 0),
    )

    assert summary["source_id"] == "public_infobanjir_rainfall"
    assert summary["record_count"] == 1
    assert summary["states"] == ["Selangor"]
    assert summary["status_counts"] == {"rain_observed": 1}
    assert summary["rain_observed_count"] == 1
    assert summary["max_recent_rainfall_mm"] == 36.5
    assert summary["latest_last_updated"] == "11/06/2026 08:00:00"
    assert summary["data_freshness_status"] == "current"
    assert summary["is_current"] is True


def test_fetch_infobanjir_rainfall_script_exists():
    script_path = Path("scripts/fetch_infobanjir_rainfall.py")
    content = script_path.read_text(encoding="utf-8")

    assert script_path.exists()
    assert "fetch_rainfall_records_for_state" in content
    assert "infobanjir_rainfall_summary.json" in content
