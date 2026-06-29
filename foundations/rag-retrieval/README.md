# RAG & Retrieval — the pattern layer

This area is about **how to retrieve well**, independent of *what* you're retrieving over. It is the reusable mechanism: chunk, index, search, rerank, assemble. A specific knowledge base (support docs, a codebase, a policy corpus) is an *application* of these patterns — keep the two separate so the mechanism stays portable across domains.

First principle, same as the rest of the kit: **don't reach for RAG when a prompt works.** If the knowledge fits in the window and rarely changes, put it in context. RAG earns its complexity only when the corpus is large, changing, or must be cited.

## Separate ingestion from query

The single most important structural rule, mirrored in [`../../rules/50-rag-system.mdc`](../../rules/50-rag-system.mdc):

- **Ingestion** (offline): load → clean → chunk → embed → index. Slow, batched, re-runnable.
- **Query** (online): embed query → retrieve → rerank → assemble → generate. Fast, per-request.

Conflating them produces systems you can't re-index without breaking serving, and can't tune serving without re-ingesting. Keep them as two pipelines that share a schema.

## Chunking — the quality ceiling

Retrieval can never surface what chunking destroyed. This is where most RAG quality is won or lost.

- **Chunk on structure, not character count** — sections, paragraphs, function boundaries. Respect the document's natural seams.
- **Overlap** adjacent chunks modestly so a fact split across a boundary survives in at least one.
- **Carry metadata on every chunk** — source, section title, position, timestamp, access scope. Metadata drives filtering and citation later.
- **Right-size for the embedding model and the answer** — too large dilutes the vector, too small strands context. Tune empirically against real queries.

## Hybrid search — BM25 + vector + RRF

Neither lexical nor semantic search is sufficient alone. Run both, then fuse.

- **BM25 (lexical)** nails exact terms, codes, names, rare tokens — where embeddings blur.
- **Vector (semantic)** nails paraphrase and intent — where keywords miss.
- **Reciprocal Rank Fusion (RRF)** merges the two ranked lists by rank position, not raw score, so you don't have to normalize incompatible scoring scales. Robust, parameter-light, hard to beat as a default.

Hybrid + RRF is the pragmatic baseline. Reach for anything fancier only after this is in place and measured.

## Reranking — precision after recall

Retrieval optimizes recall (get the candidates); reranking optimizes precision (order them right).

- Retrieve a **wide candidate set** (e.g. top 20–50), then rerank down to the few you actually pass to the model.
- A **cross-encoder reranker** scores each query–chunk pair jointly — far sharper than the bi-encoder used for first-pass retrieval, at higher per-pair cost, which is why it runs only on the shortlist.
- Reranking is the cheapest large quality win in most pipelines. Add it before you add exotic indexing.

## GraphRAG — when relationships are the answer

Flat chunk retrieval struggles with questions that span entities ("how does X connect to Y across these documents"). GraphRAG builds a structure on top:

- Extract **entities and relationships** into a graph during ingestion.
- Retrieve by **traversing connections**, not just nearest-vector — multi-hop questions become walkable.
- Best for **synthesis across many documents**; overkill for simple lookup, where it adds ingestion cost and brittleness for no gain.

Use it when the value is in the *links between* facts, not the facts themselves.

## Retrieval checklist

- [ ] Ingestion and query are separate pipelines sharing one chunk schema.
- [ ] Chunks follow document structure and carry source + section + scope metadata.
- [ ] Hybrid search (lexical + vector) fused with RRF is the baseline.
- [ ] A reranker trims a wide candidate set down to the final few.
- [ ] Retrieved context is filtered for relevance before it enters the window — see [Prompting & Context](../prompting-context/).
- [ ] Every answer can cite the chunk it came from (metadata makes this free).
- [ ] You measure retrieval quality against real queries, not vibes.

## How to use

Build the simplest tier that answers your real queries, then climb only on evidence: **prompt-in-context → hybrid + RRF → add reranking → GraphRAG** if relationships demand it. Each step adds cost and operational surface — earn it with a measured gap, not a hunch. The retrieved chunks are one slice of the assembled window; how they're ordered and budgeted against everything else lives in [Prompting & Context](../prompting-context/), and the enforced version of these rules is [`../../rules/50-rag-system.mdc`](../../rules/50-rag-system.mdc).
