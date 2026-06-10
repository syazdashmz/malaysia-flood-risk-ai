from pathlib import Path

APP_PATH = Path("app/streamlit_app.py")


def test_streamlit_app_has_public_first_layout():
    content = APP_PATH.read_text(encoding="utf-8")

    assert "Flood Risk Checker" in content
    assert "Choose a location and date" in content
    assert "Area / sample location" in content
    assert "Date to check" in content


def test_streamlit_app_separates_research_and_advanced_sections():
    content = APP_PATH.read_text(encoding="utf-8")

    assert "Research Dashboard" in content
    assert "Advanced Manual Mode" in content
    assert "Data Sources & Limits" in content
    assert "researchers and developers" in content


def test_streamlit_app_explains_current_data_limits():
    content = APP_PATH.read_text(encoding="utf-8")

    assert "Live date-specific rainfall" in content
    assert "Official validation should continue" in content
    assert "EM-DAT and MyWater/DID" in content


def test_streamlit_app_keeps_ai_training_dashboard():
    content = APP_PATH.read_text(encoding="utf-8")

    assert "Training metrics" in content
    assert "Threshold tuning" in content
    assert "Model benchmark" in content
    assert "API test panel" in content
    assert "/experimental/flood/predict" in content
