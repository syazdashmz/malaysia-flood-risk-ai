# Release Index

## v0.3.0 - Geospatial Foundation Pipeline

Release page:

    https://github.com/syazdashmz/malaysia-flood-risk-ai/releases/tag/v0.3.0

Main focus:

- Malaysia geospatial bounding-box module
- Planned administrative boundary data source registry
- Geospatial artifact planning report
- Vector dataset validation utilities for future GeoJSON/Shapefile files
- Geospatial validation report runner
- Geospatial readiness summary loader
- /geospatial/summary API endpoint
- Streamlit sidebar geospatial readiness summary
- Documentation for geospatial checks and release readiness

Validation:

- 82 tests passed locally
- Geospatial checks completed successfully

Current geospatial readiness:

- planned boundary artifacts: 3
- available boundary artifacts: 0
- missing boundary artifacts: 3
- valid vector datasets: 0
- boundary data available: False

Limitations:

- No real administrative boundary files are bundled yet
- No point-in-polygon boundary validation against real polygons yet
- No location-specific weather-to-boundary joins yet

## v0.2.1 - Weather Signal Classification Patch

Release page:

    https://github.com/syazdashmz/malaysia-flood-risk-ai/releases/tag/v0.2.1

Main focus:

- Patch release after v0.2.0
- Improved no-risk weather text classification
- Prevented no-rain and no-advisory phrases from being misclassified as advisory
- Preserved mixed forecast behavior where positive weather signals still count

Validation:

- 55 tests passed locally
- Weather pipeline validation: Valid True

Current weather sample signal counts:

- none: 4
- advisory: 0
- warning: 2
- severe: 0

## v0.2.0 - Phase 2 Weather Pipeline

Release page:

    https://github.com/syazdashmz/malaysia-flood-risk-ai/releases/tag/v0.2.0

Main focus:

- First real-data weather pipeline layer
- MET Malaysia weather API client
- Weather forecast and warning sample acquisition
- Weather JSON normalization
- Weather feature extraction
- Weather risk signal summary
- Weather pipeline validation
- FastAPI weather summary endpoint
- Streamlit weather pipeline summary display
- Portable PowerShell runner scripts
- Project runbook

Validation:

- 49 tests passed locally
- Weather pipeline validation: Valid True

Limitations:

- Small live API samples only
- Not yet location-specific
- Not yet historical
- Not yet model-training-ready

## v0.1.0 - MVP Transparent Risk Engine

Release page:

    https://github.com/syazdashmz/malaysia-flood-risk-ai/releases/tag/v0.1.0

Main focus:

- Initial project scaffold
- Transparent flood risk scoring engine
- FastAPI prediction endpoint
- Streamlit demonstration app
- Malaysia coordinate validation
- Sample Malaysia location presets
- Documentation and deployment notes
- CI workflow
- MIT license

Validation:

- MVP tests passed before release

## Current Development Direction

Next recommended milestone:

    v0.5.0 - Verified Target Label and Training Table Foundation

Planned focus:

- verified historical flood target label source integration
- observation date and district derivation
- schema-valid model-ready training table
- train/validation split strategy
- baseline ML experiment planning after readiness gate clears

## Versioning Notes

This project uses semantic-style milestone versions:

- Patch releases: fixes and documentation updates
- Minor releases: new pipeline or app/API capability
- Major releases: production-level architecture changes or trained model milestone

## Upcoming v0.4.0

Planned release theme:

Notebook and ML Readiness Foundation.

Highlights:

- notebook foundation
- notebook validation and smoke execution
- notebook data catalog
- initial EDA report
- ML training readiness reports
- complete ML readiness workflow

Training status:

Real supervised ML training remains blocked until a verified `flood_occurred`
target label and schema-valid training table are available.
