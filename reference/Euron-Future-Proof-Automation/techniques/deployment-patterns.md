# Deployment Patterns — Getting Automations Running 24/7

> **Applies to:** every automation that needs to run in production without a laptop open.

## Decision Matrix

```
Is it a one-time/scheduled task?
  YES --> scheduled CI (e.g. GitHub Actions cron) or a cron service
  NO  --> Does it receive webhooks?
            YES --> serverless function or a PaaS
            NO  --> Does it run continuously (a bot)?
                      YES --> PaaS container or a VPS
                      NO  --> serverless runtime (e.g. Modal)
```

## Pattern 1: Serverless (webhooks + APIs)
**When:** responds to HTTP requests. **Where:** a serverless host (free tiers common).
**Pro:** zero ops, auto-scales, free. **Con:** cold starts, timeout limits, no persistent state.
```bash
vercel deploy        # JS/Python serverless
modal deploy app.py  # Python serverless runtime
```

## Pattern 2: Container on PaaS (bots + workers)
**When:** runs continuously (chat bot, background worker). **Where:** a PaaS with free tier.
**Pro:** easy deploy from a repo, Docker support. **Con:** free tiers sleep / cap hours.
```bash
railway up                                       # connect repo, auto-deploy
docker build --platform linux/amd64 -t my-bot .  # build for amd64 targets
```

## Pattern 3: VPS (full control)
**When:** 24/7 uptime, self-hosted workflow engine, multiple services, or a database.
**Pro:** run anything, cheapest at scale. **Con:** you manage updates, security, backups.
```bash
ssh root@your-vps
apt update && apt install docker.io docker-compose nginx certbot
docker-compose up -d
certbot --nginx -d your-domain.com   # free, auto-renewing SSL
```

## Pattern 4: Scheduled (cron jobs)
**When:** runs on a schedule (daily report, weekly research, hourly check).
**Where:** scheduled CI (free), a cron service, or VPS cron. **Con:** not real-time; CI jobs cap.
```yaml
# .github/workflows/daily-task.yml
name: Daily Automation
on:
  schedule:
    - cron: '0 8 * * *'   # 08:00 UTC daily
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python main.py
        env:
          LLM_API_KEY: ${{ secrets.LLM_API_KEY }}
```

## Pattern 5: Cloud CLI deployment (production scale)
**When:** production-grade infra (container service, serverless functions, VMs).
**Pro:** scalable, generous free tiers. **Con:** more moving parts.
```bash
# Container registry + container service (example)
docker build --platform linux/amd64 -t my-app .
# tag, push to your registry, then force a new deployment on your service
```

## Gotchas
- **ARM vs AMD64:** ALWAYS `--platform linux/amd64` when building Docker on an Apple-silicon Mac
  for an x86 target — otherwise the image won't run.
- **Secrets in CI/CD:** use the platform's secret store, never commit `.env`.
- **Free-tier sleep:** some PaaS free tiers sleep after inactivity; a cron ping keeps them warm.
- **Domain/SSL:** a free CDN tier handles DNS + SSL + caching — use it.
- **Monitoring:** add a `/health` endpoint and an uptime monitor.

## Related
- `webhook-patterns.md` — what runs on these deployments
- `cost-optimization.md` — keeping deployment + model costs down
