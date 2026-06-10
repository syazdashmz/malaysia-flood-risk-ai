from pathlib import Path

from floodrisk.notebooks.environment import (
    NotebookDependency,
    NotebookDependencyCheck,
    NotebookEnvironmentSummary,
    check_notebook_dependency,
    check_notebook_environment,
    render_notebook_environment_report,
    write_notebook_environment_report,
)


def test_check_notebook_dependency_reports_missing_fake_dependency():
    dependency = NotebookDependency(
        name="package-that-should-not-exist-for-this-project",
        import_name="package_that_should_not_exist_for_this_project",
        required=True,
        purpose="Test missing dependency behavior.",
    )

    check = check_notebook_dependency(dependency)

    assert check.available is False
    assert check.status == "missing"
    assert check.blocks_notebook_work is True


def test_notebook_dependency_check_available_status():
    dependency = NotebookDependency(
        name="floodrisk",
        import_name="floodrisk",
        required=True,
        purpose="Project package.",
    )

    check = check_notebook_dependency(dependency)

    assert check.available is True
    assert check.status == "available"
    assert check.blocks_notebook_work is False


def test_check_notebook_environment_returns_summary():
    summary = check_notebook_environment()

    assert summary.dependency_count >= 4
    assert summary.available_count >= 1
    assert isinstance(summary.ready_for_notebook_work, bool)


def test_notebook_environment_summary_detects_blockers():
    dependency = NotebookDependency(
        name="missing",
        import_name="missing",
        required=True,
        purpose="Missing dependency.",
    )
    summary = NotebookEnvironmentSummary(
        python_version="3.12",
        platform_name="test",
        dependency_checks=[
            NotebookDependencyCheck(
                dependency=dependency,
                available=False,
                version=None,
            )
        ],
    )

    assert summary.blocking_count == 1
    assert summary.ready_for_notebook_work is False


def test_render_notebook_environment_report():
    summary = check_notebook_environment()
    report = render_notebook_environment_report(summary)

    assert "Notebook Environment Report" in report
    assert "Ready for notebook work" in report


def test_write_notebook_environment_report(tmp_path: Path):
    summary = check_notebook_environment()
    output_path = tmp_path / "notebook_environment_report.md"

    saved_path = write_notebook_environment_report(summary, output_path)

    assert saved_path.exists()
    assert "Notebook Environment Report" in saved_path.read_text(encoding="utf-8")
