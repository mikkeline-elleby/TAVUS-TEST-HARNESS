#!/usr/bin/env python3
"""
Set persona_id in a conversation config file.

Usage examples:
  python bin/set_persona_id.py --config configs/conversation/coach_intro.json --from-latest-log --disable-test-mode
  python bin/set_persona_id.py --config configs/conversation/coach_intro.json --persona-id pe123

This script reads the latest persona create log (or a provided persona-id),
updates the conversation config's persona_id, clears replica_id, and can
optionally disable test_mode.
"""

import argparse, json, sys
from pathlib import Path


def find_latest_persona_id() -> str | None:
    logs_dir = Path("logs")
    if not logs_dir.exists():
        return None
    # Look for both create and update responses, most recent first
    patterns = ["*_persona_create/response.json", "*_persona_update/response.json"]
    candidates = []
    for pat in patterns:
        candidates.extend(logs_dir.glob(pat))
    candidates = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)
    for f in candidates:
        try:
            data = json.loads(f.read_text())
            pid = data.get("persona_id") or data.get("id")
            if pid:
                return pid
        except Exception:
            continue
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Set persona_id in a conversation config JSON")
    ap.add_argument("--config", required=True, help="Path to conversation JSON (e.g., configs/conversation/coach_intro.json)")
    ap.add_argument("--persona-id", help="Persona ID to set; if omitted, use --from-latest-log")
    ap.add_argument("--from-latest-log", action="store_true", help="Pull persona_id from latest logs/*_persona_create/response.json")
    ap.add_argument("--disable-test-mode", action="store_true", help="Set test_mode to false in the config")
    args = ap.parse_args()

    pid = args.persona_id
    if not pid and args.from_latest_log:
        pid = find_latest_persona_id()
    if not pid:
        print("persona_id not provided and cannot be found from logs. Use --persona-id or --from-latest-log.", file=sys.stderr)
        return 1

    cfg_path = Path(args.config)
    if not cfg_path.exists():
        print(f"Config not found: {cfg_path}", file=sys.stderr)
        return 1
    try:
        cfg = json.loads(cfg_path.read_text())
    except Exception as e:
        print(f"Config is not valid JSON: {e}", file=sys.stderr)
        return 1

    cfg["persona_id"] = pid
    if "replica_id" in cfg:
        cfg["replica_id"] = ""
    if args.disable_test_mode:
        cfg["test_mode"] = False

    cfg_path.write_text(json.dumps(cfg, indent=4))
    print(f"Updated {cfg_path}: persona_id={pid}, test_mode={cfg.get('test_mode')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
