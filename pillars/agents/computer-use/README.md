# Computer-use agents

A computer-use agent operates a user interface the way a person does — reading the screen, moving a cursor, clicking, and typing — to drive software that has no API. Browser automation is the common case; full desktop control is the general one.

Parent: [agents](../README.md) · Foundations: [guardrails & security](../../../foundations/guardrails-security/)

## When to use it (and when not to)

This is the **last-resort integration tier.** It's slower, more brittle, and harder to verify than any structured alternative. Use it only when nothing better exists.

| Prefer... | Over computer-use, when |
|-----------|-------------------------|
| An API / SDK | The service exposes one — always faster and more reliable |
| A structured automation | The workflow can be wired with connectors ([automation](../../automation/)) |
| **DOM-level browser control** | You must drive a web app but can read its structure |
| **Pixel-level computer-use** | It's a native app with no API and no accessible DOM |

> If there's an API, use the API. Computer-use is what you reach for when there isn't one.

## How it works

```
observe (screenshot / DOM) → decide next action → act (click, type, scroll) → observe again
```

The agent runs a perceive-act loop: capture the current state, choose one action, execute it, then re-observe to confirm the effect before the next step. Two observation levels:

- **Structured (DOM / accessibility tree)** — the agent reads element references and acts on them. Faster, more reliable, less ambiguous. Prefer this for web apps.
- **Visual (screenshot + coordinates)** — the agent reasons over pixels and clicks positions. The universal fallback; use when no structure is available.

## Making it reliable

- **Verify after every action.** Re-observe and confirm the expected change happened before continuing. Never fire a sequence of clicks blind.
- **Prefer references over coordinates.** Element refs survive layout changes; pixel coordinates don't.
- **Constrain the blast radius.** Scope the agent to specific apps or sites; default to read-only and gate destructive actions behind confirmation.
- **Treat on-screen content as untrusted.** Text on a page can carry injected instructions — never follow links or commands lifted from the content without checking them.
- **Budget for flakiness.** Add retries, timeouts, and explicit waits for elements; UIs are not deterministic.

## Checklist

- [ ] Confirmed no API or connector can do the job first
- [ ] Structured (DOM) control preferred where available
- [ ] Verify-after-action loop in place
- [ ] Scope limited; destructive actions gated behind confirmation
- [ ] Screen content treated as untrusted input (injection-aware)
- [ ] Retries, timeouts, and waits for non-deterministic UI

## How to use

Reach for this only after ruling out an API and a structured automation. The agent core is standard — apply the [patterns](../patterns/) and guardrails; the computer-use part is the brittle I/O layer you wrap carefully. Back to [agents](../README.md).
