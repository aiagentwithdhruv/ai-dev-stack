# Customizing a Self-Hosted Agent + Example Configs

How to change the agent's name, personality, skills, channels, memory, and heartbeat — plus three
ready-to-adapt JSON config examples. (Config keys here mirror OpenClaw's `openclaw.json`; the
concepts transfer to any similar self-hosted agent.)

## Quick customization map

| What | Where | Time |
|------|-------|------|
| Name | Dashboard → Config → Agent Name | 30s |
| Personality | Dashboard → Config → System Prompt | 2m |
| Skills | Dashboard → Skills | 5m |
| Model | Dashboard → Config → Models | 1m |
| Channels | `configure --section channels` | 5m |
| Memory/heartbeat | Dashboard → Config | 2m |

## 1. Rename the agent
Dashboard → **Config → Agent Name** (under `agents.defaults`). Or edit the config file directly:
```bash
python3 -c "
import json, os
p = os.path.expanduser('~/.openclaw/openclaw.json')
c = json.load(open(p))
c['agents']['defaults']['name'] = 'YOUR_AGENT_NAME'
json.dump(c, open(p,'w'), indent=2)
"
chown -R 1000:1000 ~/.openclaw
docker compose down && docker compose up -d openclaw-gateway
```

## 2. Set the personality (system prompt)
The system prompt defines tone and behavior. A good one covers:
1. **Identity** — who/what role, 2. **Tone** — formal/casual/technical, 3. **Rules** — always/never,
4. **Context** — what it knows about you, 5. **Format** — how to structure replies.
```
You are [NAME], [ROLE].

## How You Communicate
- [tone, language, emoji policy]

## What You Know About Me
- [profession, goals, preferences]

## Rules
- Always: [...]
- Never: [...]

## Response Format
- [structure, length, when to ask clarifying questions]
```
See `agent-persona-prompts.md` for six full templates.

## 3. Skills
List / toggle skills in **Dashboard → Skills** (web browse, code execute, file manage, GitHub,
calendar, drive, memory, …). Some need their own API key. Remove one via config:
```bash
python3 -c "
import json, os
p = os.path.expanduser('~/.openclaw/openclaw.json')
c = json.load(open(p))
c.get('skills',{}).get('installed',{}).pop('SKILL_NAME', None)
json.dump(c, open(p,'w'), indent=2)
"
chown -R 1000:1000 ~/.openclaw && docker compose down && docker compose up -d openclaw-gateway
```

## 4. Channels & DM policy
```bash
docker compose run --rm openclaw-cli configure --section channels
```
Channels: Telegram (easiest), WhatsApp (QR), Discord, Slack, iMessage (Mac), Web.
**DM policy:** `open` (anyone — fine for a private personal bot), `pairing` (approve users first —
use for shared bots), `closed` (pre-configured users only).

## 5. Memory
| Setting | Recommended | Effect |
|---------|-------------|--------|
| `memorySearch.provider` | `local` | No embedding-API cost |
| `memorySearch.enabled` | `true` | Memory recall on |
| `memory.maxEntries` | `500`–`1000` | Cap stored memories |

