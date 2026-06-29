# Agentic Workflows Engine — the WAT pattern

A code-first pattern for AI automations: **the agent reasons, code executes.** That separation
is what keeps accuracy high. The model decides *what* to do; deterministic Python scripts do it.

## The three layers

```
┌───────────────────────────────────────────────────────────┐
│  AGENT  (the model)                                        │
│  Read the workflow → pick tools → execute → observe        │
│  → re-plan on failure → log the run → deliver the output   │
└──────────────────────────┬────────────────────────────────┘
                           │
┌──────────────────────────▼────────────────────────────────┐
│  WORKFLOWS  (workflows/*.md)                               │
│  Markdown SOPs: objective, inputs, ordered steps, tools,   │
│  outputs, error handling, cost estimate.                   │
└──────────────────────────┬────────────────────────────────┘
                           │
┌──────────────────────────▼────────────────────────────────┐
│  TOOLS  (tools/*.py)                                       │
│  Deterministic scripts. Typed inputs, typed outputs,       │
│  errors handled, one job each, runnable from the CLI.      │
└────────────────────────────────────────────────────────────┘
```

**W**orkflow → **A**gent → **T**ool. The agent sits between intent (workflows) and execution
(tools).

## Why the separation matters

When the model does *every* step directly, error compounds: ~90% reliability per step is ~59%
after five steps (0.9⁵). Offload execution to deterministic code and the only stochastic step is
the reasoning — 90% × 100% × 100% × 100% × 100% ≈ 90%. **The model thinks; scripts execute;
accuracy stays high.** Reach for a deterministic tool before asking the model to "just do it
inline."

## How the agent operates

1. **Receive a task** → check `workflows/` for an existing SOP.
2. **Reuse first** → if a workflow exists, gather its inputs and run its tools in order. If only
   loose tools exist, compose them. Only build new tools/workflows when nothing fits.
3. **Execute through tools, never inline** → a 50-line inline script is throwaway; a tool in
   `tools/` is reusable, testable, and improves over time.
4. **Fail intelligently** → read the full traceback, diagnose (bug / API / rate-limit / auth /
   bad input), fix the tool, re-run, then update the workflow so the edge case never recurs.
5. **Log every run** → `runs/YYYY-MM-DD-workflow.md`: workflow, inputs, tools called, durations,
   cost, output location, errors + resolutions. Observability compounds.

## The self-improvement loop

```
error → read full error → fix the tool → verify the fix
      → update the workflow with the new edge case → log it → system is now more robust
```

Every failure makes the system stronger. It is not optional — skip it and the system stays
fragile.

## Security model (non-negotiable)

The hardened library in `shared/` enforces these without the agent having to remember them:

- **Tool validation** (`tool_validator.py`) — AST + regex scan of any new/modified tool *before*
  it runs. Blocks dangerous imports (`subprocess`, `socket`, `pickle`, `ctypes`, …) and calls
  (`exec`, `eval`, `os.system`, `os.popen`, `__import__`, destructive `os.*`). Block on failure.
- **Path sandbox** (`sandbox.py`) — tools may only write to an allowlist (`.tmp/`, `runs/`,
  `output/`, …); protected files (`.env`, the security modules, the agent contract) and system
  dirs (`~/.ssh`, `~/.aws`, `/etc`, …) are off-limits.
- **Secret masking** (`secrets.py`) — known secret env values and key-shaped patterns are
  redacted from every log line and from any dict that gets logged. Never bypass it.
- **Input sanitisation** (`sanitize.py`) — strips shell metacharacters, validates URLs
  (http/https only; blocks localhost and private ranges → SSRF guard), validates emails.
- **Blocking budget guard** (`cost_tracker.py`) — `check_budget()` / `check_run_budget()` raise
  on limit; do **not** catch-and-ignore. Confirm with the user before retrying anything that
  costs money.
- **Secrets live in `.env` only** — never in code, never in logs, never in `.tmp/`.

## Layout

```
.
├── AGENT-CONTRACT.md     # operating instructions for the driving agent (a CLAUDE.md)
├── config/
│   ├── models.example.yaml   # provider-agnostic LLM routing (task → model)
│   ├── settings.yaml         # retries, cost limits, timeouts, logging
│   └── credentials.yaml      # tool → required env vars
├── workflows/_template.md    # shape of a new workflow
├── tools/_template.py        # shape of a new tool
├── shared/                   # the hardened library (see SOURCE.md)
├── runs/                     # run logs + costs.jsonl (auto-generated)
└── .tmp/                     # disposable intermediates
```

## LLM routing — provider-agnostic

All major providers expose an OpenAI-compatible API, so one SDK serves them all — just swap the
`base_url` and key:

```python
from openai import OpenAI

# Any OpenAI-compatible gateway/aggregator (one key → many models)
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))

# Or a direct provider
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))                       # OpenAI
# client = OpenAI(base_url="<your-gateway>/v1", api_key=os.getenv("LLM_API_KEY"))
```

Route by task type in `config/models.example.yaml` (cheap+fast for classification/extraction,
mid-tier for generation, top-tier for research/planning). Model id strings there are placeholders
— use your provider's current ids.

---

*Folded reference — see `SOURCE.md` for provenance and the sanitisation applied. Generic and
reusable; lift `shared/` directly into any code-first agent project.*
