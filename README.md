# AI Dev Stack

<p align="center">
  <img src="assets/hero.png" alt="AI Dev Stack — rules, docs, and patterns that make your AI coding tools build like a senior engineer" width="100%">
</p>

A production-grade kit of rules, docs, prompts, and patterns for AI-native development. It teaches your AI coding tools — **Cursor** and **Claude Code** — to think like a principal architect: pick the right layer, follow clean architecture, and ship deploy-ready code instead of demos. Drop it into any project and the assistant inherits a consistent operating model on the first prompt.

## Quick Start

### Cursor
```bash
curl -fsSL https://raw.githubusercontent.com/aiagentwithdhruv/ai-coding-rules/main/install.sh | bash
```

### Claude Code
```bash
curl -fsSL https://raw.githubusercontent.com/aiagentwithdhruv/ai-coding-rules/main/claude/CLAUDE.md -o CLAUDE.md
```

### Both (recommended)
```bash
curl -fsSL https://raw.githubusercontent.com/aiagentwithdhruv/ai-coding-rules/main/install.sh | bash
curl -fsSL https://raw.githubusercontent.com/aiagentwithdhruv/ai-coding-rules/main/claude/CLAUDE.md -o CLAUDE.md
```

## The mental model: substrate × two axes

Everything in the kit sits on one **substrate** and is organized along **two axes** — *how* you build and *what* you build. Reserved space (`_frontier/`) holds patterns that aren't stable yet.

```
ai-dev-stack/
├── foundations/      # SUBSTRATE — non-negotiables every build inherits
│   ├── rules/                  # clean architecture, security, response style
│   ├── docs/                   # PRD / ARCHITECTURE / API / SCHEMA / DEPLOY templates
│   ├── evals/                  # measure before you trust — task + regression evals
│   ├── observability/          # tracing, cost, latency, structured logs
│   ├── guardrails/             # layered policy → input → output → monitor
│   └── prompts/                # reusable system + task prompt patterns
│
├── pillars/          # AXIS 1 — HOW you build
│   ├── software-development/   # backend, frontend, data, API contracts, DevOps
│   ├── agents/                 # tools, schemas, orchestrator–worker, supervisor loops
│   └── automation/             # event/scheduled pipelines  → companion repo below
│
├── domains/          # AXIS 2 — WHAT you build
│   ├── rag-knowledge/          # ingestion, chunking, retrieval, grounded answers
│   ├── data-analytics/         # NL-to-SQL, metrics, reporting, BI assistants
│   ├── voice/                  # STT, TTS, real-time voice agents
│   ├── vision-doc-ai/          # OCR, document extraction, multimodal pipelines
│   ├── content-generation/     # long-form, structured, and media generation
│   └── decisioning-forecasting/# scoring, ranking, prediction, recommendations
│
└── _frontier/        # RESERVED — emerging patterns, not yet production-stable
```

**Read it as a grid.** Any project picks one or more **pillars** (the *how*) and one or more **domains** (the *what*), then stands the whole thing on **foundations**. A RAG support assistant is `pillars/agents` + `domains/rag-knowledge` on `foundations/{rules,evals,guardrails}`. A nightly report bot is `pillars/automation` + `domains/data-analytics`. The substrate never changes; the axes compose.

## The substrate — [foundations/](foundations/)

The defaults every build inherits, regardless of pillar or domain. Rules and doc templates tell the AI *how* to write code and *what* you're building; evals, observability, and guardrails keep it honest in production. Start here — see [foundations/](foundations/).

## Axis 1 — pillars (HOW you build)

| Pillar | What it covers |
|--------|----------------|
| [software-development/](pillars/software-development/) | Thin routes, services, repositories, typed API contracts, caching, CI/CD. |
| [agents/](pillars/agents/) | Tool schemas, validated outputs, orchestrator–worker and supervisor patterns. |
| [automation/](pillars/automation/) | Event-driven and scheduled pipelines — see the companion repo below. |

## Axis 2 — domains (WHAT you build)

| Domain | What it covers |
|--------|----------------|
| [rag-knowledge/](domains/rag-knowledge/) | Separate ingestion from generation; chunk metadata; grounded, cited answers. |
| [data-analytics/](domains/data-analytics/) | NL-to-SQL, read-only query agents, metrics, dashboards. |
| [voice/](domains/voice/) | Speech-to-text, text-to-speech, low-latency voice agents. |
| [vision-doc-ai/](domains/vision-doc-ai/) | OCR, document extraction, multimodal understanding. |
| [content-generation/](domains/content-generation/) | Long-form, structured, and media content with quality gates. |
| [decisioning-forecasting/](domains/decisioning-forecasting/) | Scoring, ranking, forecasting — classical models before LLMs for tabular data. |

## Companion repo

**[ai-automation-kit](https://github.com/aiagentwithdhruv/ai-automation-kit)** — n8n templates and workflow-automation patterns. The `automation` pillar links out to it so this repo stays focused on the build-time stack while workflow orchestration lives next door.

## Suggested GitHub Topics

`ai-agents` · `rag` · `llm` · `prompt-engineering` · `automation` · `mcp` · `llmops` · `evals` · `claude-code` · `cursor` · `ai-development`

## Contributing & changelog

- Adding a rule, prompt, or pattern? See [CONTRIBUTING.md](CONTRIBUTING.md) — including the generic, de-identified content rule.
- Version history lives in [CHANGELOG.md](CHANGELOG.md).

## License

MIT — use it, fork it, ship better code.
