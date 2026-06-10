from pathlib import Path

SCRIPT_PATH = Path("scripts/test_api_endpoints.ps1")


def test_api_endpoint_smoke_script_exists():
    assert SCRIPT_PATH.exists()


def test_api_endpoint_smoke_script_checks_core_endpoints():
    content = SCRIPT_PATH.read_text(encoding="utf-8")

    assert "$BaseUrl/health" in content
    assert "$BaseUrl/experimental/flood/model/status" in content
    assert "$BaseUrl/experimental/flood/predict" in content


def test_api_endpoint_smoke_script_uses_prediction_payload():
    content = SCRIPT_PATH.read_text(encoding="utf-8")

    assert 'city = "Kuala Lumpur"' in content
    assert "rainfall_7day_mm = 180" in content
    assert "is_monsoon = 1" in content
