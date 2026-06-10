from pathlib import Path

SCRIPT_PATH = Path("scripts/run_api.ps1")


def test_run_api_script_exists():
    assert SCRIPT_PATH.exists()


def test_run_api_script_sets_pythonpath():
    content = SCRIPT_PATH.read_text(encoding="utf-8")

    assert '$env:PYTHONPATH = "src"' in content
    assert "uvicorn api.main:app --reload --port 8000" in content
