# Weather Data Pipeline

## Purpose

This pipeline runs the current Phase 2 weather data workflow end to end.

It fetches small weather API samples, normalizes them, creates a feature table, and generates a data quality report.

## Command

Run from the project root:

    .\scripts\run_weather_pipeline.ps1

## Pipeline Steps

1. Fetch small weather samples

    python scripts\fetch_weather_sample.py

2. Normalize raw JSON samples into flat CSV files

    python scripts\normalize_weather_samples.py

3. Build weather feature table

    python scripts\build_weather_features.py

4. Generate weather sample data quality profile

    python scripts\profile_weather_samples.py

## Inputs

The pipeline fetches small samples from:

- https://api.data.gov.my/weather/forecast
- https://api.data.gov.my/weather/warning

## Local Outputs

Raw JSON samples:

    data/raw/weather/

Normalized CSV samples:

    data/interim/weather/

Processed weather feature table:

    data/processed/weather/

Weather quality report:

    reports/weather_sample_profile.md

Structured raw data manifest:

    data/raw/manifest.jsonl

## Git Tracking Rules

Raw, interim, and processed data artifacts are ignored by Git.

The structured manifest is tracked because it records dataset metadata.

The quality report is tracked because it is lightweight and useful for review.

## Current Limitation

This is still a small sample workflow.

It is not yet a full historical weather dataset ingestion pipeline.
