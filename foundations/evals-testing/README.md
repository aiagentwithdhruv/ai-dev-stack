# Evals & Testing

> Evals are the new unit tests. If you can't measure quality, you can't ship a change with confidence — you're just hoping.

## What this is

A discipline for measuring whether an LLM-powered system actually does its job, and whether each change makes it better or worse. Classic software has deterministic tests: same input, same output, green or red. LLM systems are non-deterministic and open-ended, so you replace exact-match assertions with **scored evaluations over a fixed set of cases**.

## Why it matters

Without evals, every prompt tweak, model swap, or RAG change is a blind bet. You fix one case and silently regress five others. Teams that survive review have an eval suite that runs on every change and gates merges. Teams that don't end up debugging in production with screenshots from angry users.

## Core building blocks

| Piece | What it is | Rule |
|-------|-----------|------|
| **Golden set** | A curated, version-controlled set of input → expected-quality cases | Start with 20-50 real cases, grow to hundreds. No synthetic-only sets. |
| **Graders** | The scoring logic per case | Prefer deterministic checks first; use LLM-as-judge only where you must. |
| **Regression gate** | CI step that blocks merge if scores drop | Fail the build, not the user. |
| **Eval report** | Per-run scores, deltas, failing cases | Diff against the last green run, not against zero. |

### Grader ladder — cheapest reliable check wins

1. **Exact / structural** — JSON schema valid? Required fields present? Enum in range? Regex match? Use this whenever the output is structured.
2. **Deterministic heuristic** — contains/excludes a string, length bounds, citation present, no PII leaked, latency under budget.
3. **LLM-as-judge** — a separate model scores subjective quality (helpfulness, faithfulness, tone) against a rubric. Use only when 1 and 2 can't capture the requirement.

### LLM-as-judge — make it trustworthy

- Give the judge a **rubric with explicit criteria and a fixed scale** (e.g. 1-5 on faithfulness), not "rate this."
- Ask for a **reason before the score** to reduce rubber-stamping.
- **Pin the judge model and prompt version** — a judge that drifts invalidates your trend line.
- **Calibrate against human labels** on a sample. If judge and human disagree often, the rubric is broken, not the system.
- Watch for self-preference and position bias; randomize ordering in pairwise comparisons.

## Starter eval checklist

- [ ] Golden set of ≥20 real cases, committed to the repo and versioned.
- [ ] Each case has an input, an expected-quality definition, and a grader.
- [ ] Structural/deterministic graders cover everything they can before any judge is used.
- [ ] LLM-as-judge uses a pinned model + rubric + reason-then-score format.
- [ ] Eval run produces a score per case and an aggregate, saved per commit.
- [ ] CI gate fails the build on regression beyond an agreed threshold.
- [ ] Failing cases are added back to the golden set (every prod incident becomes a case).
- [ ] Judge calibrated against a human-labeled sample at least once.

## How to use this

Treat the golden set as a living contract. Every bug report and every "the model did something weird" becomes a new case before you fix it — that's how the suite compounds. Run the full eval in CI on every PR that touches a prompt, model, retrieval config, or tool definition. Pair this with [../observability](../observability/README.md) so production traces feed new golden cases, and with [../model-routing-cost](../model-routing-cost/README.md) so you can prove a cheaper model holds quality before routing traffic to it.
