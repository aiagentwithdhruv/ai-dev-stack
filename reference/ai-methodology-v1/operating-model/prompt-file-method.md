# The Prompt-File Method

There is one workflow that outperforms inline conversation prompts, verbal briefings, and direct agent coordination. It's also the simplest: write the task as a standalone markdown file, point the agent at the file, receive a structured report, verify, move forward.

The prompt file is the unit of work.

---

## Why Markdown Files, Not Conversation

When you prompt an agent inside a conversation, the task inherits all the ambiguity of the conversation — unstated assumptions, context from 40 messages ago, things that were decided but never written down. The agent guesses at gaps. The gaps compound.

When you write a prompt file, you're forced to make the task self-contained. Every file path is explicit. Every constraint is stated. Every DO-NOT is written. The agent executing the file doesn't need to read your conversation history. It reads one file and executes.

Additional properties that matter:

**Git-able.** The prompt file lives in the repository. It can be diffed, reverted, reviewed. You can see exactly what instruction was given when a bug traces back to a bad prompt.

**Replayable.** If an agent session crashes mid-task, you don't reconstruct the prompt from memory. You point a fresh session at the same file.

**Diff-able.** When you update a prompt for a follow-up task, the diff shows exactly what changed — which means you can review whether the change is complete and correct before dispatching.

**Cold-start readable.** An agent with zero prior context can execute a well-written prompt file. This is the key property. Every session is effectively cold-start. Design for cold-start.

---

## The Workflow

```
1. Orchestrator writes prompt file → saves as .md in the project's prompts directory
2. Orchestrator tells human: "Paste this file to a fresh agent session: [path]"
3. Human opens new agent session → pastes file contents → agent executes
4. Agent commits → returns structured report (SHA, files changed, build status, deviations)
5. Human pastes agent report to orchestrator session
6. Orchestrator verifies (reads diff, curls endpoint, checks spec match) — 1-2 minutes
7. Orchestrator gives human specific smoke steps (numbered, under 2 minutes)
8. Human runs smoke → confirms or reports failure
9. Orchestrator tags release if confirmed, or writes targeted hotfix prompt if not
10. Orchestrator prepares next prompt file → loop repeats
```

The human's role in this loop is narrow: paste the file path, paste the report, run the smoke, confirm or report. The human is the product owner and the final tester. Not the debugger, not the prompt writer, not the git operator.

---

## Prompt File Structure

Not every prompt needs all sections. Simple hotfixes skip 4-6 of them. But the structure is consistent — agents know where to look.

```markdown
# [Task Title] — [Agent] — [Batch ID if applicable]

**Scope:** what this prompt covers
**Budget:** estimated lines to change (e.g., "≤80 lines")
**Prior state:** which tag or commit SHA this builds on
**Assignee:** which specialist should execute this

## WORKSPACE
[cwd, branch to check out, frontend/backend paths, how to start dev servers, location of this file]

## 1. Agent Rules
[who you are, what you can touch, what you absolutely cannot touch]

## 2. Git Hygiene
[checkout [branch], verify HEAD is at [SHA], use explicit git add paths — never git add -A]

## 3. Context
[what the orchestrator has pre-verified: API shapes, DB state, upstream dependencies]

## 4. Exact Edits
[file paths, line numbers or function names to find, what to change]

## 5. DO NOT
[explicit list of what to leave untouched — at least 3 items]

## 6. Verify Locally
[commands to run before committing — pytest, vite build, curl the new endpoint]

## 7. Acceptance Criteria
[numbered, testable conditions — the agent checks these before writing the report]

## 8. Commit Message
[pre-written — agent fills in SHA and file count]

## 9. Reply Template
[structured format the agent fills in — SHA, files, build status, deviations from spec]

## 10. Out of Scope
[what's deferred — this protects against scope creep mid-execution]
```

---

## The Reply Template (Section 9)

The reply template is what makes verification fast. Without it, the orchestrator reads a paragraph of prose and has to extract the relevant facts. With it, the information is in the same location every time.

Minimum required fields:

```
Done. Commit [SHA] on [branch].

1. Commit — [files changed, line count]
2. Build checks — [pytest result] / [vite build result]
3. Edit inventory — [what changed, where]
4. Deviations from spec — [list, or "None"]
5. Ready-for-orchestrator-verify: GO.
```

Deviations are expected and not failures. An agent might choose a better variable name, a smaller diff, or a safer pattern than the prompt specified. The deviation section captures these so the orchestrator can evaluate them — accept the improvement, or flag it as unintended drift.

---

## WORKSPACE Block (Always First)

Every prompt file opens with a WORKSPACE block. It takes under 8 lines. It carries everything a brand-new agent session needs to orient itself.

```markdown
## WORKSPACE

- cwd: /path/to/project/root
- branch: dev (git checkout dev && verify HEAD at [SHA])
- frontend: [subfolder path]
- backend: [subfolder path]
- dev server: [command to start, if the task requires a running server]
- this file: [path to this prompt, so agent can re-read if needed]
- never push to [remote] — local commits only until orchestrator confirms
```

A warm agent (continuing from a previous session) already has this. A cold agent doesn't. Write for cold-start. The warm agent reads it in 3 seconds and moves on. The cold agent needs it.

---

## Naming Convention

Prompt files in a directory should be scannable at a glance.

```
prompts/
  TASK-01-backend.md          — single task, backend agent
  TASK-02a-backend.md         — Task 2 Part A, backend
  TASK-02b-frontend.md        — Task 2 Part B, frontend
  TASK-03-hf1-backend.md      — Task 3 hotfix 1, backend
```

The pattern: task identifier → part indicator if staged → agent. Readable without opening the file.

---

## What the Orchestrator Does Before Writing the Prompt

The prompt file reflects work the orchestrator has already done — not work it's delegating to the agent.

Before writing a prompt for a backend endpoint:
- Curl the upstream API or check the database schema to confirm field names
- Read the existing service file to know what patterns are already in use
- Count the estimated line change to set the budget

Before writing a prompt for a frontend component:
- Read the existing component that most resembles the target
- Verify the backend endpoint the component will call (field names, response shape)
- Note the sibling pattern the new component should mirror

This pre-work takes 5-10 minutes. It eliminates the most common class of agent errors: assuming a field name, assuming a file location, assuming a pattern that isn't actually used. Pre-verification is not optional — it's what makes the prompt file executable.

---

## Crystallised Principle

**The prompt file is the unit of work. Not a conversation turn, not a ticket, not a verbal briefing. One file that carries everything an agent needs to execute, verify, and report back — without asking questions.**

If an agent needs to ask questions to execute the prompt, the prompt is incomplete. Write it until the agent can execute silently.
