from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {
    "Administrative",
    "Administrative_Duration",
    "Informational",
    "Informational_Duration",
    "ProductRelated",
    "ProductRelated_Duration",
    "BounceRates",
    "ExitRates",
    "PageValues",
    "SpecialDay",
    "Month",
    "OperatingSystems",
    "Browser",
    "Region",
    "TrafficType",
    "VisitorType",
    "Weekend",
    "Revenue",
}


def load_dataset(dataset_path: str | Path) -> pd.DataFrame:
    """Load a CSV dataset and validate its required columns.

    Args:
        dataset_path: Path to the dataset CSV file.

    Returns:
        The validated dataset.

    Raises:
        FileNotFoundError: If the dataset path does not exist.
        ValueError: If required columns are missing.
    """
    path = Path(dataset_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at '{path}'. Place the raw CSV at data/external/online_shoppers_intention.csv."
        )

    dataframe = pd.read_csv(path)
    validate_dataset(dataframe)
    return dataframe


def validate_dataset(dataframe: pd.DataFrame) -> None:
    """Validate that the dataset contains the required project columns.

    Args:
        dataframe: Dataset to validate.

    Raises:
        ValueError: If one or more required columns are missing.
    """
    if dataframe.empty:
        raise ValueError("Dataset must contain at least one row.")

    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing_columns)}")

    target_values = set(dataframe["Revenue"].dropna().unique())
    if not target_values.issubset({0, 1}):
        raise ValueError("Dataset target 'Revenue' must contain only binary values.")
    if dataframe["Revenue"].isna().any():
        raise ValueError("Dataset target 'Revenue' must not contain null values.")


def split_features_target(dataframe: pd.DataFrame, target_column: str) -> tuple[pd.DataFrame, pd.Series]:
    """Separate a dataset into features and an integer target series.

    Args:
        dataframe: Dataset containing the target column.
        target_column: Name of the target column.

    Returns:
        A tuple containing the feature DataFrame and integer target Series.

    Raises:
        ValueError: If the target column is not present.
    """
    if target_column not in dataframe.columns:
        raise ValueError(f"Target column '{target_column}' is not present in the dataset.")

    features = dataframe.drop(columns=[target_column])
    target = dataframe[target_column].astype(int)
    return features, target
