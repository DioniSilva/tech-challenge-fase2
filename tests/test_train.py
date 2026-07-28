from __future__ import annotations

import json
from dataclasses import replace

import pandas as pd
import pytest

from purchase_propensity.config import load_config
from purchase_propensity.train import build_training_pipeline
from purchase_propensity.train import run_training

from tests.test_data import build_dataframe


def test_training_pipeline_fits_synthetic_dataset() -> None:
    dataframe = build_dataframe()
    features = dataframe.drop(columns=["Revenue"])
    target = dataframe["Revenue"]
    pipeline = build_training_pipeline(features, load_config("configs/base.yaml"))

    pipeline.fit(features, target)

    predictions = pipeline.predict(features)
    assert len(predictions) == len(target)


def test_run_training_writes_metrics_and_model(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    dataframe = build_dataframe()
    expanded = pd.concat([dataframe] * 3, ignore_index=True)
    train_path = tmp_path / "train.csv"
    test_path = tmp_path / "test.csv"
    model_path = tmp_path / "artifacts" / "model.joblib"
    metrics_path = tmp_path / "artifacts" / "metrics.json"

    expanded.iloc[:6].to_csv(train_path, index=False)
    expanded.iloc[6:].to_csv(test_path, index=False)

    base_config = load_config("configs/base.yaml")
    config = replace(
        base_config,
        processed=replace(
            base_config.processed,
            train_path=train_path,
            test_path=test_path,
        ),
        artifacts=replace(
            base_config.artifacts,
            model_path=model_path,
            metrics_path=metrics_path,
        ),
    )
    monkeypatch.setattr("purchase_propensity.train.load_config", lambda _: config)

    metrics = run_training("configs/base.yaml")

    assert set(metrics) == {"accuracy", "f1", "precision", "recall", "roc_auc"}
    assert json.loads(metrics_path.read_text(encoding="utf-8"))["accuracy"] == metrics["accuracy"]
    assert model_path.exists()
    assert model_path.stat().st_size > 0
