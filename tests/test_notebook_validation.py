import json
from pathlib import Path

from floodrisk.notebooks.validation import (
    render_notebook_validation_report,
    validate_notebook,
    validate_notebook_directory,
    write_notebook_validation_report,
)


def make_notebook(path: Path, *, executed: bool = False, output: bool = False) -> Path:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["# Test\n"],
            },
            {
                "cell_type": "code",
                "execution_count": 1 if executed else None,
                "metadata": {},
                "outputs": [{"output_type": "stream", "name": "stdout", "text": "x"}]
                if output
                else [],
                "source": ["print('x')\n"],
            },
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.write_text(json.dumps(notebook), encoding="utf-8")
    return path


def test_validate_notebook_accepts_clean_notebook(tmp_path: Path):
    path = make_notebook(tmp_path / "clean.ipynb")

    validation = validate_notebook(path)

    assert validation.exists is True
    assert validation.valid_json is True
    assert validation.nbformat == 4
    assert validation.is_clean is True


def test_validate_notebook_detects_saved_output(tmp_path: Path):
    path = make_notebook(tmp_path / "dirty.ipynb", output=True)

    validation = validate_notebook(path)

    assert validation.code_cell_output_count == 1
    assert validation.has_no_saved_outputs is False
    assert validation.is_clean is False


def test_validate_notebook_detects_execution_count(tmp_path: Path):
    path = make_notebook(tmp_path / "executed.ipynb", executed=True)

    validation = validate_notebook(path)

    assert validation.executed_code_cell_count == 1
    assert validation.has_no_execution_counts is False
    assert validation.is_clean is False


def test_validate_notebook_reports_missing_file(tmp_path: Path):
    validation = validate_notebook(tmp_path / "missing.ipynb")

    assert validation.exists is False
    assert validation.is_clean is False
    assert validation.error_message == "Notebook does not exist."


def test_validate_notebook_directory(tmp_path: Path):
    make_notebook(tmp_path / "a.ipynb")
    make_notebook(tmp_path / "nested" / "b.ipynb") if False else None

    nested = tmp_path / "nested"
    nested.mkdir()
    make_notebook(nested / "b.ipynb")

    validations = validate_notebook_directory(tmp_path)

    assert len(validations) == 2
    assert all(validation.is_clean for validation in validations)


def test_render_notebook_validation_report(tmp_path: Path):
    path = make_notebook(tmp_path / "clean.ipynb")
    validations = [validate_notebook(path)]

    report = render_notebook_validation_report(validations)

    assert "Notebook Validation Report" in report
    assert "Clean notebooks: 1" in report


def test_write_notebook_validation_report(tmp_path: Path):
    path = make_notebook(tmp_path / "clean.ipynb")
    output_path = tmp_path / "notebook_validation_report.md"

    saved_path = write_notebook_validation_report(
        [validate_notebook(path)],
        output_path,
    )

    assert saved_path.exists()
    assert "Notebook Validation Report" in saved_path.read_text(encoding="utf-8")
