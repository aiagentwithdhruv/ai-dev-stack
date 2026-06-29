# Agent vs Skill — Decision Matrix, Routing, Composition

Complements the flagship's `docs/AGENTS.md` and `docs/SKILLS.md`. Those define the
file formats; this file is about **choosing** between a skill and an agent, and
**chaining** them.

## The core difference

A **skill** follows a recipe step-by-step — deterministic, same input → same output.
An **agent** reads context, evaluates it, and makes a judgment — probabilistic.

| | Skill | Agent |
|-|-------|-------|
| Nature | Deterministic task | Autonomous role |
| Follows | Exact steps | Guidelines + judgment |
| Output | Predictable | Varies with context |
| Decides | Nothing — executes | What to do, how to respond, whether to escalate |
| Example | "Scrape 100 records and dedupe" | "Review this code: PASS or FAIL" |

A skill is a recipe (anyone gets the same dish). An agent is a chef (reads the recipe,
tastes, adjusts).

## Decision matrix

| Question | Yes → | No → |
|----------|-------|------|
| Fixed, repeatable recipe? | Skill | Agent |
| Requires subjective judgment? | Agent | Skill |
| Same input should always give same output? | Skill | Agent |
| Involves evaluating quality? | Agent | Skill |
| Is it a pipeline (input → transform → output)? | Skill | Agent |
| Needs reading between the lines? | Agent | Skill |
| Can you draw it as a flowchart with no decision diamonds? | Skill | Agent |
| Must adapt to unexpected input? | Agent | Skill |

### Hybrid tasks

Some tasks need both. "Find leads and decide which are worth contacting":

1. `scrape` skill — deterministic: get the data
2. `score` skill — deterministic: rank by criteria
3. Agent judgment — probabilistic: review edge cases, override scores, add context

Use skills for the deterministic parts and an agent for the judgment.

## Orchestrator routing

The main assistant acts as an orchestrator:

```
1. Parse the request
2. Check skill triggers first → if a skill matches, run it (fast, deterministic)
3. If no skill matches, or judgment is needed → route to the best-fit agent
4. Agent processes, returns a structured result
5. Orchestrator: pass through (if confident) / augment / flag for human review
```

A routing table keeps this explicit:

```markdown
| User says | Route to | Type |
|-----------|----------|------|
| "review this code" | code-reviewer | Agent |
| "scrape leads from..." | scrape-leads | Skill |
| "research {topic}" | research | Agent |
| "send welcome emails" | welcome-email | Skill |
| "test this feature" | qa | Agent |
```

## Composition

### Skill chain (output → input)

```
[scrape] --csv--> [score] --csv--> [format]
```

Each `SKILL.md` declares typed Outputs and a "Composable With" list, so the system
can match one skill's output type to the next skill's input type.

### Agent chain

```
research-agent → code-reviewer-agent → qa-agent
```

Research a solution, build it, review the code, then test it.

### Parallel agent evaluation

```
reviewer-A ─┐
            ├─→ orchestrator compares verdicts, resolves conflicts
reviewer-B ─┘
```

Two reviewers evaluate the same artifact independently.

### Agent–skill hybrid

```
scrape (skill) → score (skill) → outreach-advisor (agent)
```

A deterministic pipeline feeds an agent that makes the final judgment call.

## Principles

1. **Separation of concerns** — agents judge, skills execute; never mix them in one file.
2. **Explicit boundaries** — a code-reviewer reviews, it does not fix code.
3. **Structured output** — agents return a defined format, not freeform essays.
4. **Fail-safe defaults** — when uncertain, an agent says so rather than guessing.
5. **Testable** — every agent ships with example inputs/outputs that define correct
   behavior. If you can't write the examples, the role isn't defined clearly enough.
6. **Reuse before rebuild** — check the skill index before authoring a new skill.

## Minimal agent prompt template

```markdown
# Agent: {name}
## Role
You are a {role}, specialized in {domain}.
## Task
1. {what to analyze} 2. {what criteria to apply} 3. {what to decide/produce}
## Output Format
{structured: verdict / categories / scores / report sections}
## Rules
- ALWAYS: {non-negotiable} - NEVER: {prohibited} - WHEN UNCERTAIN: {fallback}
```
