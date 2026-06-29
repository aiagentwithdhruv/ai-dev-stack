# Deploy & MLOps

> An AI system isn't software plus a model — it's code, prompts, models, data, and config that must ship together and roll back together. If any one of those can change without a deploy, you can't reproduce a bug.

## What this is

The delivery discipline for LLM systems: CI/CD that gates on evals, containerized serving, versioning of everything that affects output, and staged rollouts that catch regressions before they reach everyone. Classic MLOps adapted to the reality that the "model" is often a hosted API and the real artifacts you control are prompts, retrieval config, and orchestration code.

## Why it matters

The gap between a notebook that works and a service that stays up is where most AI projects die. Without versioning you can't answer "what changed?" Without staged rollout, one bad prompt edit hits 100% of traffic. Without CI gating on quality, you ship regressions you can't see until users report them. The teams that ship reliably treat the model system like any other production service — repeatable builds, automated gates, reversible deploys.

## Core practices

| Practice | What it means | Rule |
|----------|--------------|------|
| **CI/CD for AI** | Pipeline runs lint, tests, and **evals** on every change | Eval regression fails the build (see [../evals-testing](../evals-testing/README.md)) |
| **Containerized serving** | Package the serving layer as a reproducible image | Same image runs in dev, staging, prod |
| **Version everything** | Code, prompts, model ids, retrieval config, datasets | If it changes output, it has a version |
| **Staged rollout** | Canary → percentage → full, with auto-rollback | Limit blast radius; never flip 0→100% |

### CI/CD for AI

Extend the normal pipeline with an eval stage. On every PR that touches a prompt, model, retrieval config, or agent: build → unit tests → **eval gate** → deploy to staging. The eval gate compares scores against the last green run and blocks merge on regression. This is the single highest-leverage habit for shipping AI safely.

### Containerized serving

- Build a reproducible image for the serving/orchestration layer; pin dependency versions.
- Build for the target architecture, not just your laptop — cross-compile if your dev machine differs from prod.
- Keep secrets out of the image; inject config and credentials at runtime from a secret manager.
- Health checks and graceful shutdown so orchestrators can manage rollout and recovery.

### Versioning & reproducibility

- **Prompts** — versioned, reviewed, stamped on every trace (see [../observability](../observability/README.md)).
- **Models** — pin provider model ids; a silent upstream model update is a deploy you didn't make. Track it in [../model-routing-cost](../model-routing-cost/README.md).
- **Data/retrieval** — version the corpus, chunking config, and index so retrieval behavior is reproducible.
- **Config** — environment-driven, validated at startup, never hard-coded.

### Staged rollout

- Canary first — a small slice of traffic — watch evals, cost, and latency.
- Expand by percentage; define a rollback trigger up front (quality, error rate, cost, latency).
- Automate rollback. A revert is cheap; a 100% bad deploy is not.

## Deploy checklist

- [ ] CI runs lint + unit tests + eval gate on every relevant change.
- [ ] Eval regression blocks the merge.
- [ ] Serving layer is a reproducible, version-pinned container built for the prod architecture.
- [ ] Secrets injected at runtime from a secret manager, never baked into image or repo.
- [ ] Prompts, model ids, retrieval config, and datasets are all versioned.
- [ ] Provider model ids pinned; upstream changes tracked.
- [ ] Rollouts are staged (canary → percentage → full) with a defined rollback trigger.
- [ ] Rollback is automated and tested.
- [ ] Health checks and graceful shutdown wired for orchestrated deploys.

## How to use this

Stand up the eval gate before you optimize anything else — it's what makes every later change safe. Version prompts and model ids from the first deploy; these are the two things that most often change output with no code diff and leave you unable to reproduce a bug. Treat the model system as a normal production service that happens to be non-deterministic, and lean on [../observability](../observability/README.md) to watch each rollout stage.
