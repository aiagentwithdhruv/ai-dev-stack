# Context Compact / Session Handoff

A prompt that snapshots the current session into a compact, durable brief so a fresh session — or a different person — can resume without re-deriving everything. It captures state, next steps, and open questions, and deliberately drops the noise.

**When to use:** the context window is filling up, you're ending the day mid-task, or you're handing work to another session/agent. Run it *before* you compact or close, while the full history is still in context. The output becomes the first message of the next session.

```
Produce a HANDOFF BRIEF that lets a fresh session resume this work with zero loss of
necessary state and zero re-reading of this conversation. Be ruthless about signal: include
what the next session MUST know, drop everything it can re-derive cheaply.

## Rules
- Write for a competent stranger, not for me. Spell out names, paths, and decisions — no "as
  discussed", no unexplained pronouns.
- Facts only. If something is assumed or unverified, label it.
- Reference real artifacts by path and identifier (file:line, branch, ticket, command).
- Prefer a short list of load-bearing facts over a long narrative.
- Do NOT include dead ends we already abandoned, except as a one-line "don't retry X because Y".

## Output — HANDOFF BRIEF
  TASK: <the goal in one or two sentences — what "done" means>

  STATE NOW: <where things actually stand — what's built, merged, passing, deployed>

  DONE THIS SESSION:
    - <concrete result> (artifact: file/branch/command)
    - ...

  IN FLIGHT: <work started but not finished, and exactly where it stopped>

  NEXT STEPS (ordered):
    1. <the very next action, concrete enough to start immediately>
    2. ...

  OPEN QUESTIONS / BLOCKERS:
    - <decision needed or dependency waited on — and who/what unblocks it>

  KEY FACTS TO CARRY:
    - <paths, commands, IDs, config, env, conventions the next session needs>

  DON'T REDO: <approaches already tried and rejected, one line each, with the reason>

## Self-check
- Could someone who never saw this chat execute NEXT STEPS #1 right now? If not, add detail.
- Did you smuggle in any "as we said" references? Replace with the actual fact.
```

## How to use

1. Run this as the **last** action of a session, before `/compact` or before closing — you need the full history in context for it to be accurate.
2. Save the brief (paste it into a handoff file, a ticket, or the project's running context doc).
3. Start the next session by **pasting the brief first**, then your next instruction. The new session boots with exactly the state it needs and nothing it doesn't.

## Why this beats raw auto-compaction

Automatic context compaction summarizes by recency and volume — it keeps what was said a lot, not what matters. A handoff brief is **intent-shaped**: it keeps the task, the live state, and the next action, and explicitly discards abandoned paths. The `DON'T REDO` line is what stops the next session from cheerfully re-walking a dead end you already ruled out.

Pairs with [orchestrator-worker.md](orchestrator-worker.md) for multi-session work: each worker hands off with this, the orchestrator stitches the briefs together. See also the session-hygiene patterns in [`../foundations/`](../foundations/).
