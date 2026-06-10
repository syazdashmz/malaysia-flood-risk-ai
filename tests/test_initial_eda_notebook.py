import json
from pathlib import Path


def test_initial_eda_notebook_exists():
    assert Path("notebooks/exploration/01_initial_data_catalog_eda.ipynb").exists()


def test_initial_eda_notebook_is_valid_json():
    path = Path("notebooks/exploration/01_initial_data_catalog_eda.ipynb")
    notebook = json.loads(path.read_text(encoding="utf-8"))

    assert notebook["nbformat"] == 4
    assert len(notebook["cells"]) >= 8


def test_initial_eda_notebook_has_no_saved_outputs():
    path = Path("notebooks/exploration/01_initial_data_catalog_eda.ipynb")
    notebook = json.loads(path.read_text(encoding="utf-8"))

    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]

    assert code_cells
    assert all(cell["execution_count"] is None for cell in code_cells)
    assert all(cell["outputs"] == [] for cell in code_cells)


def test_initial_eda_notebook_mentions_no_model_training():
    path = Path("notebooks/exploration/01_initial_data_catalog_eda.ipynb")
    content = path.read_text(encoding="utf-8")

    assert "It does not train a model." in content
    assert "training readiness blockers" in content
