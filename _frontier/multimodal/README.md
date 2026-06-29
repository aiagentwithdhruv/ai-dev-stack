# _frontier/multimodal/ — Multimodal as Default Input

> **Status: reserved — coming.** Maturity: **Cross-cutting**. Touches many existing rules rather than forming a new layer.

The assumption that inputs are images, PDFs, audio, and video — not just text — and that
this is the *default*, not a special case. Reserved here because the pattern cuts across
the API, RAG, agent, and storage rules at once; it needs threading through the existing
layers, not a standalone rule of its own.

See the umbrella in [`../README.md`](../README.md) and the stable core in
[`../../foundations/`](../../foundations/).

## Why it matters

Most real business inputs were never plain text: scanned contracts, screenshots, voice
notes, product photos, recorded calls. Designing around text-only and bolting media on
later forces rework through every layer — ingestion, validation, retrieval, storage, and
the model call itself. Treating media as a first-class input from the start keeps those
layers honest.

## What this will cover

- **Ingestion** — accepting and normalizing images, PDFs, audio, and video at the API
  boundary, with validation and size/type limits like any other untrusted input.
- **Extraction & grounding** — pulling structured content from documents and media so it
  feeds [retrieval and RAG](../../rules/) instead of being passed around as opaque blobs.
- **Multimodal RAG** — indexing and retrieving across modalities, with chunk metadata that
  records the source modality and location.
- **Storage & references** — keeping large media out of the database, referenced by stable
  IDs, served through a controlled path rather than embedded.
- **Cost & latency** — media tokens and processing are expensive; budgeting and caching
  decisions belong in the design, not as an afterthought.

## Early checklist (when you design for media)

- [ ] Media inputs are validated and bounded at the boundary, same as text.
- [ ] Large files are stored by reference, never inlined into the database.
- [ ] Retrieval metadata records source modality and location for every chunk.
- [ ] Extraction failures degrade gracefully — partial content beats a hard error.
- [ ] Cost and latency of media processing are budgeted and cached deliberately.
- [ ] No untrusted media reaches a model without passing the same guardrails as text.

## How to use

When a feature might take media, design for it from the first layer — don't special-case
it later. Reuse the existing [rules](../../rules/) and [docs](../../docs/) templates;
this area exists to remind you to thread media through all of them rather than to replace
any. It graduates once that threading is captured directly in those rules.
