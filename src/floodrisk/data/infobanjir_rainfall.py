"""Public InfoBanjir rainfall page parser."""

from __future__ import annotations

import json
import re
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
RAINFALL_PATH = "/hujan/data-hujan/"
RAINFALL_STATION_OPTIONS_PATH = "/wp-content/themes/shapely/agency/searchstationRF.php"
RAINFALL_RESULT_PATH = "/wp-content/themes/shapely/agency/searchresultrainfall.php"
USER_AGENT = f"malaysia-flood-risk-ai/{__version__}"

RAINFALL_LAST_UPDATED_FORMATS = ("%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M")
RAINFALL_DATE_FORMAT = "%d/%m/%Y"
DEFAULT_FRESHNESS_MAX_AGE_HOURS = 24.0


@dataclass(frozen=True)
class InfoBanjirRainfallStationOption:
    """One rainfall station option returned by Public InfoBanjir."""

    district: str
    station_id: str
    station_name: str


@dataclass(frozen=True)
class InfoBanjirRainfallRecord:
    """One parsed Public InfoBanjir rainfall row."""

    source_id: str
    source_url: str
    state_code: str
    state_name: str
    station_no: int | None
    station_id: str
    station_name: str
    district: str
    last_updated: str
    daily_rainfall_mm: list[dict[str, Any]]
    current_day_date: str | None
    current_day_rainfall_mm: float | None
    extra_rainfall_mm: float | None
    total_recent_rainfall_mm: float | None
    max_recent_rainfall_mm: float | None
    computed_status: str


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


def build_rainfall_url(
    *,
    state_code: str,
    lang: str = "en",
) -> str:
    """Build Public InfoBanjir rainfall page URL for one state."""
    params = urlencode({"state": state_code, "lang": lang})
    return f"{INFOBANJIR_BASE_URL}{RAINFALL_PATH}?{params}"


def build_rainfall_station_options_url(
    *,
    district: str,
    lang: str = "en",
    login_status: str = "",
) -> str:
    """Build Public InfoBanjir rainfall station option endpoint URL."""
    params = urlencode(
        {
            "name": district,
            "lang": lang,
            "loginStatus": login_status,
        }
    )
    return f"{INFOBANJIR_BASE_URL}{RAINFALL_STATION_OPTIONS_PATH}?{params}"


def build_rainfall_result_url(
    *,
    state_code: str,
    district: str,
    station_id: str,
) -> str:
    """Build Public InfoBanjir station-specific rainfall result URL."""
    params = urlencode(
        {
            "state": state_code,
            "district": district,
            "station": station_id,
        }
    )
    return f"{INFOBANJIR_BASE_URL}{RAINFALL_RESULT_PATH}?{params}"


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


def parse_select_options(html: str, select_key: str) -> list[tuple[str, str]]:
    """Parse option values for a select element by id or name."""
    parser = SimpleHTMLSelectParser()
    parser.feed(html)
    return parser.selects.get(select_key, [])


def parse_district_options_from_html(html: str) -> list[str]:
    """Parse district options from a Public InfoBanjir rainfall page."""
    options = parse_select_options(html, "district")

    return [
        label
        for value, label in options
        if value.strip() and value.strip().upper() != "ALL" and label.strip()
    ]


def parse_rainfall_station_options_from_html(
    html: str,
    *,
    district: str,
) -> list[InfoBanjirRainfallStationOption]:
    """Parse rainfall station options returned by Public InfoBanjir."""
    parser = SimpleHTMLSelectParser()
    parser.feed(f'<select id="station">{html}</select>')

    station_options: list[InfoBanjirRainfallStationOption] = []

    for value, label in parser.selects.get("station", []):
        station_id = value.strip()
        station_name = label.strip()

        if not station_id or station_id.upper() == "ALL":
            continue

        station_options.append(
            InfoBanjirRainfallStationOption(
                district=district,
                station_id=station_id,
                station_name=station_name,
            )
        )

    return station_options


def strip_html_tags(value: str) -> str:
    """Remove HTML tags and normalize whitespace."""
    value = re.sub(r"<[^>]+>", "", value)
    return " ".join(value.split())


