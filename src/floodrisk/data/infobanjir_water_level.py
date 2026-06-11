"""Public InfoBanjir water-level page parser."""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from floodrisk.version import __version__

INFOBANJIR_BASE_URL = "https://publicinfobanjir.water.gov.my"
WATER_LEVEL_PATH = "/aras-air/data-paras-air/"
STATION_OPTIONS_PATH = "/wp-content/themes/shapely/agency/searchstationwl.php"
WATER_LEVEL_RESULT_PATH = "/wp-content/themes/shapely/agency/searchresultwaterlevel.php"
USER_AGENT = f"malaysia-flood-risk-ai/{__version__}"

INVALID_WATER_LEVEL_VALUES = {-9999.0, -9999.00}
INFOBANJIR_LAST_UPDATED_FORMAT = "%d/%m/%Y %H:%M"
DEFAULT_FRESHNESS_MAX_AGE_HOURS = 24.0


@dataclass(frozen=True)
class InfoBanjirStationOption:
    """One station option returned by Public InfoBanjir."""

    district: str
    station_id: str
    station_name: str


@dataclass(frozen=True)
class InfoBanjirWaterLevelRecord:
    """One parsed Public InfoBanjir river water-level row."""

    source_id: str
    source_url: str
    state_code: str
    state_name: str
    station_no: int | None
    station_id: str
    station_name: str
    district: str
    main_basin: str
    sub_river_basin: str
    last_updated: str
    water_level_m: float | None
    normal_threshold_m: float | None
    alert_threshold_m: float | None
    warning_threshold_m: float | None
    danger_threshold_m: float | None
    computed_status: str


class SimpleHTMLTableParser(HTMLParser):
    """Small no-dependency parser for HTML table rows."""

    def __init__(self) -> None:
        super().__init__()
        self.tables: list[list[list[str]]] = []
        self._current_table: list[list[str]] | None = None
        self._current_row: list[str] | None = None
        self._current_cell: list[str] | None = None

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        del attrs
        normalized_tag = tag.lower()

        if normalized_tag == "table":
            self._current_table = []
        elif normalized_tag == "tr" and self._current_table is not None:
            self._current_row = []
        elif normalized_tag in {"td", "th"} and self._current_row is not None:
            self._current_cell = []

    def handle_data(self, data: str) -> None:
        if self._current_cell is not None:
            self._current_cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        normalized_tag = tag.lower()

        if normalized_tag in {"td", "th"} and self._current_cell is not None:
            cell_text = " ".join("".join(self._current_cell).split())
            if self._current_row is not None:
                self._current_row.append(cell_text)
            self._current_cell = None

        elif normalized_tag == "tr" and self._current_row is not None:
            if any(cell for cell in self._current_row) and self._current_table is not None:
                self._current_table.append(self._current_row)
            self._current_row = None

        elif normalized_tag == "table" and self._current_table is not None:
            if self._current_table:
                self.tables.append(self._current_table)
            self._current_table = None


class SimpleHTMLSelectParser(HTMLParser):
    """Small no-dependency parser for HTML select option values."""

    def __init__(self) -> None:
        super().__init__()
        self.selects: dict[str, list[tuple[str, str]]] = {}
        self._current_select_key: str | None = None
        self._current_option_value: str | None = None
        self._current_option_label: list[str] | None = None

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        normalized_tag = tag.lower()
        attrs_dict = {key.lower(): value for key, value in attrs}

        if normalized_tag == "select":
            select_key = attrs_dict.get("id") or attrs_dict.get("name")
            self._current_select_key = select_key
            if select_key and select_key not in self.selects:
                self.selects[select_key] = []

        elif normalized_tag == "option" and self._current_select_key:
            self._current_option_value = attrs_dict.get("value") or ""
            self._current_option_label = []

    def handle_data(self, data: str) -> None:
        if self._current_option_label is not None:
            self._current_option_label.append(data)

    def handle_endtag(self, tag: str) -> None:
        normalized_tag = tag.lower()

        if normalized_tag == "option" and self._current_option_label is not None:
            label = " ".join("".join(self._current_option_label).split())
            value = self._current_option_value or ""

            if self._current_select_key:
                self.selects.setdefault(self._current_select_key, []).append((value, label))

            self._current_option_value = None
            self._current_option_label = None

        elif normalized_tag == "select":
            self._current_select_key = None


