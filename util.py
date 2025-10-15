
import os, json, time, pathlib, requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TAVUS_API_KEY")
if not API_KEY:
    raise SystemExit("Missing TAVUS_API_KEY in .env")

WEBHOOK_URL = os.getenv("WEBHOOK_URL") or None
PREFERRED_REPLICA = (os.getenv("TAVUS_REPLICA_ID") or "").strip()

PERSONA_ENDPOINT = os.getenv("PERSONA_ENDPOINT", "https://tavusapi.com/v2/personas")
CONVERSATION_ENDPOINT = os.getenv("CONVERSATION_ENDPOINT", "https://tavusapi.com/v2/conversations")
REPLICAS_ENDPOINT = os.getenv("REPLICAS_ENDPOINT", "https://tavusapi.com/v2/replicas")

H = {"x-api-key": API_KEY}

def now_slug():
    return time.strftime("%Y%m%d-%H%M%S")

def save_log(action: str, payload: Dict[str, Any], response: requests.Response, endpoint: str) -> pathlib.Path:
    run_dir = pathlib.Path("logs") / f"{now_slug()}_{action}"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "payload.json").write_text(json.dumps(payload, indent=2))
    try:
        (run_dir / "response.json").write_text(json.dumps(response.json(), indent=2))
    except Exception:
        (run_dir / "response.json").write_text(response.text)
    (run_dir / "meta.json").write_text(json.dumps({
        "endpoint": endpoint,
        "status_code": response.status_code,
        "headers": dict(response.headers),
    }, indent=2))
    return run_dir

def pretty_print_response(r: requests.Response):
    print("\nStatus:", r.status_code)
    try:
        print(json.dumps(r.json(), indent=2))
    except Exception:
        print(r.text)

def pick_replica(overridden: Optional[str] = None) -> str:
    if overridden and overridden.strip():
        return overridden.strip()
    if PREFERRED_REPLICA:
        return PREFERRED_REPLICA
    r = requests.get(REPLICAS_ENDPOINT, headers=H, timeout=30)
    if r.status_code != 200:
        raise SystemExit(f"Failed to list replicas: {r.status_code} {r.text}")
    data = r.json().get("data", [])
    completed = [d for d in data if str(d.get("status", "")).lower() == "completed"]
    if not completed:
        raise SystemExit("No completed replicas found. Create/train one in the Tavus dashboard first.")
    print(f"Auto-selected replica: {completed[0].get('replica_name')} ({completed[0].get('replica_id')})")
    return completed[0]["replica_id"]
