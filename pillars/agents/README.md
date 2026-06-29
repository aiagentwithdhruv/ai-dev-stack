# Agents — systems that reason, use tools, and act

An agent takes a goal, decides its own steps, calls tools, and acts on the result — with an autonomy you don't get from a fixed script. This pillar covers when to reach for one, how to structure it, and the sub-disciplines (voice, computer-use, retrieval) that are agents in a specific medium.

Build on the [foundations](../../foundations/) ([prompting & context](../../foundations/prompting-context/), [model routing](../../foundations/model-routing-cost/), [evals](../../foundations/evals-testing/)) and the agent [rules](../../rules/) — tool schemas, validated outputs, supervisor patterns. This page is the map.

## First: do you need an agent?

Agents trade determinism for flexibility. Pay that price only when the task demands it.

| Reach for... | When |
|--------------|------|
| A single function call | One model call answers the whole task |
| A fixed workflow | The steps are known and repeatable ([automation](../automation/)) |
| **A single agent** | The path is open-ended but one role can handle it with tools |
| **Multi-agent** | The work splits cleanly into roles that benefit from isolation |

> Don't escalate a tier until the simpler one can't express the problem. Most "agent" tasks are really workflows with one model call in the middle.

## Single vs multi-agent

- **Single agent** — one loop: reason → call tool → observe → repeat until done. Simplest to build, debug, and eval. Start here.
- **Multi-agent** — several specialised agents coordinated by an orchestrator. Worth it when subtasks are genuinely independent (parallel speed), need different tools or models, or benefit from an independent verifier. The cost is coordination, shared state, and harder debugging — don't reach for it by default.

The dominant multi-agent shape is **orchestrator-worker**: a lead decomposes the goal, fans work out to isolated workers, and verifies their results before integrating. See [patterns](./patterns/).

## Tool use and MCP

An agent is only as capable as its tools. Define each tool with a **typed schema**, validate every argument at the boundary, and validate the output before the model acts on it. A standard tool protocol (such as MCP) lets one agent reuse tools across hosts without bespoke glue — define the tool once, expose it everywhere.

Guardrails are not optional on tool-using agents: constrain what each tool can do (read-only by default, writes behind confirmation), and never let model output reach a dangerous sink unchecked. See [guardrails & security](../../foundations/guardrails-security/).

## Memory

- **Working context** — what's in the prompt right now. Keep it lean; context is a budget, not a bucket.
- **Durable memory** — facts and decisions persisted across sessions, retrieved when relevant. Write summaries, not transcripts.
- **Retrieval** — pulling private knowledge in on demand; see [agentic-rag](./agentic-rag/).

The discipline is *context engineering*: put the right thing in the window at the right time, and nothing else.

## Sub-sections

| Section | What it covers |
|---------|----------------|
| **[patterns/](./patterns/)** | Orchestrator-worker, fan-out/verify, adversarial verification, agent-as-markdown, model-routing-per-role |
| **[voice/](./voice/)** | Voice agents — STT → LLM → TTS, realtime |
| **[computer-use/](./computer-use/)** | Browser and desktop agents that operate a UI |
| **[agentic-rag/](./agentic-rag/)** | Agents that retrieve and reason over private knowledge |

## How to use

Start at the decision table — most tasks stop there. If you do need an agent, read [patterns](./patterns/) before writing code, then pick the sub-section for your medium. Re-check [evals](../../foundations/evals-testing/): an agent you can't measure is an agent you can't trust.
