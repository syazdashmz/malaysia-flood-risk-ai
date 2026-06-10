from pathlib import Path


def test_changelog_has_v0_4_0_before_v0_3_0():
    content = Path("CHANGELOG.md").read_text(encoding="utf-8")

    assert content.index("## [0.4.0]") < content.index("## [0.3.0]")
    assert "## Unreleased" in content


def test_changelog_documents_v0_4_0_training_status():
    content = Path("CHANGELOG.md").read_text(encoding="utf-8")

    assert "Real supervised ML training remains blocked" in content
    assert "verified historical `flood_occurred` target source" in content
    assert "162 tests passed locally" in content
