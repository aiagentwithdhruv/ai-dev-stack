# Agent Runtime Patterns

> Implementation-level companions to [`pillars/agents/`](../../pillars/agents/) and
> [`prompts/context-compact-handoff.md`](../../prompts/context-compact-handoff.md). Three
> patterns that long-running agent loops need but that conceptual guides usually skip:
> token-aware compaction, tiered tool permissions, and a tool-use hook pipeline. All code is
> illustrative Python — adapt to your framework.

---

## 1. Token-aware conversation compaction

When a conversation grows past a token threshold, collapse the *older* messages into a
structured summary and keep the most recent N messages verbatim. Re-compactions **merge** into
the prior summary rather than overwrite it — so you compress context, never lose it.

A good summary extracts: recent user requests, **pending work** (messages mentioning todo /
next / remaining), key files referenced, and a short timeline. Critically, instruct the model
to **resume directly without acknowledging the summary** — otherwise it wastes tokens narrating
the handoff.

```python
CONTINUATION_PREAMBLE = (
    "This session continues a previous conversation that ran out of context. "
    "The summary below covers the earlier portion.\n\n"
)
DIRECT_RESUME = (
    "Continue from where it left off without asking further questions. "
    "Resume directly — do not acknowledge the summary or recap."
)

def should_compact(messages, preserve_recent=4, max_tokens=10_000):
    compactable = messages[:-preserve_recent] if len(messages) > preserve_recent else []
    estimated = sum(len(str(m)) // 4 + 1 for m in compactable)  # ~4 chars/token
    return len(compactable) > preserve_recent and estimated >= max_tokens

def compact_messages(messages, preserve_recent=4):
    if not should_compact(messages, preserve_recent):
        return messages
    old, recent = messages[:-preserve_recent], messages[-preserve_recent:]
    summary = build_summary(old)  # your extractor (requests, pending work, files, timeline)
    system_msg = {"role": "system", "content": CONTINUATION_PREAMBLE + summary + "\n" + DIRECT_RESUME}
    return [system_msg] + recent
```

**Pending-work inference** is just a keyword scan over recent messages — extend the list with
domain terms relevant to your app:

```python
PENDING_KEYWORDS = {"todo", "next", "pending", "follow up", "remaining", "still need"}

def infer_pending_work(messages, limit=3):
    out = []
    for msg in reversed(messages):
        text = first_text(msg)
        if text and any(kw in text.lower() for kw in PENDING_KEYWORDS):
            out.append(text[:160])
            if len(out) >= limit:
                break
    return list(reversed(out))  # restore chronological order
```

**Merge insight:** when re-compacting an already-compacted session, carry the *highlights* of
the old summary but only the *timeline* of the new one. Carrying both timelines makes them grow
quadratically across re-compactions.

---

## 2. Tiered tool permissions with runtime escalation

Authorize every tool call against an ordered set of modes. If the active mode is insufficient,
either prompt a human or deny. Keep the prompter behind an interface so the runtime never
depends on the UI. This maps cleanly onto RBAC: read-only = viewer, workspace-write = editor,
full = admin — with per-tool overrides ("delete always requires admin" regardless of session
mode).

```python
from enum import IntEnum
from dataclasses import dataclass, field
from typing import Protocol

class Mode(IntEnum):
    READ_ONLY = 0
    WORKSPACE_WRITE = 1
    DANGER_FULL = 2
    ALLOW = 99  # always pass

class Prompter(Protocol):
    def decide(self, tool_name: str, tool_input: str) -> bool: ...

@dataclass
class PermissionPolicy:
    active_mode: Mode
    tool_requirements: dict = field(default_factory=dict)  # tool_name -> Mode

    def authorize(self, tool_name, tool_input, prompter=None):
        required = self.tool_requirements.get(tool_name, Mode.DANGER_FULL)
        if self.active_mode == Mode.ALLOW or self.active_mode >= required:
            return True, ""
        if prompter is not None:
            ok = prompter.decide(tool_name, tool_input)
            return (True, "") if ok else (False, "user denied")
        return False, f"'{tool_name}' requires {required.name}; active is {self.active_mode.name}"
```

---

## 3. Pre / post tool-use hook pipeline

Run registered checks before and after every tool execution. This is the execution-time layer
most guardrail stacks are missing (policy rules and output filters don't intercept the call
itself). Use a **dedicated "deny" signal** (e.g. exit code `2`) distinct from generic failure,
so hooks can return a *warning* without blocking.

```python
import os, json, subprocess
from dataclasses import dataclass

@dataclass
class HookResult:
    allowed: bool
    messages: list

def run_hook(command, event, tool_name, tool_input, tool_output=None, is_error=False):
    payload = json.dumps({
        "event": event, "tool_name": tool_name, "tool_input": tool_input,
        "tool_output": tool_output, "is_error": is_error,
    })
    proc = subprocess.run(["sh", "-lc", command], input=payload.encode(),
                          capture_output=True, env={**os.environ})
    stdout = proc.stdout.decode().strip()
    if proc.returncode == 2:                      # 2 == deny
        return HookResult(False, [stdout or f"hook denied {tool_name}"])
    return HookResult(True, [stdout] if stdout else [])  # 0 allow, other == warn
```

Wire it into the loop: **permission check → pre-hook → execute → post-hook → push result**.
And the rule that ties it together —

> **Always push every tool result back into the conversation before the next model call —
> including errors and hook denials.** The model must see failures to reason correctly. Never
> silently drop a tool error; return `(output, is_error)` instead of raising, so the loop can
> always continue.
