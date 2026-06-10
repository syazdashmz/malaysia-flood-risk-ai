# Target Label Source Evaluation

This document defines the evaluation framework for deciding whether a future
source can be used as the real `flood_occurred` supervised ML target.

## Required Criteria

A source must satisfy all of these before it can be used for real training:

- verified authority
- historical event coverage
- binary target mapping
- location alignment
- time alignment
- documented license or usage permission
- no leakage from the rule-based `risk_score`

## Current Decision

No target-label source is ready for real supervised ML training yet.

## Generated Report

Run:

    .\scripts\run_target_label_source_evaluation.ps1

This generates:

    reports/target_label_source_evaluation.md

## Why This Matters

The project must not train a model using labels derived from its own transparent
risk score. Doing that would create target leakage and produce a misleading
model.

The next research step is to locate or prepare a verified historical flood
occurrence source that can be aligned by location and date.
