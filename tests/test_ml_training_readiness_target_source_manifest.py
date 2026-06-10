from pathlib import Path

from floodrisk.ml.training_readiness import (
    build_ml_training_readiness_summary,
    render_ml_training_readiness_report,
)


def test_ml_training_readiness_includes_target_source_manifest(tmp_path: Path):
    summary = build_ml_training_readiness_summary(tmp_path)

    assert summary.target_source_manifest_exists is False
    assert summary.target_source_manifest_valid is False
    assert summary.target_source_manifest_candidates == 0
    assert summary.target_source_manifest_ready_candidates == 0
    assert summary.target_source_manifest_has_ready_candidate is False
    assert any("Target source manifest has no candidate ready" in item for item in summary.blockers)


def test_ml_training_readiness_report_includes_target_source_manifest_gate(tmp_path: Path):
    summary = build_ml_training_readiness_summary(tmp_path)
    report = render_ml_training_readiness_report(summary)

    assert "Target source manifest exists: False" in report
    assert "Target source manifest valid: False" in report
    assert "Target source manifest has ready candidate: False" in report
