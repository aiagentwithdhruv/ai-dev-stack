# Pattern: an autonomous ops-agent on a cheap reasoning model

> Reserve your frontier model for product-facing, high-stakes work. For *your own* routine
> operations — scheduled reminders, weekly reviews, log upkeep, repo housekeeping — run an
> open-source autonomous agent on a cheap model. It costs a few dollars a month and turns static
> docs into a living, self-maintaining system.

This is the inverse of [foundations/model-routing-cost](../../foundations/model-routing-cost/):
that page routes *product* traffic across tiers; this is about routing *your own back-office
chores* to the cheapest tier that can still read a file, compute honest numbers, and write a line
back.

## When to reach for it

- The chore is **recurring and low-stakes** (a daily nudge, a weekly snapshot, a tidy-up).
- A pure [n8n-style workflow](../../pillars/automation/) is too rigid — the step needs the model to
  *read context and judge* ("which of these are silent ≥7 days?", "did this number actually move?").
- But it's not worth a frontier model: a cheap reasoning model handles it for cents.

If the steps are fully deterministic, stay in automation. If the path is open-ended and
high-value, that's a real [agent](../../pillars/agents/) on a capable model. This pattern is the
cheap middle: a scheduled agent with judgement, on a budget model.

## Architecture

```
knowledge base (your repos / docs)   <-- the agent's standing brief, read each run
        ^
        | reads + edits one file
        |
   autonomous agent framework (OSS)   <-- persistent memory, MCP client, messaging
        |
   cheap reasoning model (config)     <-- swappable; the "brain"
        |
   cron / scheduler  ----------------> daily + weekly skills fire unattended
```

- **Workspace = your knowledge repo.** The agent reads a CONTEXT pack as its standing brief every
  run, so it always acts on current state rather than stale training.
- **Skills** are small, reusable task definitions (see
  [`agent-skill-template.md`](./agent-skill-template.md)).
- **Cron** fires them on a schedule (`0 9 * * *` daily, `0 9 * * 1` weekly) via a small
  always-running ticker (a user-level service / launchd / systemd unit).
- **Persistent memory** lets it remember streaks, pipeline state, and what it did last week.
- **Messaging** (optional) lets it deliver results to a chat platform and accept tasks back.

## Provider wiring — the reusable gotchas

Most cheap models expose an **OpenAI-compatible** API. You usually don't need a new SDK; you point
the OpenAI client at a different base URL.

```bash
# .env.example  (commit the shape, never the secret)
PRIMARY_MODEL=<cheap-reasoning-model-id>
MODEL_TEMPERATURE=1          # see note below
PROVIDER_API_KEY=your-key-here
PROVIDER_BASE_URL=https://<provider-host>/v1

# Many tools read the OpenAI-named vars; alias them to the same compatible endpoint:
OPENAI_API_KEY=your-key-here
OPENAI_BASE_URL=https://<provider-host>/v1
```

Two things that bite people:

1. **`base_url` override is the whole trick.** An "OpenAI" client talks to any OpenAI-compatible
   provider once `OPENAI_BASE_URL` points at their `/v1`. No code change beyond config.
2. **Some reasoning models require `temperature=1`.** They run an internal thinking phase and
   reject (or misbehave at) lower temperatures. If a reasoning model errors on temperature or
   ignores your setting, pin it to `1`. Budget a few extra output tokens for the thinking phase —
   still cheap.

Keep secrets out of the repo entirely (gitignore `.env`, `*.key`, `secrets/`, runtime `state/` and
`logs/`). Commit only `.env.example`. Rotate the key if it ever lands in a chat or log.

## Cost reasoning

- A cheap reasoning model at roughly sub-$1 in / a few-$ out per 1M tokens runs months of small
  ops chores for a few dollars total.
- A health check should always be able to confirm *which* provider/model is active — an agent that
  can switch brains can silently switch to an expensive one. Make "what model am I on?" a
  one-command answer.

## Safety (non-negotiable for an agent that can run shell + edit files)

- **Prepare and remind; do not act irreversibly.** For anything that publishes, sends, or pushes:
  the agent drafts and stages; a human approves and triggers. Bake "never auto-publish, never
  `push`" into the skill's Rules, not just your intentions.
- **Default to asking on risky steps.** Use the framework's safe/confirm mode for shell + writes;
  reserve any "don't ask" mode for genuinely safe, idempotent tasks.
- **Scope the blast radius.** Constrain a skill to *read everything, write one known file*.
- **Honesty over cheerleading.** A review skill must report numbers that didn't move plainly —
  an ops agent that flatters you is worse than no agent.

## Checklist

- [ ] Cheap reasoning model selected; `temperature=1` if it's a reasoning model.
- [ ] OpenAI-compatible endpoint wired via `base_url`; OpenAI-named vars aliased.
- [ ] Secrets gitignored; only `.env.example` committed.
- [ ] Workspace points at the knowledge repo; skills read a standing CONTEXT brief.
- [ ] Cron entries + an always-on ticker; verified with one live manual run.
- [ ] Each skill's Rules forbid auto-publish / push; risky steps ask first.
- [ ] One command reports the active provider/model (cost guard).
