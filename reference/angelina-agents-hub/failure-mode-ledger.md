# Failure-Mode Ledger (the scar ledger)

Every time you lose time to an agent mistake, name it here with a **root cause** and a
**concrete defence**. Next time, the defence ships inside the prompt and the scar doesn't
repeat. This is the highest-leverage half of the session-archive loop.

## When a failure earns an entry

1. Observed **2+ times** (once = incident, twice = pattern).
2. Root cause identified — *why* it happens, not just the symptom.
3. The defence is concrete — a rule, a prompt line, or a tool config an agent can follow.
   "Be more careful" is not a defence.

## Entry format

```markdown
# Failure: [Name]

**First observed:** YYYY-MM-DD
**Most recent:** YYYY-MM-DD
**Occurrences:** N
**Severity:** P0 (blocks shipping) / P1 (>1h lost per occurrence) / P2 (nuisance)
**Source logs:** [link, link]

## What happens
[Concrete description, not abstract]

## Root cause
[Why it happens — specific]

## Defence (rule / prompt line / tool)
[The specific fix an agent can follow]

## Prompt addition (copy-paste)
```markdown
## CRITICAL (this failure recurs without this line):
[specific instruction]
```

## How to verify the defence works
[Observable — e.g. "this failure stopped appearing in the digest for N weeks"]

## Related failures
[Adjacent but distinct]
```

## Don't

- Don't log symptoms without root causes.
- Don't write "be more careful" — not actionable.
- Don't duplicate general LLM-agent failure modes you already track elsewhere; keep this
  to the failures *your* team actually hits.

---

## Generic seed failures (provider-neutral, reusable)

These show up on most multi-agent coding teams. Drop them in as candidates and promote to
full entries once you've seen them twice in your own logs.

### `render-vs-save-confusion`
**Symptom:** an agent produces output that works in a preview/response but never lands on
disk (or in the DB). **Root cause:** framework dual behavior — returning content inline
instead of writing a file/persisting. **Defence:** for any generator-type task, require
"verify the output file/row exists after the operation; don't trust the preview."

### `agent-works-out-of-lane`
**Symptom:** a specialist agent does work that belongs to another lane (e.g. a backend
agent writes a UI component). **Root cause:** the dispatch didn't pin the role, or the
DO-NOT list was vague. **Defence:** open every dispatch with the role boundary —
"You are the backend agent. Backend only. If this needs UI, STOP and ask for the frontend
agent to be dispatched."

### `agent-invents-api-shape`
**Symptom:** the frontend agent builds against an API shape that doesn't exist, breaking at
runtime once the real endpoint lands. **Root cause:** built without an API contract.
**Defence:** no frontend dispatch proceeds without either (a) a linked endpoint contract
(OpenAPI/types), or (b) the endpoint already merged.

### `parallel-agent-collision`
**Symptom:** two agents edit the same files in parallel and produce conflicting or
clobbering changes. **Root cause:** fan-out without file-ownership partitioning.
**Defence:** before fanning out, partition work by file ownership; one lane = one worktree;
never share a worktree across lanes.

### `context-compaction-drop`
**Symptom:** after a long session compacts/summarizes, the agent forgets a constraint it
was told earlier and regresses. **Root cause:** the constraint lived only in chat history,
not in a durable file. **Defence:** put load-bearing constraints in a file the agent
re-reads on resume (rules file / task contract), not just in the conversation.

### `silent-tool-failure`
**Symptom:** a tool call fails (timeout, empty result) and the agent proceeds as if it
succeeded. **Root cause:** no error check on the tool result. **Defence:** require the
agent to assert on tool output and stop on failure rather than continuing on a bad
assumption.

### `repeated-mistake-loop`
**Symptom:** the same fix is attempted, fails, and is attempted again unchanged.
**Root cause:** no record that the approach already failed. **Defence:** when an approach
fails twice, the agent must change strategy and log the dead end so the next session
doesn't retry it.
