from urllib.parse import parse_qs, urlparse

import pytest

from floodrisk.data.weather_client import BASE_WEATHER_URL, build_weather_url, save_json


def test_build_weather_url_without_params():
    url = build_weather_url("forecast")

    assert url == f"{BASE_WEATHER_URL}/forecast"


def test_build_weather_url_with_params():
    url = build_weather_url(
        "forecast",
        {
            "limit": 3,
            "contains": "St@location__location_id",
        },
    )

    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    assert parsed.scheme == "https"
    assert parsed.netloc == "api.data.gov.my"
    assert parsed.path == "/weather/forecast"
    assert query["limit"] == ["3"]
    assert query["contains"] == ["St@location__location_id"]


def test_build_weather_url_rejects_unsupported_endpoint():
    with pytest.raises(ValueError, match="Unsupported weather endpoint"):
        build_weather_url("earthquake")


def test_save_json(tmp_path):
    output_path = tmp_path / "sample.json"

    saved_path = save_json({"status": "ok"}, output_path)

    assert saved_path.exists()
    assert '"status": "ok"' in saved_path.read_text(encoding="utf-8")
