# domains/ — The 6 Application Verticals

> **Domains are THE WHAT companies pay for.** Foundations are THE HOW you build them.

A domain is a shippable product category — the thing a buyer signs a contract for. Every domain is assembled from the same small set of reusable building blocks (retrieval, agents, evaluation, guardrails, serving). Learn the foundations once; recombine them into any of these six verticals.

This folder is a map, not a framework. Each vertical README gives you: what it is, the typical stack, a de-identified example outline you can clone, and which foundations it leans on.

## The 6 verticals

| # | Vertical | What you sell | Primary buyer | Leans hardest on |
|---|----------|---------------|---------------|------------------|
| 1 | [RAG / Knowledge](rag-knowledge/README.md) | Grounded answers over private docs, with citations and access control | Ops, Support, Legal, HR | Retrieval, Guardrails, Eval |
| 2 | [Data Analytics](data-analytics/README.md) | BI copilot — ask in English, get SQL, charts, and a narrative | Finance, RevOps, Analysts | Agents, Guardrails, Eval |
| 3 | [Voice](voice/README.md) | Real-time voice helpdesk / dialer with sub-300ms turn-taking | Support, Sales, Collections | Serving (latency), Agents |
| 4 | [Vision / Doc AI](vision-doc-ai/README.md) | Documents (invoices, contracts, KYC) → structured JSON + routing | Finance, Compliance, Back-office | Data ingestion, Eval, HITL |
| 5 | [Content Generation](content-generation/README.md) | Brand-consistent text/image/video at scale, localized | Marketing, Brand, E-commerce | Prompting, Guardrails, Pipelines |
| 6 | [Decisioning / Forecasting](decisioning-forecasting/README.md) | Demand forecasts, churn scores, recommendations | Supply chain, Growth, Product | Classical ML, Feature store |

## How to choose a vertical

- **Start from the buyer's pain, not the model.** A domain is defined by the decision or workflow it changes, not by which LLM it calls.
- **Match the data shape to the technique.** Unstructured private docs → RAG. Structured warehouse rows → text-to-SQL or classical ML. Streaming audio → voice. Scanned files → doc AI.
- **Don't reach for an LLM when a smaller tool wins.** Tabular prediction (vertical 6) is gradient boosting territory; an LLM is overkill and slower. See [Decisioning / Forecasting](decisioning-forecasting/README.md).

## How to use this folder

1. Pick the vertical that matches the buyer's problem.
2. Read its README — copy the example outline as your starting architecture.
3. Open the foundations it lists and reuse those building blocks instead of rebuilding them.
4. Fill in the project docs ([PRD](../docs/PRD.md), [ARCHITECTURE](../docs/ARCHITECTURE.md), [API_SPEC](../docs/API_SPEC.md), [DB_SCHEMA](../docs/DB_SCHEMA.md), [DEPLOYMENT](../docs/DEPLOYMENT.md)) so your AI coding tool has the full picture.
5. Let the [engineering rules](../rules/) enforce how the code gets written.

## Related

- [foundations/](../foundations/README.md) — the reusable building blocks every vertical is made of
- [rules/](../rules/) — 15 engineering rules that govern *how* the code is written
- [docs/](../docs/README.md) — project templates your AI reads before writing code
- [Kit root](../README.md) — install and overview
