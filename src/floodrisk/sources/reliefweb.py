"""ReliefWeb discovery query planning utilities.

This module builds offline discovery plans for ReliefWeb API queries. It does not
treat ReliefWeb content as final model labels.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

RELIEFWEB_REPORTS_ENDPOINT = "https://api.reliefweb.int/v2/reports"
DEFAULT_RELIEFWEB_APPNAME = "malaysia-flood-risk-ai"
RELIEFWEB_QUERY_CONFIG_PATH = Path("configs/reliefweb_discovery_queries.json")

RELIEFWEB_REPORT_FIELDS = [
    "id",
    "name",
    "url",
    "date.created",
    "date.original",
    "source.name",
    "primary_country.name",
    "country.name",
    "disaster.name",
    "disaster_type.name",
]


@dataclass(frozen=True)
class ReliefWebDiscoveryQuery:
    """ReliefWeb discovery query definition."""

    query_id: str
    label: str
    query: str
    country: str
    disaster_type: str
    limit: int
    description: str

    @property
    def endpoint_url(self) -> str:
        """Return endpoint URL with appname query parameter."""

        return RELIEFWEB_REPORTS_ENDPOINT + "?" + urlencode({"appname": DEFAULT_RELIEFWEB_APPNAME})

    def payload(self) -> dict[str, Any]:
        """Return JSON payload for ReliefWeb POST request."""

        return {
            "query": {"value": self.query},
            "filter": {
                "operator": "AND",
                "conditions": [
                    {"field": "country", "value": self.country},
                    {"field": "disaster_type", "value": self.disaster_type},
                ],
            },
            "fields": {"include": RELIEFWEB_REPORT_FIELDS},
            "sort": ["date.created:desc"],
            "limit": self.limit,
        }

    def as_dict(self) -> dict[str, Any]:
        """Return query as a dictionary."""

        data = asdict(self)
        data["endpoint_url"] = self.endpoint_url
        data["payload"] = self.payload()
        return data


@dataclass(frozen=True)
class ReliefWebDiscoveryPlan:
    """Offline ReliefWeb discovery plan."""

    source_id: str
    direct_training_use_allowed: bool
    queries: list[ReliefWebDiscoveryQuery]

    @property
    def query_count(self) -> int:
        """Return number of discovery queries."""

        return len(self.queries)

    def as_dict(self) -> dict[str, Any]:
        """Return plan as a dictionary."""

        return {
            "source_id": self.source_id,
            "direct_training_use_allowed": self.direct_training_use_allowed,
            "query_count": self.query_count,
            "queries": [query.as_dict() for query in self.queries],
        }


def load_reliefweb_discovery_queries(
    project_root: Path,
    relative_path: Path = RELIEFWEB_QUERY_CONFIG_PATH,
) -> list[ReliefWebDiscoveryQuery]:
    """Load ReliefWeb discovery queries from config."""

    path = relative_path if relative_path.is_absolute() else project_root / relative_path
    raw_queries = json.loads(path.read_text(encoding="utf-8"))

    return [
        ReliefWebDiscoveryQuery(
            query_id=str(item["query_id"]),
            label=str(item["label"]),
            query=str(item["query"]),
            country=str(item["country"]),
            disaster_type=str(item["disaster_type"]),
            limit=int(item["limit"]),
            description=str(item["description"]),
        )
        for item in raw_queries
    ]


def build_reliefweb_discovery_plan(project_root: Path) -> ReliefWebDiscoveryPlan:
    """Build offline ReliefWeb discovery plan."""

    return ReliefWebDiscoveryPlan(
        source_id="reliefweb_api",
        direct_training_use_allowed=False,
        queries=load_reliefweb_discovery_queries(project_root),
    )


def render_reliefweb_discovery_plan_report(plan: ReliefWebDiscoveryPlan) -> str:
    """Render ReliefWeb discovery plan report."""

    lines = [
        "# ReliefWeb Discovery Plan",
        "",
        "## Summary",
        "",
        f"- Source ID: `{plan.source_id}`",
        f"- Query count: {plan.query_count}",
        f"- Direct training use allowed: {plan.direct_training_use_allowed}",
        "",
        "## Guardrail",
        "",
        (
            "ReliefWeb should be used as a discovery index first. "
            "Do not treat discovered report content as final supervised ML labels "
            "until authority, licensing, location, and dates are reviewed."
        ),
        "",
        "## Query Plan",
        "",
        "| Query ID | Label | Query | Country | Disaster Type | Limit |",
        "|---|---|---|---|---|---:|",
    ]

    for query in plan.queries:
        lines.append(
            "| "
            f"{query.query_id} | "
            f"{query.label} | "
            f"{query.query} | "
            f"{query.country} | "
            f"{query.disaster_type} | "
            f"{query.limit} |"
        )

    lines.extend(["", "## Request Payloads", ""])

    for query in plan.queries:
        lines.extend(
            [
                f"### {query.label}",
                "",
                f"Endpoint: `{query.endpoint_url}`",
                "",
                "```json",
                json.dumps(query.payload(), indent=2),
                "```",
                "",
            ]
        )

    lines.extend(
        [
            "## Decision",
            "",
            (
                "The next implementation step is a safe live discovery script that "
                "fetches report metadata only and stores a non-training discovery report."
            ),
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def write_reliefweb_discovery_plan_report(
    plan: ReliefWebDiscoveryPlan,
    output_path: Path,
) -> Path:
    """Write ReliefWeb discovery plan report."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_reliefweb_discovery_plan_report(plan),
        encoding="utf-8",
    )
    return output_path


