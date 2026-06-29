# Agent patterns

Reusable structures for building reliable agents. They're composable — most production systems stack several. Read them before writing agent code; they decide your architecture more than your framework does.

Parent: [agents](../README.md) · Foundations: [model routing](../../../foundations/model-routing-cost/), [evals](../../../foundations/evals-testing/), [guardrails](../../../foundations/guardrails-security/)

## Orchestrator-worker

One **orchestrator** owns the goal and the plan; **workers** execute isolated subtasks and report back. The orchestrator decomposes, dispatches, collects, and integrates — it does not do the detailed work itself.

- Keep workers stateless and single-purpose; pass each one everything it needs.
- Give each worker an isolated workspace so parallel work never collides.
- The orchestrator owns shared state and the merge — workers never write to trunk directly.

Use it when work splits into independent units. It's the backbone of multi-agent systems.

## Fan-out / verify

Dispatch N workers in parallel, then **verify every result before accepting it.** Fan-out buys speed; the verify step buys correctness. The two are inseparable — parallelism without verification just produces wrong answers faster.

```
plan → fan-out to workers → collect → verify each → integrate the ones that pass
```

Verification can be deterministic (tests, schema checks) or a separate reviewing agent. Never let a worker's self-report be the gate.

## Adversarial verification

The checker is a **different** agent (or model) than the producer, with an explicit mandate to find fault: wrong premises, missed edge cases, security holes, drift from spec. Independence is the mechanism — a model reviewing its own output rationalises its own mistakes.

- Producer and verifier should not share the same context window.
- Give the verifier the spec and the *intent*, not just the diff.
- Treat a premise lifted from another agent's output as **unverified** until the verifier checks it against ground truth.

## Agent-as-markdown

Define an agent's role, tools, constraints, and operating procedure as a **plain-markdown file** — versioned, diffable, and reviewable like code. The same file loads the persona at the start of a session. Behaviour becomes an artifact you can edit and audit, not prompt text scattered across a codebase.

- One file per role; keep it short and specific.
- Change behaviour by editing the file, never by re-pasting instructions.
- Store the files in the repo so changes show up in review.

## Model-routing-per-role

Match the model to the job instead of paying top-tier rates for every call.

| Role | Routing heuristic |
|------|-------------------|
| Orchestrator / planner | Strongest reasoning model — the plan sets the ceiling |
| Bulk worker | Fast, cheaper model; the task is narrow and verified downstream |
| Reviewer / verifier | Strong model, independent from the producer |
| Classification / extraction | Smallest model that passes the eval |

Route on the task's difficulty and blast radius, and keep the routing in config so it's easy to retune as models and prices change. See [model routing & cost](../../../foundations/model-routing-cost/).

## How to use

Compose, don't pick one. A typical system: an orchestrator (strong model) fans out to bulk workers (cheap model) in isolated worktrees, an independent verifier (strong model) checks each result adversarially, and every role is defined as markdown in the repo. Back to [agents](../README.md).
