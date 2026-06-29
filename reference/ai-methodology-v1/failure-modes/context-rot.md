# Context Rot

## What happens

A session runs long — 4 to 8 hours, dozens of exchanges. In hour 1, the orchestrator and human establish a constraint: "do not modify the existing auth flow." By hour 6, the orchestrator no longer holds that constraint in active context. It has been pushed below the attention threshold by the volume of subsequent exchanges. A new prompt is written that modifies the auth flow. The specialist implements it. The constraint is violated.

The code ships. The regression surfaces during the next smoke test or, worse, during client review.

## Why it happens

AI context windows have a fixed size. In long sessions, early instructions are either compressed by the model's attention mechanism or literally pushed out of the context window by subsequent content. The model is not "forgetting" in the human sense — it is working with a smaller effective window than the conversation history would suggest.

The problem is compounded when the constraint was stated conversationally ("by the way, don't touch X") rather than in a durable artefact (a rule file, a CLAUDE.md, a DO NOT block in the prompt).

## How it escalates

1. Constraint established verbally in hour 1.
2. Hours 2-5: productive work in unrelated areas.
3. Hour 6: a new task arises that is adjacent to the constrained area.
4. The orchestrator, no longer holding the constraint, writes a prompt that touches the constrained area.
5. The specialist implements correctly per the prompt.
6. The constraint is violated — but neither the orchestrator nor the specialist knows.
7. The regression is discovered at the next gate or by the human.

Born from: a session established that a particular module's tables were locked (shipped, in use by clients). Hours later, a migration was written that added a column to one of those tables. The migration broke a client's installation. The constraint had been stated once, conversationally, early in the session.

## Defence

**1. ACTIVE PROJECT header in every prompt.**

The first section of every agent prompt must state the current active module/task and any hard constraints that apply. This forces the constraint into the prompt's own context, independent of session length.

**2. Constraint-to-rule conversion.**

Any constraint established conversationally must be immediately converted to a durable artefact:
- A rule in the project's `04-rules/` directory
- A DO NOT section in the relevant CLAUDE.md
- A note in the session's checkpoint file

If it's not in a file, it doesn't exist for the next exchange.

**3. Session checkpoints every 30 minutes.**

Every 30 minutes (or after every 8 exchanges), the orchestrator writes a brief checkpoint:
```
Checkpoint [time]:
- Active task: [current task]
- Decisions locked: [list]
- Constraints in force: [list]
- Next action: [next prompt or task]
```

This checkpoint lives in a file (`/tmp/session-checkpoint.md` or project equivalent). If context compacts, the checkpoint survives.

**4. Re-read constraints before each new prompt.**

Before writing a prompt for a new task in a long session, the orchestrator re-reads the active CLAUDE.md and the session checkpoint. This catches any constraint that has faded from active attention.

**5. Prompt-level scope lock.**

Every specialist prompt includes a DO NOT block that explicitly lists what the agent must not touch, even if it looks related to the task. This makes constraints local to each prompt, not just to the session.
