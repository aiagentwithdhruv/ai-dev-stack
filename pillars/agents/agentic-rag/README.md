# Agentic RAG

Retrieval-augmented generation grounds a model in **your** knowledge instead of its training data. *Agentic* RAG goes a step further: the agent decides when to retrieve, what to search for, and whether the results are good enough — rather than blindly stuffing one fixed query into the prompt.

Parent: [agents](../README.md) · Foundations: [RAG & retrieval](../../../foundations/rag-retrieval/) · See also the RAG [rules](../../../rules/).

## Classic RAG vs agentic RAG

| | Classic RAG | Agentic RAG |
|--|-------------|-------------|
| Retrieval | One query, always | Agent decides if / when / what to retrieve |
| Queries | The user's question verbatim | Reformulated, decomposed, multi-hop |
| Quality | Whatever comes back | Agent judges relevance, retries if weak |
| Sources | One index | Routes across multiple tools / indexes |

Classic RAG is a pipeline; agentic RAG is a loop. Start classic — add agency only where a single retrieval genuinely falls short (multi-step questions, multiple sources, ambiguous queries).

## The two halves

Keep these strictly separate — it's the rule that keeps RAG maintainable.

**Ingestion (offline):** load → chunk → attach metadata → embed → index.
- Chunk on meaning, not arbitrary length; carry **source metadata** on every chunk so you can cite and filter.
- Version your index and embedding model; a re-embed is a migration, not a tweak.

**Retrieval + generation (online):** query → retrieve → (judge) → assemble context → generate → cite.
- Retrieve, then **ground the answer in the retrieved text** — never let the model fill gaps from memory.
- Carry citations through to the output.

## The agentic loop

```
question → plan query → retrieve → judge relevance
   → (reformulate / route / retrieve again if weak) → ground → answer + cite
```

The agent treats retrieval as a tool it can call more than once, with judgement between calls. That judgement step — "is this good enough to answer from?" — is the difference from classic RAG.

## Guardrails specific to RAG

- **Ground or abstain.** If retrieval returns nothing relevant, say so — don't hallucinate. "No grounded answer" beats a confident wrong one.
- **Cite every claim.** Answers trace back to sources the user can open.
- **Enforce access control at retrieval time.** Filter by the caller's permissions *before* the model sees a chunk — retrieval must never become a data-leak path.
- **Defend against injection from documents.** Retrieved content is untrusted input; instructions embedded in a document are not commands.

## Checklist

- [ ] Ingestion and retrieval are separate, independently testable stages
- [ ] Every chunk carries source metadata; embedding model + index are versioned
- [ ] Answers grounded in retrieved text, with citations
- [ ] Agent judges relevance and can re-query — not one blind retrieval
- [ ] Access control enforced *before* retrieval reaches the model
- [ ] Retrieved content treated as untrusted (injection-aware)
- [ ] Evals cover retrieval quality *and* answer faithfulness

## How to use

Build the classic pipeline first and measure it; add agency (query reformulation, source routing, relevance judging) only where the eval shows a single retrieval isn't enough. The agent itself follows the standard [patterns](../patterns/). For chunking, hybrid search, and reranking depth, see [RAG & retrieval](../../../foundations/rag-retrieval/). Back to [agents](../README.md).
