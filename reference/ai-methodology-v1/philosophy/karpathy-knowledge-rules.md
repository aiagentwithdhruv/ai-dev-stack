# Karpathy's 4 Rules for Knowledge Bases

Andrej Karpathy (former Tesla AI Director, OpenAI co-founder) articulated a deceptively simple system for managing knowledge with LLMs. Simple enough to ignore. Powerful enough to 10x agent quality when followed. These are the 4 rules — plus the operating cycle and the architectural choice they lead to.

---

## The 4 Rules

### Rule 1 — Don't Assume

If you don't know, say "I don't know." Never fill a gap with confident-sounding hallucination.

In practice: before writing a prompt that references field names, grep the real schema. Before naming an API endpoint, curl the live server and read the response. Before claiming a file exists, `ls` the directory.

The failure mode this prevents: an agent builds 3 files referencing `warehouse_name` and `notes`. The actual database has `name` and `remarks`. 30 minutes of debugging follows before anyone checks the table definition. The assumption cost real time. The grep would have cost 10 seconds.

**Applied rule:** every prompt that references field names, file paths, or API shapes must be pre-verified against the actual source — schema file, API response, or `ls` output — not memory or the spec document.

---

### Rule 2 — Don't Over-Organise

Keep it flat and simple. No unnecessary subfolders. No hierarchies that require a map to navigate.

A knowledge base with 3 levels of nesting and 14 category folders has solved the organisation problem at the cost of the retrieval problem. If you need a diagram to explain where things live, the structure is wrong.

The right question: can a cold agent, reading only the index file, find what it needs in under 30 seconds? If no, simplify.

**Applied rule:** one level of folders, each file named for its topic, an index file at the root. Add a subfolder only when the flat structure genuinely breaks (more than ~30 files in one folder, or two domains that should never mix).

---

### Rule 3 — Don't Read the Wiki Unless You Need It

Check recent context first. Check the hot cache. Only crawl the full knowledge base when the answer isn't immediately available.

This is a cost discipline rule. Every file you read consumes context window. Reading 20 technique files because "one of them might be relevant" is wasteful. The hot cache (recent decisions, current sprint state, last known good configuration) covers 80% of questions. The full wiki covers the rest.

**Applied rule:** agents check recent conversation context → hot cache → index → specific file. Never start a session by reading all 20 files in the knowledge base.

---

### Rule 4 — Ask Before Ingesting

Before absorbing new content into the knowledge base: "What to emphasise? How granular? What's the focus?" Don't blindly dump raw input into organised structure.

Raw content (a transcript, an article, a spec document) contains noise, redundancy, and context that made sense for its original format but doesn't belong in a referenceable wiki. Processing it without a brief means the knowledge base fills with semi-organised noise.

**Applied rule:** when new content arrives, the first action is 3 questions — what's the core insight, what existing file does this connect to, does this need its own entry or a paragraph in something that already exists?

---

## The Operating Cycle

Knowledge work is not linear. It's a cycle that never fully completes.

```
Ingest → Organise → Query → Lint → Repeat
```

**Ingest:** raw content enters the system (transcript, article, meeting notes, error log)
**Organise:** processed into the wiki, connected to existing entries, indexed
**Query:** agents query the wiki naturally when they need something
**Lint:** periodic health check — find stale entries, gaps, broken references, outdated information
**Repeat:** the cycle runs continuously, not in batches

The lint step is the most skipped and the most important. A knowledge base that never gets linted becomes a historical archive. It still contains accurate information from 6 months ago — which is sometimes wrong today. Weekly lint sessions (even 15 minutes) keep the knowledge base current.

---

## The Architectural Choice: Markdown Wiki vs Vector DB

For knowledge bases under ~500,000 words (approximately 400 dense markdown files), a well-organised markdown wiki outperforms a RAG system with vector embeddings.

| Dimension | Markdown Wiki | Vector DB RAG |
|-----------|--------------|---------------|
| How it finds information | Index → follow links → read file | Similarity search on embeddings |
| Understanding depth | Explicit relationships, full context | "These chunks seem similar" |
| Infrastructure | Markdown files + a text editor | Embedding model + vector DB + chunking pipeline |
| Cost | Zero (just tokens) | Ongoing compute + storage |
| Maintenance | Read, lint, update | Re-embed when content changes |
| Setup time | Minutes | Hours to days |
| Failure mode | Stale content | Wrong chunk retrieved silently |

RAG wins when you have millions of documents, real-time updates, or thousands of simultaneous users querying different things. Below that scale, it's engineering complexity in service of a retrieval problem that doesn't exist yet.

One documented case: a user reorganised 383 scattered files and 100 meeting transcripts into a compact markdown wiki. Token usage on queries dropped 95%. Not because the LLM got smarter — because the input got cleaner.

---

## The Hot Cache Pattern

The hot cache is a single file — call it `hot.md` — updated at the end of every session with the most relevant current state.

```markdown
# Hot Cache — Current State

Last updated: [date]
Current sprint: [what's in progress]
Last known good: [git tag or commit SHA]
Active constraints: [what's locked, what's blocked]
Recent decisions: [2-3 decisions made this week, in one line each]
```

A cold agent reading the hot cache gets 80% of what it needs to orient itself — without reading the full wiki. This is how you make warm-start feel cheap. The hot cache doesn't replace the wiki. It's the entry point before the wiki.

---

## Crystallised Principle

**The knowledge base that earns trust is the one that's simple enough to lint, flat enough to navigate, and current enough to act on.**

Don't assume. Don't over-organise. Don't read everything. Ask before ingesting. Then cycle: ingest, organise, query, lint, repeat. For most projects, a set of flat markdown files beats a vector database — not because vector search is bad, but because clarity of structure compounds faster than retrieval sophistication.
