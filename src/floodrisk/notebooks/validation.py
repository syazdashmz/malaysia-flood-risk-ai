"""Validation helpers for project notebooks."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class NotebookValidation:
    """Validation result for one notebook."""

    path: str
    exists: bool
    valid_json: bool
    nbformat: int | None
    cell_count: int
    markdown_cell_count: int
    code_cell_count: int
    executed_code_cell_count: int
    code_cell_output_count: int
    error_message: str | None = None

    @property
    def has_no_saved_outputs(self) -> bool:
        """Return True if no code cell has saved outputs."""

        return self.code_cell_output_count == 0

    @property
    def has_no_execution_counts(self) -> bool:
        """Return True if no code cell has execution counts."""

        return self.executed_code_cell_count == 0

    @property
    def is_clean(self) -> bool:
        """Return True if the notebook is safe to commit."""

        return (
            self.exists
            and self.valid_json
            and self.nbformat == 4
            and self.cell_count > 0
            and self.has_no_saved_outputs
            and self.has_no_execution_counts
            and self.error_message is None
        )

    def as_dict(self) -> dict[str, str | int | bool | None]:
        """Return validation result as a dictionary."""

        data = asdict(self)
        data["has_no_saved_outputs"] = self.has_no_saved_outputs
        data["has_no_execution_counts"] = self.has_no_execution_counts
        data["is_clean"] = self.is_clean
        return data


def validate_notebook(path: Path) -> NotebookValidation:
    """Validate one Jupyter notebook file."""

    if not path.exists():
        return NotebookValidation(
            path=str(path),
            exists=False,
            valid_json=False,
            nbformat=None,
            cell_count=0,
            markdown_cell_count=0,
            code_cell_count=0,
            executed_code_cell_count=0,
            code_cell_output_count=0,
            error_message="Notebook does not exist.",
        )

    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return NotebookValidation(
            path=str(path),
            exists=True,
            valid_json=False,
            nbformat=None,
            cell_count=0,
            markdown_cell_count=0,
            code_cell_count=0,
            executed_code_cell_count=0,
            code_cell_output_count=0,
            error_message=str(exc),
        )

    cells = notebook.get("cells", [])
    code_cells = [cell for cell in cells if cell.get("cell_type") == "code"]
    markdown_cells = [cell for cell in cells if cell.get("cell_type") == "markdown"]

    executed_code_cell_count = sum(
        1 for cell in code_cells if cell.get("execution_count") is not None
    )
    code_cell_output_count = sum(len(cell.get("outputs", [])) for cell in code_cells)

    return NotebookValidation(
        path=str(path),
        exists=True,
        valid_json=True,
        nbformat=notebook.get("nbformat"),
        cell_count=len(cells),
        markdown_cell_count=len(markdown_cells),
        code_cell_count=len(code_cells),
        executed_code_cell_count=executed_code_cell_count,
        code_cell_output_count=code_cell_output_count,
    )


def validate_notebook_directory(notebook_dir: Path) -> list[NotebookValidation]:
    """Validate all notebooks inside a directory recursively."""

    notebooks = sorted(notebook_dir.rglob("*.ipynb"))
    return [validate_notebook(path) for path in notebooks]


def render_notebook_validation_report(
    validations: list[NotebookValidation],
) -> str:
    """Render notebook validation results as Markdown."""

    clean_count = sum(1 for validation in validations if validation.is_clean)

    lines = [
        "# Notebook Validation Report",
        "",
        "## Summary",
        "",
        f"- Notebooks checked: {len(validations)}",
        f"- Clean notebooks: {clean_count}",
        f"- Notebooks requiring attention: {len(validations) - clean_count}",
        "",
        "## Notebook Checks",
        "",
        "| Path | Cells | Markdown | Code | Executed Code Cells | Saved Outputs | Clean |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]

    for validation in validations:
        lines.append(
            "| "
            f"{validation.path} | "
            f"{validation.cell_count} | "
            f"{validation.markdown_cell_count} | "
            f"{validation.code_cell_count} | "
            f"{validation.executed_code_cell_count} | "
            f"{validation.code_cell_output_count} | "
            f"{validation.is_clean} |"
        )

    if not validations:
        lines.extend(
            [
                "",
                "No notebooks were found.",
            ]
        )

    lines.extend(
        [
            "",
            "## Commit Rule",
            "",
            "Notebook files should be committed without saved outputs or execution counts.",
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def write_notebook_validation_report(
    validations: list[NotebookValidation],
    output_path: Path,
) -> Path:
    """Write notebook validation report."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_notebook_validation_report(validations),
        encoding="utf-8",
    )
    return output_path
