# Agent Teams — Runtime Architecture

How Claude Code's native multi-agent teams actually run: one **Team Lead** (your active
session) spawns persistent **Teammates** (separate Claude Code instances, each with its own
context window) that coordinate through a shared task list and a mailbox.

## Core components

| Component | Role | Storage |
|-----------|------|---------|
| **Team Lead** | Main session. Creates the team, spawns teammates, assigns/coordinates work, synthesizes results. | Your active session |
| **Teammates** | Separate Claude Code instances, each with its own context window. | Spawned as child processes |
| **Task list** | Shared work items teammates claim and complete. | `~/.claude/tasks/{team}/` |
| **Mailbox** | Inter-agent messaging, delivered automatically. | Automatic |
| **Team config** | Member registry (names, agent IDs, agent types). | `~/.claude/teams/{team}/config.json` |

## Lifecycle

```
1. User requests a team (or the lead proposes one, user confirms)
2. Lead creates team config + shared task list
3. Lead spawns teammates  (each loads CLAUDE.md, MCP servers, skills — NOT the lead's chat history)
4. Lead assigns tasks  OR  teammates self-claim from the shared list
5. Teammates work independently, message each other as needed
6. Lead monitors progress, synthesizes results
7. User asks the lead to shut teammates down
8. Lead cleans up team resources
```

## Task system

**States:** `pending` → `in_progress` → `completed`.

**Dependencies:** a pending task with unresolved dependencies cannot be claimed until those
complete; the system unblocks it automatically. Use dependencies to force ordering (e.g. a
review task that depends on the build task it reviews).

**Claiming:**
- *Lead assigns* — tell the lead which task goes to which teammate.
- *Self-claim* — after finishing, a teammate picks up the next unassigned, unblocked task.
- *Concurrency-safe* — file locking prevents two teammates claiming the same task.

## Context & communication

**At spawn, a teammate gets:** project context (`CLAUDE.md`, MCP servers, skills) + the lead's
spawn prompt. It does **not** get the lead's conversation history — so put everything the
teammate needs (file paths, constraints, expected output shape) into the spawn prompt.

**Mechanisms:**

| Mechanism | Description |
|-----------|-------------|
| Automatic delivery | Messages between agents arrive without the lead polling. |
| Idle notifications | A teammate that finishes and stops auto-notifies the lead. |
| Shared task list | All agents see status and claim available work. |
| Direct message | Target one specific teammate. |
| Broadcast | Send to all teammates at once — use sparingly; cost scales with team size. |

**Plan-approval flow** (for risky tasks): require teammates to plan before implementing.
Teammate works read-only in plan mode → sends a plan-approval request to the lead → lead
approves or rejects with feedback → teammate revises or, once approved, implements. You can set
approval criteria in the prompt (e.g. "only approve plans that include test coverage").

## Display modes

| Mode | How it works | Setup |
|------|-------------|-------|
| in-process (default) | All teammates in one terminal; `Shift+Down` cycles, `Ctrl+T` shows tasks | None |
| split panes (tmux) | One pane per teammate | tmux installed |
| split panes (iTerm2) | One pane per teammate | iTerm2 + `it2` CLI + Python API |
| auto | tmux panes if already in tmux, else in-process | — |

Configure via `settings.json` (`"teammateMode": "in-process" | "tmux" | "auto"`) or
`claude --teammate-mode in-process`.

## Permissions & cost

- Teammates **inherit the lead's permission mode at spawn**; you can change a teammate's mode
  *after* spawning, but not set per-teammate modes at spawn time. If the lead skips permission
  prompts, all teammates do too.
- Each teammate has its own full context window, so **token usage scales linearly** with the
  number of active teammates. Worth it for research / review / new features; for routine work a
  single session is cheaper.

## Known limitations

| Limitation | Impact |
|------------|--------|
| No session resumption for in-process teammates | `/resume` and `/rewind` don't restore them — spawn fresh ones after resume |
| Task status can lag | Teammates sometimes fail to mark tasks complete — nudge manually |
| Shutdown can be slow | A teammate finishes its current request before stopping |
| One team per session | Clean up the current team before starting a new one |
| No nested teams | Teammates can't spawn their own teams |
| Lead is fixed | Can't promote a teammate to lead or transfer leadership |
| Split panes are tmux/iTerm2 only | Not in VS Code terminal, Windows Terminal, or Ghostty |

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Teammates not appearing | `Shift+Down` to check in-process mode; confirm the task warrants a team; `which tmux` |
| Too many permission prompts | Pre-approve common operations before spawning |
| Teammates stopping on errors | Inspect output (`Shift+Down` / click pane); give instructions or spawn a replacement |
| Lead shuts down too early | Tell the lead to wait for teammates before proceeding |
| Orphaned tmux sessions | `tmux ls` then `tmux kill-session -t <name>` |
