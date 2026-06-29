# Reference: AI Automation Course Kit (folded extract)

**Origin:** a public teaching repo that pairs an agentic-automation curriculum with ~15 runnable
example automations (news bot, RAG chatbot, CRM, support tickets, voice agent, e-commerce suite,
client acquisition, etc.). Deployed on free infrastructure (GitHub Actions cron + n8n).

**Why this is here (not in the main pillars):** the flagship already carries the *prose* layer for
agents, automation, guardrails, and model-routing. The source repo also carries the **runnable
layer** that the prose describes — a small dependency-light safety harness, a set of ready-to-drop
sub-agent role files, and a few hands-on technique notes. That runnable/curated material is what
got folded here. It is reference-grade: copy a file, strip the comment header, use it.

## What's in this folder

| Path | What it is | Why it's worth keeping |
|------|------------|------------------------|
| `architecture/three-layer-agent-workflow-tools.md` | The Agent / Workflow / Tools separation, the Sense→Think→Decide→Act→Learn loop, and the accuracy-compounding argument for pushing execution into deterministic code | A clean, tool-agnostic mental model for why "let the model orchestrate, let code execute" beats end-to-end LLM pipelines |
| `agent-safety-harness/` | Six small, dependency-light Python modules: tool static-analysis, write-path sandbox, output secret-masking, input/URL sanitisation (SSRF block), retry-with-backoff, per-run/per-day cost ceiling | The flagship's `foundations/guardrails-security` is prose; this is the executable version of the same ideas |
| `subagents/` | 10 ready-to-use sub-agent definition files (frontmatter + role brief): code-reviewer, security-auditor, api-integrator, backend-builder, frontend-builder, db-architect, test-runner, researcher, deployer, mcp-builder | Drop-in role files for any multi-agent setup; complements the flagship's `docs/AGENTS.md` and `pillars/agents` prose |
| `techniques/` | Three hands-on pattern notes: webhook patterns, cost optimization, deployment patterns | Concrete recipes (signature verification, idempotency, model-routing-by-task, free-tier deploy decision matrix) under the flagship's `foundations` themes |

## What was deliberately NOT folded (leak-safety + de-dup)

- **The coding-rules / docs / claude slice of the source** (`rules/00..99`, `docs/AGENTS.md` etc.,
  `claude/CLAUDE.md` + `compose.sh`) — this is **already present** in the flagship `rules/`,
  `docs/`, and `claude/`. Not re-folded; it would be a duplicate.
- **All author/identity, course, and marketing material** — instructor bio, course logistics,
  pricing, booking links, personal product names, brand assets/logos/photos, and the personal
  RAG knowledge base. None of it is generic; all of it was excluded.
- **The 15 full example automations** verbatim — they are good teaching code but folding them
  whole would be a dump. Their reusable *patterns* are captured in `techniques/` and
  `agent-safety-harness/` instead.

## Sanitisation applied

Every file here was rewritten to be vendor- and employer-neutral: author names, course/brand
names, booking/marketing links, and provider-specific free-tier branding were removed. The
harness modules were made self-contained (stdlib `logging` instead of a project-local logger;
the secret-masking list is now read from the environment instead of a hardcoded vendor key list).
