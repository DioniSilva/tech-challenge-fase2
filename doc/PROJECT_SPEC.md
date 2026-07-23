# Project Specification

## 1. Overview

This repository implements the FIAP Phase 02 Tech Challenge as a **binary classification** project focused on **purchase propensity prediction** from browsing behavior in an e-commerce scenario.

The main evaluation axis is **ML Engineering quality**, not modeling sophistication.

## 2. Source of Truth

Official requirements are defined by:

- `learning/postech-FIAP/raw/fase-02/01-final_project.pdf`

Supporting repository guidance:

- `./AGENTS.md`
- `./README.md`

If any document conflicts with the official PDF, the PDF wins.

## 3. Problem Statement

Predict whether a user has purchase propensity based on browsing-related signals.

This must be implemented as a **binary classification** problem with a clearly documented target definition.

## 4. Primary Goal

Deliver a reproducible ML project that demonstrates:

- clean and maintainable code;
- environment reproducibility;
- dataset versioning;
- experiment tracking;
- model registration;
- containerized execution;
- delivery-ready documentation.

## 5. Non-Goals

Unless explicitly requested later, this project should not be treated as:

- a recommendation system;
- a ranking or next-item prediction system;
- a PyTorch-first project;
- a neural network showcase;
- a research-heavy experimentation project.

## 6. Functional Scope

The project should support the following core flow:

1. dataset preparation
2. preprocessing
3. model training
4. model evaluation
5. MLflow logging
6. model registration

## 7. Dataset Requirements

The dataset should:

- be tabular;
- support binary classification;
- have at least `5,000` rows;
- preferably represent customer behavior, purchase intent, or churn-like patterns.

Examples explicitly aligned with the PDF:

- Online Shoppers Purchasing Intention Dataset
- Customer Churn style datasets

### Current decision

- Selected dataset: `Online Shoppers Purchasing Intention Dataset`
- Dataset source: UCI Machine Learning Repository
- Unit of analysis: browsing session
- Target column: `Revenue`
- Reason for selection:
  - explicit fit with the official challenge wording
  - native binary classification target
  - e-commerce browsing context
  - lower implementation ambiguity than deriving a target from recommendation-oriented datasets

## 8. Modeling Requirements

### Required direction

- Classical ML classifier
- `scikit-learn` as the default modeling stack

### Safe initial model choices

- Logistic Regression
- Random Forest
- Gradient Boosting / XGBoost if justified

### Current baseline decision

- Baseline model: `LogisticRegression`
- Role: first compliant and reproducible benchmark
- Rationale:
  - simple to implement and explain
  - strong baseline for tabular binary classification
  - low engineering overhead
  - appropriate for the challenge focus on ML Engineering

### Minimum modeling expectations

- target clearly defined
- train/validation/test logic documented
- evaluation metrics logged
- final model artifact tracked

## 9. Engineering Requirements

### Code organization

Preferred repository structure:

```text
src/
tests/
data/
models/
configs/
scripts/
doc/
```

### Packaging and environment

- `pyproject.toml` as the main package manifest
- prefer `Poetry` as the primary path
- lock file committed
- `.env.example` provided

### Reproducibility

- project installable from scratch
- commands documented in README
- deterministic behavior where applicable through fixed seeds

## 10. DVC Requirements

The repository should include a real DVC pipeline.

A valid minimal first version is:

- `preprocess -> train`

Expanded versions may include:

- `prepare -> preprocess -> train -> evaluate`

Minimum evidence:

- `dvc.yaml`
- versioned dataset references
- reproducible pipeline execution path

## 11. MLflow Requirements

The project should use MLflow to:

- log parameters
- log metrics
- log artifacts
- log the final model
- register the best model in Model Registry

Minimum evidence:

- tracked runs
- saved metrics
- registered model entry

## 12. Docker Requirements

The project should include:

- `Dockerfile`
- `.dockerignore`
- documented container execution path

The Docker setup must be sufficient to run the main project flow reproducibly.

## 13. Documentation Requirements

The repository documentation should explain:

- project goal
- source of truth
- dataset choice
- target definition
- environment setup
- training flow
- DVC flow
- MLflow usage
- reproducibility steps

## 14. Mandatory Deliverables

- GitHub repository
- 5-minute STAR video

The repository should contain enough evidence to support the final presentation without relying on undocumented manual steps.

## 15. Acceptance Criteria

The project is considered structurally aligned when it provides evidence for:

- binary classification framing
- dataset and target definition
- installable environment
- reproducible ML pipeline
- tracked experiments in MLflow
- registered model
- Dockerized execution
- readable project documentation

## 16. Current Open Decisions

At the time this specification was created, the following items are still open:

- target definition details beyond `Revenue`
- exact feature set and preprocessing policy
- exact DVC stage breakdown
- final directory layout details

These decisions should be resolved in a way that minimizes implementation risk while preserving full compliance with the official challenge.
