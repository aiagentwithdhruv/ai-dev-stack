---
title: Technique File Format
type: meta
---

# Technique File Format

A technique file is the core unit of the learning hub. It captures one engineering pattern in enough depth that a capable agent can apply it correctly without reading source code or external documentation.

The format is designed for reuse, not completeness. You are not writing a tutorial. You are writing the minimum a competent practitioner needs to know to apply this pattern correctly and avoid its known failure modes.

---

## Structure

```markdown
---
title: [Technique name — plain English, not acronym-first]
type: [technique | decision | pattern | workflow]
tags: [comma, separated, lowercase]
source: [where this came from — paper, class, production experience, person]
last_updated: YYYY-MM-DD
applies_to: [what kind of project or task this is relevant to]
---

# [Title]

## What it is

One paragraph. Plain English. Explain this to someone who has not heard of it
before. What problem does it solve? Why does it exist?

## When to use it

A decision table or bulleted conditions. Be concrete. "Use when X" is better
than "useful for scenarios involving Y."

## How it works

The mechanism. How the technique actually operates. Can include a diagram,
pseudocode, or step sequence. This is where technical depth lives.

## Code sample

A minimal working example. 5-20 lines. Enough to understand the shape without
being a copy-paste recipe.

## Gotchas

What goes wrong. The failure modes that are not obvious. Each gotcha should
be a concrete thing that happened (or is known to happen), not a vague warning.

## Decision thresholds

Specific numbers or conditions that tell you when to upgrade, change, or
abandon this approach. Examples: "switch to X when document count exceeds N,"
"add re-ranking when precision drops below 60%."

## Related files

- [other technique or reference files this connects to]
```

---

## Example: Hybrid Search

```markdown
---
title: Hybrid Search — BM25 + Dense Retrieval
type: technique
tags: rag, retrieval, search, nlp
source: Production RAG class + Perplexity SAL paper (Apr 2026)
last_updated: 2026-04-23
applies_to: RAG systems with technical document corpora
---

# Hybrid Search — BM25 + Dense Retrieval

## What it is

Standard dense (embedding-based) retrieval finds semantically similar content.
It is excellent at "find something that means the same thing as this query" and
poor at "find the exact string `po_type` in a 184-endpoint schema." Hybrid
search fuses sparse retrieval (BM25, keyword-based) with dense retrieval to
get both semantic understanding and exact-match precision.

## When to use it

Use hybrid search when your corpus contains:
- Exact identifiers (endpoint names, field codes, product SKUs, error codes)
- Technical terms that users may phrase differently than the documents
- Any domain where precision on specific strings matters (legal, compliance,
  ERP schemas, API documentation)

Do NOT add it prematurely. If dense search alone gives context recall above
70% on your eval set, the hybrid overhead is not worth it.

## How it works

```
User query
  |
  +---> BM25 search (sparse, keyword-weighted) ---+
  |                                                +--> Reciprocal Rank
  +---> Dense search (embed query, cosine sim) ---+    Fusion (RRF)
                                                          |
                                                     Fused ranked list
                                                          |
                                                     [optional: reranker]
                                                          |
                                                     Top-K into LLM context
```

Reciprocal Rank Fusion: for each document, score = 1/(k + rank_in_sparse) +
1/(k + rank_in_dense). k=60 is a robust default. Sorted descending.

## Code sample

```python
from rank_bm25 import BM25Okapi

sparse_results = bm25.get_top_n(query.split(), corpus, n=20)
dense_results = vector_db.search(embed(query), top_k=20)

def reciprocal_rank_fusion(sparse, dense, k=60, alpha=0.7):
    scores = {}
    for rank, doc in enumerate(dense):
        scores[doc.id] = alpha * (1 / (k + rank))
    for rank, doc in enumerate(sparse):
        scores[doc.id] = scores.get(doc.id, 0) + (1 - alpha) * (1 / (k + rank))
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

fused = reciprocal_rank_fusion(sparse_results, dense_results, alpha=0.7)
```

`alpha=0.7` means 70% weight on dense, 30% on sparse. Tune based on your corpus.

## Gotchas

- BM25 requires tokenized corpus upfront. If documents update frequently,
  BM25 index must be rebuilt. For dynamic corpora, use Elasticsearch or
  OpenSearch BM25 instead of rank_bm25.
- RRF only works if both result lists cover roughly the same documents.
  If your BM25 and dense indexes are over different document sets (e.g.,
  one has metadata, one has full text), RRF results will be misleading.
- Keyword preprocessing matters. Lowercase, remove stopwords, stem or
  lemmatize for BM25. Different preprocessing than embedding pipeline.

## Decision thresholds

- Add hybrid search when dense-only context recall < 70% on eval set
- Set alpha based on corpus type: 0.7 (typical), 0.5 (very technical), 0.3 (conversational)
- Switch to dedicated search engine (Elasticsearch) when document count > 500K

## Related files

- 09-knowledge/rag-architecture.md — full RAG stack reference
- 09-knowledge/karpathy-method.md — when NOT to use search at all
```

---

## File naming convention

`[topic]-[subtopic].md` — all lowercase, hyphens not underscores.

Examples:
- `rag-hybrid-search.md`
- `deployment-ecs-fargate.md`
- `agents-react-loop.md`
- `fine-tuning-lora.md`

One topic per file. If a file grows past 300 lines, split it.

---

## Quality bar

A technique file is ready to commit when:

1. Someone who has never used this technique could apply it correctly from the file alone
2. Someone who has used it before could find the gotchas within 30 seconds
3. The decision thresholds are specific enough to act on without judgment calls

If you cannot meet bar 1, the "What it is" and "How it works" sections need more work. If you cannot meet bar 2, the "Gotchas" section is vague. If you cannot meet bar 3, "When to use it" and "Decision thresholds" need concrete numbers.
