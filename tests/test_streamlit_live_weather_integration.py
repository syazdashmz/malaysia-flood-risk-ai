from pathlib import Path

APP_PATH = Path("app/streamlit_app.py")


def test_streamlit_app_loads_live_weather_features():
    content = APP_PATH.read_text(encoding="utf-8")

    assert "load_live_weather_feature_rows" in content
    assert "LIVE_FORECAST_FEATURES_PATH" in content
    assert "LIVE_WARNING_FEATURES_PATH" in content


def test_streamlit_app_summarizes_live_weather_signal_for_public_checker():
    content = APP_PATH.read_text(encoding="utf-8")

    assert "summarize_live_weather_signal" in content
    assert "Live weather API signal" in content
    assert "weather_warning_status" in content


def test_streamlit_app_uses_live_weather_signal_to_update_payload():
    content = APP_PATH.read_text(encoding="utf-8")

    assert "payload.model_copy" in content
    assert "render_live_weather_signal(weather_signal)" in content
    assert "live_forecast_features" in content
    assert "live_warning_features" in content
