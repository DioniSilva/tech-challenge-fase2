from __future__ import annotations

from purchase_propensity.train import build_training_pipeline

from tests.test_data import build_dataframe


def test_training_pipeline_fits_synthetic_dataset() -> None:
    dataframe = build_dataframe()
    features = dataframe.drop(columns=["Revenue"])
    target = dataframe["Revenue"]
    pipeline = build_training_pipeline(features)

    pipeline.fit(features, target)

    predictions = pipeline.predict(features)
    assert len(predictions) == len(target)
