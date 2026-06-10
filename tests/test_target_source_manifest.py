from pathlib import Path

from floodrisk.ml.target_source_manifest import (
    render_target_source_manifest_report,
    validate_target_source_manifest,
)


def test_target_source_manifest_exists_and_is_valid():
    validation = validate_target_source_manifest(Path("."))

    assert validation.exists is True
    assert validation.is_valid is True
    assert validation.candidate_count >= 4


def test_target_source_manifest_has_no_ready_candidate_now():
    validation = validate_target_source_manifest(Path("."))

    assert validation.ready_candidate_count == 0
    assert validation.has_ready_candidate is False


def test_target_source_manifest_rejects_rule_based_score():
    validation = validate_target_source_manifest(Path("."))
    score_source = next(
        item for item in validation.candidates if item.source_id == "rule_based_risk_score"
    )

    assert score_source.allowed_for_real_training is False
    assert score_source.ready_for_real_training is False


def test_target_source_manifest_report_contains_decision():
    validation = validate_target_source_manifest(Path("."))
    report = render_target_source_manifest_report(validation)

    assert "Target Source Candidate Manifest Report" in report
    assert "No target source candidate is ready" in report
