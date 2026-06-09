$ErrorActionPreference = "Stop"

Set-Location "C:\Users\Danish\Coding\Project\AI\malaysia-flood-risk-ai"

conda activate flood-ai

$env:PYTHONPATH = "src;."

streamlit run app\streamlit_app.py
