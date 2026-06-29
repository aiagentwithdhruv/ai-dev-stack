---
title: New Project Checklist — Zero to First Agent in 15 Minutes
type: checklist
---

# New Project Checklist

## Before you start

This checklist assumes:
- You have Claude Code installed (`claude` CLI available)
- You have Python 3.10+ installed
- You have the `ai-methodology-v1/` framework available at a known path

If any of these are missing, resolve them before continuing.

---

## Step 1 — Create the project directory

```bash
# Replace PROJECT_NAME with your project name (lowercase, hyphens)
mkdir -p ~/projects/PROJECT_NAME
cd ~/projects/PROJECT_NAME
```

Expected: empty directory, no error.

---

## Step 2 — Initialize the directory structure

```bash
mkdir -p .claude/rules
mkdir -p agents/shared
mkdir -p 07-learning-hub/{techniques,daily,market,competitors,feed/inbox,feed/processed}
mkdir -p docs
touch 07-learning-hub/LEARNING-ZONE.md
touch 07-learning-hub/feed/inbox/README.md
```

Expected: directory tree created, no error.

Verify:
```bash
find . -type d | sort
```

You should see: `.claude/`, `.claude/rules/`, `agents/`, `agents/shared/`, `07-learning-hub/` and its subdirectories, `docs/`.

---

## Step 3 — Write CLAUDE.md

Create `.claude/CLAUDE.md` with the following structure. Fill in the bracketed fields:

```markdown
# [PROJECT_NAME] — Agent Rules

> Owner: [your name] | [your role]
> Started: [date]
> Purpose: [one sentence — what problem this project solves]

## What this project does

[2-3 sentences describing the project, the stack, and the users]

## Rules

### How agents work here

- CLAUDE.md first, code second — read all rules before writing any code
- Finish the current task before starting the next
- No mock data — show "No data yet" for empty states
- Backend schema is the contract — agree on schema before writing routes or UI
- Verify with data before recommending. Grep the codebase; do not guess.

### Code quality

- Optional chaining (`?.`) on all API data — never assume data exists
- Every array prop: `= []` default. Every string prop: `= ''` default.
- No `console.log` debug lines in committed code
- No hardcoded `localhost` in env vars — use relative paths

### Security

- Secrets in AWS Secrets Manager or equivalent — never in code or `.env` in production
- API keys never in frontend — backend proxies all external calls
- Input validation with Pydantic (Python) or Zod (TypeScript) at every system boundary

### Git

- Always work on `dev` branch. Never commit directly on `main`.
- One change per commit. Max 2 files.
- Never `git reset --hard` — use `git revert HEAD`

## Stack

[List your stack: language, framework, database, cloud provider]

## Learning hub location

`07-learning-hub/` — read LEARNING-ZONE.md at every session start.

## Session startup sequence

Every agent, every session:
1. Read this file (CLAUDE.md)
2. Read `07-learning-hub/LEARNING-ZONE.md`
3. Read the latest `07-learning-hub/daily/[date].md`
4. Read the technique file most relevant to today's task
5. Begin work
```

Expected: CLAUDE.md saved, no error.

---

## Step 4 — Write the shared agent rules

Create `agents/shared/SHARED-RULES.md`:

```markdown
# Shared Agent Rules — All Agents Read This

## Non-negotiable rules

- Read CLAUDE.md before anything else
- Check LEARNING-ZONE.md before making architectural decisions
- Do not assume. Grep the codebase. Verify with data.
- Do not give options. Make a decision and state it.
- Finish what you started. Do not begin the next task until the current one is done.
- Report back with: what you did, files changed, what to test next.

## Output format

After completing any task, your report must include:
- Files changed (path and purpose of each change)
- Commands the human needs to run (if any)
- What to test and how
- Any open questions or risks

## What "done" means

"Done" is not "I wrote the code." Done is "I wrote the code, verified it runs without errors,
confirmed the behavior matches the spec, and there are no TODOs left open."
```

Expected: file saved.

---

## Step 5 — Initialize the LEARNING-ZONE

Open `07-learning-hub/LEARNING-ZONE.md` and write the header:

