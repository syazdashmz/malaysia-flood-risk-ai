# data.gov.my Catalogue Probe Report

## Summary

- Source ID: `data_gov_my`
- Fetched at UTC: 2026-06-10T03:15:15.369477+00:00
- Candidate datasets: 3
- Successful probes: 3
- Failed probes: 0
- Direct training use allowed: False

## Guardrail

This report contains small API samples only. These samples must not be used as supervised ML target labels until authority, license, location, date fields, and target mapping are reviewed.

## Probe Results

| Dataset ID | Label | Records | Columns | Error |
|---|---|---:|---|---|
| population_district | Population Table: Administrative Districts | 3 | age, date, district, ethnicity, population, sex, state | - |
| water_consumption | Water Consumption by State and Sector | 3 | date, sector, state, value | - |
| water_pollution_basin | River Basin Pollution Monitoring | 3 | basins_monitored, date, measure, n_basins, proportion, status | - |

## Sample Records

### Population Table: Administrative Districts

```json
[
  {
    "age": "85+",
    "sex": "both",
    "date": "2021-01-01",
    "state": "Kedah",
    "district": "Langkawi",
    "ethnicity": "other_citizen",
    "population": 0.0
  },
  {
    "age": "85+",
    "sex": "both",
    "date": "2021-01-01",
    "state": "Kedah",
    "district": "Langkawi",
    "ethnicity": "other_noncitizen",
    "population": 0.0
  },
  {
    "age": "overall",
    "sex": "female",
    "date": "2021-01-01",
    "state": "Kedah",
    "district": "Langkawi",
    "ethnicity": "overall",
    "population": 46.0
  }
]
```

### Water Consumption by State and Sector

```json
[
  {
    "date": "2003-01-01",
    "state": "Malaysia",
    "value": 4394,
    "sector": "domestic"
  },
  {
    "date": "2004-01-01",
    "state": "Malaysia",
    "value": 4770,
    "sector": "domestic"
  },
  {
    "date": "2005-01-01",
    "state": "Malaysia",
    "value": 4992,
    "sector": "domestic"
  }
]
```

### River Basin Pollution Monitoring

```json
[
  {
    "date": "2000-01-01",
    "status": "clean",
    "measure": "bod5",
    "n_basins": 39,
    "proportion": 32.5,
    "basins_monitored": 120
  },
  {
    "date": "2000-01-01",
    "status": "slightly__polluted",
    "measure": "bod5",
    "n_basins": 63,
    "proportion": 52.5,
    "basins_monitored": 120
  },
  {
    "date": "2000-01-01",
    "status": "polluted",
    "measure": "bod5",
    "n_basins": 18,
    "proportion": 15.0,
    "basins_monitored": 120
  }
]
```

## Decision

Use these probes only to decide whether each dataset is useful as supporting feature/context data. Do not map them to `flood_occurred` without a separate target-label review.
