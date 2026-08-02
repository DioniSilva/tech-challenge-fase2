from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from purchase_propensity.data import REQUIRED_COLUMNS, validate_dataset

DEFAULT_OUTPUT_PATH = Path("data/external/online_shoppers_intention.csv")
EXPECTED_ROW_COUNT = 12_330
UCI_DATASET_ID = 468


@dataclass(frozen=True)
class ExportSummary:
    output_path: Path
    row_count: int
    column_count: int
    target_column: str


def _fetch_online_shoppers_dataset() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    try:
        from ucimlrepo import fetch_ucirepo
    except ImportError as exc:
        raise RuntimeError(
            "The 'ucimlrepo' package is required for dataset acquisition. "
            "Install it in the project environment before running this command."
        ) from exc

    dataset = fetch_ucirepo(id=UCI_DATASET_ID)
    features = pd.DataFrame(dataset.data.features)
    targets = pd.DataFrame(dataset.data.targets)
    metadata = dict(getattr(dataset, "metadata", {}) or {})
    return features, targets, metadata


def _build_export_dataframe(features: pd.DataFrame, targets: pd.DataFrame) -> pd.DataFrame:
    if "Revenue" not in targets.columns:
        raise ValueError("Fetched dataset does not expose the expected 'Revenue' target column.")

    dataframe = pd.concat([features, targets[["Revenue"]]], axis=1)
    validate_dataset(dataframe)

    if len(dataframe) != EXPECTED_ROW_COUNT:
        raise ValueError(
            f"Fetched dataset has {len(dataframe)} rows, expected {EXPECTED_ROW_COUNT}."
        )

    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)
    if missing_columns:
        raise ValueError(f"Fetched dataset is missing required columns: {sorted(missing_columns)}")

    return dataframe


def export_online_shoppers_dataset(
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
    *,
    overwrite: bool = False,
) -> ExportSummary:
    """Fetch, validate, and export the official UCI dataset.

    Args:
        output_path: Destination path for the exported CSV.
        overwrite: Whether to replace an existing destination file.

    Returns:
        Summary of the exported dataset.

    Raises:
        FileExistsError: If the destination exists and overwrite is false.
        ValueError: If the fetched data does not match the expected schema.
    """
    path = Path(output_path)
    if path.exists() and not overwrite:
        raise FileExistsError(
            f"Output file already exists at '{path}'. Use --overwrite to replace it."
        )

    features, targets, metadata = _fetch_online_shoppers_dataset()
    dataframe = _build_export_dataframe(features, targets)

    path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(path, index=False)

    metadata_instances = metadata.get("num_instances")
    if metadata_instances is not None and int(metadata_instances) != EXPECTED_ROW_COUNT:
        raise ValueError(
            "Fetched dataset metadata does not match the expected instance count for the "
            "official UCI dataset."
        )

    return ExportSummary(
        output_path=path,
        row_count=len(dataframe),
        column_count=len(dataframe.columns),
        target_column="Revenue",
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for dataset acquisition."""
    parser = argparse.ArgumentParser(
        description="Fetch the official UCI Online Shoppers dataset and save it locally."
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Destination CSV path. Default: data/external/online_shoppers_intention.csv",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace the destination file if it already exists.",
    )
    return parser.parse_args()


def main() -> None:
    """Fetch the dataset and print an export summary."""
    args = parse_args()
    summary = export_online_shoppers_dataset(output_path=args.output, overwrite=args.overwrite)
    print(
        f"Saved dataset to {summary.output_path} "
        f"({summary.row_count} rows, {summary.column_count} columns, target={summary.target_column})."
    )


if __name__ == "__main__":
    main()
