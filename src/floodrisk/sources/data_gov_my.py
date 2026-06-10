"""data.gov.my catalogue candidate planning utilities."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

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
