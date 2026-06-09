# Malaysia Flood Risk AI

A Malaysia-focused flood risk prediction and explainability research project.

This project estimates flood risk for locations in Malaysia using geospatial, rainfall, hydrology, exposure, and machine-learning-ready features.

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
