import json
from pathlib import Path


def test_data_gov_my_catalogue_review_config_exists():
    path = Path("configs/data_gov_my_catalogue_review.json")

    assert path.exists()


def test_data_gov_my_catalogue_review_has_no_target_label_candidates():
    reviews = json.loads(
        Path("configs/data_gov_my_catalogue_review.json").read_text(encoding="utf-8")
    )

    assert reviews
    assert all(review["target_label_candidate"] is False for review in reviews)


def test_data_gov_my_catalogue_review_keeps_population_district_supporting():
    reviews = json.loads(
        Path("configs/data_gov_my_catalogue_review.json").read_text(encoding="utf-8")
    )
    review_by_id = {review["dataset_id"]: review for review in reviews}

    assert review_by_id["population_district"]["supporting_feature_candidate"] is True
    assert (
        review_by_id["population_district"]["decision"] == "keep_as_supporting_geography_reference"
    )


def test_data_gov_my_catalogue_review_report_blocks_flood_target_mapping():
    content = Path("reports/data_gov_my_catalogue_review.md").read_text(encoding="utf-8")

    assert "Target-label candidates: 0" in content
    assert "None of these datasets should be mapped to `flood_occurred`" in content
    assert "verified historical flood event source" in content


def test_data_gov_my_catalogue_review_doc_exists():
    content = Path("docs/DATA_GOV_MY_CATALOGUE_REVIEW.md").read_text(encoding="utf-8")

    assert "population_district" in content
    assert "flood_occurred" in content