@dataclass(frozen=True)
class ReliefWebDiscoveredReport:
    """Metadata-only ReliefWeb discovered report."""

    report_id: str
    title: str
    url: str
    created_at: str
    original_date: str
    sources: list[str]
    countries: list[str]
    disasters: list[str]
    disaster_types: list[str]
    query_id: str

    def as_dict(self) -> dict[str, Any]:
        """Return discovered report as a dictionary."""

        return asdict(self)


@dataclass(frozen=True)
class ReliefWebMetadataDiscoveryResult:
    """Metadata-only ReliefWeb discovery result."""

    source_id: str
    fetched_at_utc: str
    direct_training_use_allowed: bool
    report_count: int
    reports: list[ReliefWebDiscoveredReport]
    errors: list[str]

    @property
    def has_reports(self) -> bool:
        """Return whether any metadata records were discovered."""

        return self.report_count > 0

    @property
    def is_successful(self) -> bool:
        """Return whether discovery completed without request errors."""

        return not self.errors

    def as_dict(self) -> dict[str, Any]:
        """Return discovery result as a dictionary."""

        return {
            "source_id": self.source_id,
            "fetched_at_utc": self.fetched_at_utc,
            "direct_training_use_allowed": self.direct_training_use_allowed,
            "report_count": self.report_count,
            "has_reports": self.has_reports,
            "is_successful": self.is_successful,
            "errors": self.errors,
            "reports": [report.as_dict() for report in self.reports],
        }


def _field_name_list(value: object) -> list[str]:
    """Extract ReliefWeb field name values from list/dict/string shapes."""

    if isinstance(value, list):
        names: list[str] = []

        for item in value:
            if isinstance(item, dict) and item.get("name"):
                names.append(str(item["name"]))
            elif isinstance(item, str):
                names.append(item)

        return names

    if isinstance(value, dict) and value.get("name"):
        return [str(value["name"])]

    if isinstance(value, str):
        return [value]

    return []


def normalize_reliefweb_report(
    *,
    query_id: str,
    item: dict[str, Any],
) -> ReliefWebDiscoveredReport:
    """Normalize one ReliefWeb API item into metadata-only report."""

    fields = item.get("fields", {})
    if not isinstance(fields, dict):
        fields = {}

    date_info = fields.get("date", {})
    if not isinstance(date_info, dict):
        date_info = {}

    return ReliefWebDiscoveredReport(
        report_id=str(item.get("id", "")),
        title=str(fields.get("name", "")),
        url=str(fields.get("url", "")),
        created_at=str(date_info.get("created", "")),
        original_date=str(date_info.get("original", "")),
        sources=_field_name_list(fields.get("source", [])),
        countries=_field_name_list(fields.get("country", [])),
        disasters=_field_name_list(fields.get("disaster", [])),
        disaster_types=_field_name_list(fields.get("disaster_type", [])),
        query_id=query_id,
    )


