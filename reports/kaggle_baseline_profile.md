# Kaggle Experimental Baseline Dataset Profile

## Summary

- Source role: experimental proxy baseline dataset
- Official verified target source: False
- Experimental training allowed: True
- Raw path: `data/raw/kaggle/malaysia_flood_master.csv`
- Rows: 47367
- Columns: 13
- Date range: 2010-01-14 to 2026-03-31
- Cities: 8
- Flood positive rows: 676
- Flash flood positive rows: 226
- Flash flood rows without Flood=1: 0

## Columns

- `DATE`
- `City`
- `Temperature_C`
- `Humidity_pct`
- `Wind_Speed_ms`
- `Rainfall_3day`
- `Rainfall_7day`
- `Rainfall_14day`
- `Rainfall_cumsum7`
- `Month`
- `Is_Monsoon`
- `Flood`
- `Flash_Flood`

## City Counts

- Johor Bahru: 5921
- Kota Kinabalu: 5921
- Kuala Lumpur: 5921
- Kuantan: 5921
- Kuching: 5921
- Melaka: 5921
- Shah Alam: 5921
- Kota Bharu: 5920

## Missing Values

- `DATE`: 0
- `City`: 0
- `Temperature_C`: 0
- `Humidity_pct`: 0
- `Wind_Speed_ms`: 0
- `Rainfall_3day`: 0
- `Rainfall_7day`: 0
- `Rainfall_14day`: 0
- `Rainfall_cumsum7`: 0
- `Month`: 0
- `Is_Monsoon`: 0
- `Flood`: 0
- `Flash_Flood`: 0

## Decision

Use this dataset for experimental baseline ML training only.
Do not present it as the final official verified target source.
