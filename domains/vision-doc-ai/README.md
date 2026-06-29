# Vision / Doc AI

> Document intelligence (IDP) — turn invoices, contracts, and KYC packets into structured JSON, then route them.

## What it is

Intelligent Document Processing: ingest a messy real-world document (a scanned invoice, a 40-page contract, an ID with a selfie) and emit clean, validated, structured data that a downstream system can act on. The output is a schema-conformant JSON object plus a routing decision — post to the ERP, flag for legal review, approve the KYC. The win is replacing manual data entry and the error rate that comes with it.

## Why it matters

- **Manual document handling is pure cost.** Every invoice keyed by hand is slow, expensive, and error-prone.
- **Structured output is the deliverable.** Unlike a chat answer, the output must conform to a strict schema so the next system can consume it without a human.
- **Confidence drives routing.** The system's real intelligence is knowing when it is *unsure* and sending that case to a human — not pretending every field is certain.

## Typical stack / pattern

```
Ingest (PDF / scan / photo) → OCR + layout analysis → Field extraction (VLM or LLM + schema)
                                                            │
                          Validate against schema + business rules → confidence score
                                                            │
                   high confidence ─▶ structured JSON ─▶ route to system of record
                   low  confidence ─▶ human-in-the-loop review queue ─▶ correct ─▶ route
                                                            │
                                          corrections feed the eval / improvement loop
```

- **Extraction is schema-first.** Define the target JSON (with types and required fields) and make the model fill it — per [rule 35 — API Contracts](../../rules/35-api-contracts.mdc).
- **Validation is layered:** schema validation, then business rules (totals add up, dates are plausible, IDs match a checksum).
- **Confidence thresholds split the stream** into auto-process vs human review. This dial is the product's economics.
- **Human-in-the-loop (HITL) is a feature, not a fallback.** Corrected documents become labeled data that improves the system.
- **Page/region provenance** lets a reviewer jump straight to where each field was read from.

## De-identified example outline

**Accounts-payable invoice extraction** feeding an ERP:

| Layer | Choice |
|-------|--------|
| Ingest | Email/upload inbox; PDFs and phone photos normalized to images |
| OCR + layout | Layout-aware OCR to preserve tables and line items |
| Extraction | Target schema (vendor, dates, line items, tax, total) filled by a vision-capable model |
| Validation | Schema check + arithmetic check (line items sum to total within tolerance) |
| Routing | Confidence ≥ threshold → post to ERP; below → review queue with fields pre-filled |
| HITL | Reviewer confirms/corrects; correction logged as ground truth |
| Eval | Field-level accuracy and review-rate tracked on a frozen labeled set |

## Foundations it leans on

- **Data ingestion** — parsing, OCR, normalization, deduplication, provenance
- **Evaluation** — field-level accuracy, schema-conformance rate, human-review rate
- **Guardrails & Safety** — schema enforcement, PII handling, refusal on unreadable input
- **Agents & orchestration** — routing decisions as validated tool calls
- **Observability** — log extractions with confidence and source region for audit

See [foundations/](../../foundations/README.md) for the reusable implementations.

## How to use

1. Define the target JSON schema before anything else — it is the contract for extraction, validation, and routing. Capture it in [docs/API_SPEC.md](../../docs/API_SPEC.md).
2. Build validation and the confidence threshold early; the review queue is core, not optional.
3. Treat HITL corrections as your labeled dataset and close the loop into eval.
4. Report field-level accuracy on a frozen set, not whole-document pass/fail — partial extraction is the norm.

## Related

- [domains/](../README.md) — the other five verticals
- [foundations/](../../foundations/README.md) · [rule 35 — API Contracts](../../rules/35-api-contracts.mdc) · [rule 70 — Security](../../rules/70-security.mdc)
