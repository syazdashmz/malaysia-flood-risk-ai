"""Notebook environment readiness checks."""

from __future__ import annotations

import importlib.metadata
import importlib.util
import platform
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from floodrisk.version import __version__


@dataclass(frozen=True)
class NotebookDependency:
    """Notebook dependency contract."""

    name: str
    import_name: str
    required: bool
    purpose: str

    def as_dict(self) -> dict[str, str | bool]:
        """Return dependency metadata as a dictionary."""

        return asdict(self)


@dataclass(frozen=True)
class NotebookDependencyCheck:
    """Notebook dependency check result."""

    dependency: NotebookDependency
    available: bool
    version: str | None

    @property
    def status(self) -> str:
        """Return dependency status."""

        return "available" if self.available else "missing"

    @property
    def blocks_notebook_work(self) -> bool:
        """Return True if missing dependency blocks notebook work."""

        return self.dependency.required and not self.available

    def as_dict(self) -> dict[str, str | bool | dict[str, str | bool] | None]:
        """Return dependency check as a dictionary."""

        return {
            "dependency": self.dependency.as_dict(),
            "available": self.available,
            "version": self.version,
            "status": self.status,
            "blocks_notebook_work": self.blocks_notebook_work,
        }


@dataclass(frozen=True)
class NotebookEnvironmentSummary:
    """Notebook environment readiness summary."""

    python_version: str
    platform_name: str
    dependency_checks: list[NotebookDependencyCheck]

    @property
    def dependency_count(self) -> int:
        """Return number of dependencies checked."""

        return len(self.dependency_checks)

    @property
    def available_count(self) -> int:
        """Return number of available dependencies."""

        return sum(1 for check in self.dependency_checks if check.available)

    @property
    def missing_count(self) -> int:
        """Return number of missing dependencies."""

        return sum(1 for check in self.dependency_checks if not check.available)

    @property
    def blocking_count(self) -> int:
        """Return number of required missing dependencies."""

        return sum(1 for check in self.dependency_checks if check.blocks_notebook_work)

    @property
    def ready_for_notebook_work(self) -> bool:
        """Return True if notebook environment has required dependencies."""

        return self.blocking_count == 0

    def as_dict(self) -> dict[str, str | int | bool | list[dict]]:
        """Return summary as a dictionary."""

        return {
            "python_version": self.python_version,
            "platform_name": self.platform_name,
            "dependency_count": self.dependency_count,
            "available_count": self.available_count,
            "missing_count": self.missing_count,
            "blocking_count": self.blocking_count,
            "ready_for_notebook_work": self.ready_for_notebook_work,
            "dependency_checks": [check.as_dict() for check in self.dependency_checks],
        }


NOTEBOOK_DEPENDENCIES = (
    NotebookDependency(
        name="floodrisk",
        import_name="floodrisk",
        required=True,
        purpose="Project package import for notebooks.",
    ),
    NotebookDependency(
        name="pandas",
        import_name="pandas",
        required=True,
        purpose="Tabular EDA and feature-table inspection.",
    ),
    NotebookDependency(
        name="matplotlib",
        import_name="matplotlib",
        required=True,
        purpose="Basic notebook plotting.",
    ),
    NotebookDependency(
        name="ipykernel",
        import_name="ipykernel",
        required=True,
        purpose="Python kernel support for Jupyter/VS Code notebooks.",
    ),
    NotebookDependency(
        name="geopandas",
        import_name="geopandas",
        required=False,
        purpose="Future geospatial EDA.",
    ),
    NotebookDependency(
        name="scikit-learn",
        import_name="sklearn",
        required=False,
        purpose="Future baseline ML experiments.",
    ),
    NotebookDependency(
        name="jupyterlab",
        import_name="jupyterlab",
        required=False,
        purpose="Optional browser-based notebook interface.",
    ),
)


def _dependency_version(dependency: NotebookDependency) -> str | None:
    """Return installed dependency version when available."""

    if dependency.import_name == "floodrisk":
        return __version__

    try:
        return importlib.metadata.version(dependency.name)
    except importlib.metadata.PackageNotFoundError:
        try:
            return importlib.metadata.version(dependency.import_name)
        except importlib.metadata.PackageNotFoundError:
            return None


def check_notebook_dependency(
    dependency: NotebookDependency,
) -> NotebookDependencyCheck:
    """Check one notebook dependency."""

    available = importlib.util.find_spec(dependency.import_name) is not None
    version = _dependency_version(dependency) if available else None

    return NotebookDependencyCheck(
        dependency=dependency,
        available=available,
        version=version,
    )


def check_notebook_environment() -> NotebookEnvironmentSummary:
    """Check current notebook environment readiness."""

    checks = [check_notebook_dependency(dependency) for dependency in NOTEBOOK_DEPENDENCIES]

    return NotebookEnvironmentSummary(
        python_version=sys.version.split()[0],
        platform_name=platform.platform(),
        dependency_checks=checks,
    )


def render_notebook_environment_report(summary: NotebookEnvironmentSummary) -> str:
    """Render notebook environment summary as Markdown."""

    lines = [
        "# Notebook Environment Report",
        "",
        "## Summary",
        "",
        f"- Python version: {summary.python_version}",
        f"- Platform: {summary.platform_name}",
        f"- Dependencies checked: {summary.dependency_count}",
        f"- Available dependencies: {summary.available_count}",
        f"- Missing dependencies: {summary.missing_count}",
        f"- Blocking dependencies: {summary.blocking_count}",
        f"- Ready for notebook work: {summary.ready_for_notebook_work}",
        "",
        "## Dependency Checks",
        "",
        "| Dependency | Import | Required | Status | Version | Purpose |",
        "|---|---|---:|---|---|---|",
    ]

    for check in summary.dependency_checks:
        lines.append(
            "| "
            f"{check.dependency.name} | "
            f"{check.dependency.import_name} | "
            f"{check.dependency.required} | "
            f"{check.status} | "
            f"{check.version or '-'} | "
            f"{check.dependency.purpose} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
        ]
    )

    if summary.ready_for_notebook_work:
        lines.append("The environment has the required dependencies for notebook work.")
    else:
        lines.append(
            "The environment is missing at least one required notebook dependency. "
            "Install the blocking dependency before deeper notebook work."
        )

    return "\n".join(lines).rstrip() + "\n"


def write_notebook_environment_report(
    summary: NotebookEnvironmentSummary,
    output_path: Path,
) -> Path:
    """Write notebook environment report."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_notebook_environment_report(summary),
        encoding="utf-8",
    )
    return output_path
