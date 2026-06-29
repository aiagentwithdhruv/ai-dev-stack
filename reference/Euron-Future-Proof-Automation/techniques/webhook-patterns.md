# Webhook Patterns — Event-Driven Automation

> **Applies to:** any automation that needs real-time triggers.

## Problem
Most automations need to react to events in real time: form submission, payment received, email
arrived, CRM status changed. Polling is wasteful. Webhooks are instant.

## Pattern: Universal Webhook Architecture

```
External Event --> Webhook URL (your endpoint)
  --> Validate (signature, schema)
    --> Route (classify event type)
      --> Process (run the right tool/workflow)
        --> Respond (acknowledge within timeout)
          --> Log (run log for observability)
```

## Key Rules

1. **Always respond fast** — webhook senders expect a 200 within 5-30 seconds. Do heavy
   processing AFTER responding.
2. **Validate signatures** — most services sign webhooks (HMAC-SHA256). Always verify.
3. **Idempotency** — webhooks can be sent multiple times. Use an event ID to deduplicate.
4. **Queue heavy work** — receive webhook → acknowledge → push to queue → process async.
5. **Log everything** — webhook payloads are your debug trail. Log them (with secrets masked).

## Implementation Patterns

### Pattern A: Serverless function (free, instant)
```python
# api/webhook.py — serverless function handler
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        # validate signature, process event
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True}).encode())
```

### Pattern B: FastAPI (local or VPS)
```python
@app.post("/webhook/{service}")
async def receive_webhook(service: str, request: Request):
    body = await request.json()
    # validate signature -> route to handler -> process async (background task)
    return {"status": "received"}
```

### Pattern C: Visual workflow engine (e.g. n8n)
- Create a Webhook node → get URL → paste into the external service.
- The engine handles routing, processing, and error handling.

## For Development: Local Tunnels
```bash
cloudflared tunnel --url http://localhost:8000   # Cloudflare Tunnel (free, stable)
ngrok http 8000                                  # ngrok (free, quick)
```

## Gotchas
- **Timeout kills:** if processing takes >30s the sender assumes failure and retries. Process async.
- **No HTTPS = rejected:** most services require HTTPS. Tunnels handle this automatically.
- **Rate limits:** some services batch events or rate-limit webhook calls. Handle bursts.
- **Replay attacks:** old webhooks resent maliciously. Check timestamp + signature.

## Related
- `deployment-patterns.md` — where to host webhook endpoints
- `../agent-safety-harness/sanitize.py` — sanitise inbound payloads before tools touch them