Tell the agent what to remember via the system prompt ("save important facts/decisions; check
memory before answering preference questions"). You can also pre-seed a workspace file:
```bash
cat > ~/.openclaw/workspace/ABOUT-ME.md << 'EOF'
# About My Owner
- Name / Timezone / Work / Communication preferences / Current projects
EOF
chown -R 1000:1000 ~/.openclaw
```
Then: "Read ABOUT-ME.md in your workspace and remember it."

## 6. Heartbeat (proactive wake-ups)
Dashboard → **Config → Heartbeat**: set **Every = `6h`** (free-tier friendly) and your **Timezone**.
An optional heartbeat prompt runs each tick, e.g. "Summarize today's calendar + important emails,"
or "Remind me of anything due/overdue."

## 7. Multiple agents on one host
Run separate configs/ports for, say, a personal and a work agent:
```bash
OPENCLAW_CONFIG_DIR=~/.agent-personal docker compose up -d   # port 18789
OPENCLAW_CONFIG_DIR=~/.agent-work     docker compose up -d   # port 18790
```
Each gets its own config, memory, workspace, and channels.

---

## Example configs

> These are **reference structures**, not drop-in files. Prefer the onboarding wizard to generate a
> valid config, then tweak in the dashboard. Replace every `YOUR_…` value. Never commit a real
> config — it holds API keys and tokens. After hand-editing: `chown -R 1000:1000 ~/.openclaw`.

### minimal.json — quickest start (one provider + Telegram)
```json
{
  "models": {
    "defaults": { "model": "moonshot/kimi-k2.5" },
    "providers": { "moonshot": { "auth": { "type": "key", "key": "YOUR_MOONSHOT_API_KEY" } } }
  },
  "channels": { "telegram": { "enabled": true, "botToken": "YOUR_TELEGRAM_BOT_TOKEN" } },
  "agents": { "defaults": { "name": "Assistant", "model": "moonshot/kimi-k2.5" } },
  "gateway": { "port": 18789, "bind": "loopback" },
  "heartbeat": { "enabled": true, "every": "6h", "timezone": "UTC" }
}
```

### personal-assistant.json — Telegram + WhatsApp, memory, 6h heartbeat
```json
{
  "models": {
    "defaults": { "model": "moonshot/kimi-k2.5" },
    "providers": { "moonshot": { "auth": { "type": "key", "key": "YOUR_MOONSHOT_API_KEY" } } }
  },
  "channels": {
    "telegram": { "enabled": true, "botToken": "YOUR_TELEGRAM_BOT_TOKEN" },
    "whatsapp": { "enabled": true, "type": "qr-link" }
  },
  "agents": {
    "defaults": {
      "name": "Aria",
      "model": "moonshot/kimi-k2.5",
      "systemPrompt": "You are Aria, a friendly and capable personal AI assistant. You help with daily tasks, answer questions, draft messages, and remember important information. You communicate clearly, use bullet points for lists, and always suggest next steps. You save important facts to memory automatically.",
      "imageModel": { "primary": "moonshot/kimi-k2.5" }
    }
  },
  "gateway": { "port": 18789, "bind": "loopback" },
  "heartbeat": { "enabled": true, "every": "6h", "timezone": "UTC" },
  "memory": { "enabled": true, "maxEntries": 500 },
  "memorySearch": { "enabled": true, "provider": "local" },
  "auth": { "profiles": { "moonshot:default": { "provider": "moonshot", "type": "key", "key": "YOUR_MOONSHOT_API_KEY" } } },
  "dmPolicy": "open"
}
```

### business-bot.json — professional tone, pairing DM policy
```json
{
  "models": {
    "defaults": { "model": "moonshot/kimi-k2.5" },
    "providers": { "moonshot": { "auth": { "type": "key", "key": "YOUR_MOONSHOT_API_KEY" } } }
  },
  "channels": {
    "telegram": { "enabled": true, "botToken": "YOUR_TELEGRAM_BOT_TOKEN" },
    "whatsapp": { "enabled": true, "type": "qr-link" }
  },
  "agents": {
    "defaults": {
      "name": "Atlas",
      "model": "moonshot/kimi-k2.5",
      "systemPrompt": "You are Atlas, a professional business AI assistant. You help manage clients, track projects, draft proposals, follow up on leads, and keep operations running smoothly. You communicate professionally, use structured formats (tables, bullets, headers), and prioritize revenue-generating activities. When making recommendations, evaluate by: revenue impact, time investment, scalability, and risk.",
      "imageModel": { "primary": "moonshot/kimi-k2.5" }
    }
  },
  "gateway": { "port": 18789, "bind": "loopback" },
  "heartbeat": { "enabled": true, "every": "4h", "timezone": "UTC" },
  "memory": { "enabled": true, "maxEntries": 1000 },
  "memorySearch": { "enabled": true, "provider": "local" },
  "auth": { "profiles": { "moonshot:default": { "provider": "moonshot", "type": "key", "key": "YOUR_MOONSHOT_API_KEY" } } },
  "dmPolicy": "pairing"
}
```

### Key settings, explained
| Setting | Does | Recommended |
|---------|------|-------------|
| `agents.defaults.name` | Display name | your choice |
| `agents.defaults.model` | Default LLM | a free model |
| `agents.defaults.systemPrompt` | Personality | see persona prompts |
| `gateway.bind` | Network binding | `loopback` (most secure) |
| `gateway.port` | Dashboard/API port | `18789` |
| `heartbeat.every` | Wake interval | `6h` (saves tokens) |
| `memorySearch.provider` | Memory search | `local` (no API cost) |
| `dmPolicy` | Who can DM | `open` (private) / `pairing` (shared) |
