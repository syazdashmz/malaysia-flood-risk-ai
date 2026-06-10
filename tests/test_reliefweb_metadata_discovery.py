from pathlib import Path

from floodrisk.sources.reliefweb import (
    ReliefWebMetadataDiscoveryResult,
    normalize_reliefweb_report,
    render_reliefweb_metadata_discovery_report,
)


def test_normalize_reliefweb_report_extracts_metadata_only():
    item = {
        "id": "123",
        "fields": {
            "name": "Malaysia Floods Update",
            "url": "https://reliefweb.int/report/example",
            "date": {"created": "2024-01-01T00:00:00+00:00", "original": "2024-01-01"},
            "source": [{"name": "Example Source"}],
            "country": [{"name": "Malaysia"}],
            "disaster": [{"name": "Malaysia: Floods"}],
            "disaster_type": [{"name": "Flood"}],
        },
    }

    report = normalize_reliefweb_report(query_id="malaysia_flood_reports", item=item)

    assert report.report_id == "123"
    assert report.title == "Malaysia Floods Update"
    assert report.sources == ["Example Source"]
    assert report.countries == ["Malaysia"]
    assert report.disaster_types == ["Flood"]


def test_reliefweb_metadata_report_keeps_training_guardrail():
    result = ReliefWebMetadataDiscoveryResult(
        source_id="reliefweb_api",
        fetched_at_utc="2024-01-01T00:00:00+00:00",
        direct_training_use_allowed=False,
        report_count=0,
        reports=[],
        errors=[],
    )

    report = render_reliefweb_metadata_discovery_report(result)

    assert "ReliefWeb Metadata Discovery Report" in report
    assert "metadata only" in report.lower()
    assert "Do not convert them directly into `flood_occurred` labels" in report


def test_reliefweb_metadata_discovery_script_exists():
    assert Path("scripts/discover_reliefweb_metadata.py").exists()
    assert Path("scripts/run_reliefweb_metadata_discovery.ps1").exists()
