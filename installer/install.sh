#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-python3}"
"$PYTHON" -m pip install --upgrade "$ROOT"
"$PYTHON" -m gene init
"$PYTHON" -m gene health
