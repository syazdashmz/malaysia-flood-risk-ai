import json
from pathlib import Path


def test_project_readiness_notebook_exists():
    path = Path("notebooks/00_project_readiness.ipynb")

    assert path.exists()


def test_project_readiness_notebook_is_valid_json():
    path = Path("notebooks/00_project_readiness.ipynb")
    notebook = json.loads(path.read_text(encoding="utf-8"))

    assert notebook["nbformat"] == 4
    assert "cells" in notebook
    assert len(notebook["cells"]) >= 5


def test_project_readiness_notebook_has_no_saved_outputs():
    path = Path("notebooks/00_project_readiness.ipynb")
    notebook = json.loads(path.read_text(encoding="utf-8"))

    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]

    assert code_cells
    assert all(cell["execution_count"] is None for cell in code_cells)
    assert all(cell["outputs"] == [] for cell in code_cells)


def test_notebook_docs_exist():
    assert Path("notebooks/README.md").exists()
    assert Path("docs/NOTEBOOKS.md").exists()
