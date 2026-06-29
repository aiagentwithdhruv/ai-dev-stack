# reference/AI_Lab

**Origin:** Distilled from a standalone public companion repo ("AI Agent Teams Lab") — a
collection of copy-paste prompts that turn Claude Code into coordinated **multi-agent teams**
using Claude Code's native agent-teams feature (Team Lead + Teammates + shared task list +
mailbox).

**Why it lives here (vs. the flagship's own `prompts/`):** the flagship's
[`prompts/orchestrator-worker.md`](../../prompts/orchestrator-worker.md) is a single
orchestrator prompt that *emits* worker prompts for you to dispatch one at a time. This
reference instead documents the **native Claude Code agent-teams runtime** — where the lead
spawns persistent teammates that self-claim tasks from a shared list and message each other —
plus the team-design patterns and ready-to-adapt team archetypes. Different mechanism, complementary.

## What's here

| File | What it gives you |
|------|-------------------|
| `agent-teams-architecture.md` | The runtime: team lifecycle, task states/dependencies/claiming, display modes, permission inheritance, communication mechanisms, limitations, troubleshooting |
| `patterns-and-best-practices.md` | Team sizing, task granularity, the file-conflict ownership rule, communication patterns, workflow patterns, common mistakes |
| `custom-agent-definitions.md` | Reference for defining custom agents (Markdown + YAML frontmatter): every frontmatter field, tool allow/deny lists, spawnable-subagent restriction |
| `team-hooks.md` | Team-specific lifecycle hooks (`TeammateIdle`, `TaskCompleted`) for enforcing quality gates before an agent idles or marks a task done |
| `team-prompt-templates.md` | Four condensed multi-agent team archetypes (build / research / publish / security audit) — roster + handoff graph + deliverables, ready to adapt |

## Sanitization note

The source repo was already public and MIT-licensed; its content is about the generic Claude
Code agent-teams feature, with no proprietary, client, or internal material. During folding the
following were dropped as non-reusable or identifying:

- The author's GitHub handle, clone URLs, and "Built by …" attribution line.
- The two bulky **example outputs** shipped with the source (a full generated "TaskFlow" app and
  a full generated market-research report) — these are demo artifacts, not reusable patterns. Only
  the *prompt skeletons that generate such outputs* are kept, in `team-prompt-templates.md`.
- Repo-specific badges, banner image, and index/marketing prose.

Tool/field names (e.g. `permissionMode`, `TeammateIdle`) reflect the feature as documented at the
time of extraction; verify against current Claude Code docs before relying on exact flags.
