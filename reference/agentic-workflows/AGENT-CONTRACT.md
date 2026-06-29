# Agent Contract — Agentic Workflows Engine

Drop this in as the `CLAUDE.md` of a code-first agent project. It tells the driving agent how to
operate the WAT engine (Workflow → Agent → Tool). You **reason**; deterministic Python tools
**execute**. That separation is what makes the system reliable.

## Operating procedure

### 1. Receive a task
- Check `workflows/` first — is there a workflow for this?
- If yes → read it, gather the required inputs, run its tools in order.
- If no → check whether existing tools in `tools/` compose into the task.
- If still no → build the new tool(s) and a workflow for them.

### 2. Execute through tools, never inline
**Rule:** never accomplish an execution task (API calls, data processing, file generation,
sending) by writing throwaway code in the chat. Always run or create a tool.

```
BAD:  write a 50-line scrape script inline
GOOD: python tools/scrape_website.py --url "https://example.com" --output .tmp/data.json
```

Inline code is throwaway. Tools are reusable, testable, and improve over time.

### 3. Handle failures intelligently
1. Read the **full** traceback — don't guess.
2. Diagnose: code bug / API issue / rate limit / auth / bad input.
3. Fix the tool (`tools/<name>.py`) directly.
4. Re-run and verify.
5. Update the workflow with the new edge case so it never recurs.
6. Log it to `runs/`.

**Cost guard:** before retrying any tool that hits a paid API, confirm with the user. Don't burn
credits in a loop.

### 4. Log every run
After a workflow completes, write `runs/YYYY-MM-DD-workflow-name.md`: workflow executed, inputs,
tools called (in order), duration per tool, total cost, output location, errors + how resolved.

## Writing tools
Every tool MUST:
1. Take CLI args (`argparse`/`typer`) — never hardcoded values.
2. Load secrets via `shared/env_loader.py`.
3. Return structured output (JSON to stdout, or write to a file).
4. Handle errors: catch, print a useful message, exit non-zero on failure.
5. Log via `shared/logger.py`.
6. Get a schema entry in `tools/registry.yaml` after creation.

```
BAD:  prints "done" and exits 0 even on failure
GOOD: returns {"status":"success","output_path":".tmp/result.json","records":42}
```

Start from `tools/_template.py` — it already wires in budget check, input sanitisation, and
output-path validation.

## Writing workflows
Start from `workflows/_template.md`. Every workflow has: objective, inputs (typed), tools used
(in order), numbered steps with exact commands, outputs + destination, error-handling table,
cost estimate. Workflows are living documents — update them when you learn something.

## Security guardrails (non-negotiable)

**Tool safety**
1. Validate every new/modified tool with `shared/tool_validator.py` **before** running it. Block
   on failure.
2. `exec`, `eval`, `subprocess`, `os.system`, `os.popen`, `__import__` are blocked in tools. If a
   tool genuinely needs shell access, the user must explicitly approve it.
3. Ask the user before executing a newly created tool for the first time.
4. Never embed raw external data into tool source — pass it as args or read at runtime.

**Input / output safety**
5. Sanitise all user inputs with `shared/sanitize.py`. Never use `shell=True`.
6. Validate output paths with `shared/sandbox.py` — tools only write to the allowlist
   (`.tmp/`, `runs/`, `output/`, …).
7. Validate URLs — http/https only; block internal/private network addresses (SSRF).

**Secrets & logging**
8. Secrets live in `.env`, nowhere else. Never log, print, or embed a key.
9. All logs are secret-masked by `shared/logger.py`. Never bypass it.
10. No raw keys, passwords, or PII in run logs.

**Budget**
11. Budget enforcement is **blocking** — `check_budget()` raises `BudgetExceededError`. Do not
    catch and ignore.
12. Call `check_budget()` before any paid API call (the tool template already does).
13. Use `check_run_budget(estimate)` for runs above the per-run threshold.
14. Confirm with the user before retrying anything that costs money.

**Protected from modification** (never overwrite without user approval): the `shared/` security
modules, `.env`, and this contract file.

## Rules
1. Tools first, code second.
2. Workflows are instructions — don't delete/overwrite without asking.
3. Paid API calls need approval before retry.
4. Secrets stay in `.env`.
5. Log every run.
6. On failure: fix tool → verify → update workflow → log.
7. Deliverables go to where the user can access them; `.tmp/` is disposable.
8. One tool, one job. Compose simple tools instead of building mega-scripts.
