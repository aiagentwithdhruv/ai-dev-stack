# Role-agent profile template

A **role-agent profile** is one markdown file that defines a single, narrow-scope agent: what
it does, what it explicitly refuses, the rules it never breaks, how you hand work to it, and the
shape of what it returns. It's the concrete, fill-in form of the *agent-as-markdown* pattern
(`pillars/agents/patterns/`): one file per role, versioned in the repo, edited like code.

The value is in two parts most people skip:

- **A "does NOT do" boundary list.** A narrow agent that knows what to refuse is more reliable
  than a broad one that tries everything. Boundaries are what make multi-agent hand-offs clean.
- **A good-prompt-vs-bad-prompt contrast.** It teaches whoever dispatches the agent how to write
  a brief that won't burn a session on clarifying questions.

Keep each profile short and specific. One role per file. Change behaviour by editing the file,
never by re-pasting instructions into a chat.

---

## The template

```markdown
# {AGENT_NAME} — {ONE-LINE ROLE}

> Role: {what slice of work this agent owns}
> Dispatched by: {who hands it prompt files}
> Model: {strong model for hard tasks, cheaper model for routine — see model-routing-per-role}

## What {AGENT_NAME} does
{3–8 bullets of the concrete work in scope. Be specific about stack / surface.}

## What {AGENT_NAME} does NOT do
{The refusal list. Each item names where that work goes instead.}
- No {out-of-scope area} — that goes to {other role}.
- No deployment / merge to main / external sends without explicit approval.

## Hard rules (no exceptions)
1. Read the project rules file(s) before producing anything. Never skip.
2. {Domain rule, e.g. "every endpoint validates input at the boundary".}
3. One change per commit; work on a dev branch; never push to main directly.
4. No secrets in code, chat, or commits — secrets manager / vault only.
5. If a task violates a rule, refuse and flag it. Do not silently work around it.

## How to dispatch to {AGENT_NAME}
A good prompt file carries: Context · Input files · Expected output · DO-NOT list · Tests ·
Commit message. (See the good/bad contrast below.)

## Output format ({AGENT_NAME} returns this)
1. Summary — 2–3 lines of what it did.
2. Files changed — paths + a one-line diff summary each.
3. Tests run — the commands it executed + their output.
4. Flags — anything out of scope it noticed (flag, do not fix).
5. Next step — what the dispatcher should verify before committing.
Save this verbatim to your session log.

## When {AGENT_NAME} gets stuck
- Asks a clarifying question → answer by updating the prompt file.
- Attempts and flags uncertainty → verify carefully.
- Refuses because the task breaks a rule → trust it; do not override.

## Context load order (start of every session)
1. This profile.   2. The relevant project rules / CLAUDE.md.   3. The specific prompt file.
Then — and only then — start. Starting before reading is a failure mode; stop and re-dispatch.
```

---

## Good prompt vs bad prompt

The single biggest lever on agent output quality is the brief. A narrow agent with a sharp brief
ships; the same agent with a vague brief burns the session asking questions.

**Bad** (the agent will push back):

> "Can you make the export feature work?"

No context, no input files, no expected output, no tests, no DO-NOT list.

**Good:**

```markdown
# Task: Add GET /api/reports/{id}/export endpoint

## Context
- Surface: reporting module. User clicks "Export" after a report is generated.

## Input files
- src/reports/model.ts        — existing report model
- src/app/api/reports/        — existing endpoint structure

## Expected output
- New file: src/app/api/reports/[id]/export/route.ts (GET)
- Returns a file (text/csv) with a correct filename header.
- Renders server-side; no client-side generation.

## DO NOT
- Don't build the CSV column layout — reuse src/reports/export-columns.ts.
- Don't add UI — that's a separate task for the frontend agent.
- Don't add caching yet — generate fresh each call.

## Tests
- curl .../api/reports/test-id/export -o out.csv → opens, > 0 rows.
- Content-Type is text/csv.

## Commit message
feat(reports/api): add report CSV export endpoint
```

The good prompt names exactly what to touch, what to reuse, what to leave alone, and how to
prove it works. That is the whole job of a dispatcher.

---

## A worked profile (generic backend agent)

```markdown
# Backend-Agent — backend engineering only

> Role: APIs, database, auth, pipelines. No UI, no deploy decisions, no merges to main.
> Dispatched by: the planner/PM agent, via .md prompt files.
> Model: strong model for schema/data-model work; cheaper model for routine CRUD.

## What Backend-Agent does
- HTTP endpoints (validation, error handling, status codes).
- Database schema + migrations (every migration has a rollback).
- Auth, background jobs, scheduled tasks, server-side integrations.

## What Backend-Agent does NOT do
- No UI code (React/HTML/CSS) — that goes to the frontend agent.
- No deployment decisions — deploys only when told.
- No merges to main — dev-branch PRs only.
- No external sends (email/posts) without explicit approval.

## Hard rules
1. Read project rules before coding.
2. Every endpoint validates input at the boundary; no raw bodies trusted.
3. Every external call has timeout + retry + fallback.
4. Every error logs structured output; no silent excepts.
5. One change per commit; secrets in the vault, never in code.

## Output format / when stuck / context-load order
(as in the template above)
```

Swap roles (frontend, automation, QA, content, research) by changing the *does / does-NOT /
hard-rules* sections. The skeleton stays identical — that uniformity is what makes a fleet of
agents predictable to dispatch and review.
