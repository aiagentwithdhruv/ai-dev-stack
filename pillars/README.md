# Pillars — the three build modes

Every AI-native project you ship lands in one of three modes. They sit on the same [foundations](../foundations/) — model selection, prompting, context engineering, retrieval, evals — but diverge sharply in architecture, risk profile, and what "done" means.

Pick the mode first. It decides your toolchain, your review loop, and how you verify the result.

## The three modes

| Mode | You are building... | Output | Verify by |
|------|---------------------|--------|-----------|
| **[Software Development](./software-development/)** | An app, service, or library — with AI as the engineer in the loop | Code that ships | Deterministic checks (build, types, tests) + independent review |
| **[Agents](./agents/)** | A system that reasons, uses tools, and acts with some autonomy | A running agent | Behavioural evals + adversarial verification + guardrails |
| **[Automation](./automation/)** | A deterministic workflow wiring services together | A pipeline that runs unattended | Replay on real payloads + idempotency + monitoring |

## How to choose

- **Software development** — when a human owns the result and AI accelerates the writing. The AI drafts; deterministic gates and a reviewer decide what merges.
- **Agents** — when the task is open-ended, needs tool use or retrieval, and the path can't be fully scripted ahead of time. You trade determinism for flexibility, and pay it back with evals and guardrails.
- **Automation** — when the steps are known and repeatable. Don't put a model in the loop where a deterministic workflow would do; it's cheaper, faster, and auditable. Add a model only at the steps that genuinely need judgement.

> Rule of thumb: **don't use an agent where a workflow works, and don't use a workflow where a single function call works.** Escalate a tier only when the simpler one can't express the problem.

## The modes compose

Real systems mix them. A product (software development) calls an agent (agents) for an in-app copilot, and an overnight automation (automation) refreshes the knowledge base that copilot reads. Build each part in the mode that fits it, and keep the seams explicit.

## Where automation lives

Automation is maintained in a **companion repository — `ai-automation-kit`** (n8n-first, plus general workflow automation). This pillar keeps only a [pointer page](./automation/) so the three-pillar map stays complete; the depth lives there.

## How to use

1. Identify the mode for the thing you're about to build.
2. Open that pillar's `README.md` for its patterns and checklist.
3. Cross-reference [foundations](../foundations/) for the cross-cutting concerns — [model routing](../foundations/model-routing-cost/), [evals](../foundations/evals-testing/), [guardrails](../foundations/guardrails-security/) — that every mode depends on.
