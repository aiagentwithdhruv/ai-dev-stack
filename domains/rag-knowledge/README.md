# RAG / Knowledge

> Enterprise search and grounded knowledge assistants over private documents — with citations and access control.

## What it is

A system that answers natural-language questions using *your* private corpus (policies, contracts, tickets, wikis, manuals) instead of the model's training data. Every answer is grounded in retrieved passages, cites its sources, and respects who is allowed to see what. This is the most common first AI product inside an enterprise because the data already exists and the value is obvious: stop people hunting through SharePoint.

## Why it matters

- **Trust comes from citations.** A grounded answer the user can click to verify is shippable; an ungrounded one is a liability.
- **Access control is non-negotiable.** The assistant must never surface a document the asking user could not open themselves.
- **It compounds.** Once ingestion and retrieval exist, the same backbone powers support deflection, internal search, and onboarding assistants.

## Typical stack / pattern

```
Sources → Ingest → Parse → Chunk → Embed → Index (vector + keyword)
                                                  │
Query → Rewrite → Retrieve (hybrid) → Filter by ACL → Rerank → Assemble context
                                                                      │
                                              Grounded generation → Cite → Answer
```

- **Ingestion and serving are separate codebases.** Never mix re-embedding logic into the answer path. (See [rule 50 — RAG System](../../rules/50-rag-system.mdc).)
- **Hybrid retrieval** (dense embeddings + keyword/BM25) beats either alone for enterprise jargon and exact-match IDs.
- **Access control is applied at retrieval time**, as a metadata filter on the index — not as a post-generation redaction.
- **Reranking** a wide candidate set (top-50 → top-5) is the cheapest quality win available.
- **Chunk metadata** (source, version, section, ACL group, timestamp) is the contract that makes citations and filtering possible.

## De-identified example outline

**Internal policy assistant** for a mid-size organization:

| Layer | Choice |
|-------|--------|
| Corpus | ~40k documents across HR, IT, and compliance, grouped by department |
| Ingestion | Nightly batch; deterministic chunking; ACL group stamped on every chunk |
| Store | A vector store with metadata filtering (e.g. pgvector or a hosted equivalent) + keyword index |
| Retrieval | Hybrid → ACL filter on the asking user's groups → rerank → top-5 |
| Generation | Grounded answer with inline citations; "I don't have a source for that" on low confidence |
| Guardrail | Refuse out-of-scope questions; never echo a chunk the user's groups exclude |
| Eval | Golden Q→A set per department; track answer-faithfulness and citation accuracy on every change |

## Foundations it leans on

- **Retrieval & RAG** — chunking, embeddings, hybrid search, reranking, context assembly
- **Guardrails & Safety** — scope control, ACL enforcement, prompt-injection resistance from poisoned documents
- **Evaluation** — faithfulness, citation accuracy, retrieval recall on a frozen test set
- **Data ingestion** — parsing, normalization, incremental re-embedding
- **Observability** — log retrieval traces so failures are inspectable, never silent

See [foundations/](../../foundations/README.md) for the reusable implementations of each.

## How to use

1. Start from the example outline above as your reference architecture.
2. Define your corpus and ACL model first — it drives the chunk metadata schema. Capture it in [docs/DB_SCHEMA.md](../../docs/DB_SCHEMA.md).
3. Build ingestion and retrieval as independent services per [rule 50](../../rules/50-rag-system.mdc).
4. Stand up an eval set before tuning — you cannot improve retrieval you cannot measure.

## Related

- [domains/](../README.md) — the other five verticals
- [foundations/](../../foundations/README.md) · [rule 50 — RAG](../../rules/50-rag-system.mdc) · [rule 70 — Security](../../rules/70-security.mdc)
