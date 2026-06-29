# Session Management

Every agent session starts cold. No memory of prior conversations, no context from yesterday's decisions, no awareness of what's in progress. This is not a limitation to work around — it's a constraint to design for. Sessions designed for cold-start work correctly every time. Sessions that assume warm context fail in proportion to how much they assumed.

---

## Cold-Start Prompts

A cold-start prompt gives the agent everything it needs before it reads the first task instruction. It answers: where am I, what branch am I on, what's the shape of this project, and what can I never do.

**Minimum WORKSPACE block (8 lines max):**

```markdown
## WORKSPACE

- cwd: /absolute/path/to/project/root
- branch: dev (run: git checkout dev && git log --oneline -3 to verify)
- frontend: [path relative to cwd]
- backend: [path relative to cwd]
- dev server: [command — only if the task requires a running service]
- this prompt: [absolute path to this file — agent can re-read if context drifts]
- constraint: never push to [production remote] — local commits only
```

This block takes 30 seconds to write and prevents the class of failure where an agent operates on the wrong branch, the wrong directory, or the wrong remote. The failure mode is silent: the agent executes correctly, commits to the wrong place, and the work is lost or entangled.

A warm agent reads the WORKSPACE block in 3 seconds and moves on. The cost of including it for warm sessions is negligible. The cost of omitting it for cold sessions is a broken execution.

**Write every prompt for cold-start. The warm case is free.**

---

## Handoff Between Sessions

When a task spans multiple sessions (or multiple specialists), the handoff is the highest-risk moment. Context that lived in session A's conversation history doesn't transfer to session B. Decisions made in session A don't exist in session B unless they're written down.

**Minimum handoff documentation:**

1. Current git state: `git log --oneline -5` output
2. What's complete (with commit SHAs)
3. What's in progress (partial work, if any)
4. What's blocked and why
5. Any deviations from the spec that the next session should know about
6. The exact command to pick up (which file to read, which endpoint to curl, which test to run)

The orchestrator writes this. The handoff lives in a session state file, not in conversation — conversation is ephemeral. The file persists.

**Format:**

```markdown
# Session Handoff — [Date] — [Task Name]

## Git State
Current branch: dev
HEAD: [SHA] — [commit message]
Last stable tag: [tag name]

## Completed
- [TASK-01-backend]: endpoint live, pytest green, SHA [abc1234]
- [TASK-01-frontend]: component wired, vite build clean, SHA [def5678]

## In Progress
- [TASK-02-backend]: migration written, endpoint not yet wired — partial at [file:line]

## Blocked
- [TASK-03]: waiting for confirmation of [specific field name from stakeholder]

## Deviations from Spec
- Used `remarks` instead of `notes` — actual DB column name (spec is wrong here)

## Next Action
Open fresh session → paste: [absolute path to next prompt file]
```

---

## Reuse the Same Worker Chat for Continuity

When a specialist session is in progress on a task, continue it in the same chat if possible. Don't open a new session for every small follow-up or hotfix within the same task.

The same session has:
- The git state the agent already verified
- The files it's already read (implicit context in the active window)
- The deviations it already flagged (visible in conversation history)

A fresh session for a small follow-up requires re-establishing all of this. For a 5-line hotfix, that overhead can be larger than the fix itself.

**Rule:** same task, same session. New task (different feature, different scope), new session.

**Exception:** if the current session has exceeded its useful context window (signs: agent starts contradicting earlier decisions, loses track of file paths it knew 20 messages ago), open a fresh session with a cold-start prompt and the handoff doc. Don't try to rescue a context-exhausted session.

---

## State Checkpoints for Long Tasks

Any task expected to take more than 30 minutes of agent execution should include explicit checkpoint instructions. Checkpoints protect against session crashes, context exhaustion, and network failures.

**Checkpoint instruction (in the prompt file):**

```markdown
## Checkpointing

Every 30 minutes or after completing each numbered stage:
1. Commit current state with message: `wip(scope): checkpoint [stage number] — [one line of what's done]`
2. Write checkpoint summary to /tmp/task-checkpoint.md:
   - What's done (with commit SHA)
   - What's next
   - Any deviations or blockers found
3. Continue to next stage

If session crashes or context runs out: the human can start a fresh session pointing at this prompt file + /tmp/task-checkpoint.md
```

This costs the agent 2 minutes per checkpoint. It turns a session crash from "rebuild from scratch" into "read checkpoint, resume from stage N."

**Checkpoint files live in `/tmp/` by convention** — they're temporary, per-task, not committed to the repository. If a task completes cleanly, the checkpoint file is discarded. If recovery is needed, it's there.

---

## Session State for the Orchestrator

The orchestrator holds the state across all active specialist sessions. This is the orchestrator's most important operational function.

At any point, the orchestrator should be able to answer:
- What is each active specialist session working on?
- What's the HEAD commit on each active branch?
- Which Gates have been cleared for the current task?
- What's the next action for each session?

This state lives in a running session document, updated after each Gate 4 verification:

```markdown
# Active Session State — [Date]

## Backend Session
Task: TASK-02-backend
Status: Gate 3 complete, awaiting Gate 4
HEAD: [SHA]
Next: orchestrator runs Gate 4 smoke, then writes click-script for human

## Frontend Session
Task: TASK-02-frontend
Status: Gate 4 complete, human smoke pending
HEAD: [SHA]
Next: human runs click-script at [path], reports result

## Blocked
TASK-03: waiting for [specific blocker, who owns resolving it]
```

When a session completes, it's removed from this document. When a new session starts, it's added. The document is the orchestrator's working memory — not perfect, but good enough to coordinate 6 sessions without losing track of any of them.

---

## Crystallised Principle

**Design for cold-start. Assume nothing persists between sessions except what's written to a file.**

Conversation history is ephemeral. Git commits are durable. Prompt files are durable. Checkpoint files are durable. Build your handoffs around durable artifacts, and session boundaries stop being crises.
