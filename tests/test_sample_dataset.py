from pathlib import Path

from floodrisk.data.sample_dataset import build_sample_dataset, save_sample_dataset


def test_build_sample_dataset_contains_expected_columns():
    dataset = build_sample_dataset()

    expected_columns = {
        "location_name",
        "state",
        "latitude",
        "longitude",
        "risk_score",
        "risk_class",
        "confidence",
    }

    assert expected_columns.issubset(dataset.columns)
    assert len(dataset) >= 5
    assert dataset["risk_score"].between(0, 100).all()


def test_save_sample_dataset_creates_csv(tmp_path: Path):
    output_path = tmp_path / "sample.csv"

    saved_path = save_sample_dataset(output_path)

    assert saved_path.exists()
    assert saved_path.suffix == ".csv"
