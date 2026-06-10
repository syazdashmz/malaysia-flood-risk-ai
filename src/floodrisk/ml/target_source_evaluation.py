"""Evaluate candidate sources for the future flood occurrence target label."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class TargetSourceCriterion:
    """Criterion used to evaluate a future target-label source."""

    criterion_id: str
    label: str
    required: bool
    description: str

    def as_dict(self) -> dict[str, str | bool]:
        """Return criterion as a dictionary."""

        return asdict(self)


@dataclass(frozen=True)
class TargetSourceEvaluation:
    """Evaluation result for one candidate target-label source."""

    source_id: str
    label: str
    source_type: str
    available_now: bool
    allowed_for_real_training: bool
    criteria_passed: dict[str, bool]
    notes: str

    @property
    def passed_count(self) -> int:
        """Return number of criteria that passed."""

        return sum(1 for passed in self.criteria_passed.values() if passed)

    @property
    def failed_count(self) -> int:
        """Return number of criteria that failed."""

        return sum(1 for passed in self.criteria_passed.values() if not passed)

    @property
    def ready_for_real_training(self) -> bool:
        """Return whether this source is acceptable for real training now."""

        return (
            self.available_now
            and self.allowed_for_real_training
            and all(self.criteria_passed.values())
        )

    def as_dict(self) -> dict[str, Any]:
        """Return source evaluation as a dictionary."""

        data = asdict(self)
        data["passed_count"] = self.passed_count
        data["failed_count"] = self.failed_count
        data["ready_for_real_training"] = self.ready_for_real_training
        return data


@dataclass(frozen=True)
class TargetSourceEvaluationSummary:
    """Summary of all target-source evaluations."""

    target_column: str
    criteria: list[TargetSourceCriterion]
    evaluations: list[TargetSourceEvaluation]

    @property
    def candidate_count(self) -> int:
        """Return total candidate count."""

        return len(self.evaluations)

    @property
    def ready_candidate_count(self) -> int:
        """Return number of ready candidates."""

        return sum(1 for item in self.evaluations if item.ready_for_real_training)

    @property
    def real_training_target_ready(self) -> bool:
        """Return whether any candidate source is ready for real training."""

        return self.ready_candidate_count > 0

    def as_dict(self) -> dict[str, Any]:
        """Return summary as a dictionary."""

        return {
            "target_column": self.target_column,
            "candidate_count": self.candidate_count,
            "ready_candidate_count": self.ready_candidate_count,
            "real_training_target_ready": self.real_training_target_ready,
            "criteria": [criterion.as_dict() for criterion in self.criteria],
            "evaluations": [evaluation.as_dict() for evaluation in self.evaluations],
        }


TARGET_SOURCE_CRITERIA = [
    TargetSourceCriterion(
        criterion_id="verified_authority",
        label="Verified authority",
        required=True,
        description="Source must come from a trusted or documented authority.",
    ),
    TargetSourceCriterion(
        criterion_id="historical_event_coverage",
        label="Historical event coverage",
        required=True,
        description="Source must represent past flood occurrence events.",
    ),
    TargetSourceCriterion(
        criterion_id="binary_mapping",
        label="Binary target mapping",
        required=True,
        description="Source must be mappable to flood_occurred as 0 or 1.",
    ),
    TargetSourceCriterion(
        criterion_id="location_alignment",
        label="Location alignment",
        required=True,
        description="Source must align to latitude, longitude, state, or district.",
    ),
    TargetSourceCriterion(
        criterion_id="time_alignment",
        label="Time alignment",
        required=True,
        description="Source must align to observation_date.",
    ),
    TargetSourceCriterion(
        criterion_id="license_documented",
        label="License documented",
        required=True,
        description="Usage permissions must be documented before training use.",
    ),
    TargetSourceCriterion(
        criterion_id="leakage_free",
        label="Leakage free",
        required=True,
        description="Target must not be derived from the rule-based risk score.",
    ),
]


def _candidate(
    source_id: str,
    label: str,
    source_type: str,
    available_now: bool,
    allowed_for_real_training: bool,
    criteria_passed: dict[str, bool],
    notes: str,
) -> TargetSourceEvaluation:
    """Create target source evaluation with all criteria populated."""

    all_criteria = {criterion.criterion_id: False for criterion in TARGET_SOURCE_CRITERIA}
    all_criteria.update(criteria_passed)

    return TargetSourceEvaluation(
        source_id=source_id,
        label=label,
        source_type=source_type,
        available_now=available_now,
        allowed_for_real_training=allowed_for_real_training,
        criteria_passed=all_criteria,
        notes=notes,
    )


TARGET_SOURCE_EVALUATIONS = [
    _candidate(
        source_id="verified_historical_flood_events",
        label="Verified historical flood event records",
        source_type="preferred",
        available_now=False,
        allowed_for_real_training=True,
        criteria_passed={"leakage_free": True},
        notes="Preferred source type, but no verified event file is integrated yet.",
    ),
    _candidate(
        source_id="historical_flood_extent_polygons",
        label="Historical flood extent polygons",
        source_type="acceptable",
        available_now=False,
        allowed_for_real_training=True,
        criteria_passed={"historical_event_coverage": True, "leakage_free": True},
        notes="Usable only if event dates, coverage, and licensing are verified.",
    ),
    _candidate(
        source_id="official_incident_reports",
        label="Official flood incident reports",
        source_type="acceptable",
        available_now=False,
        allowed_for_real_training=True,
        criteria_passed={"historical_event_coverage": True, "leakage_free": True},
        notes="Usable only after structured location and date fields are available.",
    ),
    _candidate(
        source_id="rule_based_risk_score",
        label="Rule-based risk score",
        source_type="rejected_for_real_training",
        available_now=True,
        allowed_for_real_training=False,
        criteria_passed={"binary_mapping": True},
        notes="Rejected because it leaks the scoring logic into the target label.",
    ),
    _candidate(
        source_id="sample_demo_dataset",
        label="Current sample demo dataset",
        source_type="rejected_for_real_training",
        available_now=True,
        allowed_for_real_training=False,
        criteria_passed={"location_alignment": True, "leakage_free": True},
        notes="Useful for demos and EDA, but not verified historical ground truth.",
    ),
]


def build_target_source_evaluation_summary() -> TargetSourceEvaluationSummary:
    """Build target-source evaluation summary."""

    return TargetSourceEvaluationSummary(
        target_column="flood_occurred",
        criteria=TARGET_SOURCE_CRITERIA.copy(),
        evaluations=TARGET_SOURCE_EVALUATIONS.copy(),
    )


def render_target_source_evaluation_report(
    summary: TargetSourceEvaluationSummary,
) -> str:
    """Render target-source evaluation report as Markdown."""

    criterion_ids = [criterion.criterion_id for criterion in summary.criteria]

    lines = [
        "# Target Label Source Evaluation",
        "",
        "## Summary",
        "",
        f"- Target column: `{summary.target_column}`",
        f"- Candidate sources: {summary.candidate_count}",
        f"- Ready candidate sources: {summary.ready_candidate_count}",
        f"- Real training target ready: {summary.real_training_target_ready}",
        "",
        "## Evaluation Criteria",
        "",
        "| Criterion | Required | Description |",
        "|---|---:|---|",
    ]

    for criterion in summary.criteria:
        lines.append(f"| {criterion.label} | {criterion.required} | {criterion.description} |")

    lines.extend(
        [
            "",
            "## Candidate Scorecard",
            "",
        ]
    )

    header = [
        "Candidate",
        "Type",
        "Available",
        "Allowed",
        "Ready",
        *criterion_ids,
        "Notes",
    ]

    lines.append("| " + " | ".join(header) + " |")
    lines.append("|" + "---|" * len(header))

    for evaluation in summary.evaluations:
        row = [
            evaluation.label,
            evaluation.source_type,
            str(evaluation.available_now),
            str(evaluation.allowed_for_real_training),
            str(evaluation.ready_for_real_training),
            *[str(evaluation.criteria_passed[item]) for item in criterion_ids],
            evaluation.notes,
        ]
        lines.append("| " + " | ".join(row) + " |")

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "No target-label source is ready for real supervised ML training yet.",
            "",
            "Next practical action:",
            "",
            (
                "Find or prepare a verified historical flood occurrence source "
                "with location, date, licensing, and binary target mapping."
            ),
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def write_target_source_evaluation_report(
    summary: TargetSourceEvaluationSummary,
    output_path: Path,
) -> Path:
    """Write target-source evaluation report."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_target_source_evaluation_report(summary),
        encoding="utf-8",
    )
    return output_path
