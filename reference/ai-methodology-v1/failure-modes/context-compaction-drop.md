# Context Compaction Drop

## What happens

A long session approaches the context window limit. The system (or the agent) compacts the session: earlier exchanges are summarised into a shorter representation. The summary captures the general shape of what happened but loses specifics — exact field names, exact constraints, exact schema decisions.

The session continues. The agent makes a decision based on the summarised state. The summarised state is wrong. The decision is wrong. The commit is wrong.

## Why it happens

Compaction is a necessary mechanism when sessions are long. It is not a flaw — it is a trade-off. The trade-off is: the further you are from the original exchange, the less precise your representation of it is.

The problem occurs when:
- A critical specific (an exact field name, an exact constraint, an exact agreed-upon value) was stated once early in the session
- That specific was not written to a durable file
- Compaction summarises the early exchange into "agreed on the schema for module X" without capturing the specific value

The agent now has the summary but not the specific. The next time the specific is needed, the agent either guesses or uses a different value.

## How it escalates

1. Hour 1: human and orchestrator agree on an exact value (a schema field name, a validation rule, a UI label).
2. Hours 2-5: work continues in other areas.
3. Hour 5: compaction occurs. The agreement is summarised as "schema discussed."
4. Hour 6: the exact value is needed again. The agent recalls "schema discussed" but not the value.
5. The agent uses a slightly different value. The new value conflicts with code written in hour 2 that used the original value.
6. Integration fails. The root cause is hard to trace because the disagreement is between an early decision and a later implementation.

Born from: a session established exact field names for a new module early in the sprint. After compaction, the orchestrator wrote a follow-up prompt using slightly different field names. The specialist implemented both sets of names in different files. The integration test found the mismatch. Tracing it required reading commit history from before the compaction.

## Defence

**1. Pre-compaction checkpoint file.**

When approaching the context limit (at ~80% usage, or before any long-running task in a lengthy session), write a checkpoint:

```markdown
# Session checkpoint — [timestamp]

## Active task
[current task, module, prompt]

## Decisions locked
- [field_name] = "[exact value]" (confirmed [time])
- [constraint] = "[exact specification]" (confirmed [time])

## State
- Branch: [branch]
- Last commit: [SHA]
- Next action: [what happens after this]

## Do not override without re-confirming
- [specific value 1]
- [specific value 2]
```

Save to `/tmp/session-checkpoint.md` or equivalent. This file survives compaction.

**2. Orchestrator reads checkpoint on wake.**

After compaction (identifiable by the agent's loss of specific detail), the orchestrator reads the checkpoint file before proceeding. This restores the specific values that compaction summarised away.

**3. Exact values go into durable artefacts immediately.**

Any agreement on an exact value (field name, constraint, configuration value) is immediately written to:
- The spec file
- The schema file
- The CLAUDE.md for the module

Not just stated in chat. Written to a file. A value that only exists in the conversation is a value that is one compaction away from being lost.

**4. Acknowledge compaction explicitly.**

If the agent notices it has lost specifics (asking for a value that was confirmed earlier, or using a different value than before): stop, acknowledge the compaction, and ask the human to re-confirm the specific before continuing.

Do not guess. Do not use a "similar" value. Re-confirm.

**5. Keep sessions scoped.**

A session that runs 8 hours without a checkpoint is a session that will compact. Break long sprints into bounded sessions (2-3 hours each) with a proper handover at the end of each:
- Write the checkpoint
- Commit current state
- Start a fresh session that reads the checkpoint

Shorter sessions are less likely to compact and easier to recover from when they do.
