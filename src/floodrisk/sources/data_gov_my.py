"""data.gov.my catalogue candidate planning utilities."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DATA_GOV_MY_CATALOGUE_ENDPOINT = "https://api.data.gov.my/data-catalogue"
DATA_GOV_MY_CANDIDATE_CONFIG_PATH = Path("configs/data_gov_my_catalogue_candidates.json")


@dataclass(frozen=True)
class DataGovMyCatalogueCandidate:
    """Candidate data.gov.my catalogue dataset."""

    dataset_id: str
    label: str
    priority: int
    role: str
    source_url: str
    api_url: str
    expected_use: str
    location_granularity: str
    temporal_granularity: str
    direct_training_use_allowed: bool
    target_label_candidate: bool
    notes: str

    def as_dict(self) -> dict[str, object]:
        """Return candidate as dictionary."""

        return asdict(self)


@dataclass(frozen=True)
class DataGovMyCataloguePlan:
    """Offline data.gov.my catalogue candidate plan."""

    source_id: str
    direct_training_use_allowed: bool
    candidates: list[DataGovMyCatalogueCandidate]

    @property
    def candidate_count(self) -> int:
        """Return number of candidate datasets."""

        return len(self.candidates)

    @property
    def target_label_candidate_count(self) -> int:
        """Return number of target-label candidates."""

        return sum(candidate.target_label_candidate for candidate in self.candidates)

    def as_dict(self) -> dict[str, object]:
        """Return plan as dictionary."""

        return {
            "source_id": self.source_id,
            "direct_training_use_allowed": self.direct_training_use_allowed,
            "candidate_count": self.candidate_count,
            "target_label_candidate_count": self.target_label_candidate_count,
            "candidates": [candidate.as_dict() for candidate in self.candidates],
        }


def load_data_gov_my_catalogue_candidates(
    project_root: Path,
    relative_path: Path = DATA_GOV_MY_CANDIDATE_CONFIG_PATH,
) -> list[DataGovMyCatalogueCandidate]:
    """Load data.gov.my catalogue candidates from config."""

    path = relative_path if relative_path.is_absolute() else project_root / relative_path
    raw_candidates = json.loads(path.read_text(encoding="utf-8"))

    return [
        DataGovMyCatalogueCandidate(
            dataset_id=str(item["dataset_id"]),
            label=str(item["label"]),
            priority=int(item["priority"]),
            role=str(item["role"]),
            source_url=str(item["source_url"]),
            api_url=str(item["api_url"]),
            expected_use=str(item["expected_use"]),
            location_granularity=str(item["location_granularity"]),
            temporal_granularity=str(item["temporal_granularity"]),
            direct_training_use_allowed=bool(item["direct_training_use_allowed"]),
            target_label_candidate=bool(item["target_label_candidate"]),
            notes=str(item["notes"]),
        )
        for item in raw_candidates
    ]


def build_data_gov_my_catalogue_plan(project_root: Path) -> DataGovMyCataloguePlan:
    """Build offline data.gov.my catalogue candidate plan."""

    candidates = sorted(
        load_data_gov_my_catalogue_candidates(project_root),
        key=lambda candidate: candidate.priority,
    )

    return DataGovMyCataloguePlan(
        source_id="data_gov_my",
        direct_training_use_allowed=False,
        candidates=candidates,
    )


def render_data_gov_my_catalogue_plan_report(plan: DataGovMyCataloguePlan) -> str:
    """Render data.gov.my catalogue candidate report."""

    lines = [
        "# data.gov.my Catalogue Candidate Plan",
        "",
        "## Summary",
        "",
        f"- Source ID: `{plan.source_id}`",
        f"- Candidate datasets: {plan.candidate_count}",
        f"- Target-label candidates: {plan.target_label_candidate_count}",
        f"- Direct training use allowed: {plan.direct_training_use_allowed}",
        "",
        "## Guardrail",
        "",
        (
            "These datasets are catalogue candidates only. They must not be used "
            "as supervised ML labels until authority, license, location fields, "
            "date fields, and target mapping are reviewed."
        ),
        "",
        "## Candidate Datasets",
        "",
        ("| Priority | Dataset ID | Label | Role | Location | Time | Target Label Candidate |"),
        "|---:|---|---|---|---|---|---:|",
    ]

    for candidate in plan.candidates:
        lines.append(
            "| "
            f"{candidate.priority} | "
            f"{candidate.dataset_id} | "
            f"{candidate.label} | "
            f"{candidate.role} | "
            f"{candidate.location_granularity} | "
            f"{candidate.temporal_granularity} | "
            f"{candidate.target_label_candidate} |"
        )

    lines.extend(["", "## API Probe URLs", ""])

    for candidate in plan.candidates:
        lines.extend(
            [
                f"### {candidate.label}",
                "",
                f"- Dataset ID: `{candidate.dataset_id}`",
                f"- Source page: {candidate.source_url}",
                f"- API probe: `{candidate.api_url}`",
                f"- Expected use: {candidate.expected_use}",
                f"- Notes: {candidate.notes}",
                "",
            ]
        )

    lines.extend(
        [
            "## Decision",
            "",
            (
                "The next implementation step is a metadata/sample-only API probe "
                "that fetches small previews for these dataset IDs and stores a "
                "non-training review report."
            ),
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def write_data_gov_my_catalogue_plan_report(
    plan: DataGovMyCataloguePlan,
    output_path: Path,
) -> Path:
    """Write data.gov.my catalogue candidate report."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_data_gov_my_catalogue_plan_report(plan),
        encoding="utf-8",
    )
    return output_path


