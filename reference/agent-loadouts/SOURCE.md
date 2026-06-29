# Reference: Agent Loadouts (portable agent-context packaging framework)

**Origin:** Distilled and de-identified from a standalone "agent-loadouts" repo — a framework for
packaging reusable, portable **context packs** ("loadouts") that give an AI agent domain expertise
on the first prompt, across Claude Code / Cursor / Codex / any LLM.

**Why it lives in `reference/` (not in a pillar):** The flagship's `docs/LOADOUT.md` already covers the
*single-project* manifest idea. This reference captures the broader, complementary idea the flagship
didn't have: a **multi-file, cross-platform, self-updating context PACK** plus a convention and tooling
to manage a *library* of them. It's kept here as a curated pattern, not wired into the install flow.

## What a loadout is

Think RPG character loadout: equip one and the agent gains the skills, knowledge, runbooks, tests, and
behavioral rules for a specific domain. Instead of a vague system prompt, the agent gets structured,
verifiable, refreshable context.

A loadout is a folder with a standard shape:

```
loadout-name/
├── LOADOUT.md           # Manifest: identity, version, deps, refresh cadence, platforms
├── .claude/CLAUDE.md    # Auto-loaded master context (keep < ~200 lines)
├── knowledge/*.md       # Domain knowledge (market, glossary, best practices)
├── skills/*/SKILL.md    # Per-system deep context + technical recipes + typed Schema
├── runbooks/*.md        # Step-by-step procedures (deploy, configure, fix)
├── tests/*.md           # Validation scenarios that prove the agent knows its domain
├── memory/MEMORY.md     # Rolling memory template
└── workflows/*.json     # Optional automation exports (e.g. n8n)
```

## What's in this reference (all generic, de-identified)

| File | What it is |
|------|------------|
| `framework.md` | The packaging model: pack anatomy, cross-platform mapping, self-update/staleness pattern, and the generic CLI + MCP tool surface for managing a loadout library. |
| `schema-section-convention.md` | The typed `## Schema` section convention for SKILL files (Inputs / Outputs / Credentials / Composable-With / Cost) so skills are programmatically discoverable and chainable. |
| `templates/LOADOUT-TEMPLATE.md` | Manifest template (front-matter: version, tier, platforms, refresh cadence). |
| `templates/CONTEXT-TEMPLATE.md` | Auto-loaded master-context (CLAUDE.md) template with self-update rules. |
| `templates/SKILL-TEMPLATE.md` | Per-system skill template: architecture, codebase map, recipes, typed Schema. |
| `templates/RUNBOOK-TEMPLATE.md` | Procedure template: pre-checks, steps, verification, rollback. |
| `templates/TEST-TEMPLATE.md` | Validation-scenario template with edge cases + e2e flow. |

The five templates are MIT-licensed placeholder scaffolds in the source repo and contain no project data.

## Deliberately NOT folded (internal / identifying)

- **The project registry / `INDEX.md`** — a private catalog of real first-party and client projects,
  revenue figures, hackathon prizes, and commercial pricing tiers. Excluded entirely.
- **`tools/schemas.json`** — typed schemas for a specific personal/commercial skill library
  (lead-gen, outreach, course-support, etc.) plus a long list of provider API-key env-var names.
  Only the *convention* is captured here (`schema-section-convention.md`), not the data.
- **Tool implementations verbatim** (`loadout_cli.py`, `loadout_mcp.py`, `check_staleness.py`,
  `add_schemas_to_skills.py`) — hardcoded a personal absolute workspace path, a private n8n/Telegram
  webhook URL, and first-party project references. Only their generic *interface* is documented in
  `framework.md`; the implementations were not copied.
- **Author handles, business model, and pricing tiers** from the source README.
