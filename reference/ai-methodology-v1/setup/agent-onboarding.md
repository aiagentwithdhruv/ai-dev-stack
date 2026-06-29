---
title: Agent Onboarding — Cold-Start Protocol
type: protocol
---

# Agent Onboarding — Cold-Start Protocol

## The cold-start problem

Every new Claude Code session is a blank slate. The agent has no memory of:
- What the project does
- What files exist and where
- What was built in previous sessions
- What rules apply
- What errors have been made and fixed
- What the current task is

A cold-start agent that receives only a task description will improvise. It will make file paths that look plausible but do not exist. It will choose patterns that seem reasonable but violate established project conventions. It will re-introduce bugs that were already fixed. This is not a limitation of the model — it is a calibration failure on the human side.

The onboarding protocol solves this by providing a structured context block at the start of every session. An agent that reads a complete WORKSPACE block knows as much about the project state as one that has been running for weeks.

---

## The WORKSPACE block

Every task prompt sent to a fresh agent must open with a WORKSPACE block. This is non-negotiable. An agent without this context will drift.

```
WORKSPACE
=========
Project: [project name]
Root: [absolute path to project root]
Branch: [current git branch, e.g., dev]
Dev servers: [list any running servers — "Backend: http://localhost:8000 | Frontend: http://localhost:3000"]

Key files:
- [.claude/CLAUDE.md] — project rules
- [agents/shared/SHARED-RULES.md] — shared agent rules
- [07-learning-hub/LEARNING-ZONE.md] — recent errors and fixes
- [07-learning-hub/daily/YYYY-MM-DD.md] — today's brief
- [relevant technique file if applicable]

Current state:
- [Last completed work: e.g., "Backend API for invoices is complete. Pytest passes 45/45."]
- [What is in progress: e.g., "Frontend invoice list page — started but not complete"]
- [What is blocked: e.g., "Payment integration blocked on API keys"]

READ BEFORE STARTING:
1. .claude/CLAUDE.md
2. agents/shared/SHARED-RULES.md
3. 07-learning-hub/LEARNING-ZONE.md
4. [any specific technique file relevant to today's task]

TASK
====
[task description starts here]
```

---

## Complete example — onboarding a backend specialist

```
WORKSPACE
=========
Project: invoice-manager
Root: /Users/alice/projects/invoice-manager
Branch: dev
Dev servers: Backend: http://localhost:8000 (uvicorn, running)
             Database: PostgreSQL on localhost:5432 (db: invoice_db)

Key files:
- .claude/CLAUDE.md — project rules (read first)
- agents/shared/SHARED-RULES.md — shared agent rules
- 07-learning-hub/LEARNING-ZONE.md — recent errors
- 07-learning-hub/techniques/deployment-aws-ecs.md (relevant today)
- backend/app/routers/ — existing API routes
- backend/app/models.py — SQLAlchemy models (source of truth for schema)
- backend/tests/ — pytest test suite (must pass before commit)

Current state:
- Clients module: complete, tested, deployed to dev
- Invoices module: GET /invoices and GET /invoices/{id} done
- POST /invoices and PATCH /invoices/{id} are next (this session)
- Frontend: not started yet — backend first

Recent errors (from LEARNING-ZONE):
- SQLAlchemy async session must use `async with` not `with` — causes runtime crash
- Pydantic v2: use model_validate() not parse_obj()

READ BEFORE STARTING:
1. .claude/CLAUDE.md
2. agents/shared/SHARED-RULES.md
3. 07-learning-hub/LEARNING-ZONE.md
4. backend/app/models.py — check schema before writing any route

TASK
====
Add POST /invoices endpoint:
- Accepts: client_id, line_items (list), due_date, notes
- Validates: client_id must exist in clients table
- Returns: created invoice with generated invoice_number (format: INV-YYYY-NNNNN)
- Writes a pytest test for success case + validation failure case
- Does NOT touch the frontend — backend only this session

Report back: files changed, command to run tests, what to test manually.
```

---

## The discipline behind the WORKSPACE block

### Current state is the most important field

"What was built before" saves the most time. Without it, the agent may re-implement something that already exists, or build on top of a foundation it does not know is there. The current state section answers: "Where does the agent enter the story?"

Be specific. "Invoice API is in progress" is less useful than "GET /invoices done. POST /invoices is the next endpoint."

### Read before starting — enforce it

List the exact files the agent must read before writing a single line of code. Agents that skip this step tend to violate project conventions within the first commit.

If an agent confirms it has read the files (via a brief acknowledgment before starting the task), trust it and proceed. If it skips straight to code output, stop the session and re-send with an explicit instruction: "Confirm you have read each of the four listed files before proceeding."

### Recent errors from LEARNING-ZONE

Pulling the 2-3 most recent LEARNING-ZONE entries into the WORKSPACE block is optional but high-value. It means the agent does not need to re-read the full LEARNING-ZONE — the most relevant context is already in front of it.

Only include errors that are relevant to today's task. An error from 3 weeks ago about a database query is not worth including in a session focused on frontend layout.

---

## Onboarding an orchestrator vs a specialist

Orchestrators and specialists have different context needs.

**Orchestrator onboarding:**

The orchestrator needs a wider view — project state across all modules, current sprint goals, which specialists exist and what they handle. Its WORKSPACE block is longer.

```
WORKSPACE — Orchestrator Session
=================================
Project: [name]
Current sprint: [sprint goal in one sentence]

Module status:
- [Module A]: complete
- [Module B]: in progress (backend done, frontend next)
- [Module C]: not started

Agents available:
- Backend specialist: handles FastAPI routes, database, tests
- Frontend specialist: handles React components, API integration

Today's goal: [what the orchestrator needs to coordinate or decide today]

Rules: .claude/CLAUDE.md + agents/shared/SHARED-RULES.md
```

**Specialist onboarding:**

Narrower focus. Only what is relevant to the specialist's domain. Do not flood a backend specialist with frontend context they will not use.

---

## First-task discipline

After the WORKSPACE block, the first task must be:

1. Scoped to one thing. Not "build the invoices module" — "add the POST /invoices endpoint with tests."
2. Concrete about expected output. Not "make it work" — "the endpoint must accept X, return Y, pass these tests."
3. Explicit about what is out of scope. "Do NOT touch the frontend this session." Agents expand scope unless told not to.

One scoped task per session is more productive than one large vague task per session. Precision compounds.

---

## After the session — feeding the learning hub

Before closing a session, ask the agent to report:

1. Files changed and why
2. Tests written and passing count
3. Any errors encountered and how they were resolved
4. Any open questions or risks for the next session

Take the errors and fixes from point 3 and add them to `07-learning-hub/LEARNING-ZONE.md` immediately. This is the closing ritual of every session. It takes 2 minutes and builds the compounding knowledge system one entry at a time.

---

## Quick-reference: session opening checklist

Before starting any agent session:

- [ ] Confirm git branch is `dev` (`git branch --show-current`)
- [ ] Confirm dev servers are running if needed
- [ ] Know the current state (what was finished last session)
- [ ] Have the WORKSPACE block written out
- [ ] Have the task scoped to one concrete deliverable
- [ ] Have the "do not" constraints written out (what is out of scope)

Send the WORKSPACE block and task. Wait for the agent to confirm it has read the required files. Then let it work.
