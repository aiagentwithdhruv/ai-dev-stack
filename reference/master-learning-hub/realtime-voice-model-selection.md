# Realtime Voice — Model Selection & Field Gotchas

> Companion to [`domains/voice/`](../../domains/voice/) and [`pillars/agents/voice/`](../../pillars/agents/voice/),
> which cover the *concepts*. This page is the concrete selection matrix + the bugs that cost a day.
>
> Pricing and model names are **indicative and move fast** — verify against current provider docs.

A realtime (speech-to-speech) model takes audio in and emits audio out in one streaming
connection, collapsing STT → LLM → TTS into a single hop for the lowest latency and most
natural turn-taking. The trade-off vs. a composed pipeline is granular control. Reach for
realtime when low-latency natural conversation *is* the product.

## Selection matrix

The market has roughly three tiers: a cheap multilingual flash model, a premium full model
with the best reasoning, and a mid model that's the production sweet spot for one language.

| Spec | Cheap flash (multilingual) | Premium full | Mid |
|---|---|---|---|
| Audio in | ~$0.005/min | ~$0.06/min | ~$0.015/min |
| Audio out | ~$0.018/min | ~$0.24/min | ~$0.06/min |
| 1-hr, user-heavy (70/30) | ~$1.40 | ~$7–9 | ~$2.50 |
| 1-hr, AI-heavy (30/70) | ~$1.40 | ~$15–18 | ~$4.50 |
| Latency | ~250–300 ms | ~300 ms | ~300 ms |
| Reasoning | Simple turns | Best | Mid |
| Tool calling | Yes, mid-stream | Yes, native | Yes, native |
| Multilingual (e.g. Indian languages) | Best (native) | OK with prompting | OK with prompting |

### The rule of thumb

- **Cheapest + multilingual** → the flash tier.
- **Best brain** (scoring, complex multi-step reasoning over the call) → the premium full model.
- **Production sweet spot for a single primary language** → the mid model.

Voice turns are frequent and latency-sensitive — route to the cheapest model that can hold
the conversation, and only escalate when reasoning quality genuinely needs it.

## Eight gotchas that fail *silently*

These don't throw errors. You get a connected socket and a bot that's mute, garbled, or
talking to itself. Each has cost someone a full day.

1. **Dual audio event names.** Some providers renamed the audio-delta event across a GA
   release. Handle *both* the old and new event names, or you get a working WebSocket and
   **zero audio**.
2. **The browser ignores your requested sample rate.** `AudioContext` commonly runs at 48 kHz
   regardless of a requested 24 kHz. You must resample to the model's expected rate inside the
   `AudioWorklet`, or the model receives garbage audio — **no error thrown**.
3. **Temperature floors.** Some realtime APIs reject temperatures below a minimum (e.g. 0.6).
   Anything lower is an API error.
4. **Autoplay policy.** Browsers block audio that isn't user-initiated. Voice widgets must
   start behind a user click; they cannot auto-start on page load.
5. **Mic-gate while the AI speaks.** If you don't mute the mic during playback
   (`if (isAISpeaking) return` on mic input), the AI hears its own output and responds to
   its own echo.
6. **Gapless PCM playback.** Schedule output chunks against a running "next start time" cursor
   on `AudioBufferSourceNode`s. Naive back-to-back playback produces clicks and gaps.
7. **WebSocket frame size.** The default `max_size` (often ~1 MB) drops the connection on long
   audio bursts. Raise it (e.g. 10 MB).
8. **Echo-driven state advance.** In a guided/scripted flow, guard phase transitions:
   `if user_turns == 0 and ai_turns > 0: don't advance`. Otherwise the state machine advances
   on the AI's own echo instead of a real user turn.

## Provider fallback pattern (production)

Pick a provider at call start and **hold it for the whole session** — transparent mid-call
failover is a debugging nightmare.

```
On call start:
  1. Detect language (first ~2s of audio, or user metadata).
  2. If multilingual:
       health-check the flash provider (fast ping)
       healthy → flash · down → mid model + log an alert
  3. If the primary single language → mid model directly.
  4. Open the WS and hold that provider for the entire call.

Circuit breaker: if the flash provider's error rate exceeds ~5% over a 5-minute window,
route ALL traffic to the mid model until it recovers.
```

## Cost note: two SDKs is the real tax

Different realtime providers have entirely different WebSocket protocols and event names.
Every new tool or feature has to be implemented twice. Ship on **one** provider first, then
port — dual-implementing from day one doubles maintenance for no product gain.
