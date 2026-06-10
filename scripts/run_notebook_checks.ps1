$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

$ScriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDirectory

Set-Location $ProjectRoot

conda activate flood-ai

$env:PYTHONPATH = "src;."

Write-Host "Project root: $ProjectRoot"
Write-Host "Validating notebooks..."
python scripts\validate_notebooks.py
Write-Host "Notebook checks completed."
