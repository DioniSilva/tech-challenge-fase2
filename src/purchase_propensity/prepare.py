from __future__ import annotations

import argparse
from pathlib import Path

from sklearn.model_selection import train_test_split

from purchase_propensity.config import load_config
from purchase_propensity.data import load_dataset


def save_processed_splits(config_path: str) -> tuple[Path, Path]:
    config = load_config(config_path)
    dataframe = load_dataset(config.dataset.raw_path)

    train_df, test_df = train_test_split(
        dataframe,
        test_size=config.split.test_size,
        random_state=config.split.random_state,
        stratify=dataframe[config.dataset.target_column].astype(int),
    )

    config.processed.train_path.parent.mkdir(parents=True, exist_ok=True)
    config.processed.test_path.parent.mkdir(parents=True, exist_ok=True)

    train_df.to_csv(config.processed.train_path, index=False)
    test_df.to_csv(config.processed.test_path, index=False)
    return config.processed.train_path, config.processed.test_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare the processed train/test splits.")
    parser.add_argument(
        "--config",
        default="configs/base.yaml",
        help="Path to the YAML config file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    train_path, test_path = save_processed_splits(config_path=args.config)
    print(f"Saved processed splits to {train_path} and {test_path}.")


if __name__ == "__main__":
    main()
