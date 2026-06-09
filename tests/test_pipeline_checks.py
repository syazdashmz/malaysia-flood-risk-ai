import json
from pathlib import Path

from floodrisk.data.pipeline_checks import (
    WEATHER_PIPELINE_REQUIRED_OUTPUTS,
    check_required_files,
    count_jsonl_records,
    render_weather_pipeline_validation,
    validate_weather_pipeline,
    write_weather_pipeline_validation,
)


def create_required_weather_outputs(project_root: Path) -> None:
    for relative_path in WEATHER_PIPELINE_REQUIRED_OUTPUTS:
        path = project_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.name.endswith(".json"):
            path.write_text(
                json.dumps({"risk_engine_weather_warning": "warning"}),
                encoding="utf-8",
            )
        elif path.name.endswith(".jsonl"):
            path.write_text("{}\n{}\n", encoding="utf-8")
        else:
            path.write_text("sample\n", encoding="utf-8")


def test_check_required_files_detects_existing_and_missing_files(tmp_path: Path):
    existing_path = tmp_path / "existing.txt"
    existing_path.write_text("ok", encoding="utf-8")

    checks = check_required_files(
        tmp_path,
        ["existing.txt", "missing.txt"],
    )

    assert checks[0].exists is True
    assert checks[1].exists is False


def test_count_jsonl_records_ignores_blank_lines(tmp_path: Path):
    input_path = tmp_path / "manifest.jsonl"
    input_path.write_text("{}\n\n{}\n", encoding="utf-8")

    assert count_jsonl_records(input_path) == 2


def test_validate_weather_pipeline_passes_with_required_outputs(tmp_path: Path):
    create_required_weather_outputs(tmp_path)

    validation = validate_weather_pipeline(tmp_path)

    assert validation.is_valid is True
    assert validation.manifest_record_count == 2
    assert validation.risk_engine_weather_warning == "warning"


def test_validate_weather_pipeline_fails_when_outputs_are_missing(tmp_path: Path):
    validation = validate_weather_pipeline(tmp_path)

    assert validation.is_valid is False
    assert validation.missing_paths


def test_write_weather_pipeline_validation(tmp_path: Path):
    create_required_weather_outputs(tmp_path)
    validation = validate_weather_pipeline(tmp_path)
    output_path = tmp_path / "validation.md"

    saved_path = write_weather_pipeline_validation(validation, output_path)
    content = saved_path.read_text(encoding="utf-8")

    assert "Weather Pipeline Validation" in content
    assert "Valid: True" in content


def test_render_weather_pipeline_validation_lists_required_files(tmp_path: Path):
    create_required_weather_outputs(tmp_path)
    validation = validate_weather_pipeline(tmp_path)

    markdown = render_weather_pipeline_validation(validation)

    assert "Required Files" in markdown
    assert "data/raw/manifest.jsonl" in markdown
