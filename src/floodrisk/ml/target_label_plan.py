"""Target label source plan for future supervised flood-risk training."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class TargetLabelRequirement:
    """Requirement for accepting a target label source."""

    requirement_id: str
    label: str
    required: bool
    description: str

    def as_dict(self) -> dict[str, str | bool]:
        """Return requirement as a dictionary."""

        return asdict(self)


@dataclass(frozen=True)
class TargetLabelSourceCandidate:
    """Candidate source for the future flood occurrence label."""

    source_id: str
    label: str
    source_type: str
    allowed_for_real_training: bool
    ready_now: bool
    reason: str

    @property
    def usable_now_for_real_training(self) -> bool:
        """Return True if the source can be used for real training now."""

        return self.allowed_for_real_training and self.ready_now

    def as_dict(self) -> dict[str, str | bool]:
        """Return source candidate as a dictionary."""

        data = asdict(self)
        data["usable_now_for_real_training"] = self.usable_now_for_real_training
        return data


@dataclass(frozen=True)
class TargetLabelSourcePlan:
    """Target label source planning summary."""

    target_column: str
    requirements: list[TargetLabelRequirement]
    candidates: list[TargetLabelSourceCandidate]

    @property
    def requirement_count(self) -> int:
        """Return number of target label requirements."""

        return len(self.requirements)

    @property
    def candidate_count(self) -> int:
        """Return number of candidate sources."""

        return len(self.candidates)

    @property
    def allowed_candidate_count(self) -> int:
        """Return number of sources allowed for real training."""

        return sum(1 for candidate in self.candidates if candidate.allowed_for_real_training)

    @property
    def ready_candidate_count(self) -> int:
        """Return number of sources ready now for real training."""

        return sum(1 for candidate in self.candidates if candidate.usable_now_for_real_training)

    @property
    def real_training_target_ready(self) -> bool:
        """Return True if any target source is ready for real training."""

        return self.ready_candidate_count > 0

    def as_dict(self) -> dict[str, str | int | bool | list[dict[str, str | bool]]]:
        """Return target label source plan as a dictionary."""

        return {
            "target_column": self.target_column,
            "requirement_count": self.requirement_count,
            "candidate_count": self.candidate_count,
            "allowed_candidate_count": self.allowed_candidate_count,
            "ready_candidate_count": self.ready_candidate_count,
            "real_training_target_ready": self.real_training_target_ready,
            "requirements": [requirement.as_dict() for requirement in self.requirements],
            "candidates": [candidate.as_dict() for candidate in self.candidates],
        }


TARGET_LABEL_REQUIREMENTS = [
    TargetLabelRequirement(
        requirement_id="binary_label",
        label="Binary flood occurrence label",
        required=True,
        description="The preferred target must map to flood_occurred as 0 or 1.",
    ),
    TargetLabelRequirement(
        requirement_id="verified_source",
        label="Verified historical source",
        required=True,
        description="The label must come from a verified historical flood source.",
    ),
    TargetLabelRequirement(
        requirement_id="location_alignment",
        label="Location alignment",
        required=True,
        description="The label must align with latitude, longitude, state, or district.",
    ),
    TargetLabelRequirement(
        requirement_id="time_alignment",
        label="Time alignment",
        required=True,
        description="The label must align with observation_date for temporal splitting.",
    ),
    TargetLabelRequirement(
        requirement_id="no_score_leakage",
        label="No risk-score leakage",
        required=True,
        description="The target must not be derived from the rule-based risk score.",
    ),
]

TARGET_LABEL_SOURCE_CANDIDATES = [
    TargetLabelSourceCandidate(
        source_id="verified_historical_flood_events",
        label="Verified historical flood event records",
        source_type="preferred",
        allowed_for_real_training=True,
        ready_now=False,
        reason="Preferred option, but no verified event dataset is integrated yet.",
    ),
    TargetLabelSourceCandidate(
        source_id="historical_flood_extent_polygons",
        label="Historical flood extent polygons",
        source_type="acceptable",
        allowed_for_real_training=True,
        ready_now=False,
        reason="Usable if event dates and polygon coverage are verified.",
    ),
    TargetLabelSourceCandidate(
        source_id="official_incident_reports",
        label="Official flood incident reports",
        source_type="acceptable",
        allowed_for_real_training=True,
        ready_now=False,
        reason="Usable if locations, dates, and event definitions are structured.",
    ),
    TargetLabelSourceCandidate(
        source_id="rule_based_risk_score",
        label="Rule-based risk score",
        source_type="rejected_for_real_training",
        allowed_for_real_training=False,
        ready_now=True,
        reason="Rejected as ground truth because it would leak engineered scoring logic.",
    ),
    TargetLabelSourceCandidate(
        source_id="sample_demo_dataset",
        label="Current sample demo dataset",
        source_type="rejected_for_real_training",
        allowed_for_real_training=False,
        ready_now=True,
        reason="Useful for demos and EDA, but not verified as historical ground truth.",
    ),
]


def build_target_label_source_plan() -> TargetLabelSourcePlan:
    """Build target label source plan."""

    return TargetLabelSourcePlan(
        target_column="flood_occurred",
        requirements=TARGET_LABEL_REQUIREMENTS.copy(),
        candidates=TARGET_LABEL_SOURCE_CANDIDATES.copy(),
    )


def render_target_label_source_plan_report(plan: TargetLabelSourcePlan) -> str:
    """Render target label source plan as Markdown."""

    lines = [
        "# Target Label Source Plan",
        "",
        "## Summary",
        "",
        f"- Target column: `{plan.target_column}`",
        f"- Requirements: {plan.requirement_count}",
        f"- Candidate sources: {plan.candidate_count}",
        f"- Sources allowed for real training: {plan.allowed_candidate_count}",
        f"- Sources ready now for real training: {plan.ready_candidate_count}",
        f"- Real training target ready: {plan.real_training_target_ready}",
        "",
        "## Target Label Requirements",
        "",
        "| Requirement | Required | Description |",
        "|---|---:|---|",
    ]

    for requirement in plan.requirements:
        lines.append(
            f"| {requirement.label} | {requirement.required} | {requirement.description} |"
        )

    lines.extend(
        [
            "",
            "## Candidate Sources",
            "",
            "| Candidate | Type | Allowed for Real Training | Ready Now | Reason |",
            "|---|---|---:|---:|---|",
        ]
    )

    for candidate in plan.candidates:
        lines.append(
            "| "
            f"{candidate.label} | "
            f"{candidate.source_type} | "
            f"{candidate.allowed_for_real_training} | "
            f"{candidate.ready_now} | "
            f"{candidate.reason} |"
        )

    lines.extend(
        [
            "",
            "## Training Guardrail",
            "",
            (
                "Do not start real supervised ML training until at least one allowed "
                "target label source is integrated and ready."
            ),
            "",
            "Current decision:",
            "",
            "    Real supervised ML training remains blocked.",
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def write_target_label_source_plan_report(
    plan: TargetLabelSourcePlan,
    output_path: Path,
) -> Path:
    """Write target label source plan report."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_target_label_source_plan_report(plan),
        encoding="utf-8",
    )
    return output_path
