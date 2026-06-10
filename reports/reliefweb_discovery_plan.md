# ReliefWeb Discovery Plan

## Summary

- Source ID: `reliefweb_api`
- Query count: 3
- Direct training use allowed: False

## Guardrail

ReliefWeb should be used as a discovery index first. Do not treat discovered report content as final supervised ML labels until authority, licensing, location, and dates are reviewed.

## Query Plan

| Query ID | Label | Query | Country | Disaster Type | Limit |
|---|---|---|---|---|---:|
| malaysia_flood_reports | Malaysia flood reports | Malaysia flood | Malaysia | Flood | 10 |
| malaysia_flood_maps | Malaysia flood maps | Malaysia flood map | Malaysia | Flood | 10 |
| malaysia_flood_response | Malaysia flood response reports | Malaysia flood response | Malaysia | Flood | 10 |

## Request Payloads

### Malaysia flood reports

Endpoint: `https://api.reliefweb.int/v2/reports?appname=malaysia-flood-risk-ai`

```json
{
  "query": {
    "value": "Malaysia flood"
  },
  "filter": {
    "operator": "AND",
    "conditions": [
      {
        "field": "country.name",
        "value": "Malaysia"
      },
      {
        "field": "disaster_type.name",
        "value": "Flood"
      }
    ]
  },
  "fields": {
    "include": [
      "id",
      "name",
      "url",
      "date.created",
      "date.original",
      "source.name",
      "primary_country.name",
      "country.name",
      "disaster.name",
      "disaster_type.name"
    ]
  },
  "sort": [
    "date.created:desc"
  ],
  "limit": 10
}
```

### Malaysia flood maps

Endpoint: `https://api.reliefweb.int/v2/reports?appname=malaysia-flood-risk-ai`

```json
{
  "query": {
    "value": "Malaysia flood map"
  },
  "filter": {
    "operator": "AND",
    "conditions": [
      {
        "field": "country.name",
        "value": "Malaysia"
      },
      {
        "field": "disaster_type.name",
        "value": "Flood"
      }
    ]
  },
  "fields": {
    "include": [
      "id",
      "name",
      "url",
      "date.created",
      "date.original",
      "source.name",
      "primary_country.name",
      "country.name",
      "disaster.name",
      "disaster_type.name"
    ]
  },
  "sort": [
    "date.created:desc"
  ],
  "limit": 10
}
```

### Malaysia flood response reports

Endpoint: `https://api.reliefweb.int/v2/reports?appname=malaysia-flood-risk-ai`

```json
{
  "query": {
    "value": "Malaysia flood response"
  },
  "filter": {
    "operator": "AND",
    "conditions": [
      {
        "field": "country.name",
        "value": "Malaysia"
      },
      {
        "field": "disaster_type.name",
        "value": "Flood"
      }
    ]
  },
  "fields": {
    "include": [
      "id",
      "name",
      "url",
      "date.created",
      "date.original",
      "source.name",
      "primary_country.name",
      "country.name",
      "disaster.name",
      "disaster_type.name"
    ]
  },
  "sort": [
    "date.created:desc"
  ],
  "limit": 10
}
```

## Decision

The next implementation step is a safe live discovery script that fetches report metadata only and stores a non-training discovery report.