@dataclass(frozen=True)
class DataGovMyCatalogueProbeResult:
    """Sample-only data.gov.my catalogue probe result for one dataset."""

    dataset_id: str
    label: str
    api_url: str
    direct_training_use_allowed: bool
    target_label_candidate: bool
    record_count: int
    sample_columns: list[str]
    sample_records: list[dict[str, Any]]
    error: str

    @property
    def is_successful(self) -> bool:
        """Return whether the API probe succeeded."""

        return self.error == ""

    def as_dict(self) -> dict[str, Any]:
        """Return probe result as dictionary."""

        return asdict(self)


@dataclass(frozen=True)
class DataGovMyCatalogueProbeSummary:
    """Sample-only data.gov.my catalogue probe summary."""

    source_id: str
    fetched_at_utc: str
    direct_training_use_allowed: bool
    candidate_count: int
    successful_probes: int
    failed_probes: int
    results: list[DataGovMyCatalogueProbeResult]

    def as_dict(self) -> dict[str, Any]:
        """Return probe summary as dictionary."""

        return {
            "source_id": self.source_id,
            "fetched_at_utc": self.fetched_at_utc,
            "direct_training_use_allowed": self.direct_training_use_allowed,
            "candidate_count": self.candidate_count,
            "successful_probes": self.successful_probes,
            "failed_probes": self.failed_probes,
            "results": [result.as_dict() for result in self.results],
        }


def _coerce_data_gov_my_records(raw: object) -> list[dict[str, Any]]:
    """Coerce data.gov.my API response into a list of records."""

    if isinstance(raw, list):
        return [item for item in raw if isinstance(item, dict)]

    if isinstance(raw, dict):
        for key in ["data", "results", "records"]:
            value = raw.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]

    return []


def _record_columns(records: list[dict[str, Any]]) -> list[str]:
    """Return sorted column names from sample records."""

    columns: set[str] = set()

    for record in records:
        columns.update(str(key) for key in record)

    return sorted(columns)


