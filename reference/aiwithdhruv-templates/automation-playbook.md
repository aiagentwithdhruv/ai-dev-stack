# Automation operations playbook

Patterns and checklists for building **deterministic workflow automation** that runs unattended.
Workflow-engine-agnostic — the examples reference n8n and GitHub Actions because they're widely
used, but the shape applies to any engine. This is the operational depth that the flagship's
`pillars/automation/` (a pointer to a companion automation kit) intentionally doesn't carry.

Reach for automation *before* an agent: a deterministic flow is cheaper, faster, and auditable.
Drop a model in only at the specific steps that need judgement (classify, extract, draft) and
keep everything else deterministic.

---

## Should this be automated? (decision tree)

```
1. Has this task happened >= 2 times across the team?
   No  -> manual is fine; log it and watch.
   Yes -> continue.
2. Is the input/output well-shaped (predictable fields, JSON)?
   No  -> fix the upstream first; the human is the bottleneck, not the engine.
   Yes -> continue.
3. Is the failure mode tolerable (retry-friendly, idempotent)?
   No  -> add observability + a human-in-the-loop checkpoint.
   Yes -> continue.
4. Will it save >= 1 hour/week within 30 days of running?
   No  -> defer. Don't build curiosities.
   Yes -> build it.
```

Rule of thumb: *would a human ever benefit from doing this twice?* If no, automate it.

---

## The 7-step shape every workflow follows

```
1. Trigger    -> cron / webhook / manual
2. Pull       -> fetch data from the source(s)
3. Validate   -> reject malformed input early (IF-branch on schema; bad path -> log + 4xx)
4. Transform  -> reshape for the destination
5. Act        -> write / send / post / charge
6. Observe    -> log the result; alert on failure
7. Reconcile  -> write an audit row somewhere a human can inspect
```

If a flow doesn't have all seven steps explicitly, something is missing — usually validation,
observability, or the reconciliation row. A "sticky note" header on the flow (what it does,
owner, last-edited date) pays for itself the first time someone else has to debug it.

---

## Idempotency checklist (for any flow that writes or sends)

1. Does the destination support an **idempotency key**? Use it.
2. If not, does it have a **unique constraint**? Use it.
3. If not, store a **hash of the request** in a "seen" table and reject duplicates.
4. Does retrying re-send to the user? If yes, that's a bug — fix it before shipping.

Test by replaying the trigger 3x. The end state must be identical to running it once.

---

## Rate limiting + backoff

Every flow that calls an external API:

- Respect `Retry-After` headers.
- Exponential backoff: 1s -> 2s -> 4s -> 8s, max ~5 retries.
- After the retry budget is exhausted: drop to the error path, alert, and **stop** — never
  retry forever.

Use the engine's built-in retry config; don't hand-roll retry loops.

---

## Secret handling

| Where a secret may live | Where it must NOT live |
|-------------------------|------------------------|
| Secrets manager / vault (canonical) | Anywhere else |
| The engine's encrypted credential store, referenced by name | Inline in a node / step |
| Per-project env vars (platform-managed) | Git repos, Sheets, chat messages, PR descriptions |
| A cloud secrets manager (in production) | Logs, error messages, screenshots |

Reference secrets by name only (e.g. `{{ $env.VAR }}`). If a secret ever lands in a chat,
screen, or commit — **rotate it immediately** and log the rotation.

---

## Observability (every automation must surface)

1. **Last-run timestamp** — visible somewhere (dashboard / sheet / channel).
2. **Last-run result** — success / failure / partial.
3. **Failure alert** — pushed to your alerting channel (Slack / Telegram / email) with enough
   context to debug, on the error path.
4. **Idempotency** — running twice doesn't double-charge / double-send.
5. **Manual trigger** — a one-click re-run for when you need it.
6. **Kill switch** — an env var or one-click disable.

Silent failures are worse than loud ones. A flow that fails quietly is a flow you find out about
from a customer.

---

## Common failure modes and defences

| Failure | Defence |
|---------|---------|
| Webhook signature not verified | Always verify (most payment/VCS providers sign payloads). |
| Retried event double-sends (e.g. a license email) | Idempotency key on the send step. |
| A credential expires silently | Weekly health-check cron that calls each integration with a no-op. |
| Outreach message ships with a literal `{{Name}}` placeholder | Template-render test before the flow goes live. |
| Flow loops forever on bad input | Hard timeout per step + circuit breaker on retries. |
| Scraper banned by the target site | Respect robots.txt/ToS; use an authorised path; back off. |
| Spreadsheet/API quota exceeded | Batch writes; never write per-row in a loop. |

---

## Definition of Done

A shipped automation:

- [ ] Runs on a schedule or trigger — no manual step inside the loop.
- [ ] Logs every run (timestamp + result) somewhere auditable.
- [ ] Alerts on failure with enough context to debug.
- [ ] Has a kill switch.
- [ ] Is idempotent — re-running != double effect.
- [ ] Keeps all credentials in the vault / engine credential store.
- [ ] Has a one-page **recipe doc** (what it does, trigger, owner, kill switch, dependencies).
- [ ] Has survived 3 consecutive scheduled runs without intervention.

Until every box is checked, it's a draft. The recipe doc is what makes the work compounding —
the next person reuses the flow without rebuilding it.

---

## Non-negotiables

- Never **auto-publish** content or **auto-send** money / trades — always a human approval gate.
- Never scrape sites that prohibit it; respect robots.txt and ToS.
- Never keep a silently-failing flow running — kill it, fix the root cause, restart.
- A new paid SaaS subscription needs a written one-paragraph rationale (cost + use case +
  alternatives) before you commit to it.
