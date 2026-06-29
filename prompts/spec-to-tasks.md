# Spec → Dependency-Ordered Tasks

A prompt that turns a PRD, spec, or feature brief into a concrete, **dependency-ordered** task list — backend-first, each task small and verifiable, with explicit blockers. It produces an execution plan, not a wish list.

**When to use:** you have requirements but no plan. Run this before writing code to get the order right, then feed the result into [orchestrator-worker.md](orchestrator-worker.md) for parallel execution or work the list top-down yourself. Reads your project docs the same way rule [`00-global-architect`](../claude/rules/00-global-architect.md) does.

```
Turn the spec below into a dependency-ordered task list an engineering team (or agents) can
execute without further clarification. Plan backend-first: the schema and contracts are the
foundation everything else builds on. Do not write implementation code — produce the plan.

## Inputs
SPEC / PRD:
{{PASTE_SPEC_OR_LINK}}
PROJECT CONTEXT (optional): {{docs/ARCHITECTURE.md, DB_SCHEMA.md, API_SPEC.md}}
CONSTRAINTS (optional): {{deadline, must-not-break, stack limits}}

## Method
1. Extract every concrete deliverable from the spec. If a requirement is vague, list it under
   OPEN QUESTIONS rather than guessing — do not invent scope.
2. Order by dependency, backend-first: data model → migrations → services/business logic →
   API contracts → frontend → integration → tests → docs/deploy.
3. Make each task: small (verifiable in one review pass), independently testable, and owned by
   one layer. Split anything that spans layers.
4. Mark dependencies explicitly. A task may only depend on tasks listed above it.
5. Flag the riskiest tasks (irreversible migrations, contract changes, external integrations)
   so they get reviewed hardest.

## Output — TASK PLAN
  GOAL: <one line — what shipping this delivers>
  ASSUMPTIONS: <what you inferred to fill gaps — each one a risk if wrong>
  OPEN QUESTIONS: <must be answered before/while building; who decides>

  TASKS (in execution order):
    T1 [layer] <title>
       does: <concrete outcome>
       depends on: none
       done when: <objective, checkable criteria>
       risk: LOW | MED | HIGH
    T2 [layer] <title>
       depends on: T1
       ...

  CRITICAL PATH: <the task chain that gates the ship date — T1 → T4 → T9>
  PARALLELIZABLE: <tasks with no shared dependency that can run at once>

## Self-check
- Does every "depends on" point only to a task ABOVE it? Fix any forward reference.
- Is each "done when" objective enough that a reviewer could verify it without you?
- Did anything land in TASKS that should have been an OPEN QUESTION? Move it.
```

## How to use

1. Read **ASSUMPTIONS** and **OPEN QUESTIONS** first. These are where a wrong plan hides — resolve the open questions before building anything on the critical path.
2. Walk the **CRITICAL PATH** to sanity-check the ship estimate; it's the chain that can't be parallelized away.
3. Hand **PARALLELIZABLE** tasks to [orchestrator-worker.md](orchestrator-worker.md) to fan out across workers, each gated by [pr-review.md](pr-review.md).

## Why backend-first, dependency-ordered

The schema is the contract — frontend, APIs, and tests all assume it. Ordering tasks so the data model and contracts land first means downstream work builds on something stable instead of churning every time the foundation shifts. The forward-reference self-check guarantees the order is actually executable, not just plausible-looking.
