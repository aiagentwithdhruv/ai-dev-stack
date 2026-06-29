# Reference: Agentic Workflows Engine (WAT pattern)

**Origin:** distilled from a standalone "code-first agentic workflow" scaffold — a small
framework that separates *reasoning* (an agent) from *execution* (deterministic Python
tools), wired together by markdown *workflows*. Folded here as a reusable reference, not
as a vendored dependency.

## Why this is in the kit

The kit's `pillars/automation/` is **n8n-first** (visual, deterministic workflow engine) and
`pillars/agents/patterns/` covers agent *architecture* conceptually. Neither ships a concrete,
**runnable code-first scaffold** for the "AI reasons, code executes" pattern. This reference
fills that gap: a minimal layout plus a genuinely reusable, security-hardened shared library
(tool validation, path sandboxing, secret masking, input sanitisation, blocking budget guard,
transient-only retry, structured logging).

## What's here

| Path | What it is |
|------|------------|
| `README.md` | The WAT pattern explained — 3-layer architecture, the accuracy-compounding rationale, the self-improvement loop, security model. Vendor-neutral. |
| `AGENT-CONTRACT.md` | Drop-in `CLAUDE.md`-style operating contract for the agent that drives the engine. |
| `shared/` | The reusable hardened library — 8 modules, copied close to verbatim (clean, no internal refs). |
| `config/` | `models.example.yaml` (provider-agnostic LLM routing), `settings.yaml`, `credentials.yaml`. |
| `templates/` | `tool_template.py` and `workflow_template.md` — the scaffolding shape for new tools/workflows. |

## Sanitisation applied

This extract was rewritten to be vendor- and employer-neutral:

- **Removed a specific LLM-gateway vendor promotion** (free-tier quota claims, signup funnel,
  audience-specific framing). Replaced with a provider-agnostic, OpenAI-compatible routing
  pattern: any compatible gateway/aggregator or a direct provider key works by swapping
  `base_url`. Example env var names kept generic (`LLM_API_KEY`, `OPENROUTER_API_KEY`,
  `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`).
- **Genericised model identifiers** (e.g. `gpt-4o-mini`, `claude-sonnet`) — use your provider's
  current model ids; treat the strings here as placeholders.
- No personal names, employer/client names, emails, credentials, internal hosts, or tenant ids
  were present in the source; none were introduced.

## How to use it

Lift `shared/` directly into a code-first agent project — it's the most reusable part. Use
`AGENT-CONTRACT.md` as the seed for that project's agent instructions, and the `templates/` as
the shape every new tool/workflow follows.
