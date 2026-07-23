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
    path = Path(dataset_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at '{path}'. Place the raw CSV at data/external/online_shoppers_intention.csv."
        )

    dataframe = pd.read_csv(path)
    validate_dataset(dataframe)
    return dataframe


def validate_dataset(dataframe: pd.DataFrame) -> None:
    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing_columns)}")


def split_features_target(dataframe: pd.DataFrame, target_column: str) -> tuple[pd.DataFrame, pd.Series]:
    if target_column not in dataframe.columns:
        raise ValueError(f"Target column '{target_column}' is not present in the dataset.")

    features = dataframe.drop(columns=[target_column])
    target = dataframe[target_column].astype(int)
    return features, target
