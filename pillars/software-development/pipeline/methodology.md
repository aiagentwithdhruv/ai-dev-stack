# A reusable end-to-end AI development pipeline

A vendor-neutral method for shipping production code with AI in the loop. It works with a single coding agent or a fleet of them, on any stack. The pipeline rests on one non-negotiable idea: **AI proposes; deterministic checks and an independent reviewer dispose.**

Use it whole, or lift individual stages. Each stage names a *gate* — the condition that must hold before work advances.

## Overview

```
constitution → spec → task graph → isolated worktree → plan gate
   → implement one task → verify floor → independent review → integrate → retro
```

## The stages

### 1. Constitution file
A durable, version-controlled file the AI reads at the start of every session: architecture, conventions, security rules, a "never do" list, and pointers to the spec docs. It is the project's standing law — short, specific, amended only deliberately.
**Gate:** present in the repo and loaded into context before any task begins.

### 2. Spec / PRD
Translate intent into a written spec with **testable acceptance criteria**. Vague goals ("make it fast") become measurable ones ("p95 < 200ms on the seed dataset"). The spec is the contract that both the implementation and the tests are judged against.
**Gate:** every requirement has an observable pass/fail condition.

### 3. Task graph
Decompose the spec into small, ordered tasks with explicit dependencies. Each task should be independently implementable and verifiable, and small enough to review in one sitting. Mark which tasks can run in parallel.
**Gate:** no task depends on an unstated artifact; the critical path is visible.

### 4. Isolated worktree per worker
Each task is implemented in its own isolated workspace — a separate branch or worktree — so parallel work never collides on shared files. One task, one workspace, one branch. This is what makes fan-out safe.
**Gate:** workspaces are independent; no two workers write the same file on the same branch.

### 5. Plan-approval gate
Before writing code, the worker produces a short plan: the approach, the files it will touch, and an **impact analysis** of what could break (hidden consumers, migrations, contracts). A lead — human or orchestrator — approves or redirects. This is the cheapest place to catch a wrong premise.
**Gate:** plan reviewed and approved; risky assumptions verified against the real codebase, not asserted.

### 6. Implement one task
The worker implements exactly one task to completion, extending existing patterns rather than inventing new ones. Finish before starting the next. Resist scope creep — anything discovered becomes a new task in the graph, not an inline detour.
**Gate:** acceptance criteria for *this* task are met; unrelated files untouched.

### 7. Deterministic verify floor
A fixed, machine-checkable set of gates every change clears with **zero skips**: format, lint, type-check, build, and tests. It is deterministic on purpose — no judgement, no negotiation. If the floor is red, the task is not done.
**Gate:** all checks green. A skipped check is a failed check.

### 8. Independent review
A *different* agent or human reviews the diff adversarially — for correctness, security, drift from the spec, and reuse opportunities. The author never reviews their own work; independence is the whole point.
**Gate:** review findings resolved, or explicitly accepted with a rationale.

### 9. Integrate
Merge to trunk in small increments, keeping trunk releasable at all times. Prefer many small merges over one large one. After integration, the next dependent task in the graph unblocks.
**Gate:** trunk builds and passes the verify floor post-merge.

### 10. Retro / learning-loop
Capture what broke and why. Every non-trivial bug becomes a new rule in the constitution or a new test in the floor, so the same mistake can't recur. The pipeline compounds — each pass makes the next one safer.
**Gate:** lesson recorded where the next session will read it.

## Why each gate exists

| Failure mode | Stage that prevents it |
|--------------|------------------------|
| AI ignores project conventions | Constitution file |
| "Done" is subjective | Testable acceptance criteria |
| Parallel work corrupts shared files | Isolated worktrees |
| Confident code built on a wrong premise | Plan-approval + impact analysis |
| Regressions slip to trunk | Deterministic verify floor |
| Author can't see their own blind spots | Independent review |
| The same bug recurs forever | Retro / learning-loop |

## How to use

Adopt the whole pipeline for non-trivial work. For small, low-risk fixes, fold stages 4–5 (dedicated worktree, formal plan gate) into the implement step. The two stages you never skip regardless of size: the **verify floor** (7) and an **independent look** (8). Everything else scales with risk.

For multi-worker execution of this pipeline, see the [agents](../../agents/) pillar — [orchestrator-worker and fan-out/verify](../../agents/patterns/) are exactly the patterns that drive stages 4–8 at scale. For the *standards* this pipeline enforces, see the engineering [rules](../../../rules/) and [foundations](../../../foundations/).
