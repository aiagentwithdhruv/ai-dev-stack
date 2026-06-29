# Switch 5 — Session Checkpoints

> **Status:** DEFERRED
> **Build only if:** a real session-crash incident occurs where context is lost mid-task
>   and the cost of reconstruction exceeds 30 minutes.
> **Do not build speculatively.** This is documented so the design is ready when needed.

---

## The Problem This Solves

Long-running tasks (>30 minutes) risk session context loss if the conversation is
accidentally closed, the process crashes, or the session times out.

Without a checkpoint, the next orchestrator session must reconstruct:
- Current branch and tip SHA
- What was committed, what is staged, what is in progress
- Open questions that were mid-resolution
- Which gate was reached

This reconstruction takes 15-45 minutes and is error-prone.

---

## The Design (implement when triggered by a real incident)

Every 30 minutes during an active task, the orchestrator writes a checkpoint file:

**Path:** `/tmp/{PROJECT_SLUG}-session-state-{TIMESTAMP}.md`

**Contents:**

```markdown
# Session Checkpoint — {TIMESTAMP}

**Project:** {PROJECT_NAME}
**Branch:** {BRANCH}
**Tip SHA:** {SHA}
**Current prompt:** {PROMPT_CODE} — {PROMPT_TITLE}
**Gate reached:** Gate {N}

## Commits so far (this task)
- {SHA_1}: {MESSAGE_1}
- {SHA_2}: {MESSAGE_2}

## Test status
- Build: {PASS | FAIL | NOT_RUN}
- Regression smoke: {N}/{TOTAL} PASS | NOT_RUN
- Feature smoke: {PASS | FAIL | NOT_RUN}

## Open questions (unresolved at checkpoint)
- {QUESTION_1}
- {QUESTION_2}

## Next action (if session resumes)
{ONE_SENTENCE describing exactly where to pick up}
```

**On resume:** the next orchestrator session reads the checkpoint and announces:
"Resuming {PROMPT_CODE} from checkpoint at Gate {N}. {N} commits made. Next: {ACTION}."

---

## Implementation notes

- `/tmp/` is the right location — intentionally ephemeral, does not pollute the repo.
- Keep only the most recent checkpoint per session. Overwrite on each write.
- If the task completes cleanly, delete the checkpoint file at the end of Gate 5.
- This switch interacts with Gate 2 (atomic commits) — if commits are truly atomic,
  reconstruction from `git log` alone may be sufficient without checkpoints.
  Evaluate that first before building this switch.

---

## Why DEFERRED

Building this speculatively adds process overhead for a problem that may not occur
in practice. If commits are truly atomic and the REPORT format is followed,
`git log --oneline -20` usually provides enough context to resume without a checkpoint.

The cost of building this prematurely: orchestrators start writing checkpoints as
a ritual, adding 1-2 minutes per interval without any real session-crash to recover from.

**Trigger condition:** a real session-crash incident where reconstruction takes >30 minutes.
Document the incident, then implement this switch targeting the specific failure mode.