```markdown
# Learning Zone — Live Error and Fix Log

> Read at every session start. Written to after every error-fix pair.

## Format

Each entry:
```
[DATE] [Error brief]
- Cause: what caused it
- Fix: what resolved it
- Rule: the rule this produces going forward
- Applies to: which agents or scenarios this is relevant to
```

## Entries

(empty — first entry will be written when the first error is encountered)
```

Expected: file saved.

---

## Step 6 — Copy 3 technique files from the framework

Copy the technique files most relevant to your project from `ai-methodology-v1/09-knowledge/` into `07-learning-hub/techniques/`. Start with 3:

```bash
# Example: an agent-heavy project
cp ~/path/to/ai-methodology-v1/09-knowledge/agent-frameworks-comparison.md \
   07-learning-hub/techniques/

cp ~/path/to/ai-methodology-v1/09-knowledge/6-layer-guardrails.md \
   07-learning-hub/techniques/

cp ~/path/to/ai-methodology-v1/09-knowledge/rag-architecture.md \
   07-learning-hub/techniques/
```

Adjust which 3 files based on your project's stack. For a voice project: `voice-ai-stack.md`. For a deployment project: `deployment-aws-ecs.md`. For a knowledge base project: `karpathy-method.md`.

Expected: 3 files in `07-learning-hub/techniques/`.

---

## Step 7 — Write the first daily brief

Create `07-learning-hub/daily/YYYY-MM-DD.md` (today's date):

```markdown
# Daily Brief — [DATE]

## Market Moves

- (project started today — no prior briefs)

## Technique of the Day

**Topic:** [the first technique file you copied in Step 6]
**Key insight:** [one sentence from that file that will matter most today]

## Action Items

- [ ] Complete project setup (this checklist)
- [ ] Define first agent's scope and system prompt
- [ ] Write first task prompt
```

Expected: file saved.

---

## Step 8 — Write the first agent definition

Create `agents/[agent-name]/AGENT.md` for the first specialist agent you need:

```markdown
# [Agent Name] — Agent Definition

## Role

[What this agent does. One paragraph. Be specific about what it handles and what it
explicitly does NOT handle.]

## Startup sequence

1. Read `.claude/CLAUDE.md`
2. Read `agents/shared/SHARED-RULES.md`
3. Read `07-learning-hub/LEARNING-ZONE.md`
4. Read the relevant technique file for today's task
5. Begin work

## Capabilities

[What tools, files, and APIs this agent has access to]

## Restrictions

- [List of things this agent must NOT do]

## Output format

[What a completed task response looks like — be specific]
```

Expected: file saved.

---

## Step 9 — Verify the setup

```bash
# Check directory structure
find . -type f | sort

# Should include at minimum:
# .claude/CLAUDE.md
# .claude/rules/ (empty dir — rules go here as you add them)
# agents/shared/SHARED-RULES.md
# agents/[agent-name]/AGENT.md
# 07-learning-hub/LEARNING-ZONE.md
# 07-learning-hub/daily/YYYY-MM-DD.md
# 07-learning-hub/techniques/ (3 files)
# 07-learning-hub/feed/inbox/README.md
```

---

## Step 10 — First session

Open Claude Code in the project root:

```bash
claude
```

In the first message, paste the WORKSPACE block from `agent-onboarding.md` filled in with your project details. Then state the first task.

If the agent reads the files and asks clarifying questions before coding — that is the correct behavior. If it immediately writes code without acknowledging the CLAUDE.md — stop, start a new session, and re-send the WORKSPACE block.

---

## Troubleshooting

**Agent starts coding immediately without reading CLAUDE.md:**
Your first message did not establish context. Start a new session. Begin with the WORKSPACE block (see `agent-onboarding.md`). Include the file contents if needed.

**Agent says "I cannot access that file":**
Check that you are running `claude` from the project root directory (the directory containing `.claude/CLAUDE.md`).

**LEARNING-ZONE.md is not being updated after sessions:**
Explicitly add to every task prompt: "After completing this task, append a LEARNING-ZONE entry if you encountered any error-fix pairs."

**Technique files are not being read:**
Add to the agent's task prompt: "Before starting, read `07-learning-hub/techniques/[relevant-file].md` and confirm you have read it."