def build_water_level_url(
    *,
    state_code: str,
    lang: str = "en",
) -> str:
    """Build Public InfoBanjir river water-level page URL for one state."""
    params = urlencode({"state": state_code, "lang": lang})
    return f"{INFOBANJIR_BASE_URL}{WATER_LEVEL_PATH}?{params}"


def build_station_options_url(
    *,
    district: str,
    lang: str = "en",
    login_status: str = "",
) -> str:
    """Build Public InfoBanjir station option endpoint URL."""
    params = urlencode(
        {
            "name": district,
            "lang": lang,
            "loginStatus": login_status,
        }
    )
    return f"{INFOBANJIR_BASE_URL}{STATION_OPTIONS_PATH}?{params}"


def build_water_level_result_url(
    *,
    state_code: str,
    district: str,
    station_id: str,
) -> str:
    """Build Public InfoBanjir station-specific water-level result URL."""
    params = urlencode(
        {
            "state": state_code,
            "district": district,
            "station": station_id,
        }
    )
    return f"{INFOBANJIR_BASE_URL}{WATER_LEVEL_RESULT_PATH}?{params}"


def fetch_html(
    url: str,
    timeout_seconds: int = 30,
    referer: str | None = None,
) -> str:
    """Fetch a public HTML page."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,*/*",
    }

    if referer:
        headers["Referer"] = referer

    request = Request(url, headers=headers)

    with urlopen(request, timeout=timeout_seconds) as response:
        return response.read().decode("utf-8", errors="ignore")


def parse_html_tables(html: str) -> list[list[list[str]]]:
    """Parse all HTML tables from a page."""
    parser = SimpleHTMLTableParser()
    parser.feed(html)
    return parser.tables


def parse_select_options(html: str, select_key: str) -> list[tuple[str, str]]:
    """Parse option values for a select element by id or name."""
    parser = SimpleHTMLSelectParser()
    parser.feed(html)
    return parser.selects.get(select_key, [])


def parse_district_options_from_html(html: str) -> list[str]:
    """Parse district options from a Public InfoBanjir water-level page."""
    options = parse_select_options(html, "district")

    return [
        label
        for value, label in options
        if value.strip() and value.strip().upper() != "ALL" and label.strip()
    ]


def parse_station_options_from_html(
    html: str,
    *,
    district: str,
) -> list[InfoBanjirStationOption]:
    """Parse station options returned by Public InfoBanjir."""
    parser = SimpleHTMLSelectParser()
    parser.feed(f'<select id="station">{html}</select>')

    station_options: list[InfoBanjirStationOption] = []

    for value, label in parser.selects.get("station", []):
        station_id = value.strip()
        station_name = label.strip()

        if not station_id or station_id.upper() == "ALL":
            continue

        station_options.append(
            InfoBanjirStationOption(
                district=district,
                station_id=station_id,
                station_name=station_name,
            )
        )

    return station_options


def parse_int(value: Any) -> int | None:
    """Parse an integer safely."""
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def parse_float(value: Any) -> float | None:
    """Parse a float safely."""
    try:
        parsed_value = float(str(value).strip().replace(",", ""))
    except (TypeError, ValueError):
        return None

    if parsed_value in INVALID_WATER_LEVEL_VALUES:
        return None

    return parsed_value


def compute_water_level_status(
    *,
    water_level_m: float | None,
    alert_threshold_m: float | None,
    warning_threshold_m: float | None,
    danger_threshold_m: float | None,
) -> str:
    """Compute status from water level and thresholds."""
    if water_level_m is None:
        return "unknown"

    if danger_threshold_m is not None and water_level_m >= danger_threshold_m:
        return "danger"

    if warning_threshold_m is not None and water_level_m >= warning_threshold_m:
        return "warning"

    if alert_threshold_m is not None and water_level_m >= alert_threshold_m:
        return "alert"

    return "normal"


def parse_infobanjir_last_updated(value: str) -> datetime | None:
    """Parse Public InfoBanjir last-updated timestamps."""
    try:
        return datetime.strptime(value.strip(), INFOBANJIR_LAST_UPDATED_FORMAT)
    except (AttributeError, ValueError):
        return None


def classify_data_freshness(
    latest_last_updated: datetime | None,
    *,
    reference_datetime: datetime | None = None,
    freshness_max_age_hours: float = DEFAULT_FRESHNESS_MAX_AGE_HOURS,
) -> dict[str, Any]:
    """Classify whether fetched Public InfoBanjir data is fresh enough."""
    if latest_last_updated is None:
        return {
            "data_freshness_status": "unknown",
            "data_freshness_age_hours": None,
            "data_freshness_max_age_hours": freshness_max_age_hours,
            "is_current": False,
        }

    now = reference_datetime or datetime.now()
    age_hours = (now - latest_last_updated).total_seconds() / 3600

    if age_hours < 0:
        status = "future_timestamp"
    elif age_hours <= freshness_max_age_hours:
        status = "current"
    else:
        status = "stale"

    return {
        "data_freshness_status": status,
        "data_freshness_age_hours": round(age_hours, 2),
        "data_freshness_max_age_hours": freshness_max_age_hours,
        "is_current": status == "current",
    }


def looks_like_water_level_data_row(row: list[str]) -> bool:
    """Return True if a table row appears to be a water-level station row."""
    if len(row) < 12:
        return False

    return parse_int(row[0]) is not None and bool(str(row[1]).strip())


def water_level_record_from_row(
    row: list[str],
    *,
    source_url: str,
    state_code: str,
    state_name: str,
) -> InfoBanjirWaterLevelRecord:
    """Convert one table row into a normalized water-level record."""
    water_level_m = parse_float(row[7])
    alert_threshold_m = parse_float(row[9])
    warning_threshold_m = parse_float(row[10])
    danger_threshold_m = parse_float(row[11])

    return InfoBanjirWaterLevelRecord(
        source_id="public_infobanjir_water_level",
        source_url=source_url,
        state_code=state_code,
        state_name=state_name,
        station_no=parse_int(row[0]),
        station_id=str(row[1]).strip(),
        station_name=str(row[2]).strip(),
        district=str(row[3]).strip(),
        main_basin=str(row[4]).strip(),
        sub_river_basin=str(row[5]).strip(),
        last_updated=str(row[6]).strip(),
        water_level_m=water_level_m,
        normal_threshold_m=parse_float(row[8]),
        alert_threshold_m=alert_threshold_m,
        warning_threshold_m=warning_threshold_m,
        danger_threshold_m=danger_threshold_m,
        computed_status=compute_water_level_status(
            water_level_m=water_level_m,
            alert_threshold_m=alert_threshold_m,
            warning_threshold_m=warning_threshold_m,
            danger_threshold_m=danger_threshold_m,
        ),
    )


def parse_water_level_records_from_html(
    html: str,
    *,
    source_url: str,
    state_code: str,
    state_name: str,
) -> list[InfoBanjirWaterLevelRecord]:
    """Parse water-level station records from Public InfoBanjir HTML."""
    records: list[InfoBanjirWaterLevelRecord] = []

    for table in parse_html_tables(html):
        for row in table:
            if looks_like_water_level_data_row(row):
                records.append(
                    water_level_record_from_row(
                        row,
                        source_url=source_url,
                        state_code=state_code,
                        state_name=state_name,
                    )
                )

    return records


def fetch_station_options_for_district(
    *,
    district: str,
    timeout_seconds: int = 30,
    referer: str | None = None,
) -> list[InfoBanjirStationOption]:
    """Fetch station options for one district."""
    url = build_station_options_url(district=district)
    html = fetch_html(url, timeout_seconds=timeout_seconds, referer=referer)

    return parse_station_options_from_html(html, district=district)


def fetch_water_level_record_for_station(
    *,
    state_code: str,
    state_name: str,
    district: str,
    station_id: str,
    timeout_seconds: int = 30,
    referer: str | None = None,
) -> list[InfoBanjirWaterLevelRecord]:
    """Fetch water-level row for one station."""
    url = build_water_level_result_url(
        state_code=state_code,
        district=district,
        station_id=station_id,
    )
    html = fetch_html(url, timeout_seconds=timeout_seconds, referer=referer)

    return parse_water_level_records_from_html(
        html,
        source_url=url,
        state_code=state_code,
        state_name=state_name,
    )


def fetch_water_level_records_for_state(
    *,
    state_code: str,
    state_name: str,
    timeout_seconds: int = 30,
) -> list[InfoBanjirWaterLevelRecord]:
    """Fetch Public InfoBanjir water-level records for one state."""
    state_url = build_water_level_url(state_code=state_code)
    state_html = fetch_html(state_url, timeout_seconds=timeout_seconds)

    districts = parse_district_options_from_html(state_html)
    records: list[InfoBanjirWaterLevelRecord] = []
    seen_station_keys: set[tuple[str, str]] = set()

    for district in districts:
        station_options = fetch_station_options_for_district(
            district=district,
            timeout_seconds=timeout_seconds,
            referer=state_url,
        )

        for station_option in station_options:
            station_key = (district, station_option.station_id)

            if station_key in seen_station_keys:
                continue

            seen_station_keys.add(station_key)

            records.extend(
                fetch_water_level_record_for_station(
                    state_code=state_code,
                    state_name=state_name,
                    district=district,
                    station_id=station_option.station_id,
                    timeout_seconds=timeout_seconds,
                    referer=state_url,
                )
            )

    return records


def water_level_records_to_dicts(
    records: Iterable[InfoBanjirWaterLevelRecord],
) -> list[dict[str, Any]]:
    """Convert water-level records into serializable dictionaries."""
    return [asdict(record) for record in records]


def summarize_water_level_records(
    records: list[InfoBanjirWaterLevelRecord],
    *,
    reference_datetime: datetime | None = None,
    freshness_max_age_hours: float = DEFAULT_FRESHNESS_MAX_AGE_HOURS,
) -> dict[str, Any]:
    """Summarize parsed Public InfoBanjir water-level records."""
    status_counts: dict[str, int] = {}
    parsed_last_updated_values = [
        parsed_value
        for record in records
        if (parsed_value := parse_infobanjir_last_updated(record.last_updated)) is not None
    ]

    oldest_last_updated = min(parsed_last_updated_values) if parsed_last_updated_values else None
    latest_last_updated = max(parsed_last_updated_values) if parsed_last_updated_values else None

    for record in records:
        status_counts[record.computed_status] = status_counts.get(record.computed_status, 0) + 1

    freshness = classify_data_freshness(
        latest_last_updated,
        reference_datetime=reference_datetime,
        freshness_max_age_hours=freshness_max_age_hours,
    )

    return {
        "source_id": "public_infobanjir_water_level",
        "record_count": len(records),
        "states": sorted({record.state_name for record in records}),
        "districts": sorted({record.district for record in records if record.district}),
        "status_counts": status_counts,
        "alert_or_worse_count": sum(
            status_counts.get(status, 0) for status in ["alert", "warning", "danger"]
        ),
        "parseable_last_updated_count": len(parsed_last_updated_values),
        "oldest_last_updated": (
            oldest_last_updated.strftime(INFOBANJIR_LAST_UPDATED_FORMAT)
            if oldest_last_updated
            else None
        ),
        "latest_last_updated": (
            latest_last_updated.strftime(INFOBANJIR_LAST_UPDATED_FORMAT)
            if latest_last_updated
            else None
        ),
        **freshness,
    }


def save_json(data: Any, output_path: Path) -> Path:
    """Save JSON output."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path
