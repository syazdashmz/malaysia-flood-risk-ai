from pathlib import Path

from floodrisk.sources.reliefweb import (
    DEFAULT_RELIEFWEB_APPNAME,
    RELIEFWEB_REPORTS_ENDPOINT,
    build_reliefweb_discovery_plan,
    render_reliefweb_discovery_plan_report,
)


def test_reliefweb_discovery_plan_loads_queries():
    plan = build_reliefweb_discovery_plan(Path("."))

    assert plan.source_id == "reliefweb_api"
    assert plan.direct_training_use_allowed is False
    assert plan.query_count >= 3


def test_reliefweb_discovery_payload_targets_malaysia_floods():
    plan = build_reliefweb_discovery_plan(Path("."))
    payload = plan.queries[0].payload()

    assert payload["query"]["value"]
    assert payload["filter"]["operator"] == "AND"
    assert {"field": "country", "value": "Malaysia"} in payload["filter"]["conditions"]
    assert {"field": "disaster_type", "value": "Flood"} in payload["filter"]["conditions"]


def test_reliefweb_discovery_endpoint_uses_v2_and_appname():
    plan = build_reliefweb_discovery_plan(Path("."))
    endpoint = plan.queries[0].endpoint_url

    assert endpoint.startswith(RELIEFWEB_REPORTS_ENDPOINT)
    assert DEFAULT_RELIEFWEB_APPNAME in endpoint
    assert "/v2/reports" in endpoint


def test_reliefweb_discovery_report_contains_guardrail():
    plan = build_reliefweb_discovery_plan(Path("."))
    report = render_reliefweb_discovery_plan_report(plan)

    assert "ReliefWeb Discovery Plan" in report
    assert "Direct training use allowed: False" in report
    assert "Do not treat discovered report content as final supervised ML labels" in report
