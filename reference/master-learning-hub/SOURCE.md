# Reference: Master Learning Hub (curated extract)

This folder is a small, **sanitized** extract from a private engineering knowledge base.
Only generic, reusable, vendor- and employer-neutral patterns were carried over. Anything
internal, client-specific, third-party, or identifying was deliberately left out.

## Why most of the source was *not* folded

The source repo was the private "brain" that the rest of this kit was originally distilled
from. Its engineering patterns (Python, FastAPI, RAG, guardrails, MCP/A2A, fine-tuning,
frontend, AWS/ECS, CI/CD, MLOps, classical ML, deep learning, NLP) already live here in
de-identified form under [`foundations/`](../../foundations/), [`pillars/`](../../pillars/),
and [`domains/`](../../domains/). Re-importing them raw would just duplicate the kit.

So this extract keeps **only the few pieces that fill a genuine gap** and are concrete enough
to be worth lifting verbatim.

## What's here

| File | What it adds that the kit didn't already have |
|------|----------------------------------------------|
| [`realtime-voice-model-selection.md`](./realtime-voice-model-selection.md) | A concrete realtime speech-to-speech model **selection matrix** plus 8 silent-failure gotchas and a provider-fallback/circuit-breaker pattern. The kit's voice pages cover the *concepts*; this is the field-tested checklist. |
| [`knowledge-graph-over-tabular-data.md`](./knowledge-graph-over-tabular-data.md) | When to reach for a **knowledge graph instead of vector RAG** for structured/tabular data, and how to build one. The kit's RAG pages assume unstructured corpora; this covers the relational case. |
| [`agent-runtime-patterns.md`](./agent-runtime-patterns.md) | Three implementation-level patterns for long-running agent loops: token-aware context **compaction**, **tiered tool permissions**, and a **pre/post tool-use hook** pipeline. |

## What was deliberately excluded (and why)

- **Enterprise / ERP / consulting patterns** — competitor intelligence, client-facing market
  analysis, and a named security framework. Client- and author-identifying. Not folded.
- **Course notes** — verbatim transcripts and notes from a third-party paid course (with
  instructor names). Not ours to redistribute; the generic lessons are already distilled into
  the kit's `foundations/`.
- **Life/business frameworks** — off-topic for an AI dev stack, and written with
  person-specific framing.
- **Market-intelligence / frontier-news digests** — point-in-time news that ages fast and
  doesn't fit this kit's evergreen-pattern style. See [`_frontier/`](../../_frontier/) for the
  kit's forward-looking placeholders instead.
- **Project scaffolding template** — referenced internal team/persona names and private paths.
- **Internal "apply-to-project" notes, file paths, pricing snapshots, and project names** were
  stripped from every file that *was* folded.

> Pricing and model names in these files are indicative and move fast — always verify against
> the provider's current docs before committing.
