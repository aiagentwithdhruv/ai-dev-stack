# Custom Agent Definitions

Custom agents are **Markdown files with YAML frontmatter**: the frontmatter configures the
agent, the body becomes its system prompt.

```markdown
---
name: my-agent
description: When Claude should delegate to this agent
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a specialist. When invoked, do X then Y then Z.
```

## Scoping & priority

Agents load from several locations; on a name collision, higher priority wins. They load at
session start — add a file manually and you must restart the session or run `/agents` to pick it up.

| Priority | Location | Scope | How to create |
|----------|----------|-------|---------------|
| 1 (highest) | `--agents` CLI flag | Current session only | Pass JSON on launch |
| 2 | `.claude/agents/` | Current project | `/agents` or a file |
| 3 | `~/.claude/agents/` | All your projects | `/agents` or a file |
| 4 (lowest) | A plugin's `agents/` dir | Where the plugin is enabled | Installed with the plugin |

**Session-only agents via CLI:**

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on quality, security, best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

**Run a whole session AS an agent** (`claude --agent code-reviewer`) — replaces the default
system prompt with the agent's; `CLAUDE.md` and project memory still load. Make it the project
default with `{ "agent": "code-reviewer" }` in `.claude/settings.json`.

## Frontmatter fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Unique id; lowercase letters and hyphens only |
| `description` | Yes | string | When Claude should delegate — write it clearly, Claude reads it to decide |
| `tools` | No | list / CSV | Allowlist of tools; inherits all if omitted |
| `disallowedTools` | No | list / CSV | Denylist; removed from the inherited/specified set |
| `model` | No | string | `sonnet` / `opus` / `haiku`, a full model id, or `inherit` (default) |
| `permissionMode` | No | string | `default` / `acceptEdits` / `dontAsk` / `bypassPermissions` / `plan` |
| `maxTurns` | No | int | Max agentic turns before the agent stops |
| `skills` | No | list | Skills to preload into the agent's context at startup |
| `mcpServers` | No | list | MCP servers available to this agent (references or inline) |
| `hooks` | No | object | Lifecycle hooks scoped to this agent |
| `memory` | No | string | `user` / `project` / `local` — enables persistent cross-session memory |
| `background` | No | bool | Always run as a background task (default `false`) |
| `effort` | No | string | `low` / `medium` / `high` / `max` — overrides the session level |
| `isolation` | No | string | `worktree` — run in a temporary git worktree (isolated repo copy) |

## Tool configuration

Internal tools: `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`, `Agent`, `WebFetch`,
`WebSearch`, `NotebookEdit`, plus any MCP tools.

- **Allowlist** — `tools: Read, Grep, Glob, Bash` → only these are available.
- **Denylist** — `disallowedTools: Write, Edit` → inherit everything except these.
- **Both set** — `disallowedTools` is applied first, then `tools` resolves against what remains.

**Restricting which subagents an agent may spawn** (applies to an agent running as the main
thread via `claude --agent`): use `Agent(...)` in `tools`.

```yaml
tools: Agent(worker, researcher), Read, Bash
```

- `Agent` alone (no parens) → may spawn any agent.
- `Agent(a, b)` → may spawn only `a` and `b`.
- Omit `Agent` entirely → may not spawn any agents.

## Useful agent archetypes

**Hook-guarded tool use** — when `tools` is too coarse, gate a tool with a hook:

```yaml
---
name: db-querier
description: Write database queries with validation
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-query.sh"
---
```

**Memory-enabled learner** — accumulates project knowledge across sessions:

```yaml
---
name: code-reviewer
description: Reviews code, accumulates project knowledge
tools: Read, Grep, Glob, Bash
memory: project
---
Review code and update your memory with patterns, conventions, and recurring issues you discover.
```
