#!/usr/bin/env bash
set -euo pipefail
# One-shot: create or update persona, wire persona_id into conversation config, then create conversation.
# Usage:
#   bin/scenarios/run_pair.sh <persona_config.json> <conversation_config.json> [--disable-test-mode] [--update-persona] [--persona-id pe_XXXX]

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <persona_config.json> <conversation_config.json> [--disable-test-mode] [--update-persona] [--persona-id pe_XXXX]" >&2
  exit 2
fi

PERSONA_CFG="$1"
CONVO_CFG="$2"
shift 2 || true

# Parse optional flags
UPDATE=false
DISABLE_TEST=false
EXPLICIT_PID=""
EXTRA_FLAGS=("${@:-}")
for ((i=0; i<${#EXTRA_FLAGS[@]}; i++)); do
  case "${EXTRA_FLAGS[$i]}" in
    --update-persona) UPDATE=true ;;
    --disable-test-mode) DISABLE_TEST=true ;;
    --persona-id)
      if (( i+1 < ${#EXTRA_FLAGS[@]} )); then
        EXPLICIT_PID="${EXTRA_FLAGS[$((i+1))]}"
      fi
      ;;
  esac
done

# Resolve bin directory
BIN_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

echo "[1/3] Creating/Updating persona from: $PERSONA_CFG"

# Build persona CLI args
PERSONA_ARGS=( persona --config "$PERSONA_CFG" )
if $UPDATE; then
  PERSONA_ARGS+=( --update )
  if [[ -n "$EXPLICIT_PID" ]]; then
    PERSONA_ARGS+=( --persona-id "$EXPLICIT_PID" )
  else
  # Try to derive persona_id or target name from config/logs without requiring jq
  PID_IN_CFG=$(python -c "import sys,json; from pathlib import Path;\n\
p=Path(sys.argv[1]);\n\
print(json.load(p.open()).get('persona_id','')) if p.exists() else print('')" "$PERSONA_CFG" 2>/dev/null || true)
  NAME_IN_CFG=$(python -c "import sys,json; from pathlib import Path;\n\
p=Path(sys.argv[1]);\n\
print(json.load(p.open()).get('persona_name','')) if p.exists() else print('')" "$PERSONA_CFG" 2>/dev/null || true)
    if [[ -n "$PID_IN_CFG" ]]; then
      PERSONA_ARGS+=( --persona-id "$PID_IN_CFG" )
    else
    PID_FROM_LOG=$(python -c "import glob, os, json;\n\
paths = glob.glob('logs/*_persona_*/response.json');\n\
paths.sort(key=lambda p: os.path.getmtime(p), reverse=True);\n\
pid='';\n\
for p in paths:\n\
  try:\n\
    d=json.load(open(p));\n\
    pid=d.get('persona_id') or d.get('id') or '';\n\
    if pid: break\n\
  except Exception: pass\n\
print(pid)" 2>/dev/null || true)
      if [[ -n "$PID_FROM_LOG" ]]; then
        PERSONA_ARGS+=( --persona-id "$PID_FROM_LOG" )
      fi
    fi
    # If still no ID, pass name for resolution in the CLI
    if ! printf '%s\n' "${PERSONA_ARGS[@]}" | grep -q -- '--persona-id'; then
      if [[ -n "$NAME_IN_CFG" ]]; then
        PERSONA_ARGS+=( --target-persona-name "$NAME_IN_CFG" )
      fi
    fi
  fi
fi

"$BIN_DIR/tune.sh" "${PERSONA_ARGS[@]}"

echo "[2/3] Injecting persona_id into: $CONVO_CFG"
SET_ARGS=( --config "$CONVO_CFG" --from-latest-log )
if $DISABLE_TEST; then
  SET_ARGS+=( --disable-test-mode )
fi
python "$BIN_DIR/set_persona_id.py" "${SET_ARGS[@]}"

echo "[3/3] Creating conversation from: $CONVO_CFG"
"$BIN_DIR/tune.sh" conversation --config "$CONVO_CFG"

# Try to print the last conversation URL if jq is available
if command -v jq >/dev/null 2>&1; then
  LATEST_RESP=$(ls -1t logs/*_conversation_create/response.json 2>/dev/null | head -n1 || true)
  if [[ -n "$LATEST_RESP" ]]; then
    URL=$(jq -r '.conversation_url // empty' "$LATEST_RESP" || true)
    if [[ -n "$URL" ]]; then
      echo "Conversation URL: $URL"
    fi
  fi
fi

echo "Done."
