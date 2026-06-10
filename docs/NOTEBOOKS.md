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
