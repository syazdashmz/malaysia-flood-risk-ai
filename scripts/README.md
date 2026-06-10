# Scripts

## Portable Runner Scripts

These scripts detect the project root from their own file location.

Run them from the repository root with PowerShell.

## Main Scripts

### Run tests

    .\scripts\run_tests.ps1

### Run quality checks

    .\scripts\run_quality.ps1

### Run API

    .\scripts\run_api.ps1

### Run Streamlit app

    .\scripts\run_app.ps1

### Run weather data pipeline

    .\scripts\run_weather_pipeline.ps1

## Weather Pipeline Scripts

These are called by the weather pipeline runner:

    python scripts\fetch_weather_sample.py
    python scripts\normalize_weather_samples.py
    python scripts\build_weather_features.py
    python scripts\summarize_weather_features.py
    python scripts\profile_weather_samples.py
    python scripts\validate_weather_pipeline.py

## API Helper

Use this only when the API server is already running:

    .\scripts\test_predict_api.ps1

### Run geospatial checks

    .\scripts\run_geospatial_checks.ps1

### Show geospatial summary

    python scripts/show_geospatial_summary.py

### Run notebook checks

    .\scripts\run_notebook_checks.ps1

### Run dataset readiness checks

    .\scripts\run_dataset_readiness.ps1

### Run training table schema check

    .\scripts\run_training_schema_check.ps1

### Run notebook environment check

    .\scripts\run_notebook_environment_check.ps1

### Run notebook data catalog

    .\scripts\run_notebook_data_catalog.ps1

### Run notebook smoke tests

    .\scripts\run_notebook_smoke_tests.ps1

### Run initial EDA report

    .\scripts\run_initial_eda_report.ps1

### Run feature table plan

    .\scripts\run_feature_table_plan.ps1

### Run feature table builder dry run

    .\scripts\run_feature_table_builder_dry_run.ps1

### Run target label source plan

    .\scripts\run_target_label_source_plan.ps1

### Run ML training readiness gate

    .\scripts\run_ml_training_readiness.ps1
