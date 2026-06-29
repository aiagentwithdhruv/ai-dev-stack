# Contributing

Thanks for improving the AI Dev Stack. Contributions are small, focused, and reusable — a rule, a doc template, a prompt, or a worked example that any team can drop into a project. Keep additions vendor-neutral and self-contained.

## Where things go

| You're adding... | Put it in | Notes |
|------------------|-----------|-------|
| An engineering rule (architecture, security, style) | `foundations/rules/` | Numbered with gaps (e.g. `05-…` fits between `00` and `10`). |
| A doc template (PRD, schema, deploy, etc.) | `foundations/docs/` | Generic placeholders only — no real product data. |
| An eval, trace setup, or guardrail | `foundations/{evals,observability,guardrails}/` | Show how to *measure* or *constrain*, not just describe. |
| A reusable prompt | `foundations/prompts/` | One job per prompt; explain the inputs and expected output. |
| A build pattern (backend, agents, automation) | `pillars/<pillar>/` | Extend existing patterns before introducing new ones. |
| An application pattern (RAG, voice, analytics…) | `domains/<domain>/` | Keep it to the domain; cross-link to pillars rather than duplicating. |
| Something genuinely new and unproven | `_frontier/` | Mark it clearly as experimental. |

## How to add a rule, skill, prompt, or example

1. **Find the layer.** Decide whether it's substrate (`foundations/`), a *how* (`pillars/`), or a *what* (`domains/`). When unsure, prefer extending an existing file over creating a new one.
2. **Match the voice.** Principal-architect tone: concise, practical, imperative. Lead with the rule or pattern, not preamble. Read a neighbouring file first.
3. **Make it runnable or checkable.** Prefer a code block, a checklist, or a `how to use` note over prose. Examples should stand alone.
4. **Cross-link, don't copy.** Reference related material with relative paths (e.g. `../foundations/rules/`) instead of duplicating it.
5. **Keep each file focused.** Roughly 40–120 lines. If it grows past that, split it.

## The generic-content rule (required)

This is a **public** repository. Everything you write must be de-identified and vendor-neutral.

**Never include:**
- Employer, client, or internal project names, codenames, or product names.
- Personal names, emails, usernames, or team/role identifiers.
- Credentials, API keys, tokens, internal IPs, hostnames, or tenant/account IDs.
- Internal URLs, file paths, or any detail that identifies a specific organization.

**Do this instead:**
- Describe concepts generically — *local-first*, *orchestrator–worker*, *audit/verify loop*, *learning loop* — without the internal story behind them.
- Use a tool's **public name** only when you reference it (e.g. Claude Code, Cursor, n8n, LiteLLM, MCP).
- Use placeholders for anything specific: `your-project`, `<TENANT_ID>`, `example.com`.

**Self-check before opening a PR:** grep your diff for company names, person names, emails, and IPs. If a sentence only makes sense because of private context, rewrite it so it works for any reader.

## Pull requests

- One logical change per PR. Keep diffs reviewable.
- Add a `CHANGELOG.md` entry under the appropriate version section.
- Confirm the generic-content self-check passed in your PR description.

## License

By contributing, you agree your work is released under the repository's MIT license.
