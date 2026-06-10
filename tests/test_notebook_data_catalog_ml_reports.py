from pathlib import Path

from floodrisk.notebooks.catalog import (
    build_notebook_data_catalog,
    list_notebook_data_assets,
    render_notebook_data_catalog_report,
)


def test_notebook_catalog_includes_ml_readiness_reports():
    assets = list_notebook_data_assets()
    asset_ids = {asset.asset_id for asset in assets}

    expected_ids = {
        "initial_eda_report",
        "feature_table_plan",
        "feature_table_builder_dry_run",
        "target_label_source_plan",
        "ml_training_readiness_report",
    }

    assert expected_ids.issubset(asset_ids)


def test_notebook_catalog_marks_ml_readiness_reports_as_optional():
    assets = list_notebook_data_assets()
    ml_assets = [
        asset
        for asset in assets
        if asset.asset_id
        in {
            "feature_table_plan",
            "feature_table_builder_dry_run",
            "target_label_source_plan",
            "ml_training_readiness_report",
        }
    ]

    assert ml_assets
    assert all(asset.required_for_eda is False for asset in ml_assets)


def test_notebook_catalog_report_mentions_ml_training_readiness():
    summary = build_notebook_data_catalog(Path.cwd())
    report = render_notebook_data_catalog_report(summary)

    assert "ML training readiness gate" in report
    assert "Target label source plan" in report
    assert "Feature table builder dry run" in report


def test_notebook_catalog_includes_target_source_readiness_artifacts():
    assets = list_notebook_data_assets()
    asset_ids = {asset.asset_id for asset in assets}

    expected_ids = {
        "target_label_source_evaluation",
        "target_source_manifest",
        "target_source_manifest_report",
        "target_event_source_schema",
        "target_event_source_template",
    }

    assert expected_ids.issubset(asset_ids)


def test_notebook_catalog_marks_target_source_artifacts_as_optional():
    assets = list_notebook_data_assets()
    target_assets = [
        asset
        for asset in assets
        if asset.asset_id
        in {
            "target_label_source_evaluation",
            "target_source_manifest",
            "target_source_manifest_report",
            "target_event_source_schema",
            "target_event_source_template",
        }
    ]

    assert target_assets
    assert all(asset.required_for_eda is False for asset in target_assets)


def test_notebook_catalog_report_mentions_target_source_artifacts():
    summary = build_notebook_data_catalog(Path.cwd())
    report = render_notebook_data_catalog_report(summary)

    assert "Target source candidate manifest" in report
    assert "Target event source schema report" in report
    assert "Historical flood event target template" in report
