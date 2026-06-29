# Knowledge Graph over Tabular / Relational Data

> Companion to [`foundations/rag-retrieval/`](../../foundations/rag-retrieval/) and
> [`domains/rag-knowledge/`](../../domains/rag-knowledge/), which assume an unstructured corpus
> (PDFs, docs, code). This page covers the case those don't: **structured, relational data where
> the relationships *are* the answer.**

First principle, same as the rest of the kit: don't reach for a graph when a prompt or plain
SQL works. A knowledge graph earns its complexity when entities are richly connected and
questions require *traversal* — multi-hop reasoning that joins many tables.

## When a graph beats vector RAG

| Scenario | Vector RAG | Knowledge graph |
|----------|-----------|-----------------|
| Unstructured docs (PDFs, text) | Best choice | Overkill |
| Structured / tabular data (SQL, spreadsheets) | Struggles | **Best choice** |
| Mixed structured + unstructured | Partial | **Strong** |
| Relationships between entities matter | Can't model | **Built for this** |
| Multi-hop ("who reports to the manager of the owner of…") | Fails | **Native** |

Vector RAG chunks text and ranks by similarity — it has no notion of *relationships* between
records. For business data where everything is connected (customer → order → product →
shipment), a graph preserves those edges and lets you walk them.

## Fundamentals

```
Nodes         = Entities          (Customer, Order, Product, Shipment)
Relationships = Edges / verbs     (PLACED, CONTAINS, FULFILLED_BY, SHIPPED_TO)
Properties    = Attributes        (date, amount, status) on nodes and edges
```

### A neutral worked example (generic e-commerce)

```
[Customer: Acme Co] --PLACED--> [Order #1042]
[Order #1042] --CONTAINS--> [Product: Widget-A]
[Order #1042] --FULFILLED_BY--> [Warehouse: North]
[Warehouse: North] --SHIPPED--> [Shipment #88]
[Shipment #88] --DELIVERED_TO--> [Customer: Acme Co]
```

A user can now ask *"Which customers have orders stuck before shipment?"* and the graph
traverses the whole chain — a query that would be a painful multi-join in SQL and impossible
for similarity search.

This generalizes to any connected domain: finance (Invoice → Payment → Vendor → Budget), HR
(Employee → Department → Manager → Review), sales (Lead → Contact → Meeting → Deal), or
manufacturing (Material → Production Order → QC → Finished Good → Delivery).

## Architecture

```
Tabular source (SQL / spreadsheets)
    │  parse → extract entities + relationships
    ▼
Construct graph  (Neo4j, or NetworkX for small/in-memory)
    │  store nodes/edges  (+ optional vector embeddings on node text)
    ▼
Two query paths:
   1. Graph query (Cypher)  — exact, structured traversal
   2. Vector search         — semantic similarity over node/edge text
    │
    ▼
LLM fuses both results → natural-language answer
```

Keep ingestion (extract → build graph → index) separate from query (translate question →
traverse / search → synthesize), exactly as with vector RAG — so you can re-index without
breaking serving and tune serving without re-ingesting.

## Minimal agent wiring

```python
from langchain_community.graphs import Neo4jGraph
# from langchain.agents import create_openai_tools_agent  # or your framework's equivalent

graph = Neo4jGraph(url="bolt://localhost:7687", username="neo4j", password="...")

# An agent equipped with a graph-query tool can translate a natural-language
# question into a structured traversal:
#   "Find all orders over 50k from last month" -> Cypher -> rows -> answer
```

## Key insight

Standard RAG searches *content*. A knowledge graph preserves *relationships*. The moment a
question is really about how records connect — not what a document says — switch retrieval
mechanisms. The same pattern underlies graph-based clinical assistants
(Disease → Symptom → Treatment → Drug) and any multi-hop question over connected business data.
