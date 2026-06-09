# Phase 2 Data Acquisition Plan

## Objective

Build a clean, reproducible, Malaysia-focused data acquisition pipeline for flood-risk modelling.

This phase prepares the project to collect, validate, document, and process real public datasets.

## Current Rule

Do not mix raw downloaded data directly into source code.

All real external datasets must go through this flow:

    data/raw
    data/interim
    data/processed

## Data Categories

### 1. Boundary Data

Purpose:

- Define Malaysia study area
- Validate coordinates
- Clip geospatial datasets
- Build grid cells for modelling

Planned examples:

- Malaysia administrative boundary
- State boundary
- District boundary

### 2. Elevation Data

Purpose:

- Extract elevation
- Derive slope
- Identify low-lying flood-prone areas

Planned examples:

- NASA SRTM DEM
- Copernicus DEM

### 3. Hydrology Data

Purpose:

- Calculate distance to rivers
- Detect river-adjacent exposure
- Support water-level station matching

Planned examples:

- OpenStreetMap waterways
- River network data
- Drainage-related layers

### 4. Rainfall and Weather Data

Purpose:

- Add dynamic hazard indicators
- Estimate rainfall intensity
- Support short-term flood risk prediction

Planned examples:

- MET Malaysia weather forecast
- MET Malaysia warning data
- Rainfall station data if accessible

### 5. Water-Level Data

Purpose:

- Add river/station status
- Support alert, warning, and danger classification

Planned examples:

- Public InfoBanjir station data

### 6. Land Cover Data

Purpose:

- Detect urban, vegetation, water, agriculture, and bare land classes
- Estimate runoff and surface absorption characteristics

Planned examples:

- Copernicus Global Land Cover
- ESA WorldCover

### 7. Historical Flood Data

Purpose:

- Create target labels
- Validate model predictions
- Compare against real flood events

Planned examples:

- Public historical flood records
- Disaster reports
- News-derived or manually curated flood inventory

## Data Governance Rules

- Record source URL
- Record download date
- Record license or access notes
- Preserve raw files unchanged
- Never manually edit raw files
- Create scripts for repeatability
- Keep large raw datasets out of Git
- Use DVC or external storage later for large datasets

## Phase 2 Deliverables

- Source inventory
- Data acquisition scripts
- Raw data manifest
- Data validation checks
- Initial Malaysia boundary file
- Initial elevation extraction workflow
- Initial feature engineering notebook
- Data quality report

## Not Yet Included

This phase has not yet downloaded any real dataset.

This document only prepares the project for real data acquisition.
