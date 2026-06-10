# data.gov.my Catalogue Candidate Plan

## Summary

- Source ID: `data_gov_my`
- Candidate datasets: 3
- Target-label candidates: 0
- Direct training use allowed: False

## Guardrail

These datasets are catalogue candidates only. They must not be used as supervised ML labels until authority, license, location fields, date fields, and target mapping are reviewed.

## Candidate Datasets

| Priority | Dataset ID | Label | Role | Location | Time | Target Label Candidate |
|---:|---|---|---|---|---|---:|
| 1 | population_district | Population Table: Administrative Districts | supporting_geography_reference | district | annual | False |
| 2 | water_consumption | Water Consumption by State and Sector | supporting_environment_feature | state | monthly | False |
| 3 | water_pollution_basin | River Basin Pollution Monitoring | supporting_hydrology_context | river_basin | annual | False |

## API Probe URLs

### Population Table: Administrative Districts

- Dataset ID: `population_district`
- Source page: https://data.gov.my/data-catalogue/population_district
- API probe: `https://api.data.gov.my/data-catalogue?id=population_district&limit=3`
- Expected use: Review district-level administrative reference data for joining or validating location fields.
- Notes: Useful as supporting geography/context data, not as flood occurrence labels.

### Water Consumption by State and Sector

- Dataset ID: `water_consumption`
- Source page: https://data.gov.my/data-catalogue/water_consumption
- API probe: `https://api.data.gov.my/data-catalogue?id=water_consumption&limit=3`
- Expected use: Review state-level water consumption data as possible contextual feature data.
- Notes: Potential supporting feature only; not a direct flood occurrence source.

### River Basin Pollution Monitoring

- Dataset ID: `water_pollution_basin`
- Source page: https://data.gov.my/data-catalogue/water_pollution_basin
- API probe: `https://api.data.gov.my/data-catalogue?id=water_pollution_basin&limit=3`
- Expected use: Review river basin monitoring data as environmental or hydrology context.
- Notes: Useful for environmental context review; not a direct flood label source.

## Decision

The next implementation step is a metadata/sample-only API probe that fetches small previews for these dataset IDs and stores a non-training review report.
