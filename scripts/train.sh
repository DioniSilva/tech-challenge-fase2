#!/usr/bin/env bash
set -euo pipefail

poetry run python -m purchase_propensity.train --config "${1:-configs/base.yaml}"
