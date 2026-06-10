from floodrisk.ml.target_source_evaluation import (
    build_target_source_evaluation_summary,
    render_target_source_evaluation_report,
)


def test_target_source_evaluation_has_required_criteria():
    summary = build_target_source_evaluation_summary()
    criterion_ids = {criterion.criterion_id for criterion in summary.criteria}

    assert "verified_authority" in criterion_ids
    assert "historical_event_coverage" in criterion_ids
    assert "binary_mapping" in criterion_ids
    assert "location_alignment" in criterion_ids
    assert "time_alignment" in criterion_ids
    assert "license_documented" in criterion_ids
    assert "leakage_free" in criterion_ids


def test_target_source_evaluation_blocks_training_now():
    summary = build_target_source_evaluation_summary()

    assert summary.target_column == "flood_occurred"
    assert summary.candidate_count >= 5
    assert summary.ready_candidate_count == 0
    assert summary.real_training_target_ready is False


def test_target_source_evaluation_rejects_rule_based_score():
    summary = build_target_source_evaluation_summary()
    score_source = next(
        item for item in summary.evaluations if item.source_id == "rule_based_risk_score"
    )

    assert score_source.available_now is True
    assert score_source.allowed_for_real_training is False
    assert score_source.ready_for_real_training is False
    assert score_source.criteria_passed["leakage_free"] is False


def test_target_source_evaluation_report_contains_decision():
    summary = build_target_source_evaluation_summary()
    report = render_target_source_evaluation_report(summary)

    assert "Target Label Source Evaluation" in report
    assert "Real training target ready: False" in report
    assert "No target-label source is ready" in report
