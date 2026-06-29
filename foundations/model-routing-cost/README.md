# Model Routing & Cost

> Never hard-code one model. The model id is a runtime decision, not a constant — bake one in and you've coupled your product to one provider's pricing, availability, and roadmap.

## What this is

A routing layer that sits between your application and the model providers. It picks the right model per request based on task difficulty, cost budget, and latency target; falls back when a provider fails; and lets you swap or add models without touching application code.

## Why it matters

Using your most capable (and most expensive) model for every request is how AI features become unprofitable. Most traffic is easy — classification, extraction, short answers — and a cheaper, faster model handles it at a fraction of the cost. Reserve the frontier model for the hard 10-20%. Just as important: providers have outages and rate limits. A system wired to a single model goes down with it; a routed system fails over and stays up.

## Core patterns

| Pattern | What it does | Why |
|---------|-------------|-----|
| **Provider abstraction** | One internal interface, many providers behind it | Swap models via config, not code |
| **Quality-tiered selection** | Route by task difficulty: cheap → mid → frontier | Pay frontier prices only where they earn it |
| **Fallback chain** | On error/timeout/rate-limit, retry the next model | Survive provider outages |
| **Budget enforcement** | Per-feature/tenant spend caps and alerts | No surprise bills; cost is a controlled input |

### Quality-tiered selection

Classify each request and route it:

- **Cheap tier** — high-volume, low-difficulty: classification, extraction, routing, short-form. Small/fast models.
- **Mid tier** — general reasoning, drafting, summarization at length.
- **Frontier tier** — hardest cases: complex multi-step reasoning, high-stakes output, anything a smaller model fails on in your evals.

Decide tiers with data, not vibes — run candidates through [../evals-testing](../evals-testing/README.md) and route down to the cheapest tier that *holds quality* on the golden set.

### Fallbacks — design for provider failure

- Build an ordered chain: primary → secondary → tertiary, ideally across providers.
- Trigger on errors, timeouts, and rate limits — not just hard failures.
- Cap retries and total latency so a failover storm doesn't blow your latency budget.
- A cross-provider fallback also covers single-provider outages, which will happen.

### Budgets — make cost a first-class control

- Set spend caps per feature and per tenant; alert before the cap, act at it.
- Attribute every call's cost back via [../observability](../observability/README.md).
- Use the data to prove a routing change saves money *before* rolling it to all traffic.

## Routing checklist

- [ ] No model id hard-coded in application logic — all routing is config-driven.
- [ ] A provider-abstraction layer hides provider-specific SDKs from the app.
- [ ] Requests are tiered cheap/mid/frontier by difficulty.
- [ ] Tier choices are validated against evals, not assumed.
- [ ] An ordered, cross-provider fallback chain handles errors, timeouts, and rate limits.
- [ ] Retry and latency caps prevent failover from breaking the latency budget.
- [ ] Per-feature/tenant budgets with alerts and cost attribution.
- [ ] Adding or swapping a model is a config change, reviewable and revertible.

## How to use this

Put the abstraction layer in from day one even if you start with a single model — it costs almost nothing early and is expensive to retrofit. Let evals decide tiers and let observability prove savings; routing without those two is guesswork. When you do move traffic to a cheaper tier, ship it as a staged rollout (see [../deploy-mlops](../deploy-mlops/README.md)) so a quality regression is caught on a slice, not the whole user base.
