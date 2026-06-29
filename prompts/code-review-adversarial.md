# Multi-Critic Adversarial Review

A verification prompt that runs **three independent critics** — correctness, security, performance — over a change, then aggregates their findings into a single verdict that **defaults to reject when uncertain**. Use it when a miss is expensive.

**When to use:** high-blast-radius changes — auth, billing, data migrations, anything touching a public contract or shared schema. For routine diffs, the single-pass [pr-review.md](pr-review.md) is enough and faster. This one trades speed for depth and a conservative bias. Reinforces rules [`70-security`](../claude/rules/70-security.md), [`80-testing-quality`](../claude/rules/80-testing-quality.md), and [`85-error-observability`](../claude/rules/85-error-observability.md).

```
You will review the change below by running THREE independent critics, one at a time. Each
critic sees the same code but cares about only its own axis and is told to be paranoid. Do not
let one critic's optimism leak into another. After all three, aggregate.

## Inputs
CHANGE / DIFF:
{{PASTE_DIFF_OR_FILES}}
INTENT: {{WHAT_THIS_IS_SUPPOSED_TO_DO}}
CONTEXT (optional): {{SCHEMA, API_SPEC, THREAT_MODEL, SLOs}}

## Critic 1 — CORRECTNESS (assume it's broken)
Does it do what INTENT says, for every input including empty/null/malformed/concurrent?
Hunt: logic errors, wrong branch, off-by-one, bad assumption about data shape, unhandled
error path, ordering/race issues, broken edge cases. Trace the non-happy paths explicitly.
Output: list of findings with `file:line` + a triggering input + expected vs actual.

## Critic 2 — SECURITY (assume it's attacked)
Hunt: injection (SQL/command/prompt), missing or wrong authz/authn, secret in code, input
unvalidated at a trust boundary, broken tenant/ownership isolation, sensitive data in logs,
unsafe deserialization, SSRF. Assume the input is hostile.
Output: findings with `file:line` + the attack + the impact.

## Critic 3 — PERFORMANCE (assume it's at scale)
Hunt: N+1 queries, unbounded loops/allocations, missing index, sync work on a hot path,
redundant IO/network, work that grows with tenant/data size. Assume 100x today's load.
Output: findings with `file:line` + the cost + when it bites.

## Aggregator — default to REJECT
- Collect all findings. Assign each a severity: CRITICAL / HIGH / MEDIUM / LOW.
- REJECT if ANY critic raised a CRITICAL or HIGH finding.
- REJECT if you are uncertain about any correctness or security item — uncertainty counts as a
  defect, not a pass. State what would resolve the doubt.
- APPROVE only if all three critics are satisfied AND no finding exceeds MEDIUM AND nothing is
  left uncertain.
- Never approve to be agreeable. An empty findings list is allowed only if you genuinely found nothing.

## Output format
  VERDICT: APPROVE | REJECT
  REASON: <one line — the deciding factor>
  CORRECTNESS: <PASS | FAIL> — <n findings>
  SECURITY:    <PASS | FAIL> — <n findings>
  PERFORMANCE: <PASS | FAIL> — <n findings>
  FINDINGS (most severe first):
    [CRITIC][SEVERITY] file:line — <problem> — <evidence> — <fix direction>
  UNCERTAIN: <open questions that forced/risk a REJECT, or "none">
  TO REACH APPROVE: <the minimum set of fixes/answers needed>
```

## How to use

- Run it on the **change in isolation** plus just enough context (schema, threat model, SLOs) for each critic to do its job. Without context, the security and performance critics guess.
- The `TO REACH APPROVE` block is the punch list — fix exactly those items, then re-run.
- `UNCERTAIN` is a feature: it forces the unknowns into daylight instead of letting them ride through on an optimistic approve.

## Why three critics and a reject-bias

A single reviewer juggling correctness, security, and performance under-weights whichever it looked at first. Splitting them forces full attention on each axis. **Defaulting to reject** flips the cost of a mistake: a false reject costs one re-run; a false approve ships the bug. On expensive changes, that asymmetry is the whole point.
