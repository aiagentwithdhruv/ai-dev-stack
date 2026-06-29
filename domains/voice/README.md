# Voice

> Real-time voice helpdesk and outbound dialers — speech in, speech out, with sub-300ms turn-taking.

## What it is

A conversational agent that talks on a phone line or in-browser call: it listens, understands, and responds in natural speech, fast enough that the conversation feels human. Inbound, it deflects support calls and answers FAQs; outbound, it runs reminders, qualification, and collections. The hard part is not the language model — it is **latency and turn-taking**. Above roughly 300ms of perceived response delay, callers start talking over the agent and the illusion breaks.

## Why it matters

- **Voice is the highest-volume, highest-cost support channel.** Even partial deflection moves real money.
- **Latency is the product.** A brilliant answer delivered a second late feels broken. The entire pipeline is engineered around a latency budget.
- **Turn-taking is what separates a demo from production.** Barge-in (the caller interrupts), endpointing (knowing they finished), and graceful handoff to a human are the make-or-break details.

## Typical stack / pattern

```
Telephony / WebRTC ─▶ VAD ─▶ Streaming STT ─▶ LLM (streaming tokens)
                       ▲                              │
                       └──── barge-in / interrupt ◀── Streaming TTS ─▶ caller
                                                        │
                                       on intent/uncertainty ─▶ warm transfer to human
```

- **Everything streams.** Partial transcripts feed the model; partial model tokens feed the synthesizer. Nothing waits for a full turn.
- **Latency budget is allocated, not hoped for:**

  | Stage | Target |
  |-------|--------|
  | Endpoint detection (VAD) | ~100-200ms after speech ends |
  | STT final | streaming, near-zero added |
  | First LLM token | < 500ms |
  | First audio out (TTS) | < 200ms |
  | **Perceived response** | **< 300ms after the caller stops** |

- **Barge-in is mandatory:** when the caller speaks, stop TTS immediately and re-listen.
- **Tools and handoff** are explicit and validated (look up an account, book a slot, transfer to a human) — per [rule 60 — Agents](../../rules/60-agents.mdc).
- **Every call is recorded and transcribed** for eval and compliance, with consent handled up front.

## De-identified example outline

**Inbound support deflection line** for a services business:

| Layer | Choice |
|-------|--------|
| Transport | Telephony provider → WebRTC media stream |
| STT | Streaming speech-to-text (e.g. a Whisper-class or hosted streaming model) |
| Brain | Streaming LLM with a tool to fetch account status and a tool to escalate |
| TTS | Low-latency streaming synthesis with barge-in support |
| Turn-taking | VAD-based endpointing; interrupt cancels in-flight audio |
| Fallback | Low confidence or "agent please" → warm transfer with context summary |
| Eval | Replay recorded calls; score task success, interruption handling, and latency percentiles |

## Foundations it leans on

- **Serving & latency** — streaming pipelines, p95/p99 latency budgeting, concurrency
- **Agents & orchestration** — validated tools for lookups, booking, and human handoff
- **Guardrails & Safety** — scope control, consent, refusal and escalation paths
- **Observability** — per-stage latency traces and full call transcripts
- **Evaluation** — call-replay scoring for task success and turn-taking quality

See [foundations/](../../foundations/README.md) for the reusable implementations.

## How to use

1. Write the latency budget table first — it constrains every component choice. Record targets in [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md).
2. Build the streaming pipeline end-to-end before adding features; prove barge-in works.
3. Define escalation and consent as first-class flows, not afterthoughts.
4. Evaluate on replayed real calls, reporting latency percentiles — averages hide the calls that fail.

## Related

- [domains/](../README.md) — the other five verticals
- [foundations/](../../foundations/README.md) · [rule 60 — Agents](../../rules/60-agents.mdc) · [rule 85 — Error & Observability](../../rules/85-error-observability.mdc)
