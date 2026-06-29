# Self-Host an Always-On Messaging AI Agent (VPS or Local)

A generic runbook for deploying a Docker-based, self-hosted AI agent (e.g. [OpenClaw](https://github.com/openclaw/openclaw))
that you reach through everyday chat apps — Telegram, WhatsApp, Discord, Slack, iMessage. Runs 24/7
on a small VPS (or locally), keeps persistent memory, and can use free LLM providers.

## System requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 1 vCPU | 2+ vCPU |
| RAM | 2 GB | 4+ GB |
| Disk | 10 GB | 20+ GB |
| OS | Ubuntu 22.04+ | Ubuntu 24.04 LTS |
| Docker | Required | Latest + compose plugin |

**Cost:** ~$5–15/month for the VPS; $0 for the LLM if you use a free provider (see
`free-llm-providers.md`). Run locally and the VPS cost is $0 too — but it's only "on" when your
machine is.

| | Local | VPS |
|---|---|---|
| Always on | Only when your computer is on | 24/7 |
| Cost | $0 | ~$5–15/mo |
| Best for | Testing, personal use | Production, demos, sharing |

---

## VPS install (Ubuntu 24.04)

### 0. Get a VPS
Any provider works (Hostinger, DigitalOcean, Hetzner, Vultr, etc.). Pick **Ubuntu 24.04 LTS**.
Note the server's **IP address** and root password / SSH key.

### 1. Connect
```bash
ssh root@YOUR_VPS_IP
```
(Most providers also offer a browser-based web terminal if SSH feels intimidating.)

### 2. Update the system
```bash
sudo apt update && sudo apt upgrade -y
```
If it reports a **pending kernel upgrade**, `reboot`, wait ~60s, and reconnect.

### 3. Install Docker + compose plugin
```bash
docker --version || curl -fsSL https://get.docker.com | sh
apt install docker-compose-plugin -y
docker --version && docker compose version   # both should print versions
```

### 4. Get the agent
```bash
cd ~
git clone https://github.com/openclaw/openclaw.git
cd openclaw
```

### 5. Run the setup wizard
```bash
./docker-setup.sh
```
This builds the image, runs onboarding, and generates security tokens. Typical wizard choices:

- Risk/security acknowledgement → **Yes**
- Onboarding mode → **QuickStart**
- Model provider → a free provider such as **Moonshot AI (Kimi K2.5)** (needs an API key)
- Default model → keep the provider's default
- Channel → **Telegram (Bot API)** is the easiest to start with
- Optional API keys (Places, etc.) → **No** for now, add later
- Configure skills → **Yes** (some may fail; that's fine)

### 6. Create a Telegram bot (if using Telegram)
1. Message **@BotFather** on Telegram → `/newbot`
2. Pick a name and a username ending in `bot`
3. Copy the bot token (`1234567890:ABC…`) and paste it when the wizard asks.

### 7. Fix permissions (the #1 cause of crashes)
The container runs as UID 1000 (`node`), but files get created as `root`. Always run:
```bash
chown -R 1000:1000 /root/.openclaw
```
Run this **every time** you hand-edit files under `~/.openclaw/`.

### 8. Start it
```bash
docker compose up -d openclaw-gateway
docker compose ps        # STATUS should be "Up …"
```
If you see `address already in use`:
```bash
fuser -k 18789/tcp && fuser -k 18790/tcp && sleep 2
docker compose up -d openclaw-gateway
```

### 9. Test
Message your bot **"Hello"** on Telegram. Give it ~30s. No reply? Check logs:
```bash
docker compose logs --tail 20 openclaw-gateway
```

### 10. Open the dashboard (web config UI)
The dashboard requires a secure context (HTTPS or localhost). From your **local** machine, tunnel it:
```bash
ssh -N -L 18789:127.0.0.1:18789 root@YOUR_VPS_IP   # keep this terminal open
```
Then browse `http://localhost:18789`. Find the token:
```bash
cat ~/openclaw/.env | grep OPENCLAW_GATEWAY_TOKEN
# URL form: http://localhost:18789/#token=YOUR_TOKEN
```

### 11. Add WhatsApp (optional)
```bash
docker compose run --rm openclaw-cli configure --section channels
# pick WhatsApp (QR link); scan the QR from WhatsApp > Settings > Linked Devices
docker compose down && fuser -k 18789/tcp && sleep 2 && docker compose up -d openclaw-gateway
```

### 12. Tune the heartbeat (save tokens)
The heartbeat wakes the agent periodically and each tick is a full API call. In the dashboard set
**Heartbeat → Every = `6h`** and **Timezone = your local timezone** (default examples use `UTC`).

---

## Local install (no VPS)

### Option A — Docker (recommended)
Needs Docker Desktop + Git.
```bash
git clone https://github.com/openclaw/openclaw.git && cd openclaw
./docker-setup.sh                       # same wizard as VPS
docker compose up -d openclaw-gateway   # dashboard at http://localhost:18789
# stop / start:
docker compose down
docker compose up -d openclaw-gateway
```
No SSH tunnel needed locally — you're on the same machine.

### Option B — Node.js (no Docker)
Needs Node.js 22+ and Git.
```bash
git clone https://github.com/openclaw/openclaw.git && cd openclaw
npm install && npm run build
node dist/index.js onboard
node dist/index.js gateway
```

> WhatsApp links can drop when a laptop sleeps; for always-on WhatsApp, use a VPS.

---

## Troubleshooting catalog

| Symptom | One-line fix |
|--------|--------------|
| Permission denied (`EACCES`/`EPERM`) | `chown -R 1000:1000 ~/.openclaw` |
| Port already in use | `fuser -k 18789/tcp && fuser -k 18790/tcp` |
| Session file locked | `rm ~/.openclaw/agents/main/sessions/*.lock` |
| Container keeps restarting | `docker compose logs --tail 20 openclaw-gateway` → fix bad config |
| `docker compose` not found | `apt install docker-compose-plugin -y` |
| Dashboard won't connect | use the SSH tunnel (HTTPS/localhost required) |

### Permission denied (EACCES / EPERM)
The container is UID 1000 but files are owned by root. Fix:
```bash
chown -R 1000:1000 ~/.openclaw
```
Prevent it by editing config through the dashboard/CLI, not as root.

### Port already in use
```bash
fuser -k 18789/tcp; fuser -k 18790/tcp; sleep 2
docker compose up -d openclaw-gateway
# if it keeps coming back: lsof -i :18789  (docker-pr = container already running)
```

### Session file locked
A timed-out agent left a stale lock:
```bash
rm ~/.openclaw/agents/main/sessions/*.lock
docker compose down && docker compose up -d openclaw-gateway
```

### Container keeps restarting (bad config loop)
```bash
docker compose logs --tail 20 openclaw-gateway
```
Common causes are an invalid provider block or a wrongly-typed field. Example — remove a broken
provider/auth profile from the JSON config:
```bash
python3 -c "
import json, os
p = os.path.expanduser('~/.openclaw/openclaw.json')
c = json.load(open(p))
c.get('models',{}).get('providers',{}).pop('gemini', None)
c.get('auth',{}).get('profiles',{}).pop('gemini:default', None)
json.dump(c, open(p,'w'), indent=2)
print('fixed')
"
chown -R 1000:1000 ~/.openclaw
docker compose down && docker compose up -d openclaw-gateway
```
Example — `imageModel` given as a string but an object is expected:
```bash
python3 -c "
import json, os
p = os.path.expanduser('~/.openclaw/openclaw.json')
c = json.load(open(p))
img = c.get('agents',{}).get('defaults',{}).get('imageModel','')
if isinstance(img, str) and img:
    c['agents']['defaults']['imageModel'] = {'primary': img}
    json.dump(c, open(p,'w'), indent=2); print('fixed')
else: print('imageModel looks OK')
"
```

### Dashboard won't connect (`requires HTTPS or localhost`)
The dashboard uses WebSockets that need a secure context. Either SSH-tunnel it (above), or put
Nginx + a Let's Encrypt cert in front:
```bash
apt install nginx certbot python3-certbot-nginx -y
# point a domain at YOUR_VPS_IP, then:
certbot --nginx -d agent.yourdomain.com
# configure nginx to proxy to 127.0.0.1:18789
```

### Gateway token mismatch / unauthorized
```bash
docker compose down && docker compose up -d openclaw-gateway
# if it persists, regenerate:
docker compose run --rm openclaw-cli configure --section gateway
```

### "Unsupported channel: whatsapp"
WhatsApp wasn't added during onboarding:
```bash
docker compose run --rm openclaw-cli configure --section channels   # pick WhatsApp, scan QR
docker compose down && fuser -k 18789/tcp && sleep 2 && docker compose up -d openclaw-gateway
```

### Bot not responding on Telegram — checklist
1. `docker compose ps` shows **Up**?
2. `docker compose logs --tail 30 openclaw-gateway` — any errors?
3. Telegram block present in config? `python3 -c "import json;print(json.load(open('$HOME/.openclaw/openclaw.json'))['channels'].get('telegram'))"`
4. Bot token correct? Check @BotFather → `/mybots`.
5. DM policy = `pairing`? You must approve your own user in the dashboard first.

### `systemctl --user unavailable` in Docker
Harmless — `systemctl` doesn't exist in containers. Manage via `docker compose`, not systemd.

### Master restart (fixes ~95% of issues) — save as a script
```bash
cat > ~/restart-agent.sh << 'SCRIPT'
#!/bin/bash
cd ~/openclaw
docker compose down
fuser -k 18789/tcp 2>/dev/null
fuser -k 18790/tcp 2>/dev/null
rm -f ~/.openclaw/agents/main/sessions/*.lock
chown -R 1000:1000 ~/.openclaw
sleep 3
docker compose up -d openclaw-gateway
sleep 5
docker compose ps
echo "Done."
SCRIPT
chmod +x ~/restart-agent.sh
```

---

## Handy day-to-day commands
```bash
docker compose ps                                   # running?
docker compose logs --tail 30 openclaw-gateway      # recent logs
docker compose run --rm openclaw-cli configure      # open config wizard
# safe restart:
docker compose down && fuser -k 18789/tcp && sleep 2 && docker compose up -d openclaw-gateway
```
