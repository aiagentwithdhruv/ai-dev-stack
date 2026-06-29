# Data Analytics

> BI copilots and text-to-SQL over a warehouse — ask in English, get SQL, a chart, and a narrative.

## What it is

A natural-language layer on top of a data warehouse. A non-technical user asks "why did revenue drop in the west region last quarter?" and the system writes safe SQL against a governed schema, runs it, and returns numbers, a chart, and a short explanation. The differentiator is not the LLM — it is the **semantic layer** that maps business terms to columns and keeps generated SQL correct and read-only.

## Why it matters

- **Analysts are a bottleneck.** Most "data requests" are simple aggregations queued behind a human. A copilot clears the queue.
- **Correctness is the whole game.** A confidently wrong number is worse than no number. The semantic layer plus validation is what makes this trustworthy.
- **Read-only by construction.** A SQL-generating agent must never mutate the warehouse — SELECT only, no INSERT/UPDATE/DELETE without explicit human confirmation.

## Typical stack / pattern

```
NL question → Resolve intent against semantic layer (metrics, dims, joins, grain)
            → Generate SQL → Validate (read-only, allowed tables, row limit, cost guard)
            → Execute on warehouse → Result set
            → Render chart + plain-language narrative → (offer "show SQL")
```

- **The semantic layer is the contract.** Curated metrics, dimensions, allowed joins, and grain — supplied as context so the model never guesses a join key.
- **SQL passes a validator before it runs:** SELECT-only, allowlisted tables, mandatory row/cost limits, no DDL/DML. (See [rule 70 — Security](../../rules/70-security.mdc).)
- **Tool-calling, not free text.** Treat "run_query" and "make_chart" as validated tools the model invokes, per [rule 60 — Agents](../../rules/60-agents.mdc).
- **NL-to-chart** picks the visual from the result shape (time series → line, category breakdown → bar) — deterministic rules, not a second LLM call.
- **Always show the SQL.** Transparency is how analysts learn to trust and correct the system.

## De-identified example outline

**Revenue analytics copilot** over a cloud warehouse:

| Layer | Choice |
|-------|--------|
| Semantic layer | ~30 curated metrics, 12 dimensions, declared joins and grain per fact table |
| Generation | NL → SQL conditioned on the semantic layer + the user's row-level access scope |
| Validation | Parse the SQL; reject anything non-SELECT, unscoped, or over a cost ceiling |
| Execution | Run on a read replica with a hard row limit and statement timeout |
| Output | Auto-selected chart + 2-sentence narrative + collapsible SQL |
| Eval | A suite of question→expected-SQL (or expected-number) pairs run on every prompt change |

## Foundations it leans on

- **Agents & orchestration** — tool schemas for query/chart, validated outputs
- **Guardrails & Safety** — SELECT-only enforcement, table allowlists, cost and row caps, row-level scope
- **Evaluation** — execution accuracy on a frozen question→answer set
- **Prompting & context** — injecting the semantic layer compactly so the model never hallucinates a column
- **Observability** — log every generated query and its cost

See [foundations/](../../foundations/README.md) for the reusable implementations.

## How to use

1. Build or import the semantic layer first — it is the source of truth the model reads. Document it in [docs/DB_SCHEMA.md](../../docs/DB_SCHEMA.md).
2. Put the SQL validator on the critical path before any execution, per [rule 70](../../rules/70-security.mdc).
3. Wire query and chart as explicit tools ([rule 60](../../rules/60-agents.mdc)).
4. Freeze an execution-accuracy eval set before you tune prompts.

## Related

- [domains/](../README.md) — the other five verticals
- [foundations/](../../foundations/README.md) · [rule 60 — Agents](../../rules/60-agents.mdc) · [rule 70 — Security](../../rules/70-security.mdc)
