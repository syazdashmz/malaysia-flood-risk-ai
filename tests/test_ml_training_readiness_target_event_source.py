from pathlib import Path

from floodrisk.ml.training_readiness import (
    build_ml_training_readiness_summary,
    render_ml_training_readiness_report,
)


def test_ml_training_readiness_includes_missing_target_event_source(tmp_path: Path):
    summary = build_ml_training_readiness_summary(tmp_path)

    assert summary.target_event_source_exists is False
    assert summary.target_event_source_rows == 0
    assert summary.target_event_source_schema_valid is False
    assert summary.target_event_source_ready is False
    assert any(
        "Historical flood event target source is not ready" in blocker
        for blocker in summary.blockers
    )


def test_ml_training_readiness_report_includes_target_event_gate(tmp_path: Path):
    summary = build_ml_training_readiness_summary(tmp_path)
    report = render_ml_training_readiness_report(summary)

    assert "Target event source exists: False" in report
    assert "Target event source schema valid: False" in report
    assert "Target event source ready: False" in report
