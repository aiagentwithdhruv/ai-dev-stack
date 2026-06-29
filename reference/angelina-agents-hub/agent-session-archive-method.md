# Agent Session Archive — the learning loop

A lightweight method for making a team of AI coding agents get **better over time**
instead of repeating the same mistakes. It's just a git repo of markdown — no app, no
build, no service. The value is the discipline, not the tooling.

> Core bet: every session that goes in makes the next session cheaper (better prompts)
> and safer (known failures avoided). Skip logging → lose the compounding.

## The loop

```
1. Human dispatches an agent (a Claude Code / LLM coding session)
2. Session completes → human copies the prompt + the response VERBATIM
3. Save one file:  archive/<role>/YYYY-MM-DD-<role>-<who>-<project>-<slug>.md
4. Commit on a `dev` branch (never straight to main), push
5. A reviewer reads the week's logs on a fixed cadence (e.g. Monday)
6. Reusable prompts  → promoted to  prompts/templates/
7. Recurring failures → promoted to failures/ (the scar ledger)
8. dev → main merged by the reviewer after review
```

Nothing goes direct to `main`. Logs land on `dev`, get reviewed, then merge. The point of
the review gate is not gatekeeping the archive — it's the moment where patterns and
failures get *extracted*.

## Folder shape

```
archive/<role>/          ← primary archive, one folder per agent role
by-project/<project>/     ← optional mirror, same logs grouped by project
by-person/<who>/          ← optional mirror, same logs grouped by who dispatched
prompts/templates/        ← battle-tested prompt templates (promoted)
patterns/                 ← reusable multi-step workflows (promoted)
failures/                 ← named failure modes + named defences (promoted)
weekly-digests/           ← one digest per review cycle
```

Mirrors are optional pointer files (a one-line link + a grep-able summary), not copies of
the body. If skipped, the reviewer cross-links during the digest.

## Hard rules

1. **Verbatim paste.** Don't edit or summarize the agent's output. The training signal is
   in the *exact* output — including the mistakes.
2. **Redact before commit.** API keys, bearer tokens, DB URLs with passwords, internal
   URLs, customer PII → replace with `{REDACTED-…}`. When unsure, redact.
3. **One session per file.** Don't bundle. One file = one `dispatch → response → review`.
4. **Consistent naming.** `YYYY-MM-DD-<role>-<who>-<project>-<slug>.md`. Date is the
   session date, not the commit date.
5. **`dev` branch only.** Merge to `main` via review.
6. **Commit daily.** Batching a week of sessions into one commit loses detail.
7. **Never delete.** Prune to `archive/` if you must; prefer keeping history intact.
8. **Link related logs.** If a session builds on a previous dispatch, reference its filename.

## Session-log template

```markdown
# [Task title in human terms]

**Date:** YYYY-MM-DD
**Role:** backend-agent
**Dispatched by:** <who>
**Project:** <project>
**Status:** success / partial / failed / iterating

---

## PROMPT
[Paste VERBATIM — the exact prompt that went in]

## RESPONSE
[Paste VERBATIM — the agent's full output, unedited]

## REVIEW
### What worked
- [What the agent got right]
### What didn't
- [Mistake or quality issue]
### What I edited
- [Changes made before committing the agent's output]
### Prompt improvements for next time
- [Additions to test on the next dispatch]
### Verdict
- KEEP-AS-IS / NEEDED-EDITS / REJECTED / ITERATED
```

## Promotion pipeline

| From | To | Trigger |
|------|----|---------|
| Session log | `prompts/templates/<role>-<pattern>.md` | Same prompt shape worked 3+ times with minimal edits |
| Session log | `patterns/<name>.md` | A reusable multi-step workflow that cuts across agents/projects |
| Session log | `failures/<name>.md` | A failure mode seen 2+ times, with a concrete defence (see `failure-mode-ledger.md`) |

Promotion is **copy + adapt**, never move — the original log stays put.

## Pattern template (bigger than a single prompt)

A *pattern* is a multi-step workflow (e.g. backend-agent + frontend-agent + qa-agent to
ship one feature), as opposed to a *template* which is one prompt for one task.

```markdown
# Pattern: [Name]
**Promoted:** YYYY-MM-DD
**Source logs:** [link, link, link]

## When this applies
- [trigger 1] / [trigger 2]

## The workflow
1. [step — who / what / why]
2. ...

## Decision points
- [where a human judges vs. lets agents autopilot]

## Known failure modes if followed wrong
- [failure → mitigation]

## Example
[concrete example from a real session]
```

## Weekly digest

Each cycle the reviewer writes `weekly-digests/YYYY-wWW.md`:

1. Sessions logged (by role, by person, by project)
2. Top patterns that worked
3. Top failures + defences added
4. Net prompt improvements (new / updated templates)
5. Recommendations for next cycle

## Why one central hub (vs. per-person archives)

- **Cross-pollination** — a pattern that works on one project helps another.
- **Single review surface** — the reviewer reads one place, not N.
- **Failure discovery** — the same failure shows up across agents, not just per person.
- **Institutional memory** — a year in, this is the corpus you'd seed a meta-prompt or
  a fine-tune from.

## What this is NOT

- Not a product codebase (no build/deploy config).
- Not a wiki (markdown archive only).
- Not a replacement for per-project bug logs — project-specific bugs stay in the project.
  This is about **agent-level** learning.
