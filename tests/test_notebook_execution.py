import json
from pathlib import Path

from floodrisk.notebooks.execution import (
    execute_notebook_smoke_test,
    render_notebook_execution_report,
    smoke_test_notebook_directory,
    write_notebook_execution_report,
)


def write_notebook(path: Path, source: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [source],
            }
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.write_text(json.dumps(notebook), encoding="utf-8")
    return path


def test_execute_notebook_smoke_test_success(tmp_path: Path):
    path = write_notebook(tmp_path / "success.ipynb", "x = 1\nx + 1\n")

    result = execute_notebook_smoke_test(path, tmp_path)

    assert result.success is True
    assert result.executed_code_cell_count == 1


def test_execute_notebook_smoke_test_failure(tmp_path: Path):
    path = write_notebook(tmp_path / "failure.ipynb", "raise RuntimeError('boom')\n")

    result = execute_notebook_smoke_test(path, tmp_path)

    assert result.success is False
    assert result.error_cell_index == 0
    assert "RuntimeError" in str(result.error_message)


def test_smoke_test_notebook_directory(tmp_path: Path):
    write_notebook(tmp_path / "a.ipynb", "x = 1\n")
    write_notebook(tmp_path / "nested" / "b.ipynb", "y = 2\n")

    summary = smoke_test_notebook_directory(tmp_path, tmp_path)

    assert summary.notebook_count == 2
    assert summary.successful_count == 2
    assert summary.failed_count == 0
    assert summary.ready_for_notebook_eda is True


def test_render_notebook_execution_report(tmp_path: Path):
    path = write_notebook(tmp_path / "success.ipynb", "x = 1\n")
    summary = smoke_test_notebook_directory(tmp_path, tmp_path)

    report = render_notebook_execution_report(summary)

    assert "Notebook Smoke Execution Report" in report
    assert "Ready for notebook EDA: True" in report
    assert str(path) in report


def test_write_notebook_execution_report(tmp_path: Path):
    write_notebook(tmp_path / "success.ipynb", "x = 1\n")
    summary = smoke_test_notebook_directory(tmp_path, tmp_path)
    output_path = tmp_path / "notebook_execution_report.md"

    saved_path = write_notebook_execution_report(summary, output_path)

    assert saved_path.exists()
    assert "Notebook Smoke Execution Report" in saved_path.read_text(encoding="utf-8")
