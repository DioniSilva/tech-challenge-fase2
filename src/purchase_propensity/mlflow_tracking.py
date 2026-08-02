from __future__ import annotations

from pathlib import Path
from typing import Any

import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow.models import infer_signature
from sklearn.pipeline import Pipeline

from purchase_propensity.config import AppConfig


def log_training_run(
    *,
    config: AppConfig,
    config_path: str | Path,
    pipeline: Pipeline,
    x_train: pd.DataFrame,
    metrics: dict[str, float],
    model_path: Path,
    metrics_path: Path,
) -> None:
    """Log a training run, artifacts, and the model registry version.

    Args:
        config: Application configuration used by the training run.
        config_path: Path to the configuration artifact.
        pipeline: Fitted scikit-learn pipeline.
        x_train: Training features used for model signature inference.
        metrics: Evaluation metrics to log.
        model_path: Path to the serialized model artifact.
        metrics_path: Path to the serialized metrics artifact.
    """
    tracking_uri = config.mlflow.tracking_uri
    experiment_name = config.mlflow.experiment_name
    registered_model_name = config.mlflow.registered_model_name

    _ensure_sqlite_parent_directory(tracking_uri)
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_registry_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    params = _build_param_payload(config)
    tags = {
        "project": "tech-challenge-fase-2",
        "problem_type": "binary_classification",
        "dataset_target": config.dataset.target_column,
        "model_name": config.model.name,
    }

    with mlflow.start_run(run_name=f"{config.model.name}-purchase-propensity"):
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)
        mlflow.set_tags(tags)
        mlflow.log_artifact(str(config_path), artifact_path="config")
        mlflow.log_artifact(str(metrics_path), artifact_path="reports")
        mlflow.log_artifact(str(model_path), artifact_path="artifacts")

        signature_input = _coerce_numeric_inputs_for_signature(x_train)
        signature = infer_signature(signature_input, pipeline.predict(x_train))
        input_example = signature_input.head(min(len(signature_input), 5))
        mlflow.sklearn.log_model(
            sk_model=pipeline,
            name=config.mlflow.model_artifact_name,
            signature=signature,
            input_example=input_example,
            registered_model_name=registered_model_name,
        )


def _ensure_sqlite_parent_directory(tracking_uri: str) -> None:
    prefix = "sqlite:///"
    if tracking_uri.startswith(prefix):
        database_path = Path(tracking_uri.removeprefix(prefix))
        database_path.parent.mkdir(parents=True, exist_ok=True)


def _build_param_payload(config: AppConfig) -> dict[str, Any]:
    params: dict[str, Any] = {
        "dataset.raw_path": str(config.dataset.raw_path),
        "dataset.target_column": config.dataset.target_column,
        "split.test_size": config.split.test_size,
        "split.random_state": config.split.random_state,
        "model.name": config.model.name,
        "processed.train_path": str(config.processed.train_path),
        "processed.test_path": str(config.processed.test_path),
        "artifacts.model_path": str(config.artifacts.model_path),
        "artifacts.metrics_path": str(config.artifacts.metrics_path),
    }
    for key, value in config.model.params.items():
        params[f"model.param.{key}"] = value
    return params


def _coerce_numeric_inputs_for_signature(dataframe: pd.DataFrame) -> pd.DataFrame:
    adjusted = dataframe.copy()
    numeric_columns = adjusted.select_dtypes(include=["integer"]).columns.tolist()
    if numeric_columns:
        adjusted[numeric_columns] = adjusted[numeric_columns].astype("float64")
    return adjusted
