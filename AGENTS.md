---
title: Agents - Tech Challenge Phase 02
status: active
language: en
---

# Agents - Tech Challenge Phase 02

Use this file as the agent contract for `repos/tech-challenges/tech-challenge-fase-2`.

This project is for the FIAP Phase 02 Tech Challenge. The current official requirements are defined by the PDF stored at:

- `learning/postech-FIAP/raw/fase-02/01-final_project.pdf`

If any older note, notebook, or decision conflicts with that PDF, the PDF wins.

## Project Goal

Build a predictive Machine Learning system to estimate a user's purchase propensity from browsing behavior in an e-commerce context.

This challenge is primarily about **ML Engineering**, not about advanced modeling.

## What The Project Is

- A binary classification project.
- A reproducible ML pipeline project.
- A Docker, DVC, and MLflow project.
- A code quality and delivery discipline project.

## What The Project Is Not

- Not a recommendation system project.
- Not a PyTorch project by default.
- Not a neural network project by default.
- Not a research-heavy modeling challenge.

Do not steer the repo toward embeddings, ranking, next-item recommendation, or recommender-specific metrics unless the user explicitly asks for an exploratory side path.

## Source Of Truth

Read sources in this order:

1. `learning/postech-FIAP/raw/fase-02/01-final_project.pdf`
2. `learning/postech-FIAP/curadoria/fase-02-containers-e-ambientes-reprodutiveis/Tech Challenge - Fase 02.md`
3. `learning/postech-FIAP/curadoria/fase-02-containers-e-ambientes-reprodutiveis/estudos/Checklist de evidências - Tech Challenge Fase 02.md`
4. Files already present in this repository

When sources disagree, prefer the highest item in the list.

## Expected Technical Direction

Prefer the simplest solution that satisfies the official requirements.

### Modeling

- Use a classical classifier with `scikit-learn`.
- Safe starting options: Logistic Regression, Random Forest, or XGBoost if justified.
- The first milestone is a working baseline, not model sophistication.
- Keep the target explicitly binary and document its semantics.
- Current baseline decision: `LogisticRegression`.

### Dataset

- Prefer a tabular binary classification dataset with at least `5,000` rows.
- The PDF explicitly suggests purchase-intent or churn-like datasets.
- Current dataset decision: `Online Shoppers Purchasing Intention Dataset`.
- Current target decision: `Revenue`.
- Why this dataset was selected:
  - explicitly aligned with the official PDF suggestions
  - native binary target
  - e-commerce browsing session framing
  - low setup ambiguity for an ML Engineering-first challenge

Do not assume that previously explored recommendation datasets are still valid for the main implementation path.

### Environment And Packaging

- Prefer `Poetry` as the primary packaging path.
- Keep `pyproject.toml` authoritative.
- Commit the lock file.
- Separate production and development dependencies.
- Use `.env` and provide `.env.example`.

### Reproducibility

- The repo should be installable from scratch.
- Docker should run the project consistently.
- DVC should track data and orchestrate the core pipeline.
- MLflow should track experiments and register the best model.

## Delivery Expectations

The mandatory deliverables are:

- GitHub repository
- 5-minute STAR video

The repo should contain enough evidence to support the video without manual reconstruction.

## Engineering Standards

### Code Quality

- Prefer small, readable modules.
- Use descriptive names.
- Add type hints to main public functions.
- Keep responsibilities separated.
- Use either OOP or functional structure intentionally; do not mix styles carelessly.

### Repository Structure

Use a structure close to:

- `src/`
- `tests/`
- `data/`
- `models/`
- `configs/`
- `scripts/`

Adjust only when there is a clear technical reason.

### Documentation

- The README must explain setup, data, training, tracking, and reproduction.
- Document assumptions, dataset choice, target definition, and pipeline steps.
- Prefer explicit commands over narrative-only descriptions.

## Pipeline Expectations

The implementation should converge toward a minimal end-to-end flow such as:

1. data acquisition or preparation
2. preprocessing
3. training
4. evaluation
5. MLflow logging
6. model registration

For DVC, a smaller initial pipeline is acceptable if it is real and reproducible.

## MLflow Expectations

- Log parameters
- Log metrics
- Log artifacts
- Log the final model
- Register the best model in Model Registry

Prefer a small number of honest, reproducible runs over many shallow runs.

## Agent Behavior Rules

- Build the smallest compliant version first.
- Do not introduce extra architecture before the repo needs it.
- Do not overfit to hypothetical future scale.
- Do not invent requirements that are not in the official PDF.
- Do not redirect the project into recommender-system design.
- When in doubt, privilege reproducibility and clarity over cleverness.

## Evidence Checklist For Agents

Before claiming the project is in good shape, verify that the repo contains evidence for:

- binary classification framing
- dataset choice and target definition
- baseline model choice
- `pyproject.toml` and lock file
- `.env.example`
- Dockerfile
- DVC pipeline
- MLflow tracking
- model registry usage
- reproducible README instructions

## Preferred Execution Order

If the repository is still early-stage, agents should usually work in this order:

1. document the dataset and target
2. define the feature/target schema
3. scaffold the project structure
4. configure packaging and environment
5. implement preprocessing and training
6. add DVC stages
7. add MLflow tracking and registry
8. containerize
9. finalize README and delivery evidence

## Communication Rule

When summarizing progress, explain the repo in terms of challenge evidence:

- what requirement is being addressed
- what artifact in the repo proves it
- what is still missing
