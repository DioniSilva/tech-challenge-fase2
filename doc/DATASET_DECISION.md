# Dataset Decision

## Decision Summary

Decision date: `2026-07-23`

- Selected dataset: `Online Shoppers Purchasing Intention Dataset`
- Selected baseline: `LogisticRegression`
- Target column: `Revenue`
- Problem type: binary classification

## Why This Decision Was Made

This dataset is the most pragmatic fit for the current Tech Challenge because it matches the official requirements with minimal ambiguity.

It was selected because:

- it is explicitly aligned with the official Phase 02 PDF suggestions;
- it already represents an e-commerce browsing context;
- it already exposes a binary target (`Revenue`);
- it avoids turning the project into a target-engineering exercise too early;
- it supports a fast path toward reproducible ML Engineering evidence.

## Why Other Previously Explored Datasets Were Not Chosen

### RetailRocket

- Strong fit for recommendation and event-based interaction modeling.
- Weak fit for the current official challenge framing.
- Would push the project toward recommender-system design and derived targets.

### Instacart

- Strong technical benchmark for purchase-history modeling.
- Still not a natural purchase-propensity classification dataset.
- Better suited for recommendation or reorder-style problems.

### Olist

- Strong business context and richer relational signals.
- However, it requires deriving a clean binary target and defining the analysis grain carefully.
- Higher early-stage ambiguity than the chosen dataset.

### MovieLens

- Canonical for recommendation benchmarks.
- Misaligned with the current challenge framing.

## Baseline Rationale

`LogisticRegression` was chosen as the first baseline because it is:

- simple;
- interpretable;
- standard for tabular binary classification;
- easy to reproduce;
- sufficient for an engineering-first first milestone.

The goal of the baseline is not to maximize performance immediately. The goal is to establish a correct, reproducible, and documentable first version of the project.

## Implementation Consequences

This decision implies:

- the project should be structured around session-level binary classification;
- the first training pipeline should be built around `Revenue`;
- preprocessing should prioritize clarity and reproducibility;
- evaluation should use standard classification metrics;
- MLflow runs should compare future models against `LogisticRegression`.

## Source References

- Official challenge PDF: `learning/postech-FIAP/raw/fase-02/01-final_project.pdf`
- Project guidance: `./PROJECT_SPEC.md`
- Agent guidance: `../AGENTS.md`
