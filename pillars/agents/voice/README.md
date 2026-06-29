# Voice agents

A voice agent is an agent whose medium is speech. The reasoning core is the same as any [agent](../README.md); the surrounding pipeline turns audio into text, runs the agent, and turns the answer back into audio — fast enough to feel like a conversation.

Foundations: [prompting & context](../../../foundations/prompting-context/), [evals](../../../foundations/evals-testing/)

## The pipeline

```
mic → STT → LLM (+ tools) → TTS → speaker
```

| Stage | Job | What to optimise |
|-------|-----|------------------|
| **STT** (speech-to-text) | Transcribe the user's audio | Accuracy on your domain vocab; streaming partials |
| **LLM** | Understand intent, call tools, draft the reply | Same agent loop as any other medium |
| **TTS** (text-to-speech) | Speak the reply | Naturalness; low time-to-first-audio |

## Latency is the whole game

In text, a two-second pause is invisible. In voice, it's a broken conversation. The budget you design around is end-to-end — mouth to ear — and it's the sum of every stage.

- **Stream everything.** Streaming STT (partial transcripts) and streaming TTS (start speaking before the full reply is generated). Don't wait for complete turns.
- **Pipeline, don't serialize.** Begin synthesizing the start of the reply while the model is still producing the rest.
- **Handle barge-in.** A real conversation lets the user interrupt. Detect speech during playback, stop the TTS, and re-listen.
- **Route to the cheapest model that holds the conversation.** Voice turns are frequent and latency-sensitive — choose accordingly (see [model-routing](../patterns/)).

## Realtime vs composed pipeline

- **Composed pipeline** (separate STT, LLM, TTS) — maximum control and model choice at each stage; you own the latency budget and the observability at each seam.
- **Realtime speech-to-speech** — a single model takes audio in and emits audio out, collapsing the stages for the lowest latency and most natural turn-taking, at the cost of granular control.

Start composed when you need tool use, custom logic, and per-stage observability. Reach for realtime when natural, low-latency conversation *is* the product.

## Checklist

- [ ] End-to-end latency budgeted and measured, not assumed
- [ ] Streaming STT and streaming TTS — no waiting on full turns
- [ ] Barge-in / interruption handled
- [ ] Domain vocabulary tuned in STT
- [ ] Tool calls validated like any agent (typed schemas, checked outputs)
- [ ] Graceful fallback when a stage fails (timeout, retry, hand-off)

## How to use

Treat the LLM stage as a standard agent — all the [patterns](../patterns/) and guardrails apply. The voice-specific work is the latency engineering around it. Back to [agents](../README.md).
