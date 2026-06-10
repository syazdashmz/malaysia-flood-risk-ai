"""Dataset readiness utilities for notebook and ML planning."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class DatasetReadinessCheck:
    """One dataset readiness check."""

    check_id: str
    label: str
    relative_path: str
    required_for_training: bool
    description: str

    def as_dict(self) -> dict[str, str | bool]:
        """Return check metadata as a dictionary."""

        return asdict(self)


@dataclass(frozen=True)
class DatasetReadinessResult:
    """Result for one dataset readiness check."""

    check: DatasetReadinessCheck
    exists: bool

    @property
    def status(self) -> str:
        """Return readiness status."""

        return "available" if self.exists else "missing"

    @property
    def blocks_training(self) -> bool:
        """Return True if this missing item blocks training."""

        return self.check.required_for_training and not self.exists

    def as_dict(self) -> dict[str, str | bool | dict[str, str | bool]]:
        """Return readiness result as a dictionary."""

        return {
            "check": self.check.as_dict(),
            "exists": self.exists,
            "status": self.status,
            "blocks_training": self.blocks_training,
        }


@dataclass(frozen=True)
class DatasetReadinessSummary:
    """Dataset readiness summary."""

    results: list[DatasetReadinessResult]

    @property
    def check_count(self) -> int:
        """Return number of checks."""

        return len(self.results)

    @property
    def available_count(self) -> int:
        """Return number of available items."""

        return sum(1 for result in self.results if result.exists)

    @property
    def missing_count(self) -> int:
        """Return number of missing items."""

        return sum(1 for result in self.results if not result.exists)

    @property
    def blocking_count(self) -> int:
        """Return number of missing training-blocking items."""

        return sum(1 for result in self.results if result.blocks_training)

    @property
    def ready_for_training(self) -> bool:
        """Return True if dataset foundation is ready for ML training."""

        return self.blocking_count == 0

    def as_dict(self) -> dict[str, int | bool | list[dict]]:
        """Return summary as a dictionary."""

        return {
            "check_count": self.check_count,
            "available_count": self.available_count,
            "missing_count": self.missing_count,
            "blocking_count": self.blocking_count,
            "ready_for_training": self.ready_for_training,
            "results": [result.as_dict() for result in self.results],
        }


DATASET_READINESS_CHECKS = [
    DatasetReadinessCheck(
        check_id="sample_locations",
        label="Sample Malaysia locations",
        relative_path="data/samples/sample_malaysia_locations.csv",
        required_for_training=False,
        description="Small sample location dataset for demos and sanity checks.",
    ),
    DatasetReadinessCheck(
        check_id="weather_summary",
        label="Weather risk signal summary",
        relative_path="reports/weather_risk_signal_summary.json",
        required_for_training=False,
        description="Current weather sample summary from the Phase 2 weather pipeline.",
    ),
    DatasetReadinessCheck(
        check_id="geospatial_validation",
        label="Geospatial validation report",
        relative_path="reports/geospatial_validation_report.md",
        required_for_training=False,
        description="Current readiness report for planned geospatial boundary artifacts.",
    ),
    DatasetReadinessCheck(
        check_id="project_readiness_notebook",
        label="Project readiness notebook",
        relative_path="notebooks/00_project_readiness.ipynb",
        required_for_training=False,
        description="Notebook scaffold for reviewing project readiness.",
    ),
    DatasetReadinessCheck(
        check_id="training_dataset_design",
        label="Training dataset design document",
        relative_path="docs/TRAINING_DATASET.md",
        required_for_training=True,
        description="Defines target label, feature table, split strategy, and leakage risks.",
    ),
    DatasetReadinessCheck(
        check_id="model_training_table",
        label="Model-ready training table",
        relative_path="data/processed/model_training/training_features.csv",
        required_for_training=True,
        description="Clean tabular dataset for baseline ML training.",
    ),
]


def list_dataset_readiness_checks() -> list[DatasetReadinessCheck]:
    """Return dataset readiness checks."""

    return DATASET_READINESS_CHECKS.copy()


def build_dataset_readiness_summary(project_root: Path) -> DatasetReadinessSummary:
    """Build dataset readiness summary."""

    results = [
        DatasetReadinessResult(
            check=check,
            exists=(project_root / check.relative_path).exists(),
        )
        for check in DATASET_READINESS_CHECKS
    ]

    return DatasetReadinessSummary(results=results)


def render_dataset_readiness_report(summary: DatasetReadinessSummary) -> str:
    """Render dataset readiness summary as Markdown."""

    lines = [
        "# Dataset Readiness Report",
        "",
        "## Summary",
        "",
        f"- Checks: {summary.check_count}",
        f"- Available: {summary.available_count}",
        f"- Missing: {summary.missing_count}",
        f"- Blocking training: {summary.blocking_count}",
        f"- Ready for ML training: {summary.ready_for_training}",
        "",
        "## Checks",
        "",
        "| Check | Path | Required for Training | Status | Blocks Training |",
        "|---|---|---:|---|---:|",
    ]

    for result in summary.results:
        lines.append(
            "| "
            f"{result.check.label} | "
            f"{result.check.relative_path} | "
            f"{result.check.required_for_training} | "
            f"{result.status} | "
            f"{result.blocks_training} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
        ]
    )

    if summary.ready_for_training:
        lines.append("The dataset foundation is ready for baseline ML training.")
    else:
        lines.append(
            "The dataset foundation is not ready for real ML training yet. "
            "Training should wait until blocking items are resolved."
        )

    lines.extend(
        [
            "",
            "## Next Required Training Items",
            "",
            "1. Define the training target label.",
            "2. Document feature columns and leakage risks.",
            "3. Create a model-ready training table.",
            "4. Define train/validation split strategy.",
            "5. Only then start baseline ML experiments.",
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def write_dataset_readiness_report(
    summary: DatasetReadinessSummary,
    output_path: Path,
) -> Path:
    """Write dataset readiness report."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_dataset_readiness_report(summary),
        encoding="utf-8",
    )
    return output_path
