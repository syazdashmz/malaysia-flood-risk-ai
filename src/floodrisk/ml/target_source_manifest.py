"""Validate candidate target-label source manifest."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

TARGET_SOURCE_MANIFEST_PATH = Path("configs/target_source_candidates.json")

REQUIRED_TARGET_SOURCE_FIELDS = [
    "source_id",
    "label",
    "source_type",
    "authority",
    "access_url",
    "license_name",
    "license_status",
    "data_format",
    "expected_location_fields",
    "expected_date_fields",
    "target_mapping",
    "current_status",
    "allowed_for_real_training",
    "notes",
]

ALLOWED_LICENSE_STATUSES = {
    "verified",
    "pending_review",
    "unknown",
    "restricted",
}

ALLOWED_CURRENT_STATUSES = {
    "planned",
    "candidate",
    "ready",
    "rejected",
}


@dataclass(frozen=True)
class TargetSourceManifestCandidate:
    """Normalized target-source manifest candidate."""

    source_id: str
    label: str
    source_type: str
    authority: str
    access_url: str
    license_name: str
    license_status: str
    data_format: str
    expected_location_fields: list[str]
    expected_date_fields: list[str]
    target_mapping: str
    current_status: str
    allowed_for_real_training: bool
    notes: str

    @property
    def ready_for_real_training(self) -> bool:
        """Return whether this candidate is ready for real training."""

        return (
            self.allowed_for_real_training
            and self.current_status == "ready"
            and self.license_status == "verified"
            and bool(self.authority.strip())
            and bool(self.expected_location_fields)
            and bool(self.expected_date_fields)
        )

    def as_dict(self) -> dict[str, Any]:
        """Return candidate as a dictionary."""

        data = asdict(self)
        data["ready_for_real_training"] = self.ready_for_real_training
        return data


@dataclass(frozen=True)
class TargetSourceManifestValidation:
    """Validation result for the target-source manifest."""

    path: str
    exists: bool
    candidate_count: int
    ready_candidate_count: int
    candidates: list[TargetSourceManifestCandidate]
    invalid_entries: list[str]

    @property
    def is_valid(self) -> bool:
        """Return whether manifest is structurally valid."""

        return self.exists and not self.invalid_entries

    @property
    def has_ready_candidate(self) -> bool:
        """Return whether at least one candidate is ready for training."""

        return self.ready_candidate_count > 0

    def as_dict(self) -> dict[str, Any]:
        """Return validation as a dictionary."""

        return {
            "path": self.path,
            "exists": self.exists,
            "candidate_count": self.candidate_count,
            "ready_candidate_count": self.ready_candidate_count,
            "is_valid": self.is_valid,
            "has_ready_candidate": self.has_ready_candidate,
            "invalid_entries": self.invalid_entries,
            "candidates": [candidate.as_dict() for candidate in self.candidates],
        }


def _validate_raw_candidate(index: int, item: object) -> list[str]:
    """Validate one raw candidate object."""

    issues: list[str] = []

    if not isinstance(item, dict):
        return [f"candidate {index}: entry must be an object"]

    for field in REQUIRED_TARGET_SOURCE_FIELDS:
        if field not in item:
            issues.append(f"candidate {index}: missing required field {field}")

    if issues:
        return issues

    if item["license_status"] not in ALLOWED_LICENSE_STATUSES:
        issues.append(
            f"candidate {index}: license_status must be one of {sorted(ALLOWED_LICENSE_STATUSES)}"
        )

    if item["current_status"] not in ALLOWED_CURRENT_STATUSES:
        issues.append(
            f"candidate {index}: current_status must be one of {sorted(ALLOWED_CURRENT_STATUSES)}"
        )

    if not isinstance(item["expected_location_fields"], list):
        issues.append(f"candidate {index}: expected_location_fields must be a list")

    if not isinstance(item["expected_date_fields"], list):
        issues.append(f"candidate {index}: expected_date_fields must be a list")

    if not isinstance(item["allowed_for_real_training"], bool):
        issues.append(f"candidate {index}: allowed_for_real_training must be boolean")

    return issues


def _build_candidate(item: dict[str, Any]) -> TargetSourceManifestCandidate:
    """Build normalized candidate from manifest item."""

    return TargetSourceManifestCandidate(
        source_id=str(item["source_id"]),
        label=str(item["label"]),
        source_type=str(item["source_type"]),
        authority=str(item["authority"]),
        access_url=str(item["access_url"]),
        license_name=str(item["license_name"]),
        license_status=str(item["license_status"]),
        data_format=str(item["data_format"]),
        expected_location_fields=[str(value) for value in item["expected_location_fields"]],
        expected_date_fields=[str(value) for value in item["expected_date_fields"]],
        target_mapping=str(item["target_mapping"]),
        current_status=str(item["current_status"]),
        allowed_for_real_training=bool(item["allowed_for_real_training"]),
        notes=str(item["notes"]),
    )


def validate_target_source_manifest(
    project_root: Path,
    relative_path: Path = TARGET_SOURCE_MANIFEST_PATH,
) -> TargetSourceManifestValidation:
    """Validate target-source candidate manifest."""

    path = relative_path if relative_path.is_absolute() else project_root / relative_path
    display_path = str(relative_path) if relative_path.is_absolute() else relative_path.as_posix()

    if not path.exists():
        return TargetSourceManifestValidation(
            path=display_path,
            exists=False,
            candidate_count=0,
            ready_candidate_count=0,
            candidates=[],
            invalid_entries=["manifest file is missing"],
        )

    raw = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(raw, list):
        return TargetSourceManifestValidation(
            path=display_path,
            exists=True,
            candidate_count=0,
            ready_candidate_count=0,
            candidates=[],
            invalid_entries=["manifest root must be a list"],
        )

    invalid_entries: list[str] = []
    candidates: list[TargetSourceManifestCandidate] = []

    for index, item in enumerate(raw, start=1):
        issues = _validate_raw_candidate(index, item)
        invalid_entries.extend(issues)

        if not issues and isinstance(item, dict):
            candidates.append(_build_candidate(item))

    ready_candidate_count = sum(1 for candidate in candidates if candidate.ready_for_real_training)

    return TargetSourceManifestValidation(
        path=display_path,
        exists=True,
        candidate_count=len(candidates),
        ready_candidate_count=ready_candidate_count,
        candidates=candidates,
        invalid_entries=invalid_entries,
    )


def render_target_source_manifest_report(
    validation: TargetSourceManifestValidation,
) -> str:
    """Render target-source manifest report."""

    lines = [
        "# Target Source Candidate Manifest Report",
        "",
        "## Summary",
        "",
        f"- Path: `{validation.path}`",
        f"- Exists: {validation.exists}",
        f"- Manifest valid: {validation.is_valid}",
        f"- Candidate sources: {validation.candidate_count}",
        f"- Ready candidate sources: {validation.ready_candidate_count}",
        f"- Has ready candidate: {validation.has_ready_candidate}",
        "",
        "## Invalid Entries",
        "",
    ]

    if validation.invalid_entries:
        for issue in validation.invalid_entries:
            lines.append(f"- {issue}")
    else:
        lines.append("No invalid entries found.")

    lines.extend(
        [
            "",
            "## Candidate Sources",
            "",
            "| Source | Type | License | Status | Allowed | Ready | Notes |",
            "|---|---|---|---|---:|---:|---|",
        ]
    )

    for candidate in validation.candidates:
        lines.append(
            "| "
            f"{candidate.label} | "
            f"{candidate.source_type} | "
            f"{candidate.license_status} | "
            f"{candidate.current_status} | "
            f"{candidate.allowed_for_real_training} | "
            f"{candidate.ready_for_real_training} | "
            f"{candidate.notes} |"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
        ]
    )

    if validation.has_ready_candidate:
        lines.append("At least one target source candidate is ready for real training review.")
    else:
        lines.append("No target source candidate is ready for real training yet.")

    return "\n".join(lines).rstrip() + "\n"


def write_target_source_manifest_report(
    validation: TargetSourceManifestValidation,
    output_path: Path,
) -> Path:
    """Write target-source manifest report."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_target_source_manifest_report(validation),
        encoding="utf-8",
    )
    return output_path
