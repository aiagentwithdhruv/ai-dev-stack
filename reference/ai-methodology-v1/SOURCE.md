# Reference: AI Development Methodology (operating-model layer)

**Origin:** folded from a standalone, self-described vendor-neutral methodology repo
(`ai-methodology-v1`, "An operating system for AI projects"). That repo packaged the
operating model accumulated across 20+ production AI builds. This folder keeps the parts
that the rest of `ai-dev-stack` does **not** already cover.

## Why this is here (and not duplicated)

The rest of `ai-dev-stack` is a **technical** AI stack: `foundations/`, `pillars/`,
`domains/`, `prompts/`, coding `rules/`, architecture `docs/`. It tells you *how to build
the AI system*.

This reference is the **operating-model** layer on top: how to *run* an AI-assisted
project with an agent team without losing work, repeating mistakes, or drowning in 12-hour
manual sessions. It is process discipline, not technology.

## What's in this folder

| Folder | What it gives you |
|--------|-------------------|
| `philosophy/` | Operating principles: hold-position (a question is not a correction), the orchestrator model, plus knowledge-base rules attributed to two public thinkers (Naval Ravikant, Andrej Karpathy). |
| `operating-model/` | The core discipline: 5 anti-drift gates, the prompt-file method, parallel-agent hygiene, cold-start session management, the additive "system improvement" protocol, and a 7-role team structure. |
| `failure-modes/` | The "scar ledger" — 8 named failure patterns (context rot, silent failures, render-vs-save, repeated mistakes, parallel-agent collision, destructive ops, compaction drop, notes nobody reads) each with a concrete defence. |
| `learning-hub/` | How knowledge compounds: three knowledge streams (internal / external / curated) and the technique-file format. |
| `orchestrator-auto-workflows/` | Five **provisional** automation switches (eval-loop, weekly heartbeat, active-project header, screenshot smoke, session checkpoints). Each marked with its own validation status. |
| `templates/` | Reusable starters: a prompt-file template, a completion-report template, and a `command-center/` dashboard generator (YAML data → safe, idempotent, backed-up single-file HTML). |
| `setup/` | A new-project checklist (zero to first agent in ~15 min) and an agent cold-start onboarding protocol. |

## Cross-reference notes

- Files occasionally point at a `04-rules/` or `09-knowledge/` path from the original
  repo. Those two sections were **not** folded:
  - `09-knowledge/` (RAG, multi-agent, voice, guardrails, deployment, fine-tuning, MCP/A2A,
    agent-frameworks) duplicated material already in this kit — see `foundations/`,
    `domains/`, and `pillars/agents/` instead.
  - `04-rules/` (git, code-quality, security, testing, commit-hygiene, …) duplicated this
    kit's coding rules — see `rules/` and `claude/rules/` instead.
- The `setup/new-project-checklist.md` Step 6 says to copy 3 technique files from
  `09-knowledge/`; for this kit, pull the equivalents from `foundations/` and `domains/`.

## Sanitization applied during the fold

The source was already largely de-projected (it used the generic word "orchestrator"
throughout). The only changes made here:

- `philosophy/orchestrator-model.md` — renamed from a file named after a specific
  agent persona; body was already persona-neutral.
- `orchestrator-auto-workflows/` — folder + header renamed off a specific agent persona.
- `templates/completion-report.template.md` — the "production validation" footer was
  rewritten to drop an internal project name, dates, and internal bug IDs.
- **Excluded entirely:** one failure-mode file that recounted two real incidents with real
  teammate names, an internal project name, and commit SHAs. Its lesson is fully preserved
  in `failure-modes/parallel-agent-collision.md`, which is the clean, generic version.
- **Excluded entirely:** the source's `agent-master-rule-v1.md`, which was branded to a
  specific author/employer and referenced internal infra (in-house push target,
  tenant GUC migration numbers, named specialists). Its generic lessons are already in
  this kit's `rules/` and in `operating-model/`.

Nothing in this folder names a real person, employer, client, product, credential, host,
or tenant.
