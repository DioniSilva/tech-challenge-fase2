from __future__ import annotations

import argparse
from pprint import pprint

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from purchase_propensity.config import load_config
from purchase_propensity.data import load_dataset, split_features_target
from purchase_propensity.evaluate import evaluate_model
from purchase_propensity.features import build_preprocessor


def build_training_pipeline(features) -> Pipeline:
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(features)),
            ("model", LogisticRegression(max_iter=1000)),
        ]
    )


def run_training(config_path: str) -> dict[str, float]:
    config = load_config(config_path)
    dataframe = load_dataset(config.dataset.raw_path)
    features, target = split_features_target(dataframe, target_column=config.dataset.target_column)
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=config.split.test_size,
        random_state=config.split.random_state,
        stratify=target,
    )

    pipeline = build_training_pipeline(features)
    pipeline.fit(x_train, y_train)

    y_pred = pipeline.predict(x_test)
    y_score = pipeline.predict_proba(x_test)[:, 1]
    return evaluate_model(y_true=y_test, y_pred=y_pred, y_score=y_score)


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
    pprint(metrics)


if __name__ == "__main__":
    main()
