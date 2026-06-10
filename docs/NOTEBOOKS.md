# Notebook Foundation

## Purpose

This document tracks the notebook foundation for the v0.4.0 milestone.

Target milestone:

    v0.4.0 - Notebook and Data Exploration Foundation

## Current Notebook

The first notebook scaffold is:

    notebooks/00_project_readiness.ipynb

Purpose:

- review project state
- inspect version metadata
- inspect geospatial readiness
- document questions before real model training

## Folder Structure

| Folder | Purpose |
|---|---|
| notebooks/ | top-level notebook documentation and milestone notebooks |
| notebooks/exploration/ | future exploratory data analysis notebooks |
| notebooks/experiments/ | future baseline model experiment notebooks |

## Notebook Rules

Notebook files should:

- avoid large outputs
- avoid hidden production logic
- use reusable package modules where possible
- support reproducible analysis
- document assumptions clearly

## Training Status

Real AI/ML training has not started yet.

The project still needs:

- target label definition
- historical flood label source
- model-ready feature table
- train/validation split strategy
- baseline evaluation plan

## Notebook Validation

Run notebook checks with:

    .\scripts\run_notebook_checks.ps1

This generates:

    reports/notebook_validation_report.md

The validator checks:

- valid notebook JSON
- notebook format version
- cell counts
- executed code cells
- saved code outputs

Notebook commits should stay clean with no execution counts and no saved outputs.

## Dataset Readiness Report

Run dataset readiness checks with:

    .\scripts\run_dataset_readiness.ps1

This generates:

    reports/dataset_readiness_report.md

The report shows whether the project has the minimum dataset foundation required for real ML training.

## Training Dataset Design

The planned model-training dataset is documented in:

    docs/TRAINING_DATASET.md

This document defines:

- preferred target label
- planned training table path
- expected feature groups
- leakage risks
- recommended split strategy
- baseline model plan

Real ML training should not start until the dataset readiness report no longer has blocking training items.

## Dataset Readiness and Training Schema

The dataset readiness report is connected to the training table schema validator.

This means the model-ready training table blocker is cleared only when:

- the training table exists
- all required columns are present
- the target column exists
- the table has at least one row

A placeholder CSV with the wrong schema does not make the project training-ready.

## Notebook Environment Check

Run notebook environment checks with:

    .\scripts\run_notebook_environment_check.ps1

This generates:

    reports/notebook_environment_report.md

The report checks:

- project package import
- pandas availability
- matplotlib availability
- ipykernel availability
- optional geospatial and ML notebook dependencies

## Notebook Data Catalog

Generate the notebook data catalog with:

    .\scripts\run_notebook_data_catalog.ps1

This generates:

    reports/notebook_data_catalog_report.md

The catalog lists available assets for initial EDA, including:

- sample location data
- weather summary reports
- geospatial readiness reports
- notebook readiness reports
- training schema reports
- future model-training table status

## Initial EDA Notebook

The first exploration notebook is:

    notebooks/exploration/01_initial_data_catalog_eda.ipynb

Purpose:

- inspect the notebook data catalog
- inspect sample Malaysia locations
- inspect weather summary data
- inspect dataset and training readiness reports
- document what still blocks real ML training

This notebook does not train a model.

## Notebook Smoke Execution

Run notebook smoke execution checks with:

    .\scripts\run_notebook_smoke_tests.ps1

This generates:

    reports/notebook_execution_report.md

The smoke test executes notebook code cells in memory without saving outputs back into notebook files.

## Initial EDA Report

Generate the initial EDA report with:

    .\scripts\run_initial_eda_report.ps1

This generates:

    reports/initial_eda_report.md

The report summarizes:

- sample location rows and columns
- numeric profiles
- weather summary keys
- weather signal counts
- initial EDA readiness
- real ML training readiness
