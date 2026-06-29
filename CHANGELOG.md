# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-06-29

### Added
- **Two new pillars** under `pillars/`: `agents/` (tool schemas, orchestrator–worker and supervisor patterns) and `automation/` (event-driven and scheduled pipelines, linking to the companion automation repo).
- **Application domains** under `domains/`: `rag-knowledge`, `data-analytics`, `voice`, `vision-doc-ai`, `content-generation`, and `decisioning-forecasting`.
- **New foundations**: `evals/`, `observability/`, and `guardrails/` — the production-trust layer that sits alongside rules and docs.
- **Sample prompts** under `foundations/prompts/` — reusable system and task prompt patterns.
- `_frontier/` — reserved space for emerging patterns that are not yet production-stable.

### Changed
- **Restructured the repository into `foundations/` × `pillars/` × `domains/`** — a substrate plus two composable axes (HOW you build × WHAT you build), replacing the flat `rules/` + `docs/` layout.
- Rewrote the top-level `README.md` as an umbrella front door with the substrate-and-two-axes map.
- The existing engineering rules and doc templates now live under `foundations/` and `pillars/software-development/`.

### Migration
- Existing installs are unaffected: the Quick Start `curl` commands still fetch the same Cursor rules and `CLAUDE.md`. The restructure reorganizes the source tree, not the installed artifacts.

## [1.3.0] - 2026-03-08

### Added
- `SKILLS.md`, `AGENTS.md`, `LOADOUT.md`, and `MCP.md` doc templates.
- `.claude/settings.json` permission-config template.
- Hero image and content-distribution kit.

### Changed
- Renamed the project to `ai-coding-rules`.

## [1.2.0] - 2026-03-08

### Added
- Claude Code support via a single combined `CLAUDE.md` containing all 15 rules.
- Individual Claude Code rule files plus `compose.sh` for building custom rule sets.

## [1.1.0] - 2026-03-08

### Added
- Five project doc templates: `PRD.md`, `ARCHITECTURE.md`, `API_SPEC.md`, `DB_SCHEMA.md`, `DEPLOYMENT.md`.

## [1.0.0] - 2026-03-08

### Added
- Initial release: 15 production-grade Cursor rules for AI-native full-stack development.
