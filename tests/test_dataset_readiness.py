from pathlib import Path

from floodrisk.ml.training_schema import REQUIRED_TRAINING_COLUMNS
from floodrisk.notebooks.readiness import (
    build_dataset_readiness_summary,
    list_dataset_readiness_checks,
    render_dataset_readiness_report,
    write_dataset_readiness_report,
)


def write_training_csv(path: Path, columns: tuple[str, ...]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = ",".join(columns)
    row = ",".join("1" for _ in columns)
    path.write_text(f"{header}\n{row}\n", encoding="utf-8")
    return path


def test_list_dataset_readiness_checks_contains_training_blockers():
    checks = list_dataset_readiness_checks()
    blocking_checks = [check for check in checks if check.required_for_training]

    assert len(checks) >= 6
    assert len(blocking_checks) == 2


def test_build_dataset_readiness_summary_reports_missing_training_items(
    tmp_path: Path,
):
    summary = build_dataset_readiness_summary(tmp_path)

    assert summary.check_count >= 6
    assert summary.blocking_count == 2
    assert summary.ready_for_training is False


def test_build_dataset_readiness_summary_rejects_invalid_training_table(
    tmp_path: Path,
):
    design_path = tmp_path / "docs" / "TRAINING_DATASET.md"
    training_table_path = (
        tmp_path / "data" / "processed" / "model_training" / "training_features.csv"
    )

    design_path.parent.mkdir(parents=True, exist_ok=True)
    training_table_path.parent.mkdir(parents=True, exist_ok=True)

    design_path.write_text("# Training Dataset\n", encoding="utf-8")
    training_table_path.write_text("target\n0\n", encoding="utf-8")

    summary = build_dataset_readiness_summary(tmp_path)

    assert summary.blocking_count == 1
    assert summary.ready_for_training is False


def test_build_dataset_readiness_summary_detects_training_ready_table(
    tmp_path: Path,
):
    design_path = tmp_path / "docs" / "TRAINING_DATASET.md"
    training_table_path = (
        tmp_path / "data" / "processed" / "model_training" / "training_features.csv"
    )

    design_path.parent.mkdir(parents=True, exist_ok=True)
    design_path.write_text("# Training Dataset\n", encoding="utf-8")
    write_training_csv(training_table_path, REQUIRED_TRAINING_COLUMNS)

    summary = build_dataset_readiness_summary(tmp_path)

    assert summary.blocking_count == 0
    assert summary.ready_for_training is True


def test_render_dataset_readiness_report_contains_training_status(tmp_path: Path):
    summary = build_dataset_readiness_summary(tmp_path)
    report = render_dataset_readiness_report(summary)

    assert "Dataset Readiness Report" in report
    assert "Ready for ML training: False" in report
    assert "Training dataset design document" in report
    assert "Training Table Rule" in report


def test_write_dataset_readiness_report(tmp_path: Path):
    summary = build_dataset_readiness_summary(tmp_path)
    output_path = tmp_path / "dataset_readiness_report.md"

    saved_path = write_dataset_readiness_report(summary, output_path)

    assert saved_path.exists()
    assert "Dataset Readiness Report" in saved_path.read_text(encoding="utf-8")
