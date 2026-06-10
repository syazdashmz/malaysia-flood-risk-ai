"""Combined ML training readiness gate."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from floodrisk.ml.feature_table_builder import build_feature_table_preview
from floodrisk.ml.target_event_schema import validate_target_event_source_schema
from floodrisk.ml.target_label_plan import build_target_label_source_plan
from floodrisk.ml.target_source_manifest import validate_target_source_manifest
from floodrisk.ml.training_schema import validate_training_table_schema


@dataclass(frozen=True)
class MLTrainingReadinessSummary:
    """Combined readiness status for real supervised ML training."""

    target_column: str
    target_ready: bool
    allowed_target_sources: int
    ready_target_sources: int
    target_source_manifest_exists: bool
    target_source_manifest_valid: bool
    target_source_manifest_candidates: int
    target_source_manifest_ready_candidates: int
    target_source_manifest_has_ready_candidate: bool
    target_event_source_exists: bool
    target_event_source_rows: int
    target_event_source_schema_valid: bool
    target_event_source_ready: bool
    feature_source_exists: bool
    feature_source_rows: int
    mapped_feature_columns: int
    missing_feature_columns: list[str]
    feature_builder_can_create_training_table: bool
    training_table_exists: bool
    training_table_schema_valid: bool
    training_table_has_rows: bool
    training_table_ready: bool
    blockers: list[str]

    @property
    def real_ml_training_ready(self) -> bool:
        """Return True if all real ML training gates are clear."""

        return (
            self.target_ready
            and self.target_source_manifest_has_ready_candidate
            and self.target_event_source_ready
            and self.feature_builder_can_create_training_table
            and self.training_table_ready
            and not self.blockers
        )

    def as_dict(self) -> dict[str, Any]:
        """Return readiness summary as a dictionary."""

        data = asdict(self)
        data["real_ml_training_ready"] = self.real_ml_training_ready
        return data


def _build_blockers(
    *,
    target_ready: bool,
    target_source_manifest_has_ready_candidate: bool,
    target_event_source_ready: bool,
    feature_builder_can_create_training_table: bool,
    training_table_schema_valid: bool,
    training_table_has_rows: bool,
) -> list[str]:
    """Build blocker list for real supervised ML training."""

    blockers: list[str] = []

    if not target_ready:
        blockers.append("No verified target label source is ready for real training.")

    if not target_source_manifest_has_ready_candidate:
        blockers.append("Target source manifest has no candidate ready for real training yet.")

    if not target_event_source_ready:
        blockers.append(
            "Historical flood event target source is not ready for label generation yet."
        )

    if not feature_builder_can_create_training_table:
        blockers.append("Feature table builder is not allowed to create a real training table yet.")

    if not training_table_schema_valid:
        blockers.append("Model-ready training table schema is not valid yet.")

    if not training_table_has_rows:
        blockers.append("Model-ready training table has no rows yet.")

    return blockers


def build_ml_training_readiness_summary(project_root: Path) -> MLTrainingReadinessSummary:
    """Build combined ML training readiness summary."""

    target_plan = build_target_label_source_plan()
    target_manifest_validation = validate_target_source_manifest(project_root)
    target_event_validation = validate_target_event_source_schema(project_root)
    feature_preview = build_feature_table_preview(project_root, output_allowed=False)

    training_table_path = (
        project_root / "data" / "processed" / "model_training" / "training_features.csv"
    )
    schema_validation = validate_training_table_schema(training_table_path)

    target_ready = (
        target_manifest_validation.has_ready_candidate
        and target_event_validation.is_ready_for_target_generation
    )

    ready_target_sources = max(
        target_plan.ready_candidate_count,
        target_manifest_validation.ready_candidate_count,
        int(target_ready),
    )

    blockers = _build_blockers(
        target_ready=target_ready,
        target_source_manifest_has_ready_candidate=(target_manifest_validation.has_ready_candidate),
        target_event_source_ready=target_event_validation.is_ready_for_target_generation,
        feature_builder_can_create_training_table=(feature_preview.can_create_real_training_table),
        training_table_schema_valid=schema_validation.is_schema_valid,
        training_table_has_rows=schema_validation.has_rows,
    )

    return MLTrainingReadinessSummary(
        target_column=target_plan.target_column,
        target_ready=target_ready,
        allowed_target_sources=target_plan.allowed_candidate_count,
        ready_target_sources=ready_target_sources,
        target_source_manifest_exists=target_manifest_validation.exists,
        target_source_manifest_valid=target_manifest_validation.is_valid,
        target_source_manifest_candidates=target_manifest_validation.candidate_count,
        target_source_manifest_ready_candidates=(target_manifest_validation.ready_candidate_count),
        target_source_manifest_has_ready_candidate=(target_manifest_validation.has_ready_candidate),
        target_event_source_exists=target_event_validation.exists,
        target_event_source_rows=target_event_validation.row_count,
        target_event_source_schema_valid=target_event_validation.is_schema_valid,
        target_event_source_ready=target_event_validation.is_ready_for_target_generation,
        feature_source_exists=feature_preview.source_exists,
        feature_source_rows=feature_preview.source_row_count,
        mapped_feature_columns=len(feature_preview.mapped_training_columns),
        missing_feature_columns=feature_preview.missing_training_columns,
        feature_builder_can_create_training_table=(feature_preview.can_create_real_training_table),
        training_table_exists=schema_validation.exists,
        training_table_schema_valid=schema_validation.is_schema_valid,
        training_table_has_rows=schema_validation.has_rows,
        training_table_ready=schema_validation.is_training_ready,
        blockers=blockers,
    )


def render_ml_training_readiness_report(
    summary: MLTrainingReadinessSummary,
) -> str:
    """Render combined ML training readiness gate report."""

    lines = [
        "# ML Training Readiness Gate",
        "",
        "## Summary",
        "",
        f"- Target column: `{summary.target_column}`",
        f"- Target ready: {summary.target_ready}",
        f"- Allowed target sources: {summary.allowed_target_sources}",
        f"- Ready target sources: {summary.ready_target_sources}",
        f"- Target source manifest exists: {summary.target_source_manifest_exists}",
        f"- Target source manifest valid: {summary.target_source_manifest_valid}",
        f"- Target source manifest candidates: {summary.target_source_manifest_candidates}",
        (
            "- Target source manifest ready candidates: "
            f"{summary.target_source_manifest_ready_candidates}"
        ),
        (
            "- Target source manifest has ready candidate: "
            f"{summary.target_source_manifest_has_ready_candidate}"
        ),
        f"- Target event source exists: {summary.target_event_source_exists}",
        f"- Target event source rows: {summary.target_event_source_rows}",
        (f"- Target event source schema valid: {summary.target_event_source_schema_valid}"),
        f"- Target event source ready: {summary.target_event_source_ready}",
        f"- Feature source exists: {summary.feature_source_exists}",
        f"- Feature source rows: {summary.feature_source_rows}",
        f"- Mapped feature columns: {summary.mapped_feature_columns}",
        f"- Missing feature columns: {len(summary.missing_feature_columns)}",
        (
            "- Feature builder can create training table: "
            f"{summary.feature_builder_can_create_training_table}"
        ),
        f"- Training table exists: {summary.training_table_exists}",
        f"- Training table schema valid: {summary.training_table_schema_valid}",
        f"- Training table has rows: {summary.training_table_has_rows}",
        f"- Training table ready: {summary.training_table_ready}",
        f"- Real ML training ready: {summary.real_ml_training_ready}",
        "",
        "## Blockers",
        "",
    ]

    if summary.blockers:
        for blocker in summary.blockers:
            lines.append(f"- {blocker}")
    else:
        lines.append("No blockers remain.")

    lines.extend(
        [
            "",
            "## Missing Feature Columns",
            "",
        ]
    )

    if summary.missing_feature_columns:
        for column in summary.missing_feature_columns:
            lines.append(f"- {column}")
    else:
        lines.append("No feature columns are missing.")

    lines.extend(
        [
            "",
            "## Decision",
            "",
        ]
    )

    if summary.real_ml_training_ready:
        lines.append("Real supervised ML training can start.")
    else:
        lines.append("Real supervised ML training must remain blocked until all gates are clear.")

    return "\n".join(lines).rstrip() + "\n"


def write_ml_training_readiness_report(
    summary: MLTrainingReadinessSummary,
    output_path: Path,
) -> Path:
    """Write ML training readiness report."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_ml_training_readiness_report(summary),
        encoding="utf-8",
    )
    return output_path
