#!/usr/bin/env bash
set -euo pipefail

poetry run python -m purchase_propensity.dataset_fetch "$@"
