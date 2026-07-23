# Minimal Project Structure Specification

## 1. Purpose

This document defines the **minimum viable repository structure** for the FIAP Phase 02 Tech Challenge implementation.

The goal is not to design the final ideal architecture up front. The goal is to define the smallest structure that:

- supports the selected dataset and baseline;
- keeps the project reproducible;
- creates clean paths for DVC, MLflow, and Docker;
- prevents early chaos in code and file organization.

## 2. Scope

This specification covers:

- top-level directories
- minimum required files
- ownership of each folder
- what should not be added yet

It does **not** define the full implementation details of preprocessing, training, or deployment.

## 3. Design Principles

The minimum structure should follow these principles:

### 3.1 Small but real

Every folder should exist because it has a clear near-term purpose.

### 3.2 Reproducibility first

The structure must support a project that can be installed, run, and reviewed from scratch.

### 3.3 Explicit separation of concerns

Data, source code, configs, scripts, and documentation should not be mixed casually.

### 3.4 Easy agent navigation

An agent should be able to infer where code, configs, artifacts, and docs belong without guessing.

### 3.5 Minimal startup path

The project must include only the minimum required to initialize correctly through a `Makefile` backed by `Poetry`.

This means:

- the repository should be startable through a small set of `make` targets;
- those targets should call `Poetry` as the Python environment and dependency entrypoint;
- no extra structure should be introduced before it is needed to support that startup path.

## 4. Current Project Decisions That Shape The Structure

The structure must reflect the current repository decisions:

- dataset: `Online Shoppers Purchasing Intention Dataset`
- target: `Revenue`
- baseline: `LogisticRegression`
- problem type: binary classification
- engineering focus: `Poetry`, `DVC`, `MLflow`, `Docker`

## 5. Minimum Target Structure

The minimum target structure is:

```text
.
├── AGENTS.md
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
├── .dockerignore
├── doc/
├── raw/
├── data/
├── src/
├── tests/
├── configs/
└── scripts/
```

## 6. Folder-Level Contract

### 6.1 `doc/`

Purpose:

- durable project documentation
- decisions
- specs
- implementation notes that are not raw course material

Must contain at least:

- `PROJECT_SPEC.md`
- `DATASET_DECISION.md`
- `MINIMAL_PROJECT_STRUCTURE_SPEC.md`

Should not contain:

- generated experiment outputs
- temporary scratch notes

### 6.2 `raw/`

Purpose:

- immutable or near-immutable source assets local to this repository

Recommended first use:

- store the downloaded raw dataset file or source reference notes if needed

Rules:

- raw files should not be manually edited
- transformed tables should not live here

### 6.3 `data/`

Purpose:

- project-owned working data area
- outputs from preparation and preprocessing
- DVC-tracked dataset references

Suggested internal layout once created:

```text
data/
├── external/
├── interim/
└── processed/
```

Interpretation:

- `external/`: dataset copies or imported source files used by the project
- `interim/`: cleaned but not final modeling tables
- `processed/`: model-ready datasets

Rules:

- do not mix handwritten documentation with data files
- do not commit large data files outside the intended DVC path

### 6.4 `src/`

Purpose:

- application and pipeline source code

Suggested internal layout for the minimum version:

```text
src/
└── purchase_propensity/
    ├── __init__.py
    ├── config.py
    ├── data.py
    ├── features.py
    ├── train.py
    ├── evaluate.py
    └── pipelines/
```

Module responsibilities:

- `config.py`: runtime settings and path resolution
- `data.py`: dataset loading and schema validation
- `features.py`: preprocessing and feature handling
- `train.py`: model training entry logic
- `evaluate.py`: offline metrics and evaluation logic
- `pipelines/`: orchestration helpers if needed

Rules:

- avoid placing notebooks or ad hoc scripts inside `src/`
- avoid creating deep package trees before there is real need

### 6.5 `tests/`

Purpose:

- automated validation for critical project logic

Minimum expectation:

