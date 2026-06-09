# Release Index

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

    v0.3.0 - Geospatial Foundation Pipeline

Planned focus:

- Malaysia administrative boundary source planning
- Location normalization
- Boundary/geospatial dataset acquisition workflow
- Basic geospatial validation
- Link weather signals to locations more cleanly

## Versioning Notes

This project uses semantic-style milestone versions:

- Patch releases: fixes and documentation updates
- Minor releases: new pipeline or app/API capability
- Major releases: production-level architecture changes or trained model milestone
