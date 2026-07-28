#!/usr/bin/env bash
set -euo pipefail

poetry run python -m purchase_propensity.prepare --config "${1:-configs/base.yaml}"
