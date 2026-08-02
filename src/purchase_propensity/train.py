from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from purchase_propensity.config import AppConfig, load_config
from purchase_propensity.data import load_dataset, split_features_target
from purchase_propensity.evaluate import evaluate_model
from purchase_propensity.features import build_preprocessor
from purchase_propensity.mlflow_tracking import log_training_run


def build_training_pipeline(features: pd.DataFrame, config: AppConfig) -> Pipeline:
    """Build the configured preprocessing and classification pipeline.

    Args:
        features: Training features used to configure preprocessing columns.
        config: Application configuration with model settings.

    Returns:
        A fitted-ready scikit-learn pipeline.

    Raises:
        ValueError: If the configured model is unsupported.
    """
    if config.model.name != "LogisticRegression":
        raise ValueError(f"Unsupported model '{config.model.name}'.")

    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(features)),
            ("model", LogisticRegression(**config.model.params)),
        ]
    )


def train_model(
    features: pd.DataFrame,
    target: pd.Series,
    config: AppConfig,
) -> Pipeline:
    """Build and fit the configured model pipeline.

    Args:
        features: Training feature values.
        target: Training target values.
        config: Application configuration with model settings.

    Returns:
        Fitted scikit-learn pipeline.
    """
    pipeline = build_training_pipeline(features, config)
    pipeline.fit(features, target)
    return pipeline


def evaluate_trained_model(
    pipeline: Pipeline,
    features: pd.DataFrame,
    target: pd.Series,
) -> dict[str, float]:
    """Evaluate a fitted model pipeline on a labeled dataset."""
    predictions = pipeline.predict(features)
    scores = pipeline.predict_proba(features)[:, 1]
    return evaluate_model(y_true=target, y_pred=predictions, y_score=scores)


def run_training(config_path: str) -> dict[str, float]:
    """Train, evaluate, persist, and track the purchase propensity model.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        Evaluation metrics calculated on the held-out test split.
    """
    config = load_config(config_path)
    train_df = load_dataset(config.processed.train_path)
    test_df = load_dataset(config.processed.test_path)

    x_train, y_train = split_features_target(train_df, target_column=config.dataset.target_column)
    x_test, y_test = split_features_target(test_df, target_column=config.dataset.target_column)

    pipeline = train_model(x_train, y_train, config)
    metrics = evaluate_trained_model(pipeline, x_test, y_test)

    _save_training_outputs(
        pipeline=pipeline,
        metrics=metrics,
        model_path=config.artifacts.model_path,
        metrics_path=config.artifacts.metrics_path,
    )
    log_training_run(
        config=config,
        config_path=config_path,
        pipeline=pipeline,
        x_train=x_train,
        metrics=metrics,
        model_path=config.artifacts.model_path,
        metrics_path=config.artifacts.metrics_path,
    )
    return metrics


def _save_training_outputs(
    pipeline: Pipeline,
    metrics: dict[str, float],
    model_path: Path,
    metrics_path: Path,
) -> None:
    """Persist the trained pipeline and its evaluation metrics."""
    model_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path)
    metrics_path.write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the training entrypoint."""
    parser = argparse.ArgumentParser(description="Train the purchase propensity baseline.")
    parser.add_argument(
        "--config",
        default="configs/base.yaml",
        help="Path to the YAML config file.",
    )
    return parser.parse_args()


def main() -> None:
    """Run model training and print the resulting metrics."""
    args = parse_args()
    metrics = run_training(config_path=args.config)
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
