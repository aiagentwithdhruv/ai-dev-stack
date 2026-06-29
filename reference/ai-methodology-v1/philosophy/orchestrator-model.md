# The Orchestrator Model

There is a role in AI-assisted development that has no clean equivalent in traditional engineering. It's not the manager. It's not the tech lead. It's not the developer. It sits between the human and the builder agents — translating intent into precise instructions, reviewing output for drift, and owning quality gates without touching product code directly.

Call this role the Orchestrator.

---

## The Separation That Makes Everything Work

The orchestrator writes prompts. The orchestrator reviews git diffs. The orchestrator runs smoke checks. The orchestrator tags releases.

The orchestrator does not edit product code.

This separation is not a convention — it's a load-bearing constraint. Here's why.

When the orchestrator edits code directly, two things happen simultaneously:

1. The agent that was supposed to do the work loses track of what it owns.
2. The orchestrator loses the perspective required to verify the work.

You cannot review a commit you wrote yourself with the same eyes you'd use to review someone else's. You're too close to what you intended to see what actually landed. The person who writes the code is the worst person to catch its drift from the spec — not because they're careless, but because they remember the intent and unconsciously read the code through that lens.

The orchestrator's value comes from distance. Preserve it.

---

## The Team Structure

```
Human (Architect)
    |
Orchestrator (writes prompts, reviews, tags)
    |
    +-- Backend Specialist (FastAPI, schema, migrations, pytest)
    +-- Frontend Specialist (React, Vite, component logic)
    +-- DevOps Specialist (Docker, CI/CD, infrastructure)
    +-- Content Specialist (copy, brand, editorial)
    +-- QA Specialist (load testing, pre-launch, edge cases)
    +-- Senior DevOps (escalation — AWS, production incidents)
```

The specialists build. The orchestrator coordinates. The human approves.

No specialist communicates directly with the human for task assignment. Instructions flow through the orchestrator, which formats them as prompt files — self-contained, verifiable, replayable. Feedback flows back through structured reports that the orchestrator reads before the human sees them.

This is not bureaucracy. It's signal compression. The human shouldn't need to parse a 200-line git diff to know whether a feature landed correctly. The orchestrator reads the diff, curls the endpoint, confirms the spec match, and delivers a binary answer: verified clean, or here's what's wrong.

---

## What the Orchestrator Owns

**Owns:**
- Prompt files for every task (written before the specialist sees the task)
- Review of every commit before declaring it complete
- The 5-gate verification cycle (see `02-operating-model/5-anti-drift-gates.md`)
- Release tagging decisions
- Session state and handoff documentation
- Flagging scope creep before it lands in the codebase

**Does not own:**
- Writing `.py`, `.tsx`, `.sql`, `.yaml` product files
- Making architectural decisions without surfacing them to the human first
- Declaring a feature done without the human's browser confirmation
- Deciding what gets shipped — that authority stays with the human

---

## The Human's Role

The human is the architect, not the trigger.

The architect decides what gets built and why. The architect approves releases. The architect runs the final browser smoke test — the confirmation that real UI, real data, real interactions match the intent.

What the architect does not do: write 200-line prompts, chase file paths, debug line numbers, manage which agent is working on which file. That work lives with the orchestrator.

The architect's highest-value activities:
- Bringing requirements from stakeholders into the system
- Running 2-minute click-through smoke tests on finished features
- Deciding when a module is ready to demo to clients
- Catching intent drift — when the built thing technically works but isn't what was meant

When the architect is also chasing file paths, the orchestrator isn't doing its job.

---

## Why Parallel Capacity Requires This Model

A single orchestrator can coordinate 2 specialists simultaneously on non-overlapping files. When the backend specialist is writing a new API endpoint, the frontend specialist is building the corresponding UI component. The orchestrator has written both prompt files, verified the API contract between them, and is standing by to receive and review both reports.

Without the orchestrator model, the human coordinates both. That means serial execution — wait for backend, review it, brief the frontend, wait again. The elapsed time roughly doubles.

With the orchestrator: both prompts go out, both reports come back, the orchestrator cross-checks them against each other (does the frontend expect the exact fields the backend returns?), flags any mismatch before it hits integration, and delivers a single consolidated verification to the human.

The limit is 6 concurrent specialist sessions across 2 active products. Beyond that, drift compounds faster than review capacity. The orchestrator cannot verify 8 simultaneous diffs with the same rigour it can verify 4. Rigour is the constraint, not intelligence.

---

## Drift Prevention as the Core Function

Without an orchestrator, drift accumulates silently.

A specialist takes a prompt and executes it. If the prompt is slightly ambiguous, the specialist makes a reasonable assumption. That assumption may be correct — or it may diverge from spec in a way that doesn't surface until integration. By then, 3 more features have been built on top of the assumption.

The orchestrator's job at Gate 4 (orchestrator-side smoke) is to catch this before it compounds. Read the diff. Does the field name match the schema? Does the endpoint path match what the frontend is calling? Does the response shape match the Pydantic model? These are 30-second checks that prevent 3-hour debug sessions.

The production record: a project that ran without this model had ~30% drift between spec and shipped code, with 5-8 hour debug rounds for typical bugs. The same project, after adopting this model, ran at under 5% drift with sub-15-minute debug times. The code wasn't different. The review layer was.

---

## Crystallised Principle

**The orchestrator's value is the distance it maintains from product code. Collapse that distance and you lose the only reviewer who reads the diff with fresh eyes.**

Write prompts. Review output. Tag releases. Never touch product code. That separation is the whole model.
