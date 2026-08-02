from __future__ import annotations

import pytest

from purchase_propensity.data import load_dataset, split_features_target, validate_dataset
from tests.helpers import build_dataframe


def test_validate_dataset_accepts_expected_schema() -> None:
    validate_dataset(build_dataframe())


def test_split_features_target_returns_expected_shapes() -> None:
    dataframe = build_dataframe()
    features, target = split_features_target(dataframe, target_column="Revenue")

    assert "Revenue" not in features.columns
    assert target.tolist() == [0, 1, 1]


def test_validate_dataset_rejects_missing_columns() -> None:
    dataframe = build_dataframe().drop(columns=["Revenue"])

    with pytest.raises(ValueError, match="missing required columns"):
        validate_dataset(dataframe)


def test_validate_dataset_rejects_empty_dataset() -> None:
    dataframe = build_dataframe().iloc[0:0]

    with pytest.raises(ValueError, match="at least one row"):
        validate_dataset(dataframe)


def test_validate_dataset_rejects_non_binary_target() -> None:
    dataframe = build_dataframe()
    dataframe.loc[0, "Revenue"] = 2

    with pytest.raises(ValueError, match="only binary values"):
        validate_dataset(dataframe)


def test_validate_dataset_rejects_null_target() -> None:
    dataframe = build_dataframe()
    dataframe.loc[0, "Revenue"] = None

    with pytest.raises(ValueError, match="must not contain null"):
        validate_dataset(dataframe)


def test_load_dataset_rejects_missing_path(tmp_path) -> None:
    with pytest.raises(FileNotFoundError, match="Dataset not found"):
        load_dataset(tmp_path / "missing.csv")


def test_split_features_target_rejects_missing_target() -> None:
    with pytest.raises(ValueError, match="Target column 'Missing' is not present"):
        split_features_target(build_dataframe(), target_column="Missing")
