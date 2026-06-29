# Three-Layer Architecture: Agent / Workflow / Tools

A tool-agnostic pattern for building agentic automations that stay reliable as they grow. The
core idea: **the model reasons, deterministic code executes.** Keep those two responsibilities in
separate layers and accuracy stops compounding downward.

## The core loop

Every automation should embody one recurring loop:

```
Sense --> Think --> Decide --> Act --> Learn
```

- **Sense** — gather inputs (events, API data, files, user message).
- **Think** — the model reasons about what to do.
- **Decide** — choose the next step / tool / branch.
- **Act** — run a deterministic tool that executes the step.
- **Learn** — log the run; fold failures back into the workflow.

## The three layers

```
AGENT  (the model)          -->  reasoning, planning, deciding
   |
WORKFLOWS (markdown SOPs)   -->  ordered steps, inputs, outputs, branch points
   |
TOOLS  (deterministic code) -->  execution: API calls, parsing, I/O, transforms
```

- **Agent** decides *what* to do and *in what order*. It does not do the work itself.
- **Workflows** are plain-language standard operating procedures the agent reads. They name the
  steps, the inputs each needs, the expected output, and where to branch. Versionable, reviewable,
  teachable — no code.
- **Tools** are small, single-purpose functions/CLIs. One tool, one job. They are deterministic:
  same input, same output. They never reason.

## Why split it: accuracy compounds

If the model performs every step end-to-end, per-step error multiplies:

```
0.90 ^ 5 steps  = 0.59      # ~59% chance the whole chain is correct
```

Push execution into deterministic tools and only the *reasoning* steps carry model error:

```
0.90  x  1.00 x 1.00 x 1.00 x 1.00  = 0.90   # the deterministic steps don't degrade
```

**The agent reasons. Scripts execute. Accuracy stays high.**

## Operating rules that fall out of this

1. **Tools first, code second.** Before writing a new tool, check whether composing existing tools
   already does the job.
2. **One tool, one job.** Small, deterministic, independently testable. Composition over a single
   clever mega-tool.
3. **Workflows are the contract.** The agent's behaviour is defined by the SOP it reads, not by
   ad-hoc prompting. Change behaviour by editing the workflow.
4. **Paid/irreversible actions need a gate.** Cost ceilings and human approval sit between
   "Decide" and "Act" for anything that spends money or is hard to undo.
5. **Log every run.** The run log is the observability and the training signal for the Learn step.
6. **Self-improvement loop:** fix → verify → update the workflow → log the lesson. The system gets
   better because the workflow absorbs each fix.

## When to reach for this

Use the full three-layer split when an automation has multiple steps, some of which need judgement
and some of which are mechanical. If the whole task is a single model call, you don't need a
workflow or a tool layer — don't over-build. Escalate layers only when the simpler shape can't
express the problem.

> See also: the flagship `pillars/automation` (deterministic-first), `pillars/agents`
> (when to go agentic), and `foundations/guardrails-security` for the gate at "Act".
