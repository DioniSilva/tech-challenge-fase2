from __future__ import annotations

import pandas as pd
import pytest

from purchase_propensity import dataset_fetch


def build_features() -> pd.DataFrame:
    row_count = dataset_fetch.EXPECTED_ROW_COUNT
    return pd.DataFrame(
        {
            "Administrative": [0] * row_count,
            "Administrative_Duration": [0.0] * row_count,
            "Informational": [0] * row_count,
            "Informational_Duration": [0.0] * row_count,
            "ProductRelated": [1] * row_count,
            "ProductRelated_Duration": [10.0] * row_count,
            "BounceRates": [0.1] * row_count,
            "ExitRates": [0.2] * row_count,
            "PageValues": [0.0] * row_count,
            "SpecialDay": [0.0] * row_count,
            "Month": ["Feb"] * row_count,
            "OperatingSystems": [1] * row_count,
            "Browser": [1] * row_count,
            "Region": [1] * row_count,
            "TrafficType": [1] * row_count,
            "VisitorType": ["Returning_Visitor"] * row_count,
            "Weekend": [False] * row_count,
        }
    )


def build_targets() -> pd.DataFrame:
    return pd.DataFrame({"Revenue": [False] * dataset_fetch.EXPECTED_ROW_COUNT})


def test_build_export_dataframe_returns_expected_shape() -> None:
    dataframe = dataset_fetch._build_export_dataframe(build_features(), build_targets())

    assert dataframe.shape == (dataset_fetch.EXPECTED_ROW_COUNT, len(dataset_fetch.REQUIRED_COLUMNS))
    assert "Revenue" in dataframe.columns


def test_export_online_shoppers_dataset_writes_csv(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        dataset_fetch,
        "_fetch_online_shoppers_dataset",
        lambda: (build_features(), build_targets(), {"num_instances": dataset_fetch.EXPECTED_ROW_COUNT}),
    )

    output_path = tmp_path / "online_shoppers_intention.csv"
    summary = dataset_fetch.export_online_shoppers_dataset(output_path=output_path)

    saved = pd.read_csv(output_path)

    assert summary.output_path == output_path
    assert summary.row_count == dataset_fetch.EXPECTED_ROW_COUNT
    assert saved.shape == (dataset_fetch.EXPECTED_ROW_COUNT, len(dataset_fetch.REQUIRED_COLUMNS))


def test_export_online_shoppers_dataset_requires_overwrite(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        dataset_fetch,
        "_fetch_online_shoppers_dataset",
        lambda: (build_features(), build_targets(), {"num_instances": dataset_fetch.EXPECTED_ROW_COUNT}),
    )

    output_path = tmp_path / "online_shoppers_intention.csv"
    output_path.write_text("existing", encoding="utf-8")

    with pytest.raises(FileExistsError):
        dataset_fetch.export_online_shoppers_dataset(output_path=output_path)
