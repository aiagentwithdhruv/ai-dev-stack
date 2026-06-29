# Source: autonomous ops-agent config (sanitized extract)

This folder is a curated, vendor-neutral extract from a private agent-configuration repo.
The original was a thin config layer on top of an open-source autonomous-agent framework
(Hermes-style), pointed at a personal knowledge base and run on a **cheap reasoning model**
instead of a frontier model — to automate routine "operations" chores (scheduled reminders,
a weekly scoreboard review) cheaply and unattended.

## Why it's worth keeping

The flagship already covers app-level [model routing & cost](../../foundations/model-routing-cost/)
and the [automation](../../pillars/automation/) vs [agents](../../pillars/agents/) decision. This
extract adds three concrete things those pages don't spell out:

1. **A worked pattern** — running an OSS autonomous agent on a *cheap reasoning model* to maintain
   your own knowledge base / ops, rather than maintaining it by hand. See
   [`autonomous-ops-agent-on-cheap-model.md`](./autonomous-ops-agent-on-cheap-model.md).
2. **A real provider-wiring gotcha** — pointing an "OpenAI client" at a non-OpenAI,
   OpenAI-compatible endpoint via `base_url`, and the fact that some **reasoning models require
   `temperature=1`**. Same file.
3. **A vendor-neutral agent SKILL template** — frontmatter + Steps + Rules, plus the
   cron-schedule and human-approval safety pattern. See
   [`agent-skill-template.md`](./agent-skill-template.md).

## What was deliberately left out (privacy / not reusable)

- All personal identity: owner name, personal email, personal-brand "OS" naming.
- The two real skills' *content* — they were 100% personal (a job-application pipeline and a
  personal growth scoreboard). Only the **shape** is kept, fully abstracted, in the template.
- Specific private repo names, file paths, and pipeline data.
- Any secret material and the provider API key (the original kept secrets gitignored; the key
  value is not, and never was, in any folded file).

Nothing here is tied to a person, employer, or client. If you need the framework itself, it is
public OSS; this folder only captures the reusable *patterns* for layering on top of it.