def fetch_reliefweb_query_metadata(
    query: ReliefWebDiscoveryQuery,
    *,
    timeout_seconds: int = 30,
) -> list[ReliefWebDiscoveredReport]:
    """Fetch metadata-only ReliefWeb reports for one query."""

    payload_bytes = json.dumps(query.payload()).encode("utf-8")
    request = urllib.request.Request(
        query.endpoint_url,
        data=payload_bytes,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        body = response.read().decode("utf-8")

    raw = json.loads(body)
    data = raw.get("data", [])

    if not isinstance(data, list):
        return []

    return [
        normalize_reliefweb_report(query_id=query.query_id, item=item)
        for item in data
        if isinstance(item, dict)
    ]


def discover_reliefweb_metadata(
    project_root: Path,
    *,
    timeout_seconds: int = 30,
) -> ReliefWebMetadataDiscoveryResult:
    """Run live metadata-only ReliefWeb discovery."""

    plan = build_reliefweb_discovery_plan(project_root)
    reports: list[ReliefWebDiscoveredReport] = []
    errors: list[str] = []

    for query in plan.queries:
        try:
            reports.extend(
                fetch_reliefweb_query_metadata(
                    query,
                    timeout_seconds=timeout_seconds,
                )
            )
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace").strip()
            message = f"{query.query_id}: HTTP {exc.code} {exc.reason}"

            if error_body:
                message += f" - {error_body[:500]}"

            errors.append(message)
        except (OSError, TimeoutError, urllib.error.URLError, json.JSONDecodeError) as exc:
            errors.append(f"{query.query_id}: {exc}")

    unique_reports = {report.report_id: report for report in reports if report.report_id}

    return ReliefWebMetadataDiscoveryResult(
        source_id=plan.source_id,
        fetched_at_utc=datetime.now(UTC).isoformat(),
        direct_training_use_allowed=False,
        report_count=len(unique_reports),
        reports=list(unique_reports.values()),
        errors=errors,
    )


def render_reliefweb_metadata_discovery_report(
    result: ReliefWebMetadataDiscoveryResult,
) -> str:
    """Render metadata-only ReliefWeb discovery report."""

    lines = [
        "# ReliefWeb Metadata Discovery Report",
        "",
        "## Summary",
        "",
        f"- Source ID: `{result.source_id}`",
        f"- Fetched at UTC: {result.fetched_at_utc}",
        f"- Direct training use allowed: {result.direct_training_use_allowed}",
        f"- Report metadata records: {result.report_count}",
        f"- Successful: {result.is_successful}",
        "",
        "## Guardrail",
        "",
        (
            "This report contains metadata only. It must not be used as supervised "
            "ML training labels until source authority, licensing, location, dates, "
            "and target mapping are reviewed."
        ),
        "",
        "## Errors",
        "",
    ]

    if result.errors:
        for error in result.errors:
            lines.append(f"- {error}")
    else:
        lines.append("No request errors found.")

    lines.extend(
        [
            "",
            "## Discovered Reports",
            "",
            "| ID | Title | Original Date | Sources | Countries | Disasters | URL |",
            "|---|---|---|---|---|---|---|",
        ]
    )

    for report in result.reports:
        lines.append(
            "| "
            f"{report.report_id} | "
            f"{report.title} | "
            f"{report.original_date} | "
            f"{', '.join(report.sources)} | "
            f"{', '.join(report.countries)} | "
            f"{', '.join(report.disasters)} | "
            f"{report.url} |"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            (
                "Use these records only for source review and follow-up dataset "
                "selection. Do not convert them directly into `flood_occurred` labels."
            ),
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def write_reliefweb_metadata_discovery_outputs(
    result: ReliefWebMetadataDiscoveryResult,
    *,
    json_output_path: Path,
    report_output_path: Path,
) -> tuple[Path, Path]:
    """Write ReliefWeb metadata discovery JSON and report outputs."""

    json_output_path.parent.mkdir(parents=True, exist_ok=True)
    report_output_path.parent.mkdir(parents=True, exist_ok=True)

    json_output_path.write_text(
        json.dumps(result.as_dict(), indent=2),
        encoding="utf-8",
    )
    report_output_path.write_text(
        render_reliefweb_metadata_discovery_report(result),
        encoding="utf-8",
    )

    return json_output_path, report_output_path
