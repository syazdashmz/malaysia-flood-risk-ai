# Changelog

## 0.2.0 - Phase 2 Weather Pipeline

### Added

- MET Malaysia weather API client
- Small live weather sample acquisition workflow
- Weather JSON normalization utility
- Weather feature extraction utility
- Weather risk signal summary
- Weather pipeline validation report
- FastAPI weather summary endpoint
- Streamlit weather pipeline summary display
- Portable project runner scripts
- Project runbook

### Notes

- Raw, interim, and processed weather data artifacts remain ignored.
- Lightweight metadata and reports are tracked for review.
- Weather integration currently uses small sample data only.

## 0.2.1 - Weather Signal Classification Patch

### Fixed

- Improved no-risk weather text classification.
- Prevented phrases such as Tiada hujan, No rain, No Advisory, and No weather advisory from being misclassified as advisory.
- Preserved mixed forecast behavior where a no-risk phrase and a valid positive signal can still produce an advisory.

### Validation

- 55 tests passed locally.
- Weather pipeline validation report shows Valid: True.
- Weather signal summary now reports none: 4, warning: 2, advisory: 0, severe: 0 for the current sample.

## Unreleased

## 0.3.0 - Geospatial Foundation Pipeline

### Added

- Added geospatial foundation module for Malaysia bounding-box utilities.
- Added planned geospatial data source registry.
- Added geospatial artifact planning report.
- Added vector dataset validation utilities for future GeoJSON/Shapefile boundary files.
- Added geospatial validation report runner.
- Added geospatial summary loader.
- Added `/geospatial/summary` API endpoint.
- Added Streamlit sidebar geospatial readiness summary.

### Validation

- 82 tests passed locally.
- Geospatial validation currently reports 3 planned artifacts, 0 available artifacts, 3 missing artifacts, and 0 valid vector datasets.

### Added

- Weather summary loader utility for app/API integration

- Streamlit weather pipeline summary display

- FastAPI weather summary endpoint

- MET Malaysia weather API client
- Small real weather sample acquisition workflow
- Weather JSON normalization utility
- Weather feature extraction utility
- Weather data quality profiling report
- One-command weather pipeline runner
- Idempotent raw data manifest recording
All notable changes to this project will be documented in this file.

## v0.1.0 - MVP Foundation

### Added

- Transparent flood-risk scoring engine
- FastAPI prediction API
- Streamlit demo application
- Malaysia coordinate validation
- Generated sample Malaysia flood-risk dataset
- Sample location presets
- Data source registry
- Research methodology documentation
- Usage documentation
- Deployment guide
- GitHub Actions CI workflow
- Ruff formatting and linting workflow
- MIT License

### Current Scope

This release is a software foundation MVP.

It does not yet include real downloaded datasets or trained machine-learning models.
