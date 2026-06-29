# Foundations — the substrate

The rules in [`../rules/`](../rules/) tell an AI coding tool **how** to write code. The docs in [`../docs/`](../docs/) tell it **what** you are building. The foundations are the layer underneath both: the **substrate** — the durable engineering concepts an AI-native team relies on regardless of which model, editor, or framework is in front of it.

Think of it as the part that does not change when you swap Cursor for Claude Code, or one model vendor for another. Frameworks rotate. The substrate stays.

## Why this layer exists

Most AI-coding guidance is tool-specific and expires fast. A prompt trick that works this quarter breaks next quarter. The foundations capture the patterns that survive model upgrades: how you assemble context, how you retrieve knowledge, how you delegate to agents, how you verify their output, and how the system learns from its own mistakes.

Read these when you want to understand *the principle*, then drop into [`../rules/`](../rules/) for the enforced version.

## The 10 foundation areas

| # | Area | What it covers | Rule it maps to |
|---|------|----------------|-----------------|
| 1 | **[Setup](./setup/)** | Install rules into Claude Code, Cursor, and other editors | — |
| 2 | **[Prompting & Context](./prompting-context/)** | System prompts, few-shot, structured output, context-window assembly, history compression | — |
| 3 | **[RAG & Retrieval](./rag-retrieval/)** | Chunking, hybrid search, reranking, GraphRAG — the retrieval *pattern* layer | [`50-rag-system`](../rules/50-rag-system.mdc) |
| 4 | **Agents & Orchestration** | Tool schemas, orchestrator–worker, lane ownership, supervisor patterns | [`60-agents`](../rules/60-agents.mdc) |
| 5 | **Evaluation & Testing** | Golden sets, LLM-as-judge, regression suites, deterministic units | [`80-testing-quality`](../rules/80-testing-quality.mdc) |
| 6 | **Observability** | Tracing, structured logging, token/cost/latency, health checks | [`85-error-observability`](../rules/85-error-observability.mdc) |
| 7 | **Security & Guardrails** | Prompt-injection resistance, layered guardrails, secret hygiene | [`70-security`](../rules/70-security.mdc) |
| 8 | **Data & Model Versioning** | Versioned datasets, named checkpoints, reproducibility | [`55-data-model-versioning`](../rules/55-data-model-versioning.mdc) |
| 9 | **Deployment & Serving** | Model gateways, containers, environment config, CI/CD | [`90-devops-deployment`](../rules/90-devops-deployment.mdc) |
| 10 | **Learning Loop** | The audit/verify loop, an error log, knowledge that compounds across sessions | — |

Areas 1–3 ship with their own README in this folder. Areas 4–10 are anchored by the rule file in the right-hand column — read the rule for the enforced behavior, and treat the row here as the conceptual map.

## How to use

- **New project?** Start at [Setup](./setup/) — get the rules into your editor first, then everything else has a place to live.
- **Designing an AI feature?** Read [Prompting & Context](./prompting-context/) and [RAG & Retrieval](./rag-retrieval/) before you write a line. Most production failures are context-assembly failures, not model failures.
- **Scaling a team of agents?** Areas 4–6 (orchestration, evaluation, observability) are where multi-agent systems live or die.
- **Want the enforced version?** Every concept here has a counterpart in [`../rules/`](../rules/). The foundations explain the *why*; the rules enforce the *what*.

## Design principles for this layer

- **Vendor-neutral by default.** Concepts are described so they survive a model or editor swap. Where a concrete tool helps, only its public name is used.
- **Don't reach for the heavy tool first.** Don't use an agent when a function works. Don't use RAG when a prompt works. Don't fine-tune when retrieval works.
- **The schema is the contract.** Decide the data shape — chunk metadata, tool input/output, eval record — before the implementation.
- **Verify, then trust.** Every generation path should have a path that checks it. The [Learning Loop](#the-10-foundation-areas) closes that circle.
