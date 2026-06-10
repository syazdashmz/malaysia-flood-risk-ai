"""ReliefWeb discovery query planning utilities.

This module builds offline discovery plans for ReliefWeb API queries. It does not
treat ReliefWeb content as final model labels.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
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
                    {"field": "country.name", "value": self.country},
                    {"field": "disaster_type.name", "value": self.disaster_type},
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
