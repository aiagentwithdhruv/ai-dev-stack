# Orchestrator Automation Switches

> PROVISIONAL — v1 additions, not yet validated across 2+ projects.
> Each file is marked with its validation status.
> Adopt only after reading the "Why" and "Tradeoffs" sections in each file.

---

## What this folder is

The core methodology (gates, prompt-files, sprint rules) is battle-tested.
These switches extend the orchestrator's behavior with automated habits:
self-correction, weekly heartbeat, context hygiene, UI verification, session recovery.

They are presented as discrete, adoptable switches — not a monolithic system.
Turn on the ones that fit your project. Skip the ones that don't.

---

## Switches

| File | Name | Status | What it does |
|------|------|--------|--------------|
| `switch-1-eval-loop.md` | Eval Loop | Provisional | Lesson written into the prompt that caused the error, same commit |
| `switch-2-monday-heartbeat.md` | Monday Heartbeat | Provisional | Weekly sprint-health report to the human's desktop |
| `switch-3-active-project-header.md` | Active Project Header | Provisional | Every prompt opens with `ACTIVE PROJECT:` to prevent context bleed |
| `switch-4-screenshot-smoke.md` | Screenshot Smoke | Provisional | UI prompt-files include a post-restart screenshot step |
| `switch-5-session-checkpoints.md` | Session Checkpoints | DEFERRED | Written-out design; only build after a real session-crash incident |

---

## How to adopt a switch

1. Read the full switch file — especially the "Why" and "Tradeoffs" sections.
2. Add the switch behavior to your orchestrator's operating instructions (agent loadout or CLAUDE.md).
3. Run it for one sprint and evaluate. If it adds friction without catching errors, disable it.
4. If you find improvements, update the switch file and note the date.

---

## Provisional flag explained

Provisional = the switch has been designed and reasoned through, but has not yet
been observed working correctly across at least 2 separate projects over at least 1 month.

Provisional switches may have undetected failure modes.
They are safe to try — they are not safe to treat as gospel.
