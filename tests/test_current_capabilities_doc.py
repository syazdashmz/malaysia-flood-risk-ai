from pathlib import Path

DOC_PATH = Path("docs/CURRENT_CAPABILITIES.md")
README_PATH = Path("README.md")


def test_current_capabilities_document_exists():
    assert DOC_PATH.exists()


def test_current_capabilities_document_mentions_ai_pipeline():
    content = DOC_PATH.read_text(encoding="utf-8")

    assert "Experimental AI Flood Prediction" in content
    assert "FastAPI" in content
    assert "Streamlit" in content
    assert "EM-DAT" in content
    assert "MyWater" in content


def test_readme_links_current_capabilities_document():
    content = README_PATH.read_text(encoding="utf-8")

    assert "docs/CURRENT_CAPABILITIES.md" in content
    assert "experimental AI flood prediction pipeline" in content
