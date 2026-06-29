# Source: OpenClaw Self-Host Setup Guide

**Origin:** A public, standalone setup guide for [OpenClaw](https://github.com/openclaw/openclaw)
— an open-source, self-hosted AI agent you run on your own VPS or local machine and talk to
through everyday messaging apps (Telegram, WhatsApp, Discord, Slack, iMessage).

**Why it lives here:** The flagship covers building agents, RAG, model routing, and guardrails,
but it had no end-to-end runbook for **self-hosting an always-on personal/assistant agent on a
cheap VPS**, no **free/cheap LLM provider catalog**, and no ready-made **agent persona prompt
library**. Those three things are the reusable, generic value, so they were extracted and
neutralized here.

## What's in this folder

| File | What it is |
|------|------------|
| `self-host-vps-runbook.md` | Generic runbook: deploy a Docker-based messaging AI agent on a VPS (or locally), plus a troubleshooting catalog (permissions, ports, locks, dashboard/SSL, restart script). |
| `free-llm-providers.md` | Comparison of free/low-cost LLM providers and a token-cost optimization checklist. |
| `customization-and-configs.md` | How to rename the agent, set personality/system prompt, manage skills, channels, memory, heartbeat; plus 3 example JSON config files. |
| `agent-persona-prompts.md` | 6 reusable system-prompt persona templates (personal assistant, business, coding, sales coach, research analyst, creative writer). |

## Sanitization applied (what was removed, and why)

This extract is rewritten to be vendor- and author-neutral. The following were stripped from the
original public repo before folding:

- **Personal infrastructure** — a real VPS public IP and its `ssh root@<ip>` / SSH-tunnel commands
  (the original "Deployment" quick-reference table). Replaced with `YOUR_VPS_IP` placeholders.
- **Author / brand identity** — personal name, LinkedIn profile, Calendly booking link, YouTube
  link, and "Built by …" credits. Removed entirely.
- **Personal agent name** — the original defaulted the agent to a specific personal name and used
  it in an example config and an error heading. Replaced with the neutral name `Aria`.
- **Location signal** — an `Asia/Kolkata` timezone used in examples. Replaced with `UTC` plus a
  "set your local timezone" note.
- **A creator-affiliated provider** — one niche provider tied to the original author's ecosystem
  was dropped from the provider catalog. Only mainstream, generally-available providers were kept.

Nothing in the original tied to any employer, client, or proprietary product; no credentials or
secrets were present (config keys were already `YOUR_…` placeholders).

> OpenClaw itself, provider names (Moonshot/Kimi, Gemini, Groq, Cerebras, OpenRouter, Ollama),
> and VPS host names are public, generic facts and are kept.
