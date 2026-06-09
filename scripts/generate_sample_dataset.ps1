$ErrorActionPreference = "Stop"

Set-Location "C:\Users\Danish\Coding\Project\AI\malaysia-flood-risk-ai"

conda activate flood-ai

$env:PYTHONPATH = "src;."

python -m floodrisk.data.sample_dataset
