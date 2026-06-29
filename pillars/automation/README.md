# Automation — pointer

> **Automation is maintained in a companion repository: `ai-automation-kit`.**
> This page is a signpost so the three-pillar map stays complete. The depth lives there.

## What this pillar covers

The **automation** build mode is for deterministic workflows that wire services together and run unattended — triggers, connectors, branching, retries, and scheduled jobs. It is **n8n-first** (visual, self-hostable workflow automation), but the patterns apply to any workflow engine.

Automation is the right mode when the steps are known and repeatable. Reach for it *before* an [agent](../agents/): a deterministic workflow is cheaper, faster, and auditable. Add a model only at the specific steps that need judgement — classification, extraction, drafting — and keep the rest deterministic.

## What lives in the companion repo

- **n8n-first patterns** — workflow structure, error handling, idempotency, retries
- **General workflow automation** — triggers, schedules, webhooks, connectors
- **LLM-in-the-loop steps** — where and how to drop a model into an otherwise deterministic pipeline
- **Operational concerns** — secrets, monitoring, replay on real payloads, cost control

## When to stay here vs go agentic

| Stay in automation | Escalate to [agents](../agents/) |
|--------------------|----------------------------------|
| Steps are known and ordered | The path is open-ended |
| Same shape every run | Each run needs different reasoning |
| A model call is one step | The model drives the whole flow |

## How to use

Decide the mode here, then build it in `ai-automation-kit`. For the broader map of all three build modes, see the [pillars overview](../README.md); for the cross-cutting concerns every mode shares, see [foundations](../../foundations/).

---

*Link: `ai-automation-kit` — companion repository (n8n-first + general workflow automation). https://github.com/aiagentwithdhruv/ai-automation-kit*
