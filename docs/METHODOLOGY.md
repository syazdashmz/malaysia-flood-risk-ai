# Research Methodology

## Objective

Build a Malaysia-wide flood-risk prediction and explanation system for research, education, and public awareness.

## Core Formulation

Flood risk is treated as a combination of susceptibility, dynamic hazard, exposure, and vulnerability.

Formula:

Flood Risk = Susceptibility x Dynamic Hazard x Exposure x Vulnerability

## Components

### 1. Susceptibility

Static physical conditions that make a location naturally flood-prone.

Examples:

- Low elevation
- Flat slope
- Close to river
- Flooded historically
- Built-up or wetland land cover

### 2. Dynamic Hazard

Changing environmental conditions that increase near-term risk.

Examples:

- Heavy 24-hour rainfall
- Accumulated 72-hour rainfall
- River water-level warning
- Severe weather warning

### 3. Exposure

People and assets that may be affected.

Examples:

- Population density
- Buildings
- Roads
- Public facilities

### 4. Vulnerability

How sensitive the area is to flood damage.

Examples:

- Drainage limitations
- Urban density
- Critical infrastructure
- Low-lying settlements

## Phase 1 Model

The first model is a transparent weighted scoring engine.

Purpose:

- Explain risk clearly
- Validate app/API workflow
- Create a baseline before machine learning

## Phase 2 Model

Train supervised ML models after building a cleaned dataset.

Candidate models:

- Logistic Regression
- Random Forest
- XGBoost
- LightGBM

## Evaluation

Use metrics that matter for flood safety:

- ROC-AUC
- PR-AUC
- Recall
- False negative rate
- Brier score
- Calibration curve
- Spatial validation
- Temporal validation

## Public Disclaimer

This project is not an official emergency system. Results are for research and awareness only.
