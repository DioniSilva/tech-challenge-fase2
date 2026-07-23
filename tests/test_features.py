from __future__ import annotations

from purchase_propensity.features import build_preprocessor

from tests.test_data import build_dataframe


def test_preprocessor_fits_dataframe() -> None:
    dataframe = build_dataframe().drop(columns=["Revenue"])
    preprocessor = build_preprocessor(dataframe)

    transformed = preprocessor.fit_transform(dataframe)

    assert transformed.shape[0] == len(dataframe)