def fetch_data_gov_my_candidate_sample(
    candidate: DataGovMyCatalogueCandidate,
    *,
    timeout_seconds: int = 30,
) -> DataGovMyCatalogueProbeResult:
    """Fetch a small sample from one data.gov.my catalogue candidate."""

    request = urllib.request.Request(
        candidate.api_url,
        headers={"Accept": "application/json"},
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8")

        raw = json.loads(body)
        records = _coerce_data_gov_my_records(raw)

        return DataGovMyCatalogueProbeResult(
            dataset_id=candidate.dataset_id,
            label=candidate.label,
            api_url=candidate.api_url,
            direct_training_use_allowed=False,
            target_label_candidate=candidate.target_label_candidate,
            record_count=len(records),
            sample_columns=_record_columns(records),
            sample_records=records[:3],
            error="",
        )
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace").strip()
        message = f"HTTP {exc.code} {exc.reason}"

        if error_body:
            message += f" - {error_body[:500]}"

        return DataGovMyCatalogueProbeResult(
            dataset_id=candidate.dataset_id,
            label=candidate.label,
            api_url=candidate.api_url,
            direct_training_use_allowed=False,
            target_label_candidate=candidate.target_label_candidate,
            record_count=0,
            sample_columns=[],
            sample_records=[],
            error=message,
        )
    except (OSError, TimeoutError, urllib.error.URLError, json.JSONDecodeError) as exc:
        return DataGovMyCatalogueProbeResult(
            dataset_id=candidate.dataset_id,
            label=candidate.label,
            api_url=candidate.api_url,
            direct_training_use_allowed=False,
            target_label_candidate=candidate.target_label_candidate,
            record_count=0,
            sample_columns=[],
            sample_records=[],
            error=str(exc),
        )


def probe_data_gov_my_catalogue_candidates(
    project_root: Path,
    *,
    timeout_seconds: int = 30,
) -> DataGovMyCatalogueProbeSummary:
    """Probe all configured data.gov.my candidates with sample-only requests."""

    plan = build_data_gov_my_catalogue_plan(project_root)
    results = [
        fetch_data_gov_my_candidate_sample(
            candidate,
            timeout_seconds=timeout_seconds,
        )
        for candidate in plan.candidates
    ]

    successful = sum(result.is_successful for result in results)

    return DataGovMyCatalogueProbeSummary(
        source_id=plan.source_id,
        fetched_at_utc=datetime.now(UTC).isoformat(),
        direct_training_use_allowed=False,
        candidate_count=len(results),
        successful_probes=successful,
        failed_probes=len(results) - successful,
        results=results,
    )


def _markdown_cell(value: object) -> str:
    """Return a safe markdown table cell."""

    return str(value).replace("|", "\\|").replace("\n", " ")


def render_data_gov_my_catalogue_probe_report(
    summary: DataGovMyCatalogueProbeSummary,
) -> str:
    """Render sample-only data.gov.my catalogue probe report."""

    lines = [
        "# data.gov.my Catalogue Probe Report",
        "",
        "## Summary",
        "",
        f"- Source ID: `{summary.source_id}`",
        f"- Fetched at UTC: {summary.fetched_at_utc}",
        f"- Candidate datasets: {summary.candidate_count}",
        f"- Successful probes: {summary.successful_probes}",
        f"- Failed probes: {summary.failed_probes}",
        f"- Direct training use allowed: {summary.direct_training_use_allowed}",
        "",
        "## Guardrail",
        "",
        (
            "This report contains small API samples only. These samples must not be "
            "used as supervised ML target labels until authority, license, location, "
            "date fields, and target mapping are reviewed."
        ),
        "",
        "## Probe Results",
        "",
        "| Dataset ID | Label | Records | Columns | Error |",
        "|---|---|---:|---|---|",
    ]

    for result in summary.results:
        lines.append(
            "| "
            f"{result.dataset_id} | "
            f"{result.label} | "
            f"{result.record_count} | "
            f"{_markdown_cell(', '.join(result.sample_columns))} | "
            f"{_markdown_cell(result.error or '-')} |"
        )

    lines.extend(["", "## Sample Records", ""])

    for result in summary.results:
        lines.extend([f"### {result.label}", ""])

        if not result.sample_records:
            lines.extend(["No sample records available.", ""])
            continue

        lines.extend(["```json", json.dumps(result.sample_records, indent=2), "```", ""])

    lines.extend(
        [
            "## Decision",
            "",
            (
                "Use these probes only to decide whether each dataset is useful as "
                "supporting feature/context data. Do not map them to `flood_occurred` "
                "without a separate target-label review."
            ),
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def write_data_gov_my_catalogue_probe_outputs(
    summary: DataGovMyCatalogueProbeSummary,
    *,
    json_output_path: Path,
    report_output_path: Path,
) -> tuple[Path, Path]:
    """Write data.gov.my catalogue probe JSON and report outputs."""

    json_output_path.parent.mkdir(parents=True, exist_ok=True)
    report_output_path.parent.mkdir(parents=True, exist_ok=True)

    json_output_path.write_text(
        json.dumps(summary.as_dict(), indent=2),
        encoding="utf-8",
    )
    report_output_path.write_text(
        render_data_gov_my_catalogue_probe_report(summary),
        encoding="utf-8",
    )

    return json_output_path, report_output_path
