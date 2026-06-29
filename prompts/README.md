# prompts/ — Reusable Prompt Library

A library of copy-paste prompts for AI-native engineering work. Each file is a complete, production-tested prompt you can paste into Cursor, Claude Code, or any LLM chat — with a short **when to use** note so you pick the right one fast.

These are the working counterpart to the rules in [`../claude/rules/`](../claude/rules/) and the patterns in [`../foundations/`](../foundations/): rules tell the AI *how* to code, these prompts tell it *what job to do right now*.

## The prompts

| File | Job | When to reach for it |
|------|-----|----------------------|
| [agent-system-prompt.md](agent-system-prompt.md) | Stand up a capable, bounded agent | You're defining an agent's role, tools, output format, and scope |
| [orchestrator-worker.md](orchestrator-worker.md) | Decompose one big task into parallel workers | A task is too large/risky for a single pass |
| [spec-to-tasks.md](spec-to-tasks.md) | Turn a PRD/spec into a dependency-ordered plan | You have requirements but no execution order |
| [pr-review.md](pr-review.md) | Single adversarial reviewer, PASS/FAIL + evidence | Gating a diff before merge |
| [code-review-adversarial.md](code-review-adversarial.md) | Multi-critic verify, default-to-reject | High-risk change where a miss is expensive |
| [context-compact-handoff.md](context-compact-handoff.md) | Snapshot session state for a clean resume | Context is filling up, or you're handing off |
| [rag-answer.md](rag-answer.md) | Grounded answer with citations + "I don't know" | Answering strictly from retrieved sources |

## How to use these

1. **Open the file, copy the fenced prompt block.** Everything inside the ` ``` ` is the prompt — the prose around it is guidance for you, not the model.
2. **Fill the `{{PLACEHOLDERS}}`.** Each prompt marks its inputs in `{{DOUBLE_BRACES}}`. Leave none blank.
3. **Paste as the system prompt or the first message.** Prompts labeled *system prompt* (agent, RAG) belong in the system slot. The rest work as a first user message.
4. **Keep your project docs reachable.** Several prompts reference `docs/PRD.md`, `docs/ARCHITECTURE.md`, etc. — the same files the [`00-global-architect`](../claude/rules/00-global-architect.md) rule reads. See [`../docs/`](../docs/) for templates.

## Conventions used across all prompts

- **`{{PLACEHOLDER}}`** — a value you must supply before sending.
- **Scope boundary** — every agent/worker prompt states what it must *not* do. This is load-bearing, not decoration. Don't delete it.
- **Structured output** — review and orchestration prompts demand a fixed output shape so results are machine-parsable and diffable.
- **Default-to-reject** — verification prompts treat uncertainty as failure. Silence is not a pass.
- **Evidence over opinion** — findings cite `file:line` or a quoted snippet. "Looks fine" is not an allowed verdict.

## Composing prompts

These chain naturally:

```
spec-to-tasks       →  produces an ordered task list
  └─ orchestrator-worker  →  fans each task out to a worker (agent-system-prompt)
       └─ pr-review / code-review-adversarial  →  gates each result
            └─ context-compact-handoff  →  snapshots state before the next session
```

Start narrow. A single well-scoped agent prompt beats an elaborate orchestration you can't debug.
