from pathlib import Path

APP_PATH = Path("app/streamlit_app.py")


def test_streamlit_app_has_research_dashboard():
    content = APP_PATH.read_text(encoding="utf-8")

    assert "Research Dashboard" in content
    assert "Training metrics" in content
    assert "Threshold tuning" in content
    assert "Model benchmark" in content
    assert "API test panel" in content


def test_streamlit_app_loads_training_and_benchmark_reports():
    content = APP_PATH.read_text(encoding="utf-8")

    assert "kaggle_flood_baseline_training_metrics.json" in content
    assert "kaggle_flood_threshold_tuning_metrics.json" in content
    assert "kaggle_flood_model_benchmark_metrics.json" in content
    assert "render_benchmark_metrics" in content


def test_streamlit_app_has_api_prediction_panel():
    content = APP_PATH.read_text(encoding="utf-8")

    assert "Check API model status" in content
    assert "Run sample API prediction" in content
    assert "/experimental/flood/model/status" in content
    assert "/experimental/flood/predict" in content
