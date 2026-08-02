from __future__ import annotations

from dataclasses import replace

import pandas as pd
import pytest

from purchase_propensity.config import load_config
from purchase_propensity.prepare import save_processed_splits
from tests.helpers import build_dataframe


def test_save_processed_splits_writes_train_and_test_csv(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    raw_path = tmp_path / "raw.csv"
    train_path = tmp_path / "processed" / "train.csv"
    test_path = tmp_path / "processed" / "test.csv"

    dataframe = pd.concat([build_dataframe()] * 6, ignore_index=True)
    dataframe.to_csv(raw_path, index=False)

    base_config = load_config("configs/base.yaml")
    config = replace(
        base_config,
        dataset=replace(base_config.dataset, raw_path=raw_path),
        processed=replace(
            base_config.processed,
            train_path=train_path,
            test_path=test_path,
        ),
    )
    monkeypatch.setattr("purchase_propensity.prepare.load_config", lambda _: config)

    returned_train_path, returned_test_path = save_processed_splits("configs/base.yaml")

    saved_train = pd.read_csv(train_path)
    saved_test = pd.read_csv(test_path)

    assert returned_train_path == train_path
    assert returned_test_path == test_path
    assert len(saved_train) + len(saved_test) == len(dataframe)
    assert "Revenue" in saved_train.columns
    assert "Revenue" in saved_test.columns
