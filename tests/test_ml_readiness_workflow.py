from pathlib import Path


def test_ml_training_readiness_doc_exists():
    path = Path("docs/ML_TRAINING_READINESS.md")

    assert path.exists()

    content = path.read_text(encoding="utf-8")

    assert "ML Training Readiness Workflow" in content
    assert "Real supervised ML training remains blocked" in content
    assert "verified historical flood" in content
    assert "risk_score" in content


def test_ml_readiness_suite_script_exists():
    path = Path("scripts/run_ml_readiness_suite.ps1")

    assert path.exists()

    content = path.read_text(encoding="utf-8")

    assert "run_target_label_source_plan.ps1" in content
    assert "run_feature_table_plan.ps1" in content
    assert "run_feature_table_builder_dry_run.ps1" in content
    assert "run_ml_training_readiness.ps1" in content


def test_training_dataset_doc_links_ml_readiness_workflow():
    path = Path("docs/TRAINING_DATASET.md")
    content = path.read_text(encoding="utf-8")

    assert "ML Training Readiness Gate" in content
