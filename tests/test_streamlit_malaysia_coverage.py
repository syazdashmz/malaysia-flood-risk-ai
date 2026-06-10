from pathlib import Path

APP_PATH = Path("app/streamlit_app.py")


def test_streamlit_app_loads_malaysia_admin_coverage():
    content = APP_PATH.read_text(encoding="utf-8")

    assert "load_malaysia_admin_coverage" in content
    assert "load_admin_regions_df" in content
    assert "build_public_location_catalog" in content


def test_streamlit_app_has_region_fallback_for_all_malaysia():
    content = APP_PATH.read_text(encoding="utf-8")

    assert "admin_region_fallback" in content
    assert "State / federal territory" in content
    assert "Malaysia-wide regional fallback profile" in content


def test_streamlit_app_combines_sample_and_admin_locations():
    content = APP_PATH.read_text(encoding="utf-8")

    assert "sample_location" in content
    assert "pd.concat" in content
    assert "admin_regions_df" in content
