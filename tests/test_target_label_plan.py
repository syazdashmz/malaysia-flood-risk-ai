from pathlib import Path

from floodrisk.ml.target_label_plan import (
    build_target_label_source_plan,
    render_target_label_source_plan_report,
    write_target_label_source_plan_report,
)


def test_target_label_source_plan_targets_flood_occurred():
    plan = build_target_label_source_plan()

    assert plan.target_column == "flood_occurred"
    assert plan.requirement_count >= 5


def test_target_label_source_plan_requires_verified_source():
    plan = build_target_label_source_plan()
    requirement_ids = {requirement.requirement_id for requirement in plan.requirements}

    assert "verified_source" in requirement_ids
    assert "no_score_leakage" in requirement_ids


def test_target_label_source_plan_blocks_real_training_now():
    plan = build_target_label_source_plan()

    assert plan.allowed_candidate_count >= 1
    assert plan.ready_candidate_count == 0
    assert plan.real_training_target_ready is False


def test_target_label_source_plan_rejects_rule_based_score():
    plan = build_target_label_source_plan()
    score_candidate = next(
        candidate for candidate in plan.candidates if candidate.source_id == "rule_based_risk_score"
    )

    assert score_candidate.ready_now is True
    assert score_candidate.allowed_for_real_training is False
    assert score_candidate.usable_now_for_real_training is False


def test_render_target_label_source_plan_report():
    report = render_target_label_source_plan_report(build_target_label_source_plan())

    assert "Target Label Source Plan" in report
    assert "Real training target ready: False" in report
    assert "Real supervised ML training remains blocked" in report


def test_write_target_label_source_plan_report(tmp_path: Path):
    output_path = tmp_path / "target_label_source_plan.md"
    saved_path = write_target_label_source_plan_report(
        build_target_label_source_plan(),
        output_path,
    )

    assert saved_path.exists()
    assert "Target Label Source Plan" in saved_path.read_text(encoding="utf-8")
