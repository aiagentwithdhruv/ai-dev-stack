# Vendor-neutral agent SKILL template

A "skill" is a small, reusable task definition an autonomous agent loads on demand or on a schedule.
The shape below works for most OSS agent frameworks: YAML frontmatter for metadata, then prose
**Steps** (what to do, in order) and **Rules** (hard constraints). Keep skills short, concrete, and
action-first — the agent reads them every run.

## Template

```markdown
---
name: <kebab-case-id>
description: "<one sentence: what this skill delivers, for whom, when>"
version: 1.0.0
platforms: [macos, linux]
metadata:
  agent:
    tags: [<area>, <cadence>, <topic>]
    related_skills: [<other-skill-id>]
---

# <Human Title>

You are <role>. Workdir is `<repo-or-path>`. <One line on the goal and the desired tone:
short / concrete / action-first.>

## Steps
1. **Read** the standing context: `<file-a>`, `<file-b>`. (Always act on current state, not memory.)
2. **Compute / decide** with exact numbers — never "many", "several", "a lot".
3. **Produce the deliverable** (your reply text *is* the delivered message), or **edit one known
   file** and nothing else.
4. **Stage, do not publish.** If a commit is needed, commit locally with a clear message; never
   `push`. Never send/post on the user's behalf.
5. **Hand back** a 4-6 line summary: the headline, the single biggest move, the single biggest gap,
   the one action that matters most next.

## Rules
- Exact numbers. No fluff. No emojis (unless asked).
- Action-first: lead with the decision/targets, not preamble.
- Never auto-publish, never push, never act irreversibly — prepare and remind; a human approves.
- Read broadly, write narrowly (one known file). Don't touch other repos except to read them.
- Honesty over comfort: if a number didn't move, say so plainly.
```

## Two common skill shapes (abstracted)

These are the generic patterns behind a "daily nudge" and a "weekly review" — domain stripped out.

### A. Recurring nudge (e.g. cron `0 9 * * *`)

- Reads a pipeline/queue file + a method/checklist file.
- Emits a short card: today's top 1-2 priorities, a time-boxed plan, anything overdue
  (e.g. "silent ≥ N days"), one line of motivation.
- **Prepares and reminds only** — never acts on the user's behalf.

### B. Weekly scoreboard review (e.g. cron `0 9 * * 1`)

- Reads the current scoreboard + the source-of-truth files for each tracked metric.
- Computes this week's exact deltas (totals + change vs last week).
- Updates *one* scoreboard file: refresh the table + append one honest dated log line (newest on
  top), one clause per tracked area — what moved, what didn't.
- Commits locally with a dated message; **does not push** — hands a 4-6 line summary to the human,
  ending with "committed locally as `<msg>` — review and push when ready."

## Wiring it on a schedule

```bash
# list / inspect skills the agent knows
<agent> skills

# run one on demand (good for testing before you schedule it)
<agent> -z "run <skill-id>" --skills <skill-id>

# schedule it (cron expression + skill); a small always-on ticker fires them
<agent> cron   # daily nudge: 0 9 * * *   |   weekly review: 0 9 * * 1
```

Verify with one live manual run before trusting the cron — confirm it read the *real* files and
produced a correct result, then leave it unattended.
