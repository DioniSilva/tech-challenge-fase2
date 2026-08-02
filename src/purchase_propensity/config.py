from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml
from dotenv import load_dotenv


@dataclass(frozen=True)
class DatasetConfig:
    raw_path: Path
    target_column: str


@dataclass(frozen=True)
class SplitConfig:
    test_size: float
    random_state: int


@dataclass(frozen=True)
class ModelConfig:
    name: str
    params: dict[str, int | float | str | bool]


@dataclass(frozen=True)
class ProcessedDataConfig:
    train_path: Path
    test_path: Path


@dataclass(frozen=True)
class ArtifactConfig:
    model_path: Path
    metrics_path: Path


@dataclass(frozen=True)
class MlflowConfig:
    tracking_uri: str
    experiment_name: str
    registered_model_name: str
    model_artifact_name: str


@dataclass(frozen=True)
class AppConfig:
    dataset: DatasetConfig
    split: SplitConfig
    model: ModelConfig
    processed: ProcessedDataConfig
    artifacts: ArtifactConfig
    mlflow: MlflowConfig


def _validate_payload(payload: dict[str, object]) -> None:
    """Validate the required configuration sections and scalar values."""
    required_sections = {
        "dataset",
        "split",
        "model",
        "processed",
        "artifacts",
        "mlflow",
    }
    missing_sections = required_sections.difference(payload)
    if missing_sections:
        raise ValueError(f"Configuration is missing sections: {sorted(missing_sections)}")

    split = payload["split"]
    if not isinstance(split, dict):
        raise ValueError("Configuration section 'split' must be a mapping.")
    test_size = split.get("test_size")
    if not isinstance(test_size, int | float) or not 0 < float(test_size) < 1:
        raise ValueError("Configuration 'split.test_size' must be between 0 and 1.")

    model = payload["model"]
    if not isinstance(model, dict):
        raise ValueError("Configuration section 'model' must be a mapping.")
    if model.get("name") != "LogisticRegression":
        raise ValueError("Configuration 'model.name' must be 'LogisticRegression'.")


def load_config(config_path: str | Path) -> AppConfig:
    """Load the application configuration from a YAML file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        Parsed and typed application configuration.
    """
    load_dotenv()
    path = Path(config_path)
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Configuration root must be a mapping.")
    _validate_payload(payload)
    return AppConfig(
        dataset=DatasetConfig(
            raw_path=Path(payload["dataset"]["raw_path"]),
            target_column=payload["dataset"]["target_column"],
        ),
        split=SplitConfig(
            test_size=float(payload["split"]["test_size"]),
            random_state=int(payload["split"]["random_state"]),
        ),
        model=ModelConfig(
            name=payload["model"]["name"],
            params=dict(payload["model"].get("params", {})),
        ),
        processed=ProcessedDataConfig(
            train_path=Path(payload["processed"]["train_path"]),
            test_path=Path(payload["processed"]["test_path"]),
        ),
        artifacts=ArtifactConfig(
            model_path=Path(payload["artifacts"]["model_path"]),
            metrics_path=Path(payload["artifacts"]["metrics_path"]),
        ),
        mlflow=MlflowConfig(
            tracking_uri=os.getenv(
                "MLFLOW_TRACKING_URI",
                payload["mlflow"]["tracking_uri"],
            ),
            experiment_name=os.getenv(
                "MLFLOW_EXPERIMENT_NAME",
                payload["mlflow"]["experiment_name"],
            ),
            registered_model_name=os.getenv(
                "MLFLOW_REGISTERED_MODEL_NAME",
                payload["mlflow"]["registered_model_name"],
            ),
            model_artifact_name=payload["mlflow"].get("model_artifact_name", "model"),
        ),
    )
