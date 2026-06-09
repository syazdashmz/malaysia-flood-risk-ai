# Project Status

## Current Version

v0.2.0 MVP foundation

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

No machine-learning model has been trained yet.

The current prediction output comes from a transparent scoring engine, not a trained ML model.

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

    .\scripts
un_weather_pipeline.ps1

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
