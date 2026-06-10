# Current Project Capabilities

This document summarizes what the project can currently do after the experimental
AI pipeline merge.

## 1. Transparent Flood Risk Scoring

The project includes a rule-based flood risk engine that produces interpretable
risk scores from rainfall, water level, warning, geospatial, and population
context.

This remains useful because it is explainable and does not depend on a trained
machine learning model.

## 2. Experimental AI Flood Prediction

The project now includes an experimental machine learning pipeline trained on the
Kaggle Malaysia flood and flash flood dataset.

The current experimental model:

- uses `Flood` as the target column
- uses weather, rainfall, city, month, and monsoon features
- saves a local `joblib` model artifact
- saves model metadata
- exposes prediction through FastAPI
- is tested through automated API and ML tests

## 3. API Capabilities

The FastAPI app supports:

- health checks
- rule-based flood risk scoring
- experimental model status inspection
- experimental flood prediction

The experimental prediction endpoint returns:

- model availability
- flood probability
- predicted flood boolean
- selected threshold
- warning level
- source and guardrail metadata

## 4. Streamlit Capabilities

The Streamlit app provides an interactive dashboard for the flood risk workflow
and now includes experimental AI model readiness visibility.

## 5. Data Source Status

The project currently separates data sources into two tracks:

| Track | Source | Role |
|---|---|---|
| Experimental ML | Kaggle Malaysia flood dataset | Baseline training and API demo |
| Official validation | EM-DAT | Official flood event review and validation |
| Official validation | MyWater / DID exports | Future Malaysia-local flood event validation |

## 6. Guardrails

The experimental AI model is not presented as an official verified flood warning
system.

The project keeps this distinction explicit:

- Kaggle is used for experimental baseline training only
- EM-DAT and MyWater remain official validation tracks
- users are told to follow official Malaysian warnings and emergency instructions

## 7. Current Engineering Quality

The project currently includes:

- automated tests
- Ruff linting and formatting
- model training reports
- threshold tuning reports
- model artifact metadata
- API smoke-test scripts
- local API runner script
- source review documents
- ML readiness reports

## 8. Next Development Direction

Recommended next steps:

1. polish the README for portfolio presentation
2. add sample API request/response examples
3. add Streamlit screenshots or demo GIFs
4. compare Kaggle predictions against official EM-DAT/MyWater events
5. prepare a release tag for the experimental AI pipeline milestone
