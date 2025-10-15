#!/usr/bin/env bash
set -euo pipefail
# Usage examples:
#   bin/tune.sh persona --persona-name "Coach" --system-prompt "..." --default-replica-id r4317e64d25a
#   bin/tune.sh conversation --persona-id pe123 --name "Demo" --test-mode --context "..."

# Resolve Python interpreter
PY=${PYTHON:-}
if [[ -z "${PY}" ]]; then
  if [[ -x ".venv/bin/python" ]]; then
    PY=".venv/bin/python"
  elif command -v python3 >/dev/null 2>&1; then
    PY="$(command -v python3)"
  elif command -v python >/dev/null 2>&1; then
    PY="$(command -v python)"
  else
    echo "Python interpreter not found. Please install Python 3 and try again." >&2
    exit 1
  fi
fi

# Ensure required packages are available
if ! "$PY" -c "import requests, dotenv" >/dev/null 2>&1; then
  echo "Python packages missing (requests, python-dotenv). Install with:" >&2
  echo "  $PY -m pip install -r requirements.txt" >&2
  exit 1
fi

exec "$PY" tune.py "$@"
