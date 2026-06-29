# Observability

> The #1 reason AI pilots fail review isn't model quality — it's that nobody can answer "what did it do, what did it cost, and why did it slow down?" If you can't see it, you can't operate it.

## What this is

End-to-end visibility into an LLM system: every request traced span-by-span, every token and dollar accounted for, every prompt version pinned, and drift detected before users feel it. It's standard production observability (traces, metrics, logs) extended with the things LLMs add — tokens, cost, prompt versions, and output quality.

## Why it matters

A demo proves a system *can* work. Observability proves it *keeps* working under real traffic. Review boards and clients don't approve systems they can't audit. When a multi-step agent gives a wrong answer, a trace tells you which tool call or retrieval step broke it; without one you're guessing. When the monthly bill triples, cost-per-request attribution tells you which feature did it.

## The four things to instrument

| Signal | Capture | Why |
|--------|---------|-----|
| **Traces** | One span per LLM call, tool call, retrieval, and agent step — parented into a single request trace | Reconstruct exactly what happened in a multi-step flow |
| **Cost & tokens** | Input/output tokens and computed cost per call, tagged by feature, model, and tenant | Attribute spend, catch runaway loops, prove routing savings |
| **Latency** | Per-span duration plus end-to-end; track p50/p95/p99, not averages | Averages hide the tail that users actually complain about |
| **Quality** | Sampled outputs scored offline, plus user feedback signals | Detect silent quality decay between deploys |

### Use OpenTelemetry as the backbone

Emit spans in the **OTEL** format so traces, metrics, and logs flow to any backend you choose and you're never locked to one vendor. Model each LLM call as a span with attributes: model id, prompt version, input/output token counts, cost, temperature, and a trace id that ties the whole request together. Propagate that trace id across services and tool calls.

### Prompt versioning is non-negotiable

- Give every prompt a **version id** and stamp it on every trace.
- Treat prompts as code: change → review → version bump → deploy.
- You must be able to answer "which prompt produced this output?" months later.
- When quality moves, the first question is always "what version was live?"

### Drift — catch it before users do

- **Quality drift** — output scores trend down though nothing was deployed (provider model update, data shift). Mitigate by pinning model versions and running [../evals-testing](../evals-testing/README.md) on a schedule, not just in CI.
- **Cost/latency drift** — token usage or p95 creeps up. Alert on rolling baselines, not fixed thresholds.
- **Input drift** — real traffic diverges from your golden set. Feed sampled production inputs back into evals.

## Observability checklist

- [ ] OTEL tracing on every LLM call, tool call, retrieval, and agent hop.
- [ ] Token counts and computed cost on every call, tagged by feature/model/tenant.
- [ ] Latency tracked as p50/p95/p99 end-to-end and per span.
- [ ] Prompt version id stamped on every trace.
- [ ] A sampling pipeline scores production outputs offline.
- [ ] Alerts on rolling baselines for cost, latency, and quality.
- [ ] Trace id propagated across services so any request is fully reconstructable.
- [ ] No PII or secrets in logs or span attributes (see [../guardrails-security](../guardrails-security/README.md)).

## How to use this

Wire OTEL in from the first prototype, not after the pilot is "done" — retrofitting tracing into a working agent is painful and you'll skip it. Make prompt version a first-class field everywhere. Production traces are the richest source of new eval cases, so close the loop with [../evals-testing](../evals-testing/README.md), and use cost attribution to drive decisions in [../model-routing-cost](../model-routing-cost/README.md).
