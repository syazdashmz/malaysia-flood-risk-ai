import json
from pathlib import Path


def test_reliefweb_documentation_marks_access_blocked():
    content = Path("docs/RELIEFWEB_DISCOVERY.md").read_text(encoding="utf-8")

    assert "Blocked Pending Approved Appname" in content
    assert "HTTP 403 Forbidden" in content
    assert "data.gov.my" in content


def test_source_research_shortlist_moves_data_gov_my_next():
    sources = json.loads(Path("configs/source_research_shortlist.json").read_text(encoding="utf-8"))
    source_by_id = {source["source_id"]: source for source in sources}

    assert source_by_id["reliefweb_api"]["initial_decision"] == "blocked_pending_approved_appname"
    assert source_by_id["data_gov_my"]["initial_decision"] == "review_next"


def test_data_gov_my_discovery_plan_exists():
    content = Path("docs/DATA_GOV_MY_DISCOVERY.md").read_text(encoding="utf-8")

    assert "https://api.data.gov.my/data-catalogue" in content
    assert "flood_occurred" in content
    assert "Use data.gov.my as the next official Malaysia-first source discovery path" in content


def test_data_gov_my_discovery_keywords_exist():
    keywords_path = Path("configs/data_gov_my_discovery_keywords.json")
    keywords = json.loads(keywords_path.read_text(encoding="utf-8"))
    values = {item["keyword"] for item in keywords}

    assert {"flood", "banjir", "rainfall", "river", "weather", "district"}.issubset(values)
