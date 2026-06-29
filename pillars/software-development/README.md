# Software Development — AI-assisted SDLC

AI as the engineer in the loop, end to end: from spec to shipped code. The model does the typing; **deterministic gates and an independent reviewer decide what merges.** That one principle is what separates AI-assisted engineering from prompt-and-pray.

This pillar assumes the [foundations](../../foundations/) (model selection, [prompting & context](../../foundations/prompting-context/)) and the repo's engineering [rules](../../rules/) are already loaded. Those are the *standards*. This is the *process* that applies them.

## The loop

```
spec → plan → implement → verify → review → integrate → learn
```

Each stage has an owner and an exit condition. Nothing advances on vibes — every gate is either machine-checkable or signed off by a second party.

| Stage | What happens | Exit condition |
|-------|--------------|----------------|
| **Spec** | Capture intent as a PRD/spec with acceptance criteria | Criteria are testable, not aspirational |
| **Plan** | AI proposes an approach + impact analysis before writing code | A human or lead approves the plan |
| **Implement** | One task at a time, in an isolated workspace | Task complete, criteria met |
| **Verify** | Lint, type-check, build, tests — the deterministic floor | All green, no skips |
| **Review** | A *different* agent or human reviews adversarially | Findings resolved |
| **Integrate** | Merge to trunk | Trunk stays releasable |
| **Learn** | Capture what broke; feed it back into the rules | Lesson recorded |

The full, reusable version of this loop — with worktrees, task graphs, and the verify floor — is in **[pipeline/methodology.md](./pipeline/methodology.md)**.

## The four AI leverage points

AI earns its keep at four specific points in the SDLC. Use it deliberately at each:

1. **Spec-driven development** — turn a rough intent into a structured spec with explicit acceptance criteria *before* any code. The spec becomes the contract the implementation and the tests are both checked against.
2. **Code generation** — generate against the spec and the repo's existing patterns, not from a blank prompt. Extend conventions; don't invent new ones.
3. **AI review** — a second model reviews the diff for correctness, security, and drift from the spec. Independence matters: the reviewer must not be the author.
4. **Test generation** — derive tests from acceptance criteria, not from the implementation (which only encodes the bugs you already wrote). Tests are the deterministic floor every change clears.

## Checklist

- [ ] Durable rules / constitution file present and loaded every session
- [ ] Spec written with **testable** acceptance criteria before coding
- [ ] AI proposes a plan + impact analysis; a human approves before implementation
- [ ] Work happens in an isolated workspace per task — no shared scratch
- [ ] Deterministic floor (lint + types + build + tests) passes before review
- [ ] Review performed by a different agent or human than the author
- [ ] Trunk stays releasable after every merge
- [ ] Every non-trivial bug becomes a new rule or test ([evals](../../foundations/evals-testing/))

## How to use

Read this page for the shape of the loop, then go to [pipeline/methodology.md](./pipeline/methodology.md) for the step-by-step method you can drop onto any project. For multi-worker execution (orchestration, fan-out), continue to the [agents](../agents/) pillar.
