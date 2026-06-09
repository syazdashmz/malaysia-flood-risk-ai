# Geospatial Artifact Plan

## Purpose

This report tracks expected local geospatial boundary artifacts for the v0.3.0 geospatial foundation milestone.

No boundary file is bundled until source reliability, licensing, and redistribution rules are verified.

## Planned Artifacts

| Dataset ID | Path | Required for MVP | Status |
|---|---|---:|---|
| malaysia_admin_boundary | data/external/geospatial/malaysia_admin_boundary.geojson | False | planned_missing |
| malaysia_state_boundary | data/external/geospatial/malaysia_state_boundary.geojson | False | planned_missing |
| malaysia_district_boundary | data/external/geospatial/malaysia_district_boundary.geojson | False | planned_missing |

## Next Actions

1. Verify authoritative boundary data sources.
2. Confirm license and redistribution permissions.
3. Download data manually only after verification.
4. Store raw external files under data/external/geospatial/.
5. Add geometry loading and validation checks.
