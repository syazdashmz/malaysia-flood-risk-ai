# Geospatial Foundation

## Purpose

This document tracks the geospatial foundation work for the next major project milestone.

Target milestone:

    v0.3.0 - Geospatial Foundation Pipeline

## Current Implementation

The project now has a dedicated geospatial module:

    src/floodrisk/geospatial/

The first module centralizes Malaysia bounding-box logic:

    src/floodrisk/geospatial/malaysia.py

This keeps coordinate validation reusable across:

- Pydantic input schemas
- API validation
- Streamlit validation
- future geospatial data pipelines
- future location-aware weather joins

## Current Malaysia Bounding Box

The current broad Malaysia bounding box is:

- minimum latitude: -1.5
- maximum latitude: 7.5
- minimum longitude: 99.0
- maximum longitude: 120.0

This is intentionally broad.

It is suitable for MVP-level coordinate rejection, but it is not a replacement for administrative boundary polygons.

## Current Limitation

The current validation checks only whether a coordinate falls within a broad rectangular bounding box.

It does not yet confirm whether the coordinate falls inside an actual Malaysian administrative boundary polygon.

## Next Recommended Work

Recommended next geospatial steps:

1. Define administrative boundary dataset requirements
2. Add a boundary data source registry
3. Add local placeholder manifest records for planned boundary datasets
4. Add GeoDataFrame loading utilities
5. Add geometry validity checks
6. Add point-in-boundary validation after a boundary dataset is selected

## Data Source Registry

The planned geospatial data source registry is documented in:

    docs/GEOSPATIAL_DATA_SOURCES.md

The code registry is located at:

    src/floodrisk/geospatial/sources.py

## Artifact Planning

The expected local geospatial artifact paths are documented in:

    reports/geospatial_artifact_plan.md

The artifact planning utility is located at:

    src/floodrisk/geospatial/artifacts.py

Generate the report with:

    python scripts/generate_geospatial_artifact_plan.py

## Vector Dataset Validation

Basic vector dataset validation utilities are located at:

    src/floodrisk/geospatial/vector.py

The validator checks:

- file existence
- row count
- CRS presence
- geometry column presence
- invalid geometry count
- empty geometry count

This prepares the project for safe validation of future GeoJSON or Shapefile boundary datasets.

## Geospatial Check Runner

The geospatial check runner is:

    .\scripts\run_geospatial_checks.ps1

It regenerates:

    reports/geospatial_artifact_plan.md
    reports/geospatial_validation_report.md

The validation report summarizes:

- planned artifacts
- available artifacts
- missing artifacts
- valid vector datasets

## Geospatial Summary Loader

The geospatial summary loader is located at:

    src/floodrisk/geospatial/summary.py

It provides a compact dictionary summary for future API and Streamlit integration.

Show the current summary with:

    python scripts/show_geospatial_summary.py

## API Integration

The geospatial readiness summary is available through the API endpoint:

    GET /geospatial/summary

This endpoint is intended for dashboards, health checks, and future UI integration.
