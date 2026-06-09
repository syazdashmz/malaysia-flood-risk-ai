$ErrorActionPreference = "Stop"

Set-Location "C:\Users\Danish\Coding\Project\AI\malaysia-flood-risk-ai"

conda activate flood-ai

$env:PYTHONPATH = "src;."

ruff format .
ruff check . --fix
pytest
git status
