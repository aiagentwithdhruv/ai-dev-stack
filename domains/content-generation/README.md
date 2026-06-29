# Content Generation

> Creative and marketing output — text, image, and video — at scale, on-brand, and localized.

## What it is

A production line for creative assets. A brief goes in; on-brand copy, images, and video come out, adapted across channels and languages, with a human approving before anything publishes. The value is throughput without brand drift: produce a campaign's worth of variants in minutes while keeping voice, palette, and legal constraints consistent. The engineering challenge is **consistency and control**, not raw generation — anyone can make one image; the product makes a thousand that all look like the same brand.

## Why it matters

- **Creative volume is the constraint.** Modern marketing needs dozens of variants per channel per locale; humans cannot keep up by hand.
- **Brand consistency is the moat.** Output that drifts off-voice or off-palette is unusable, no matter how clever.
- **Approval is mandatory.** Nothing auto-publishes. A human signs off before anything goes live — this is a hard product rule, not a setting.

## Typical stack / pattern

```
Brief → Inject brand system (voice, palette, do/don't, reference assets)
      → Multi-modal generation (copy / image / video) → N variants
      → Brand + safety checks (tone, banned claims, trademark, NSFW)
      → Localization (translate + transcreate per locale)
      → Human approval gate ──▶ publish to channels
```

- **The brand system is reusable context:** tone rules, style references, and prohibited claims supplied to every generation. It is the analog of the semantic layer in analytics. (See [rule 99 — Response Style](../../rules/99-response-style.mdc) for the consistency mindset.)
- **Generate wide, then filter.** Produce many candidates, then rank/filter against brand and safety checks rather than trusting a single shot.
- **Localization is transcreation, not translation** — idiom, length, and imagery adapt per market.
- **Safety and legal checks run before the human**, so reviewers only see compliant candidates.
- **Orchestrate the steps as a pipeline** with retries and idempotency, per [rule 60 — Agents](../../rules/60-agents.mdc) — this is where workflow tools (e.g. an n8n-style runner) earn their place.
- **Human approval is a required gate**, never bypassed.

## De-identified example outline

**Campaign asset factory** for an e-commerce brand:

| Layer | Choice |
|-------|--------|
| Input | A campaign brief + the brand kit (voice guide, palette, logo, reference shots) |
| Copy | On-voice headlines and body in N variants per channel |
| Visual | Product/lifestyle images conditioned on brand references |
| Video | Short-form cuts assembled from generated stills + voiceover |
| Localization | Transcreated per target market, not literally translated |
| Checks | Banned-claim filter, trademark/NSFW screen, length/format per channel |
| Approval | Reviewer picks finals from compliant candidates; only then publish |

## Foundations it leans on

- **Prompting & context** — encoding brand voice and style references compactly and repeatably
- **Guardrails & Safety** — banned claims, trademark/NSFW screening, brand-consistency checks
- **Pipelines & orchestration** — multi-step, multi-modal generation with retries and idempotency
- **Evaluation** — brand-fit and safety pass rates; human acceptance rate per variant type
- **Observability** — track which prompts and references yield approved assets

See [foundations/](../../foundations/README.md) for the reusable implementations.

## How to use

1. Codify the brand system first — it is the context every generation reads. Document it alongside the [PRD](../../docs/PRD.md).
2. Build the safety/brand checks before scaling volume, so reviewers never see non-compliant output.
3. Keep the human approval gate hard-wired; nothing publishes without sign-off.
4. Measure human acceptance rate per asset type and feed it back into prompt and reference tuning.

## Related

- [domains/](../README.md) — the other five verticals
- [foundations/](../../foundations/README.md) · [rule 60 — Agents](../../rules/60-agents.mdc) · [rule 99 — Response Style](../../rules/99-response-style.mdc)
