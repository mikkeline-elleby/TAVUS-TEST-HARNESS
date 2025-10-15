#!/usr/bin/env python3
"""
Minimal local webhook receiver for Tavus callbacks.
- Uses Python standard library only (no Flask needed)
- By default listens on 0.0.0.0:8080 and accepts POSTs to /tavus/callback
- Logs request headers and JSON body to stdout and to logs/<timestamp>_webhook/

Usage:
  python bin/webhook_server.py --port 8080 --path /tavus/callback

In another terminal, set your callback URL accordingly:
  export WEBHOOK_URL="http://<your-host-or-ngrok>:8080/tavus/callback"

Tip: For local development exposing to Tavus cloud, use a tunneling tool (ngrok, Cloudflare Tunnel, etc.)
  ngrok http 8080
  export WEBHOOK_URL="https://<ngrok-subdomain>.ngrok.io/tavus/callback"
"""

import argparse
import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from pathlib import Path

LOGS_DIR = Path("logs")


def now_slug():
    return time.strftime("%Y%m%d-%H%M%S")


class TavusWebhookHandler(BaseHTTPRequestHandler):
    server_version = "TavusWebhook/1.0"

    def do_POST(self):
        parsed = urlparse(self.path)
        # Optionally restrict to a specific path if provided via server config
        allowed_path = getattr(self.server, "allowed_path", None)
        if allowed_path and parsed.path != allowed_path:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        length = int(self.headers.get('Content-Length', '0'))
        raw = self.rfile.read(length) if length > 0 else b""
        try:
            body = json.loads(raw.decode('utf-8') or '{}')
        except Exception:
            body = {"_raw": raw.decode('utf-8', errors='replace')}

        # Persist to logs
        run_dir = LOGS_DIR / f"{now_slug()}_webhook"
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "headers.json").write_text(json.dumps({k: v for k, v in self.headers.items()}, indent=2))
        (run_dir / "body.json").write_text(json.dumps(body, indent=2))
        (run_dir / "meta.json").write_text(json.dumps({
            "path": parsed.path,
            "client": self.client_address[0],
        }, indent=2))

        # Print to console as well
        print("\n[Webhook] POST", parsed.path)
        print(json.dumps(body, indent=2))

        # Respond OK
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b"{\n  \"ok\": true\n}")

    def log_message(self, fmt, *args):
        # Quieter logs (avoid double-printing request line)
        pass


def main():
    ap = argparse.ArgumentParser(description="Run a minimal webhook receiver for Tavus callbacks")
    ap.add_argument("--host", default="0.0.0.0", help="Host/IP to bind")
    ap.add_argument("--port", type=int, default=8080, help="Port to bind")
    ap.add_argument("--path", default="/tavus/callback", help="Path to accept posts on")
    args = ap.parse_args()

    httpd = HTTPServer((args.host, args.port), TavusWebhookHandler)
    # Stash allowed path on server instance
    setattr(httpd, "allowed_path", args.path)

    print(f"Webhook listening on http://{args.host}:{args.port}{args.path}")
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
