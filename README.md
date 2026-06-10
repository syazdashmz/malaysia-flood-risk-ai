# Malaysia Flood Risk AI

[![CI](https://github.com/syazdashmz/malaysia-flood-risk-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/syazdashmz/malaysia-flood-risk-ai/actions/workflows/ci.yml)

A Malaysia-focused flood risk prediction and explainability research project.

This project estimates flood risk for locations in Malaysia using geospatial, rainfall, hydrology, exposure, and machine-learning-ready features.

## Project Status

- Current version: v0.2.0 MVP foundation
- Status document: docs/PROJECT_STATUS.md
- Changelog: CHANGELOG.md

No real external datasets have been downloaded yet.
No machine-learning model has been trained yet.

## Current Status

MVP foundation completed.

- Transparent flood-risk scoring engine
- FastAPI prediction backend
- Streamlit public demo app
- Malaysia coordinate validation
- Sample Malaysia location presets
- Sample generated demo dataset
- Data source registry
- Research methodology documentation
- Automated tests

## Repository

- GitHub: https://github.com/syazdashmz/malaysia-flood-risk-ai
- CI Workflow: https://github.com/syazdashmz/malaysia-flood-risk-ai/actions/workflows/ci.yml

## Project Goal

Build a Malaysia-wide flood-risk intelligence platform that helps users understand flood risk through:

- Simple location-based prediction
- Clear risk score
- Risk class
- Top contributing factors
- Public-facing explanation
- API access
- Future real data integration
- Future machine-learning model training

## Important Disclaimer

This project is for research, education, portfolio, and public awareness only.

It is not an official emergency warning system.

Always follow official Malaysian flood warnings, local authorities, and emergency instructions.

## Tech Stack

- Python 3.12
- Conda / Miniforge
- FastAPI
- Streamlit
- Pydantic
- Pandas
- GeoPandas
- Rasterio
- scikit-learn
- XGBoost
- LightGBM
- MLflow
- DVC
- Pytest
- Ruff

## Project Structure

- api: FastAPI backend
- app: Streamlit web application
- configs: Data source registry and configuration files
- data: Local data folders
- docs: Research and data documentation
- models: Future trained model artifacts
- notebooks: Future Jupyter notebooks
- reports: Figures and reports
- scripts: Helper PowerShell scripts
- src/floodrisk: Main Python package
- tests: Automated tests

## Setup

Run from the project root:

    conda env create -f environment.yml
    conda activate flood-ai
    python -m ipykernel install --user --name flood-ai --display-name "Python (flood-ai)"

## Run Tests

    pytest

## Run API

    .\scripts\run_api.ps1

Open:

    http://127.0.0.1:8000/docs

## Run Web App

    .\scripts\run_app.ps1

Open:

    http://localhost:8501

## Generate Sample Dataset

    .\scripts\generate_sample_dataset.ps1

Output:

    data/samples/sample_malaysia_locations.csv

## Current MVP Inputs

- Latitude
- Longitude
- Elevation
- Slope
- Distance to nearest river
- Distance to nearest historical flood area
- 24-hour rainfall
- 72-hour rainfall
- Water-level status
- Weather-warning status
- Land-cover class
- Population density

## Current MVP Outputs

- Risk score from 0 to 100
- Risk class
- Confidence level
- Top risk factors
- Recommendation
- JSON output

## Planned Data Sources

- MET Malaysia forecast API
- MET Malaysia warning API
- Public InfoBanjir
- NASA SRTM DEM
- Copernicus Land Cover
- OpenStreetMap
- Historical flood inventory
- Malaysia administrative boundary

## Phase 2 Weather Pipeline

A small real-data weather sample pipeline has been added.

- Data source: MET Malaysia via Malaysia Open API
- Pipeline guide: docs/WEATHER_PIPELINE.md
- Command: .\scripts
un_weather_pipeline.ps1
- Quality report: reports/weather_sample_profile.md

This is a small sample workflow only. It is not yet a full historical ingestion pipeline.

## Research Roadmap

### Phase 1: Transparent MVP

Completed.

### Phase 2: Real Data Acquisition

Planned.

- Gather official and public flood-related data
- Clean historical flood inventory
- Add Malaysia boundary validation
- Add geospatial feature extraction
- Add rainfall and warning data clients

### Phase 3: Machine Learning Dataset

Planned.

- Create grid-based Malaysia dataset
- Engineer static and dynamic flood-risk features
- Avoid target leakage
- Add spatial and temporal validation

### Phase 4: Model Training

Planned.

- Logistic Regression baseline
- Random Forest
- XGBoost
- LightGBM
- Probability calibration
- SHAP explainability

### Phase 5: Deployment

Planned.

- Public Streamlit demo
- FastAPI deployment
- Docker support
- GitHub-ready documentation

## Deployment

The current MVP can be deployed as a Streamlit demo.

- App entry point: app/streamlit_app.py
- Lightweight dependency file: requirements.txt
- Deployment guide: docs/DEPLOYMENT.md

This deployment uses the transparent scoring engine and sample demo data only.

## License

This project is released under the MIT License.

## Project Runbook

For daily commands, local development workflow, weather pipeline usage, and app/API run instructions, see:

    docs/RUNBOOK.md

## Releases

Release history and milestone notes are documented in:

    docs/RELEASES.md

Latest release:

    v0.3.0 - Geospatial Foundation Pipeline

## Geospatial Foundation

The project includes a v0.3.0 geospatial foundation layer for future boundary-aware flood-risk modeling.

Current geospatial capabilities:

- Malaysia bounding-box utilities
- planned administrative boundary data source registry
- local geospatial artifact planning
- vector dataset validation utilities
- geospatial validation report runner
- geospatial readiness summary
- `/geospatial/summary` API endpoint
- Streamlit geospatial readiness sidebar

Current limitation:

- Administrative boundary files are planned but not bundled yet.
- Real point-in-boundary validation will be added only after authoritative boundary data is selected and licensing is verified.

Run geospatial checks with:

    .\scripts\run_geospatial_checks.ps1

## Next Milestone

Planned next milestone:

    v0.4.0 - Notebook and Data Exploration Foundation

The next phase will prepare reproducible notebook-based exploration before real AI/ML training.