- basic tests for data loading
- basic tests for preprocessing
- at least one smoke test for training pipeline logic if feasible

Suggested initial layout:

```text
tests/
├── test_data.py
├── test_features.py
└── test_train.py
```

### 6.6 `configs/`

Purpose:

- static project configuration files

Expected early uses:

- training parameters
- split configuration
- feature toggles

Suggested initial contents:

- `base.yaml`
- optional `train.yaml`

Rules:

- configs should hold project settings, not secrets
- secrets belong in `.env`

### 6.7 `scripts/`

Purpose:

- thin executable wrappers for repeated project tasks

Good early uses:

- dataset fetch or copy helper
- preprocessing runner
- training runner

Rules:

- scripts should be small wrappers, not the main business logic
- core logic should live under `src/`

## 7. Minimum Required Root Files

### 7.1 `pyproject.toml`

Required because:

- the project needs a defined Python environment
- the challenge expects modern dependency management

Minimum role:

- declare project metadata
- declare runtime dependencies
- declare dev dependencies

This file is mandatory because the minimum startup contract depends on `Poetry`.

### 7.2 `.env.example`

Required because:

- the project should externalize runtime settings early

Typical variables may include:

- data paths
- MLflow tracking URI
- model output path

### 7.3 `.gitignore`

Required because:

- the project will generate environments, caches, model artifacts, and data outputs

### 7.4 `.dockerignore`

Required because:

- Docker is part of the expected engineering flow

### 7.5 `README.md`

Required because:

- the repository must explain how to run and review the project

### 7.6 `Makefile`

Required because:

- the minimum project structure must be initializable through `make`;
- the repository should expose a short, ergonomic entrypoint for common development actions;
- `Makefile` is the expected orchestration layer above `Poetry`.

Minimum role:

- expose startup-oriented targets such as environment install and project bootstrap;
- delegate Python execution to `Poetry`;
- remain thin and orchestration-focused.

## 8. DVC Readiness Requirements

The structure should be ready for DVC from the start even if `dvc.yaml` is added later.

This means:

- the project should have a clear place for raw and processed data
- preprocessing and training entrypoints should be separable
- scripts and source layout should map naturally to DVC stages

Minimal future DVC stage mapping:

- `prepare`
- `preprocess`
- `train`

## 8.1 Minimum startup contract

Before broader implementation begins, the repository should be able to initialize correctly through a `Makefile` plus `Poetry`.

The minimum accepted startup path is:

1. install dependencies with `Poetry`
2. expose that flow through `make`
3. provide documented commands in the README

At this stage, the project does not need full training, DVC, MLflow, or Docker integration yet.
It does need a clean and working bootstrap path.

## 9. MLflow Readiness Requirements

The structure should make MLflow easy to add without refactoring the repository.

This means:

- training code should be isolated
- evaluation code should be isolated
- configs should be external
- artifact paths should be explicit

## 10. What Should Not Be Added Yet

Do not add the following before there is a concrete need:

- microservice layers
- API folders
- frontend folders
- notebook-heavy architecture inside the repo root
- multiple model families
- advanced package nesting
- deployment-specific infrastructure beyond what the challenge actually needs

## 11. First Scaffolding Pass

A compliant first scaffolding pass should create:

- `src/`
- `tests/`
- `configs/`
- `scripts/`
- `data/`
- root config files
- `Makefile`

It does **not** need to create:

- full Docker setup
- full DVC pipeline
- full MLflow integration

Those come after the structure is in place.

## 12. Acceptance Criteria

The minimum structure is accepted when:

- each top-level folder has a clear purpose
- root files support environment and reproducibility
- the project can be initialized correctly through `make` using `Poetry`
- source code has a single obvious home
- tests have a single obvious home
- data flow can evolve into DVC stages without reorganization
- documentation and decisions are easy to find

## 13. Recommended Next Action

After approving this structure specification, the next implementation step should be:

1. scaffold the folders and root files
2. define the package name under `src/`
3. create the initial dataset loading and training entrypoints
