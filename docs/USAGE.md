# Usage Guide

## 1. Activate Environment

    conda activate flood-ai

## 2. Run Tests

    pytest

Expected result:

    9 passed

## 3. Run API

    .\scripts\run_api.ps1

Open:

    http://127.0.0.1:8000/docs

## 4. Run Streamlit App

    .\scripts\run_app.ps1

Open:

    http://localhost:8501

## 5. Generate Sample Dataset

    .\scripts\generate_sample_dataset.ps1

Output file:

    data/samples/sample_malaysia_locations.csv

## 6. Stop Running Server

Use:

    Ctrl + C

## Weather Pipeline Integration

The Streamlit app can now read the latest local weather pipeline summary from:

    reports/weather_risk_signal_summary.json

When the summary is available, the app:

- Shows the latest weather pipeline signal in the sidebar
- Displays record counts from the local weather sample workflow
- Uses the generated weather warning signal as the default manual-mode weather input

To refresh the local weather signal before opening the app:

    .\scripts
un_weather_pipeline.ps1

Then run the app:

    .\scripts
un_app.ps1

## API Geospatial Summary

The API exposes the current geospatial readiness summary at:

    GET /geospatial/summary

The endpoint reports:

- planned geospatial artifact count
- available artifact count
- missing artifact count
- valid vector dataset count
- whether boundary data is currently available
- artifact-level statuses

At this stage, the expected result is that planned boundary artifacts are still missing until verified boundary datasets are added.
