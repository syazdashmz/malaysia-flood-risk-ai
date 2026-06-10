$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

$ScriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDirectory

Set-Location $ProjectRoot

conda activate flood-ai

$env:PYTHONPATH = "src;."

Write-Host "Project root: $ProjectRoot"
Write-Host "Running experimental AI flood pipeline..."

Write-Host "Step 1/4: Profiling Kaggle experimental dataset..."
python scripts\profile_kaggle_baseline_dataset.py

Write-Host "Step 2/4: Training experimental flood baseline..."
python scripts\train_kaggle_flood_baseline.py

Write-Host "Step 3/4: Tuning experimental decision thresholds..."
python scripts\tune_kaggle_flood_threshold.py

Write-Host "Step 4/4: Running focused API and ML tests..."
python -m pytest tests\test_experimental_flood_model.py tests\test_api.py tests\test_kaggle_flood_baseline_training.py tests\test_kaggle_flood_threshold_tuning.py -q

Write-Host "Experimental AI flood pipeline completed."
