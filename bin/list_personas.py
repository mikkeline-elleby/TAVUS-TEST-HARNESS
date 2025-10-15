#!/usr/bin/env python3
"""
List Tavus personas with optional filtering.

Usage:
  python bin/list_personas.py                # table output
  python bin/list_personas.py --grep Coach   # filter by name contains 'Coach'
  python bin/list_personas.py --json         # raw JSON output
"""

import argparse, json
from typing import List, Dict, Any
import requests
from util import H, PERSONA_ENDPOINT


def fetch_personas() -> List[Dict[str, Any]]:
    r = requests.get(PERSONA_ENDPOINT, headers=H, timeout=60)
    if r.status_code != 200:
        raise SystemExit(f"Failed to list personas: {r.status_code} {r.text}")
    data = r.json()
    if isinstance(data, dict) and isinstance(data.get("data"), list):
        return data["data"]
    if isinstance(data, list):
        return data
    # Unknown shape
    return []


def main():
    ap = argparse.ArgumentParser(description="List personas")
    ap.add_argument("--grep", help="Filter persona_name contains", default="")
    ap.add_argument("--json", action="store_true", help="Print raw JSON")
    args = ap.parse_args()

    items = fetch_personas()
    if args.grep:
        q = args.grep.lower()
        items = [x for x in items if q in str(x.get("persona_name", "")).lower()]
    if args.json:
        print(json.dumps(items, indent=2))
        return

    # Table view
    rows = []
    for it in items:
        pid = it.get("persona_id") or it.get("id") or ""
        name = it.get("persona_name", "")
        updated = it.get("updated_at") or it.get("created_at") or ""
        rows.append((pid, name, updated))
    # Column widths
    w_pid = max([len(r[0]) for r in rows] + [10])
    w_name = max([len(r[1]) for r in rows] + [12])
    header = f"{'persona_id'.ljust(w_pid)}  {'persona_name'.ljust(w_name)}  updated_at"
    print(header)
    print("-" * len(header))
    for pid, name, updated in rows:
        print(f"{pid.ljust(w_pid)}  {name.ljust(w_name)}  {updated}")


if __name__ == "__main__":
    main()
