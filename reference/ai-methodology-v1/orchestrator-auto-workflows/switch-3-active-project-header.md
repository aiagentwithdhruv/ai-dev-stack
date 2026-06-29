# Switch 3 — Active Project Header

> **Status:** PROVISIONAL — designed, not yet validated across 2+ projects.
> **Category:** Context hygiene
> **Cost:** zero — one line added to the prompt-file template
> **Benefit:** prevents instruction bleed when a specialist works across multiple projects

---

## The Rule

Every prompt-file opens with this line, immediately after the title:

```
> **ACTIVE PROJECT: {PROJECT_NAME}**
```

This line appears before the WORKSPACE block, before CONTEXT, before everything else.

---

## Why — LLM in-session instruction bleed

A specialist agent may work on Project A in the morning and Project B in the afternoon.
The LLM's in-context state does not reset between tasks — it carries forward priors
from earlier in the session. If a prompt-file does not explicitly declare which project
it belongs to, the model may silently apply constraints, field names, or architectural
decisions from the previous project.

This is not hypothetical. Common failure modes:

- Schema field names from Project A appear in Project B's code.
- The wrong repo path is used because the previous task set it.
- Security or RBAC patterns from one project's spec override another's.

The `ACTIVE PROJECT:` line is a context anchor. It is the first thing the model reads,
which means it is the frame through which all subsequent instructions are interpreted.

---

## Implementation

In `prompt-file.template.md`, the header is already included:

```markdown
# {PROMPT_FILE_TITLE} — {PROMPT_CODE}

> **ACTIVE PROJECT: {PROJECT_NAME}**
> **Issued by:** {ORCHESTRATOR_NAME}
> ...
```

Nothing else changes. The orchestrator fills in `{PROJECT_NAME}` for every prompt.

---

## When this matters most

- Specialists who work on 2+ projects in a single day.
- Projects with overlapping domain language (e.g., two SaaS products with "organizations" and "tenants").
- Late-sprint handoffs where context from earlier in the session is stale.

It matters least when a specialist works exclusively on one project per session.
Even then, it costs nothing — keep it.

---

## Tradeoffs

- No downside. One line. Zero friction.
- Does not fully prevent bleed — it reduces it. If bleed is severe, the specialist
  needs a fresh session (new conversation), not just a header.
- For high-stakes tasks (schema migrations, auth rewrites), consider starting a
  fresh session regardless of what was worked on earlier.
