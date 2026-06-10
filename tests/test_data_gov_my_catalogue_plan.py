from pathlib import Path

from floodrisk.sources.data_gov_my import (
    DATA_GOV_MY_CATALOGUE_ENDPOINT,
    build_data_gov_my_catalogue_plan,
    render_data_gov_my_catalogue_plan_report,
)


def test_data_gov_my_catalogue_plan_loads_candidates():
    plan = build_data_gov_my_catalogue_plan(Path("."))

    assert plan.source_id == "data_gov_my"
    assert plan.direct_training_use_allowed is False
    assert plan.candidate_count == 3


def test_data_gov_my_catalogue_plan_has_expected_dataset_ids():
    plan = build_data_gov_my_catalogue_plan(Path("."))
    dataset_ids = {candidate.dataset_id for candidate in plan.candidates}

    assert "population_district" in dataset_ids
    assert "water_consumption" in dataset_ids
    assert "water_pollution_basin" in dataset_ids


def test_data_gov_my_catalogue_candidates_are_not_target_labels():
    plan = build_data_gov_my_catalogue_plan(Path("."))

    assert plan.target_label_candidate_count == 0
    assert all(candidate.direct_training_use_allowed is False for candidate in plan.candidates)


def test_data_gov_my_catalogue_report_contains_api_guardrail():
    plan = build_data_gov_my_catalogue_plan(Path("."))
    report = render_data_gov_my_catalogue_plan_report(plan)

    assert DATA_GOV_MY_CATALOGUE_ENDPOINT in report
    assert "data.gov.my Catalogue Candidate Plan" in report
    assert "must not be used as supervised ML labels" in report
