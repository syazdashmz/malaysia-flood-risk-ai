# Project Status

## Current Version

v0.5.0 Experimental AI Baseline Pipeline

## Completed

- Project repository created and pushed to GitHub
- Python package structure created
- Conda environment configured
- Transparent flood-risk scoring engine implemented
- Pydantic input/output schemas implemented
- FastAPI backend implemented
- Streamlit demo app implemented
- Sample Malaysia location presets added
- Sample generated demo dataset added
- Malaysia coordinate validation added
- Automated tests added
- Ruff formatting and linting workflow added
- GitHub Actions CI added
- MIT License added
- README, usage, methodology, data source, and deployment docs added

## Current Data Status

No real external flood, rainfall, elevation, land cover, river, or historical flood datasets have been downloaded yet.

The current MVP uses:

- Manual input features
- Transparent scoring logic
- Small generated sample demo dataset
- Sample Malaysia location presets

## Current Model Status

An experimental Kaggle-based Logistic Regression flood baseline has been trained
for research workflow testing.

The main public demo prediction output still comes from a transparent scoring
engine. The Kaggle model is available only as an experimental proxy baseline and
must not be presented as the final official verified Malaysia flood model.

Experimental model integration:

- local model artifact path: `models/kaggle_flood_baseline.joblib`
- local metadata path: `models/kaggle_flood_baseline_metadata.json`
- API status endpoint: `GET /experimental/flood/model/status`
- API prediction endpoint: `POST /experimental/flood/predict`
- workflow runner: `.\scripts\run_experimental_ai_pipeline.ps1`

## Phase 2 Weather Pipeline Progress

Completed:

- MET Malaysia weather API client
- Small weather forecast sample fetch
- Small weather warning sample fetch
- Raw data manifest recording
- Idempotent manifest upsert logic
- JSON-to-CSV normalization utility
- Weather sample data quality profiling
- Weather signal feature extraction
- One-command weather pipeline runner

Current local pipeline command:

    .\scripts\run_weather_pipeline.ps1

Current weather pipeline outputs:

- Raw JSON samples in data/raw/weather/
- Normalized CSV files in data/interim/weather/
- Processed weather feature table in data/processed/weather/
- Quality report in reports/weather_sample_profile.md
- Structured manifest in data/raw/manifest.jsonl

Git tracking rule:

- Raw, interim, and processed data files remain ignored.
- Lightweight metadata and quality reports may be tracked.

## App/API Weather Integration Progress

Completed:

- FastAPI weather summary endpoint at GET /weather/summary
- Streamlit sidebar display for latest weather pipeline summary
- Streamlit manual-mode default weather signal from local generated summary
- Weather summary loader utility for app/API reuse

Current limitation:

- Weather integration uses the latest local sample summary.
- It is not yet location-specific or historical.

## Next Major Phase

Phase 2: Real Data Acquisition

Planned work:

- Download or fetch real public data sources
- Validate data licensing and usability
- Build data ingestion scripts
- Clean and normalize raw datasets
- Create geospatial feature extraction pipeline
- Prepare machine-learning-ready training dataset

## MVP Limitations

- No real-time data integration yet
- No trained ML model yet
- No official warning authority
- No production deployment yet
- No real geospatial feature extraction yet
- No historical validation against real flood events yet

## Research Disclaimer

This project is for research, education, portfolio, and public awareness only.

It is not an official flood warning system.

## Patch Status - 0.2.1

Completed:

- Improved no-risk weather signal handling.
- Added tests for no-rain and no-advisory phrases.
- Rebuilt weather pipeline reports after classification fix.

Current weather sample signal counts:

- none: 4
- advisory: 0
- warning: 2
- severe: 0

## Phase 3 Status - Geospatial Foundation

Completed:

- Created reusable Malaysia geospatial bounding-box module.
- Moved coordinate bounding-box logic into the geospatial layer while preserving existing validation behavior.
- Added planned administrative boundary data source registry.
- Added expected local boundary artifact plan.
- Added vector dataset validation utilities for future GeoJSON/Shapefile files.
- Added geospatial validation report runner.
- Added geospatial summary loader for app/API integration.
- Added `/geospatial/summary` API endpoint.
- Added Streamlit geospatial readiness summary.

Current geospatial readiness:

- planned artifacts: 3
- available artifacts: 0
- missing artifacts: 3
- valid vector datasets: 0
- boundary data available: False

Current limitation:

- Real administrative boundary files are not bundled yet.
- Bounding-box validation is still broad and does not replace point-in-polygon boundary validation.

## Release Readiness - v0.3.0

The v0.3.0 Geospatial Foundation Pipeline milestone is ready for release.

Validation:

- 82 tests passed locally.
- Geospatial checks completed successfully.
- Boundary artifacts are correctly reported as planned but missing.
- No unverified administrative boundary files are bundled.

## v0.4.0 Notebook and ML Readiness Foundation

The v0.4.0 milestone adds the notebook, EDA, and ML-readiness foundation.

Current decision:

- Initial notebook-based EDA is ready.
- Real supervised ML training remains blocked.

Key additions:

- notebook validation
- notebook smoke execution
- notebook data catalog
- initial EDA report
- training dataset design
- feature table generation plan
- feature table builder dry run
- target label source plan
- combined ML training readiness gate
- complete ML readiness suite runner

See:

    docs/V0_4_0_MILESTONE.md
    docs/ML_TRAINING_READINESS.md

## Release Readiness - v0.4.0

The v0.4.0 Notebook and ML Readiness Foundation milestone is ready for release.

Validation:

- 162 tests passed locally.
- Notebook checks completed successfully.
- Notebook data catalog includes EDA and ML-readiness reports.
- ML training readiness gate correctly keeps real supervised ML training blocked.

Current ML training decision:

- Initial notebook-based EDA is ready.
- Experimental Kaggle baseline training is available for workflow testing.
- Real official supervised ML training remains blocked until a verified target label and schema-valid training table exist.

## v0.5.0 Experimental AI Baseline Pipeline

The v0.5.0 continuation adds an API-facing experimental AI model workflow.

Key additions:

- reusable experimental flood model serving utilities
- trained model artifact output from the Kaggle baseline trainer
- local model metadata output
- experimental FastAPI model status endpoint
- experimental FastAPI prediction endpoint
- Streamlit model-readiness sidebar summary
- focused tests for model status, feature mapping, and prediction output
- clear AI engineering workflow documentation

Current decision:

- Use the Kaggle model for experimental research and API workflow testing.
- Keep the transparent rule-based scoring engine as the stable public demo.
- Keep real official supervised ML training blocked until verified target labels exist.
