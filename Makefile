POETRY ?= poetry
PYTHON_BIN := $(shell for bin in python3.12 python3.11; do command -v $$bin >/dev/null 2>&1 && { printf "%s" "$$bin"; break; }; done)
PACKAGE_MODULE := purchase_propensity
CONFIG_PATH ?= configs/base.yaml

.PHONY: help venv setup check test prepare train fetch-data dvc-repro mlflow-ui

help:
	@printf "Available targets:\n"
	@printf "  make venv   - create the local Poetry virtual environment\n"
	@printf "  make setup  - install project dependencies with Poetry\n"
	@printf "  make check  - validate pyproject metadata\n"
	@printf "  make test   - run automated tests\n"
	@printf "  make prepare - generate processed train/test splits from the raw dataset\n"
	@printf "  make train  - run the baseline training entrypoint\n"
	@printf "  make fetch-data - fetch the official UCI dataset into data/external/\n"
	@printf "  make dvc-repro - reproduce the configured DVC pipeline\n"
	@printf "  make mlflow-ui - start the local MLflow UI for the project tracking database\n"

venv:
	@if [ -z "$(PYTHON_BIN)" ]; then \
		printf "Compatible interpreter not found. Install Python 3.11 or 3.12 and rerun 'make venv'.\n"; \
		exit 1; \
	fi
	$(POETRY) config virtualenvs.in-project true --local
	$(POETRY) env use $(PYTHON_BIN)

setup: venv
	$(POETRY) install

check:
	$(POETRY) check

test:
	$(POETRY) run pytest -q

prepare:
	$(POETRY) run python -m $(PACKAGE_MODULE).prepare --config $(CONFIG_PATH)

train:
	$(POETRY) run python -m $(PACKAGE_MODULE).train --config $(CONFIG_PATH)

fetch-data:
	$(POETRY) run python -m $(PACKAGE_MODULE).dataset_fetch

dvc-repro:
	$(POETRY) run dvc repro

mlflow-ui:
	$(POETRY) run mlflow ui --backend-store-uri sqlite:///mlruns/mlflow.db
