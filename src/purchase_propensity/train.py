from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from purchase_propensity.config import AppConfig, load_config
from purchase_propensity.data import load_dataset, split_features_target
from purchase_propensity.evaluate import evaluate_model
from purchase_propensity.features import build_preprocessor


def build_training_pipeline(features, config: AppConfig) -> Pipeline:
    if config.model.name != "LogisticRegression":
        raise ValueError(f"Unsupported model '{config.model.name}'.")

    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(features)),
            ("model", LogisticRegression(**config.model.params)),
        ]
    )


def run_training(config_path: str) -> dict[str, float]:
    config = load_config(config_path)
    train_df = load_dataset(config.processed.train_path)
    test_df = load_dataset(config.processed.test_path)

    x_train, y_train = split_features_target(train_df, target_column=config.dataset.target_column)
    x_test, y_test = split_features_target(test_df, target_column=config.dataset.target_column)

    pipeline = build_training_pipeline(x_train, config)
    pipeline.fit(x_train, y_train)

    y_pred = pipeline.predict(x_test)
    y_score = pipeline.predict_proba(x_test)[:, 1]
    metrics = evaluate_model(y_true=y_test, y_pred=y_pred, y_score=y_score)

    _save_training_outputs(
        pipeline=pipeline,
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
    model_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path)
    metrics_path.write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the purchase propensity baseline.")
    parser.add_argument(
        "--config",
        default="configs/base.yaml",
        help="Path to the YAML config file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metrics = run_training(config_path=args.config)
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
