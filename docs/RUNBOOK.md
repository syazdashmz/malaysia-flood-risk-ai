# Project Runbook

## Purpose

This runbook lists the main local commands for developing, testing, running, and validating Malaysia Flood Risk AI.

The PowerShell runner scripts are portable. They detect the project root from their own location, so they work from any clone of this repository.

## Environment

Activate the project environment:

    conda activate flood-ai

Recommended project root:

    C:\Users\Danish\Coding\Project\AI\malaysia-flood-risk-ai

## Daily Quality Check

Run all quality checks:

    .\scripts\run_quality.ps1

This runs:

    ruff check .
    ruff format --check .
    pytest

## Tests Only

Run tests:

    .\scripts\run_tests.ps1

## Weather Pipeline

Refresh the local Phase 2 weather sample workflow:

    .\scripts\run_weather_pipeline.ps1

This runs:

1. Fetch small MET Malaysia weather samples
2. Normalize raw JSON to flat CSV
3. Build weather feature table
4. Summarize weather risk signal
5. Generate weather data quality report
6. Validate generated weather outputs

Tracked weather reports:

    reports/weather_risk_signal_summary.json
    reports/weather_sample_profile.md
    reports/weather_pipeline_validation.md

Ignored local data artifacts:

    data/raw/weather/
    data/interim/weather/
    data/processed/weather/

## FastAPI Backend

Run the API:

    .\scripts\run_api.ps1

Useful local URLs:

    http://127.0.0.1:8000/docs
    http://127.0.0.1:8000/health
    http://127.0.0.1:8000/weather/summary

## Streamlit App

Run the app:

    .\scripts\run_app.ps1

Local URL:

    http://localhost:8501

## Recommended Local Workflow

For normal development:

1. Update code
2. Run quality checks

        .\scripts\run_quality.ps1

3. Commit changes

        git add .
        git commit -m "Your commit message"

4. Push

        git push

For weather-data refresh work:

1. Run the weather pipeline

        .\scripts\run_weather_pipeline.ps1

2. Review reports

        reports/weather_risk_signal_summary.json
        reports/weather_sample_profile.md
        reports/weather_pipeline_validation.md

3. Commit only lightweight metadata/report changes if needed

        git add data\raw\manifest.jsonl reports\
        git commit -m "Update weather pipeline reports"

## Current Limitations

The current weather workflow uses small live API samples only.

It is not yet:

- location-specific
- historical
- model-training-ready
- a complete hydrology dataset pipeline

## Geospatial Checks

Run the geospatial foundation checks with:

    .\scripts\run_geospatial_checks.ps1

This regenerates:

    reports/geospatial_artifact_plan.md
    reports/geospatial_validation_report.md

Expected current result:

- planned artifacts: 3
- available artifacts: 0
- missing artifacts: 3
- valid vector datasets: 0

This is expected until verified administrative boundary files are added locally.
