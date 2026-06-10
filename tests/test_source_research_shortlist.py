import json
from pathlib import Path


def test_source_research_shortlist_config_exists():
    path = Path("configs/source_research_shortlist.json")

    assert path.exists()


def test_source_research_shortlist_config_has_expected_sources():
    sources = json.loads(Path("configs/source_research_shortlist.json").read_text(encoding="utf-8"))
    source_ids = {source["source_id"] for source in sources}

    assert "reliefweb_api" in source_ids
    assert "emdat" in source_ids
    assert "data_gov_my" in source_ids
    assert "public_info_banjir_jps" in source_ids


def test_source_research_shortlist_keeps_sources_out_of_direct_training():
    sources = json.loads(Path("configs/source_research_shortlist.json").read_text(encoding="utf-8"))

    assert all(source["allowed_direct_training_use"] is False for source in sources)


def test_source_research_shortlist_document_exists_and_prioritizes_reliefweb():
    content = Path("docs/SOURCE_RESEARCH_SHORTLIST.md").read_text(encoding="utf-8")

    assert "ReliefWeb API" in content
    assert "review first" in content.lower()
    assert "Create a source discovery module" in content
