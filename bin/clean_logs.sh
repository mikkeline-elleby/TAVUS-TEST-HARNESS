#!/usr/bin/env bash
set -euo pipefail
# Delete old log runs under logs/ with optional retention and dry-run.
# Usage:
#   bin/clean_logs.sh            # delete logs older than 7 days
#   bin/clean_logs.sh --days 3   # delete logs older than 3 days
#   bin/clean_logs.sh --days 14 --dry-run

DAYS=7
DRY=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --days)
      shift
      DAYS=${1:-7}
      ;;
    --dry-run)
      DRY=true
      ;;
  esac
  shift || true
done

if [[ ! -d logs ]]; then
  echo "No logs/ directory; nothing to clean."
  exit 0
fi

if [[ "$DAYS" == "0" ]]; then
  echo "--days 0 specified: selecting ALL log runs under logs/."
  mapfile -t TARGETS < <(find logs -mindepth 1 -maxdepth 1 -type d -printf '%P\n' | grep -E '_persona_|_conversation_' || true)
else
  # Find top-level run folders older than $DAYS days (format: YYYYMMDD-..._persona_* or *_conversation_*)
  mapfile -t TARGETS < <(find logs -mindepth 1 -maxdepth 1 -type d -mtime +"$DAYS" -printf '%P\n' | grep -E '_persona_|_conversation_' || true)
fi

if [[ ${#TARGETS[@]} -eq 0 ]]; then
  echo "No logs older than $DAYS days."
  exit 0
fi

echo "Will remove ${#TARGETS[@]} log runs older than $DAYS days:"
printf ' - %s\n' "${TARGETS[@]}"

if $DRY; then
  echo "Dry run: nothing deleted."
  exit 0
fi

for d in "${TARGETS[@]}"; do
  rm -rf "logs/$d"
done

echo "Done."
