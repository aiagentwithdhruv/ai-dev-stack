# Prompting & Context Engineering

The model is fixed. The **context you assemble around it** is the only variable you control at runtime — and it is where most production AI features succeed or fail. This area covers how to build the input: the system prompt, the examples, the output contract, and the moving parts of the context window.

The mental shift: stop "prompting" (one clever message) and start **context engineering** (deciding, every turn, exactly which tokens occupy a finite window).

## The system prompt is architecture, not a greeting

Treat the system prompt like the architect rule treats code: a contract, not prose.

- **Role + scope in the first lines.** Who the model is, what it owns, what it must never do.
- **State invariants explicitly.** Output format, refusal conditions, tone — anything you'd otherwise re-explain every turn.
- **Negative space matters.** "Do not invent fields not present in the source" prevents more failures than three positive instructions.
- **Keep it stable.** A system prompt that changes per request can't be cached and can't be reasoned about. Push the per-request variation into the user turn.

## Few-shot: examples beat adjectives

When behavior is hard to describe, show it. A few well-chosen input→output pairs outperform a paragraph of description.

- **2–5 examples** is the usual sweet spot; more crowds the window for diminishing returns.
- **Cover the edges, not the easy case** — the empty input, the ambiguous one, the one that should be refused.
- **Match the exact output shape** you want back. The model copies structure as much as content.
- **Order matters** — the last example carries extra weight. Put the most representative case last.

## Structured output: make the boundary machine-checkable

Free-text output is unverifiable. Constrain it so the boundary can be validated.

- Define a **schema** (JSON Schema, a typed model, or a strict template) and ask for output that conforms.
- **Validate on receipt.** Reject and retry on parse failure rather than passing malformed data downstream.
- Prefer **native structured-output / tool-call modes** when the model offers them over "respond in JSON" prose instructions.
- Keep the schema **flat and named** — deeply nested or anonymous shapes are where models drift.

## Context-window assembly

The window is a budget. Every token spent on one thing is unavailable to another. Assemble it deliberately, in priority order:

1. **System prompt** — stable, cacheable, first.
2. **Tools / output schema** — the contract for this turn.
3. **Retrieved context** — only what's relevant (see [RAG & Retrieval](../rag-retrieval/)). More is not better; irrelevant chunks dilute attention.
4. **Conversation history** — compressed (below).
5. **Current user turn** — last, closest to the model's attention.

Two failure modes to watch: **dilution** (so much marginal context the signal drowns) and **lost-in-the-middle** (content buried mid-window gets less attention than the head or tail). Put what must be obeyed at the edges.

## History compression

Conversations outgrow the window. Don't truncate blindly — compress.

- **Summarize older turns** into a running brief; keep recent turns verbatim.
- **Pin durable facts** (decisions, constraints, IDs) into a structured scratchpad that survives summarization instead of living in chat scrollback.
- **Evict, don't accumulate.** Tool outputs and intermediate reasoning rarely need to persist once their conclusion is captured.
- **Re-anchor after compaction** — restate the active goal and constraints so the post-summary model isn't reasoning from a lossy digest.

## Context-assembly checklist

- [ ] System prompt is stable and cacheable across requests.
- [ ] Output has a schema, and the schema is validated on receipt.
- [ ] Few-shot examples cover edges and match the target shape.
- [ ] Retrieved context is filtered for relevance, not dumped wholesale.
- [ ] History is compressed with durable facts pinned, not naively truncated.
- [ ] Must-obey content sits at the head or tail, never buried mid-window.
- [ ] Token budget is accounted for per section — you know what's spending the window.

## How to use

Design the context like a function signature: decide the inputs and the output contract first, then fill the body. When a feature misbehaves, audit the **assembled context** before blaming the model — print the exact tokens you sent. Most "the model is dumb" bugs are "the context was wrong" bugs. For the retrieval slice of context, continue to [RAG & Retrieval](../rag-retrieval/); for the enforced agent contract, see [`../../rules/60-agents.mdc`](../../rules/60-agents.mdc).
