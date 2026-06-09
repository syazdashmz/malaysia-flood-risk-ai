# Deployment Guide

## Current Deployment Target

The current MVP is ready for Streamlit-based demo deployment.

The web app entry point is:

    app/streamlit_app.py

The lightweight deployment dependency file is:

    requirements.txt

## Recommended Public Demo Deployment

Use the GitHub repository:

    https://github.com/syazdashmz/malaysia-flood-risk-ai

Set the Streamlit app file path to:

    app/streamlit_app.py

## Important Notes

This deployment uses the transparent MVP scoring engine and sample demo data.

It does not yet use real-time flood data, downloaded geospatial datasets, or trained machine-learning models.

## Local Verification Before Deployment

Run:

    .\scripts\run_quality.ps1

Or manually run:

    ruff format .
    ruff check .
    pytest

## App Disclaimer

This app is for research, education, portfolio, and public awareness only.

It is not an official flood warning system.

Always follow official Malaysian flood warnings, local authorities, and emergency instructions.
