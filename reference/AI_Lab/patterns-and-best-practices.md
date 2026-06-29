# Agent Teams — Patterns & Best Practices

## Team sizing

| Size | Best for | Tasks per teammate |
|------|----------|--------------------|
| 2–3 | Focused work, debate between perspectives | 5–6 |
| 3–5 | Most workflows (recommended default) | 5–6 |
| 5+ | Only when work genuinely benefits from scale | Diminishing returns |

**Rule:** 3 focused teammates usually beat 5 scattered ones. Start small, scale only when
parallel work adds real value.

```
Rough formula: teammates = ceil(N_independent_tasks / 5), capped at 5
               unless the tasks are truly independent.
```

## Task granularity — the Goldilocks zone

| Size | Problem | Example |
|------|---------|---------|
| Too small | Coordination overhead > benefit | "Add a semicolon to line 42" |
| Too large | Long stretches with no check-in; wasted-effort risk | "Rewrite the entire backend" |
| Just right | Self-contained, one clear deliverable | "Implement the auth endpoint with tests" |

A good task produces a clear deliverable (a function, a test file, a review report). Signals a
task is too big: a teammate works >15 min with no check-in. If the lead under-decomposes, tell
it "split the work into smaller pieces."

## The #1 failure mode: two teammates editing the same file

Prevent it structurally by assigning **ownership**, not by hoping:

1. **By file/module** — each teammate owns a disjoint set of files (`src/auth/`, `src/api/`, `tests/`).
2. **By layer** — frontend / backend / migrations+tests.
3. **Sequential for shared files** — if a file *must* be touched by two units, make those tasks
   dependent so they run in order, never concurrently.
4. **New files only** — for greenfield work, each teammate creates new files instead of editing
   existing ones.

## Prompting teammates

- **Give full context** — teammates don't inherit the lead's chat. Put file paths, stack facts,
  and the expected output shape into the spawn prompt.
- **Specify the model when it matters** — e.g. "use Sonnet for each teammate."
- **Steer the lead** with explicit instructions:

| Problem | Instruction to the lead |
|---------|-------------------------|
| Lead implements instead of delegating | "Wait for your teammates to complete their tasks before proceeding" |
| Lead shuts down too early | "Don't clean up until all teammates have reported their findings" |
| Teammates overlap | "Ensure each teammate works on different files — no overlapping ownership" |
| Need an approval gate | "Require plan approval before they make any changes" |
| Want approval criteria | "Only approve plans that include test coverage" |

## Communication patterns

- **Direct message** — targeted questions between two teammates ("have the frontend teammate ask
  the API teammate about the `/users` response format").
- **Broadcast** — to all teammates; use sparingly, cost scales with team size.
- **Adversarial debate** — spawn several teammates to chase different hypotheses, then compare —
  strong for debugging and decisions.

## Workflow patterns

1. **Parallel research → sequential synthesis** — N teammates investigate in parallel, then one
   synthesizes recommendations.
2. **Build + verify** — builders implement modules; a reviewer checks each, with review tasks
   *depending on* the build tasks.
3. **Competing implementations** — two teammates implement the same thing differently (e.g. Redis
   vs in-memory LRU cache), document tradeoffs, you pick the winner.
4. **Cross-layer feature** — frontend / backend / tests teammates, each owning their own directory.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Teams for simple tasks | Use a single session or subagents |
| Not pre-approving permissions | Set permission rules before spawning |
| Letting teams run unattended too long | Check in; redirect approaches that aren't working |
| Teammates editing the same files | Break work by file/module ownership |
| Starting with implementation | Start with research/review to learn the workflow |
| Too many teammates | Start with 3–5, scale only when justified |
| Vague spawn prompts | Include file paths, context, and the expected output format |
| Not using task dependencies | Mark dependent tasks so they aren't claimed prematurely |

## Getting-started progression

1. Research / review first — low risk, clear boundaries, shows parallel value.
2. Debugging with competing hypotheses — multiple angles, adversarial debate.
3. New-module implementation — each teammate owns separate files.
4. Cross-layer features — frontend + backend + tests in parallel.
