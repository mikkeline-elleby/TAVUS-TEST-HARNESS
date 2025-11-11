# Tavus Test Harness

Minimal harness for creating personas and conversations against the Tavus API using config files plus a small helper script set.

## 1) Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Populate `TAVUS_API_KEY` in `.env`.

## 2) Sync policies & run a sample

Upsert objectives and guardrails defined under `presets/` then create the sample persona and a conversation:

```bash
source .venv/bin/activate
python bin/sync_policies.py
bin/tune.sh persona --config configs/persona/facilitator.example.json
bin/tune.sh conversation --config configs/conversation/facilitator_kickoff.json
```

Persona config uses `objectives_name` and `guardrails_name`; IDs are resolved automatically.

## 3) Webhook (optional)

To receive live events:

Terminal A:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Terminal B (tunnel + persist):
```bash
ngrok http 8000
bin/set_webhook_url.sh "https://<your-ngrok>.ngrok-free.app/tavus/callback"
```

Terminal C (create conversation):
```bash
bin/tune.sh conversation --config configs/conversation/facilitator_kickoff.json
```

`bin/set_webhook_url.sh` writes `WEBHOOK_URL` into `.env`. Run it after the tunnel is up.

## 4) Utilities

```bash
bin/demo.sh            # quick end‑to‑end demo
bin/clean_logs.sh      # prune old logs (keeps 7 days by default)
```

Webhook payloads are stored under `webhook/` (ignored by git). API request/response logs live under `logs/` categorized into subfolders.

## 5) Editing flow recap
1. Adjust presets (objectives, guardrails, layers, tools).
2. `python bin/sync_policies.py` to upsert changes.
3. Update persona config, then run persona & conversation commands.

See `presets/README.md` and `configs/README.md` for detailed schema guidance.


