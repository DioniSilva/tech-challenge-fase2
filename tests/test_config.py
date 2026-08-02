from __future__ import annotations

from pathlib import Path

import pytest

from purchase_propensity.config import load_config


def write_config(tmp_path: Path, content: str) -> Path:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(content, encoding="utf-8")
    return config_path


def test_load_config_rejects_missing_sections(tmp_path: Path) -> None:
    config_path = write_config(tmp_path, "dataset: {}")

    with pytest.raises(ValueError, match="missing sections"):
        load_config(config_path)


def test_load_config_rejects_invalid_test_size(tmp_path: Path) -> None:
    config_path = write_config(
        tmp_path,
        """
dataset: {raw_path: raw.csv, target_column: Revenue}
split: {test_size: 1.0, random_state: 42}
model: {name: LogisticRegression, params: {}}
processed: {train_path: train.csv, test_path: test.csv}
artifacts: {model_path: model.joblib, metrics_path: metrics.json}
mlflow: {tracking_uri: sqlite:///mlflow.db, experiment_name: test, registered_model_name: test}
""",
    )

    with pytest.raises(ValueError, match="test_size"):
        load_config(config_path)


def test_load_config_rejects_unsupported_model(tmp_path: Path) -> None:
    config_path = write_config(
        tmp_path,
        """
dataset: {raw_path: raw.csv, target_column: Revenue}
split: {test_size: 0.2, random_state: 42}
model: {name: RandomForest, params: {}}
processed: {train_path: train.csv, test_path: test.csv}
artifacts: {model_path: model.joblib, metrics_path: metrics.json}
mlflow: {tracking_uri: sqlite:///mlflow.db, experiment_name: test, registered_model_name: test}
""",
    )

    with pytest.raises(ValueError, match="model.name"):
        load_config(config_path)


def test_load_config_applies_mlflow_environment_overrides(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MLFLOW_TRACKING_URI", "sqlite:///tmp/override.db")
    monkeypatch.setenv("MLFLOW_EXPERIMENT_NAME", "override-experiment")
    monkeypatch.setenv("MLFLOW_REGISTERED_MODEL_NAME", "override-model")

    config = load_config("configs/base.yaml")

    assert config.mlflow.tracking_uri == "sqlite:///tmp/override.db"
    assert config.mlflow.experiment_name == "override-experiment"
    assert config.mlflow.registered_model_name == "override-model"
