from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


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
class AppConfig:
    dataset: DatasetConfig
    split: SplitConfig
    model: ModelConfig


def load_config(config_path: str | Path) -> AppConfig:
    path = Path(config_path)
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
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
    )
