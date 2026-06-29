# Team Hooks — Quality Gates for Agent Teams

Hooks are shell commands (or prompt/agent checks) that fire at points in an agent's lifecycle.
Two are specific to agent teams and let you enforce quality gates before an agent stops or marks
a task done. Configure them in `settings.json`.

## `TeammateIdle`

**Fires when:** a teammate is about to go idle after finishing its turn.
**Use for:** gating before a teammate stops — e.g. build artifacts must exist, lint must pass.

Stdin (JSON) includes: `session_id`, `transcript_path`, `cwd`, `permission_mode`,
`hook_event_name`, `teammate_name`, `team_name`.

**Control behavior:**

| Goal | How | Effect |
|------|-----|--------|
| Keep the teammate working | Exit code `2` + message on stderr | Teammate receives stderr as feedback and continues |
| Stop the teammate entirely | Print JSON `{"continue": false, "stopReason": "..."}` | Teammate stops; reason shown to user |
| Allow idle | Exit code `0` | Teammate idles normally |

```bash
#!/bin/bash
# .claude/hooks/validate-build.sh — require a build artifact before idling
if [ ! -f "./dist/output.js" ]; then
  echo "Build artifact missing. Run the build before stopping." >&2
  exit 2   # teammate gets the feedback and keeps working
fi
exit 0
```

## `TaskCompleted`

**Fires when:** a task is being marked completed — either explicitly via the task tool, or when a
teammate ends its turn while holding in-progress tasks.
**Use for:** completion criteria like passing tests or lint.

Stdin (JSON) includes the same session fields plus `task_id`, `task_subject`,
`task_description`. Same control surface as `TeammateIdle`: exit `2` + stderr to bounce the
completion back with feedback, `{"continue": false, ...}` to stop, exit `0` to allow.

```bash
#!/bin/bash
# Block task completion unless the test suite passes
if ! npm test --silent >/dev/null 2>&1; then
  echo "Tests failing — task cannot be marked complete until green." >&2
  exit 2
fi
exit 0
```

## Notes

- Hooks can be scoped to a single agent via the `hooks` frontmatter field (see
  `custom-agent-definitions.md`) or applied globally in `settings.json`.
- Prefer exit-code `2` + stderr (a *correctable* signal the agent can act on) over a hard stop,
  unless the failure is genuinely terminal.
- Keep hook scripts fast and side-effect-free where possible — they run on every relevant
  lifecycle event across every teammate.