def extract_html_cells(html: str, tag_name: str) -> list[str]:
    """Extract HTML cell contents with a tolerant regex."""
    cells = re.findall(
        rf"<{tag_name}\b[^>]*>(.*?)</{tag_name}>",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return [strip_html_tags(cell) for cell in cells]


def extract_rainfall_date_headers(html: str) -> tuple[list[str], str | None]:
    """Extract historical and current rainfall date labels from response headers."""
    headers = extract_html_cells(html, "th")
    date_labels = []

    for header in headers:
        date_labels.extend(re.findall(r"\d{2}/\d{2}/\d{4}", header))

    seen_dates: set[str] = set()
    unique_dates = []

    for date_label in date_labels:
        if date_label not in seen_dates:
            seen_dates.add(date_label)
            unique_dates.append(date_label)

    if len(unique_dates) >= 7:
        return unique_dates[1:7], unique_dates[0]

    if len(unique_dates) >= 6:
        return unique_dates[:6], unique_dates[6] if len(unique_dates) > 6 else None

    return unique_dates, None


def parse_int(value: Any) -> int | None:
    """Parse an integer safely."""
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def parse_float(value: Any) -> float | None:
    """Parse a float safely."""
    try:
        return float(str(value).strip().replace(",", ""))
    except (TypeError, ValueError):
        return None


def parse_infobanjir_rainfall_last_updated(value: str) -> datetime | None:
    """Parse Public InfoBanjir rainfall last-updated timestamps."""
    for timestamp_format in RAINFALL_LAST_UPDATED_FORMATS:
        try:
            return datetime.strptime(value.strip(), timestamp_format)
        except (AttributeError, ValueError):
            continue

    return None


def classify_data_freshness(
    latest_last_updated: datetime | None,
    *,
    reference_datetime: datetime | None = None,
    freshness_max_age_hours: float = DEFAULT_FRESHNESS_MAX_AGE_HOURS,
) -> dict[str, Any]:
    """Classify whether fetched Public InfoBanjir rainfall data is fresh enough."""
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


def compute_rainfall_status(values: Iterable[float | None]) -> str:
    """Compute a conservative rainfall status from observed rainfall values."""
    parsed_values = [value for value in values if value is not None]

    if not parsed_values:
        return "unknown"

    if max(parsed_values) > 0:
        return "rain_observed"

    return "no_rain"


def looks_like_rainfall_data_row(row: list[str]) -> bool:
    """Return True if a cell row appears to be a rainfall station row."""
    if len(row) < 13:
        return False

    return parse_int(row[0]) is not None and bool(str(row[1]).strip())


def rainfall_record_from_cells(
    cells: list[str],
    *,
    historical_date_labels: list[str],
    current_day_date: str | None,
    source_url: str,
    state_code: str,
    state_name: str,
) -> InfoBanjirRainfallRecord:
    """Convert one 13-cell rainfall row into a normalized rainfall record."""
    historical_values = [parse_float(value) for value in cells[5:11]]
    current_day_rainfall_mm = parse_float(cells[11])
    extra_rainfall_mm = parse_float(cells[12])

    daily_rainfall_mm = [
        {
            "date": historical_date_labels[index] if index < len(historical_date_labels) else None,
            "rainfall_mm": rainfall_value,
        }
        for index, rainfall_value in enumerate(historical_values)
    ]

    recent_values = [*historical_values, current_day_rainfall_mm]
    parsed_recent_values = [value for value in recent_values if value is not None]

    total_recent_rainfall_mm = round(sum(parsed_recent_values), 2) if parsed_recent_values else None
    max_recent_rainfall_mm = max(parsed_recent_values) if parsed_recent_values else None

    return InfoBanjirRainfallRecord(
        source_id="public_infobanjir_rainfall",
        source_url=source_url,
        state_code=state_code,
        state_name=state_name,
        station_no=parse_int(cells[0]),
        station_id=str(cells[1]).strip(),
        station_name=str(cells[2]).strip(),
        district=str(cells[3]).strip(),
        last_updated=str(cells[4]).strip(),
        daily_rainfall_mm=daily_rainfall_mm,
        current_day_date=current_day_date,
        current_day_rainfall_mm=current_day_rainfall_mm,
        extra_rainfall_mm=extra_rainfall_mm,
        total_recent_rainfall_mm=total_recent_rainfall_mm,
        max_recent_rainfall_mm=max_recent_rainfall_mm,
        computed_status=compute_rainfall_status(recent_values),
    )


def parse_rainfall_records_from_html(
    html: str,
    *,
    source_url: str,
    state_code: str,
    state_name: str,
) -> list[InfoBanjirRainfallRecord]:
    """Parse rainfall station records from Public InfoBanjir malformed HTML."""
    historical_date_labels, current_day_date = extract_rainfall_date_headers(html)
    cells = extract_html_cells(html, "td")
    records: list[InfoBanjirRainfallRecord] = []

    for index in range(0, len(cells), 13):
        row = cells[index : index + 13]

        if looks_like_rainfall_data_row(row):
            records.append(
                rainfall_record_from_cells(
                    row,
                    historical_date_labels=historical_date_labels,
                    current_day_date=current_day_date,
                    source_url=source_url,
                    state_code=state_code,
                    state_name=state_name,
                )
            )

    return records


def fetch_rainfall_station_options_for_district(
    *,
    district: str,
    timeout_seconds: int = 30,
    referer: str | None = None,
) -> list[InfoBanjirRainfallStationOption]:
    """Fetch rainfall station options for one district."""
    url = build_rainfall_station_options_url(district=district)
    html = fetch_html(url, timeout_seconds=timeout_seconds, referer=referer)

    return parse_rainfall_station_options_from_html(html, district=district)


def fetch_rainfall_record_for_station(
    *,
    state_code: str,
    state_name: str,
    district: str,
    station_id: str,
    timeout_seconds: int = 30,
    referer: str | None = None,
) -> list[InfoBanjirRainfallRecord]:
    """Fetch rainfall row for one station."""
    url = build_rainfall_result_url(
        state_code=state_code,
        district=district,
        station_id=station_id,
    )
    html = fetch_html(url, timeout_seconds=timeout_seconds, referer=referer)

    return parse_rainfall_records_from_html(
        html,
        source_url=url,
        state_code=state_code,
        state_name=state_name,
    )


def fetch_rainfall_records_for_state(
    *,
    state_code: str,
    state_name: str,
    timeout_seconds: int = 30,
) -> list[InfoBanjirRainfallRecord]:
    """Fetch Public InfoBanjir rainfall records for one state."""
    state_url = build_rainfall_url(state_code=state_code)
    state_html = fetch_html(state_url, timeout_seconds=timeout_seconds)

    districts = parse_district_options_from_html(state_html)
    records: list[InfoBanjirRainfallRecord] = []
    seen_station_keys: set[tuple[str, str]] = set()

    for district in districts:
        station_options = fetch_rainfall_station_options_for_district(
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
                fetch_rainfall_record_for_station(
                    state_code=state_code,
                    state_name=state_name,
                    district=district,
                    station_id=station_option.station_id,
                    timeout_seconds=timeout_seconds,
                    referer=state_url,
                )
            )

    return records


def rainfall_records_to_dicts(
    records: Iterable[InfoBanjirRainfallRecord],
) -> list[dict[str, Any]]:
    """Convert rainfall records into serializable dictionaries."""
    return [asdict(record) for record in records]


def summarize_rainfall_records(
    records: list[InfoBanjirRainfallRecord],
    *,
    reference_datetime: datetime | None = None,
    freshness_max_age_hours: float = DEFAULT_FRESHNESS_MAX_AGE_HOURS,
) -> dict[str, Any]:
    """Summarize parsed Public InfoBanjir rainfall records."""
    status_counts: dict[str, int] = {}
    parsed_last_updated_values = [
        parsed_value
        for record in records
        if (parsed_value := parse_infobanjir_rainfall_last_updated(record.last_updated)) is not None
    ]

    oldest_last_updated = min(parsed_last_updated_values) if parsed_last_updated_values else None
    latest_last_updated = max(parsed_last_updated_values) if parsed_last_updated_values else None

    for record in records:
        status_counts[record.computed_status] = status_counts.get(record.computed_status, 0) + 1

    max_recent_rainfall_values = [
        record.max_recent_rainfall_mm
        for record in records
        if record.max_recent_rainfall_mm is not None
    ]

    freshness = classify_data_freshness(
        latest_last_updated,
        reference_datetime=reference_datetime,
        freshness_max_age_hours=freshness_max_age_hours,
    )

    return {
        "source_id": "public_infobanjir_rainfall",
        "record_count": len(records),
        "states": sorted({record.state_name for record in records}),
        "districts": sorted({record.district for record in records if record.district}),
        "status_counts": status_counts,
        "rain_observed_count": status_counts.get("rain_observed", 0),
        "max_recent_rainfall_mm": max(max_recent_rainfall_values)
        if max_recent_rainfall_values
        else None,
        "parseable_last_updated_count": len(parsed_last_updated_values),
        "oldest_last_updated": (
            oldest_last_updated.strftime(RAINFALL_LAST_UPDATED_FORMATS[0])
            if oldest_last_updated
            else None
        ),
        "latest_last_updated": (
            latest_last_updated.strftime(RAINFALL_LAST_UPDATED_FORMATS[0])
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
