# Workflow Discipline — Shipping with AI Coding Agents

Generic, team-neutral discipline distilled from a high-commit build. The theme:
**the goal is not speed, it's never losing control.** Speed comes from safety —
small commits and rollback points are permission to move fast.

---

## Scope and specs

- **Match design depth to task size.** Full doc chain (business brief → product spec
  → high-level design → low-level design → conventions file → build) for a new
  module; a focused spec for a feature; contract-only for an enhancement; straight to
  build for a bug fix or polish. Never skip steps on a new module; never
  over-document a one-line fix.
- **Threshold test:** touches >3 files or >1 module → write a high-level design.
  Touches >10 files or changes a status flow / data model / API contract → write a
  low-level design.
- **Diagrams are optional unless they save time.** Mandatory only for: an ER diagram
  when adding/changing >3 tables, and a state-machine diagram for any entity with ≥4
  states. Rule of thumb: if drawing it takes longer than explaining it, skip it.
- **Design screens before code.** Feedback on a mockup costs minutes; feedback on
  built code costs hours.

## Sequencing

- **Backend first — the schema is the contract.** Build and curl-verify the API,
  publish the spec, then build the frontend against it. Zero guessing, zero renaming,
  zero mock fallback.
- **One module at a time.** "Fully done" means every feature spec'd, built, tested,
  reviewed, merged — not "mostly works on three things."
- **Build connection points early.** Add nullable foreign-key columns for modules not
  built yet, so future modules plug in without refactoring.

## Agent safety

- **One change per prompt; cap files per prompt.** Never combine a refactor with a
  new feature. Ten small prompts that each work beat one big prompt that crashes.
- **A slow prompt that works first try beats a fast one that crashes** and needs a
  long recovery.
- **If a change breaks things, reset to the last good point** rather than fixing
  forward repeatedly — stacked forward-fixes tend to make it worse.
- **Separate orchestration from editing.** Whoever plans/reviews/writes prompts
  should not also hand-edit source in the same breath; route every code change
  through an explicit, reviewable prompt.

## The "done" gate (test like a user, not a developer)

Before any "done" claim:

1. Build passes with zero errors.
2. Browser console has zero red errors.
3. Zero mock / hardcoded data.
4. Zero leftover debug log lines.
5. Tested on a tenant **with** data.
6. Tested on an **empty** tenant (no data).
7. Every button is wired or removed — none dead.
8. The status flow works end to end.
9. Switching tenant changes the data correctly.
10. The built feature matches **every line** of the spec (field names, edge cases).

- **No TODOs across the seam.** A backend endpoint with no frontend button is 0%
  done. Build backend + frontend + test in one pass.
- **Build passing ≠ working.** Never merge without a runtime check in the browser.

## Promote carefully

- **Test → push → tag are three gates, not one.** Verify (build/curl/read), then a
  human tests in the browser, then push, and only **then** tag a stable point.
- **Stable tags are for feature-complete, user-visible moments**, not per-commit
  milestones. Tagging a bare migration with no UI gives you nothing to roll back to.
- **Test locally → deploy → monitor. Never skip the local test.**

## No mock data, ever

| Situation        | Wrong                     | Right               |
|------------------|---------------------------|---------------------|
| API returns empty | show hardcoded data       | show "No data yet"  |
| Field is null     | show a fake value         | show "—"            |
| API fails         | fall back to a mock array | show an error state |
| Need test data    | fake records in code      | seed data in the DB |

## Pick the simplest thing that works

Don't reach for the heavier tool when the lighter one solves it:
rules/if-else before a model · prompting before RAG · RAG before fine-tuning ·
fine-tuning before training from scratch.

## Learn from every bug

For each bug, record: **Error → Cause → Fix → Rule → Applies-to**, in a shared
lessons log. The next session reads it so the same mistake never repeats.
