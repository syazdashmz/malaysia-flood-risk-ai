"""Notebook smoke execution utilities.

These checks execute notebook code cells in memory without writing outputs
back into the notebook files.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class NotebookExecutionResult:
    """Smoke execution result for one notebook."""

    path: str
    exists: bool
    valid_json: bool
    code_cell_count: int
    executed_code_cell_count: int
    success: bool
    error_cell_index: int | None = None
    error_message: str | None = None

    def as_dict(self) -> dict[str, str | int | bool | None]:
        """Return execution result as a dictionary."""

        return asdict(self)


@dataclass(frozen=True)
class NotebookExecutionSummary:
    """Smoke execution summary for notebooks."""

    results: list[NotebookExecutionResult]

    @property
    def notebook_count(self) -> int:
        """Return number of notebooks checked."""

        return len(self.results)

    @property
    def successful_count(self) -> int:
        """Return number of successfully executed notebooks."""

        return sum(1 for result in self.results if result.success)

    @property
    def failed_count(self) -> int:
        """Return number of failed notebooks."""

        return sum(1 for result in self.results if not result.success)

    @property
    def ready_for_notebook_eda(self) -> bool:
        """Return True if all notebooks execute successfully."""

        return self.failed_count == 0

    def as_dict(self) -> dict[str, int | bool | list[dict[str, Any]]]:
        """Return execution summary as a dictionary."""

        return {
            "notebook_count": self.notebook_count,
            "successful_count": self.successful_count,
            "failed_count": self.failed_count,
            "ready_for_notebook_eda": self.ready_for_notebook_eda,
            "results": [result.as_dict() for result in self.results],
        }


def execute_notebook_smoke_test(
    notebook_path: Path,
    project_root: Path,
) -> NotebookExecutionResult:
    """Execute notebook code cells in memory without saving outputs."""

    if not notebook_path.exists():
        return NotebookExecutionResult(
            path=str(notebook_path),
            exists=False,
            valid_json=False,
            code_cell_count=0,
            executed_code_cell_count=0,
            success=False,
            error_message="Notebook does not exist.",
        )

    try:
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return NotebookExecutionResult(
            path=str(notebook_path),
            exists=True,
            valid_json=False,
            code_cell_count=0,
            executed_code_cell_count=0,
            success=False,
            error_message=str(exc),
        )

    code_cells = [cell for cell in notebook.get("cells", []) if cell.get("cell_type") == "code"]

    namespace: dict[str, Any] = {"__name__": "__notebook_smoke_test__"}
    current_directory = Path.cwd()

    try:
        os.chdir(project_root)

        for index, cell in enumerate(code_cells):
            source = "".join(cell.get("source", []))

            try:
                with (
                    contextlib.redirect_stdout(io.StringIO()),
                    contextlib.redirect_stderr(io.StringIO()),
                ):
                    exec(compile(source, str(notebook_path), "exec"), namespace)
            except Exception as exc:  # noqa: BLE001
                return NotebookExecutionResult(
                    path=str(notebook_path),
                    exists=True,
                    valid_json=True,
                    code_cell_count=len(code_cells),
                    executed_code_cell_count=index,
                    success=False,
                    error_cell_index=index,
                    error_message=f"{type(exc).__name__}: {exc}",
                )
    finally:
        os.chdir(current_directory)

    return NotebookExecutionResult(
        path=str(notebook_path),
        exists=True,
        valid_json=True,
        code_cell_count=len(code_cells),
        executed_code_cell_count=len(code_cells),
        success=True,
    )


def smoke_test_notebook_directory(
    notebook_dir: Path,
    project_root: Path,
) -> NotebookExecutionSummary:
    """Smoke test all notebooks in a directory."""

    notebooks = sorted(notebook_dir.rglob("*.ipynb"))
    results = [
        execute_notebook_smoke_test(
            notebook_path=notebook,
            project_root=project_root,
        )
        for notebook in notebooks
    ]

    return NotebookExecutionSummary(results=results)


def render_notebook_execution_report(summary: NotebookExecutionSummary) -> str:
    """Render notebook smoke execution summary as Markdown."""

    lines = [
        "# Notebook Smoke Execution Report",
        "",
        "## Summary",
        "",
        f"- Notebooks checked: {summary.notebook_count}",
        f"- Successful notebooks: {summary.successful_count}",
        f"- Failed notebooks: {summary.failed_count}",
        f"- Ready for notebook EDA: {summary.ready_for_notebook_eda}",
        "",
        "## Notebook Execution Checks",
        "",
        "| Path | Code Cells | Executed Code Cells | Success | Error |",
        "|---|---:|---:|---|---|",
    ]

    for result in summary.results:
        lines.append(
            "| "
            f"{result.path} | "
            f"{result.code_cell_count} | "
            f"{result.executed_code_cell_count} | "
            f"{result.success} | "
            f"{result.error_message or '-'} |"
        )

    if not summary.results:
        lines.extend(
            [
                "",
                "No notebooks were found.",
            ]
        )

    lines.extend(
        [
            "",
            "## Rule",
            "",
            ("Notebook smoke execution must not save outputs back into committed notebook files."),
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def write_notebook_execution_report(
    summary: NotebookExecutionSummary,
    output_path: Path,
) -> Path:
    """Write notebook smoke execution report."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_notebook_execution_report(summary),
        encoding="utf-8",
    )
    return output_path
