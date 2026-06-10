# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

### Planned

- Verified historical flood target label source integration.
- Observation date and district derivation.
- Schema-valid model-ready training table.
- Train/validation split strategy.
- Baseline ML experiment planning after readiness gate clears.

## [0.5.0] - 2026-06-10

### Added

- Added experimental Kaggle flood model serving utilities.
- Added local model artifact and metadata output to the Kaggle trainer.
- Added experimental FastAPI model status endpoint.
- Added experimental FastAPI prediction endpoint.
- Added Streamlit experimental model-readiness summary.
- Added one-command experimental AI pipeline runner.
- Added direct AI engineering workflow documentation.
- Added tests for experimental model status, feature mapping, prediction output, and API validation.

### Guardrail

- The Kaggle model is experimental proxy AI only.
- The transparent scoring engine remains the public demo baseline.
- Real official supervised ML training remains blocked until verified `flood_occurred` labels exist.

## [0.4.0] - 2026-06-10

### Added

- Added notebook foundation and initial EDA notebook.
- Added notebook validation and smoke execution reports.
- Added notebook data catalog with ML-readiness reports.
- Added initial EDA report generator.
- Added training dataset design and schema validator.
- Added feature table generation plan.
- Added feature table builder dry-run.
- Added target label source plan.
- Added combined ML training readiness gate.
- Added complete ML readiness suite runner.
- Added v0.4.0 milestone documentation.

### Validation

- 162 tests passed locally.
- Notebook smoke execution checked 2 notebooks successfully.
- Notebook validation confirmed 2 clean notebooks.
- Notebook data catalog reports 14 assets, 13 available, and 1 missing.
- ML readiness gate correctly keeps real supervised ML training blocked.

### Training Status

- Real supervised ML training remains blocked.
- The rule-based `risk_score` is not accepted as the real target label.
- A verified historical `flood_occurred` target source is still required.
- A schema-valid, non-empty model-ready training table is still required.

## [0.3.0] - Geospatial Foundation Pipeline

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
- Geospatial validation reports 3 planned artifacts, 0 available artifacts, 3 missing artifacts, and 0 valid vector datasets.

### Limitations

- No real administrative boundary files are bundled yet.
- No point-in-polygon boundary validation against real polygons yet.
- No location-specific weather-to-boundary joins yet.

## [0.2.1] - Weather Signal Classification Patch

### Fixed

- Improved no-risk weather text classification.
- Prevented phrases such as Tiada hujan, No rain, No Advisory, and No weather advisory from being misclassified as advisory.
- Preserved mixed forecast behavior where a no-risk phrase and a valid positive signal can still produce an advisory.

### Validation

- 55 tests passed locally.
- Weather pipeline validation report shows Valid: True.
- Weather signal summary reports none: 4, warning: 2, advisory: 0, severe: 0 for the current sample.

## [0.2.0] - Phase 2 Weather Pipeline

### Added

- Added MET Malaysia weather API client.
- Added small live weather sample acquisition workflow.
- Added weather JSON normalization utility.
- Added weather feature extraction utility.
- Added weather data quality profiling report.
- Added weather risk signal summary.
- Added weather pipeline validation report.
- Added FastAPI weather summary endpoint.
- Added Streamlit weather pipeline summary display.
- Added portable project runner scripts.
- Added project runbook.

### Notes

- Raw, interim, and processed weather data artifacts remain ignored.
- Lightweight metadata and reports are tracked for review.
- Weather integration currently uses small sample data only.

## [0.1.0] - MVP Foundation

### Added

- Added transparent flood-risk scoring engine.
- Added FastAPI prediction API.
- Added Streamlit demo application.
- Added Malaysia coordinate validation.
- Added generated sample Malaysia flood-risk dataset.
- Added sample location presets.
- Added data source registry.
- Added research methodology documentation.
- Added usage documentation.
- Added deployment guide.
- Added GitHub Actions CI workflow.
- Added Ruff formatting and linting workflow.
- Added MIT License.

### Current Scope

This release is a software foundation MVP.

It does not yet include real downloaded datasets or trained machine-learning models.
