$ErrorActionPreference = "Stop"

Set-Location "C:\Users\Danish\Coding\Project\AI\malaysia-flood-risk-ai"

conda activate flood-ai

$env:PYTHONPATH = "src;."

uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
