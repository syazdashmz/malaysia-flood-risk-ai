from floodrisk.sources.data_gov_my import (
    DataGovMyCatalogueCandidate,
    DataGovMyCatalogueProbeResult,
    _coerce_data_gov_my_records,
    render_data_gov_my_catalogue_probe_report,
)


def test_data_gov_my_records_coerce_list_response():
    records = _coerce_data_gov_my_records([{"state": "Selangor"}, "bad"])

    assert records == [{"state": "Selangor"}]


def test_data_gov_my_records_coerce_dict_data_response():
    records = _coerce_data_gov_my_records({"data": [{"district": "Petaling"}]})

    assert records == [{"district": "Petaling"}]


def test_data_gov_my_probe_report_keeps_training_guardrail():
    result = DataGovMyCatalogueProbeResult(
        dataset_id="population_district",
        label="Population Table: Administrative Districts",
        api_url="https://api.data.gov.my/data-catalogue?id=population_district&limit=3",
        direct_training_use_allowed=False,
        target_label_candidate=False,
        record_count=1,
        sample_columns=["district", "population"],
        sample_records=[{"district": "Petaling", "population": 1}],
        error="",
    )

    from floodrisk.sources.data_gov_my import DataGovMyCatalogueProbeSummary

    summary = DataGovMyCatalogueProbeSummary(
        source_id="data_gov_my",
        fetched_at_utc="2024-01-01T00:00:00+00:00",
        direct_training_use_allowed=False,
        candidate_count=1,
        successful_probes=1,
        failed_probes=0,
        results=[result],
    )

    report = render_data_gov_my_catalogue_probe_report(summary)

    assert "data.gov.my Catalogue Probe Report" in report
    assert "small API samples only" in report
    assert "Do not map them to `flood_occurred`" in report


def test_data_gov_my_candidate_dataclass_direct_training_disabled():
    candidate = DataGovMyCatalogueCandidate(
        dataset_id="water_consumption",
        label="Water Consumption",
        priority=1,
        role="supporting_environment_feature",
        source_url="https://data.gov.my/data-catalogue/water_consumption",
        api_url="https://api.data.gov.my/data-catalogue?id=water_consumption&limit=3",
        expected_use="Review sample data.",
        location_granularity="state",
        temporal_granularity="monthly",
        direct_training_use_allowed=False,
        target_label_candidate=False,
        notes="Supporting data only.",
    )

    assert candidate.direct_training_use_allowed is False
    assert candidate.target_label_candidate is False
