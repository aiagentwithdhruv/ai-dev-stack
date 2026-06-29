# The 5 Anti-Drift Gates

Drift is the gap between what the spec said and what shipped. At low levels, drift is annoying — field names that don't match, UI that doesn't reflect the requirement, small deviations that each take 20 minutes to find and fix. At high levels, drift is project-killing — a codebase where no one is confident what any part actually does, debug rounds measured in hours, clients seeing broken behaviour in demos.

These 5 gates exist to catch drift before it compounds. Each gate has a specific failure mode it targets. Skip any gate and that failure mode passes silently.

This system reduced drift from ~30% of shipped code to under 5%. The difference is not intelligence — the same agents, the same models, the same prompts. The difference is a structured review layer that catches problems early, when they're cheap to fix.

---

## Gate 1 — Preflight

**When:** Before any code is written.

**What it catches:** Wrong field names, missing endpoints, assumed file paths, spec vs. reality mismatch.

**Checklist:**

1. Read the authoritative spec (not memory of the spec — the actual document)
2. Grep the codebase for existing implementations that overlap with this task
3. Check real schema: `grep "CREATE TABLE" migrations/*.sql` or `\d tablename` against a live database — confirm field names and types
4. Curl the upstream endpoint (if this task depends on an API that already exists): verify response shape, field names, status codes
5. Confirm the Pydantic model (or equivalent schema) matches both the DB columns and the API response

**Cost of skipping:**

A task that references `warehouse_name` when the actual column is `name` goes through an entire development cycle before anyone notices. The agent writes the code. The build passes. The unit test passes (because it mocks the field). The endpoint 500s in integration. 30-60 minutes of debugging traces back to a field name that could have been verified in 10 seconds.

**Gate 1 is the cheapest gate.** Grep takes seconds. Getting this wrong costs hours.

---

## Gate 2 — Atomic Commits

**When:** During development, as the specialist works.

**What it catches:** Scope creep, entangled changes, parallel-session interference, unrecoverable states.

**Checklist:**

1. One logical change per commit. Max 2 files. If a commit touches 5 files across 3 concerns, it's not atomic — split it.
2. Commit message format: `feat(scope): one-line summary`. Readable in `git log --oneline`.
3. Never `git add -A` or `git add .` — use explicit paths only: `git add backend/routes/orders.py`
4. Before `git commit`: run `git diff --cached --stat`. Verify every file listed belongs to this task. If foreign files appear, `git restore --staged <foreign-path>` before committing.
5. Never `--amend` a commit that's been shared. Never `--no-verify`. Never `git reset --hard` — use `git revert HEAD`.
6. Each commit must leave the system in a working state. Partial implementations that break tests are not commits — they're work in progress.

**Cost of skipping:**

When 2 agents work the same git tree simultaneously, `git add -A` scoops the other session's pre-staged files into the wrong commit. Now a backend commit contains a frontend file it has no business touching. Untangling this mid-sprint requires rebase surgery that itself introduces risk. The simple rule — explicit paths, `git diff --cached --stat` before commit — costs 5 seconds. The recovery costs 30+ minutes.

**Gate 2 is about reversibility.** Small commits can be reverted individually. Large entangled commits can't.

---

## Gate 3 — Self-Verification

**When:** After the code is written, before the agent writes its report.

**What it catches:** Build failures, test regressions, broken endpoints, Vite cache corruption, uvicorn not reflecting new code.

**Checklist:**

For backend changes:
1. `pytest -x` — stops at first failure, surface test regressions before they pile up
2. Curl the new endpoint with a real token — don't assume it works because the code compiled
3. Check the response shape with `| python3 -m json.tool` — confirm fields match the Pydantic schema
4. If the task modifies an existing endpoint: re-run the smoke check for that endpoint before declaring done

For frontend changes:
1. `npx vite build` — catches type errors, import failures, and bundle issues that `tsc --noEmit` misses
2. Open the page in the browser — render it, click the buttons, check the console for errors
3. If the task involves a state transition (form submit, modal, list update): complete the full flow

After any git reset or file restore:
- `rm -rf node_modules/.vite` — stale cache will render broken code even after a correct fix

After any backend commit where uvicorn is running:
- `pkill -f uvicorn && nohup uvicorn ... &` — `--reload` is unreliable on rapid changes, stale routes persist

**Cost of skipping:**

"Working" is not a ship signal. An agent that reports "done" without running `vite build` may have a TypeScript error that only surfaces at bundle time. An agent that doesn't restart uvicorn after a backend change may curl a cached route. The human then hits the broken state and has to debug something the agent should have caught. Gate 3 is the agent's own quality check — skip it and the human becomes the tester for problems the agent should own.

---

## Gate 4 — Orchestrator-Side Smoke

**When:** After the agent's report arrives, before the human sees a "verified" status.

**What it catches:** Drift between what the report claims and what the code actually does; regressions in other endpoints caused by the new commit.

**Two parts — both required:**

**Gate 4a — Regression check:**
Run the automated smoke script against all standard endpoints. Expected output: all pass.

```bash
# Example: 15-20 endpoint checks, runs in under 30 seconds
bash scripts/smoke.sh
```

This catches breakage in OTHER parts of the system — something the new commit accidentally broke by changing a shared utility, a model, or a route.

**Gate 4b — Feature smoke:**
For backend commits: the orchestrator runs the new endpoint with real data and inspects the response.

```bash
TOKEN=$(cat /tmp/auth-token.txt)
curl -sS -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/new-endpoint | python3 -m json.tool
```

For POST endpoints: build a real payload, submit it, verify the response and the database state.

For frontend commits: since the orchestrator can't drive a browser, provide the human with a numbered click-script (under 2 minutes) covering the golden path and at least one edge case.

**If either part fails:**
1. Investigate the failing surface only — do not touch unrelated code
2. Write a targeted hotfix prompt for the specialist
3. Re-run both Gate 4a and 4b after the hotfix
4. Only report "verified clean" to the human after both pass

**Cost of skipping:**

Gate 4 is the last catch point before the human's time is spent. A regression that slips past Gate 4 gets caught during the human's smoke test — which takes longer, requires the human to describe the failure, and costs a round-trip to diagnosis. Catching it at Gate 4 costs the orchestrator 2 minutes. Catching it at Gate 5 costs 15.

---

## Gate 5 — Human Browser Smoke

**When:** After Gate 4 passes, before any release tag is applied.

**What it catches:** Intent drift — cases where the code technically works but doesn't do what the human actually wanted.

**How it works:**

The orchestrator provides a numbered click-script: specific pages to visit, specific actions to perform, specific outcomes to expect. The human runs through it (under 2 minutes for a normal feature, under 5 for a complex one).

The human confirms or reports failure. Two outcomes:
- "Green" → orchestrator applies release tag
- "Broken" or "not what I wanted" → orchestrator diagnoses, writes hotfix prompt, cycles back to Gate 3

**"Verified clean" does not mean "done."**

Gates 1-4 passing means: no regressions, no spec drift, no broken builds, no endpoint failures. It does not mean the feature matches what the human intended in the context of the real product. Gate 5 is the only gate that catches intent drift. Only the human can run it.

For backend-only changes (migrations, schema, no UI surface): Gate 5 is a curl check, not a browser. The orchestrator provides the command; the human runs it once.

**Cost of skipping:**

Gate 5 was the last gate added to this system, because it felt redundant — if Gates 1-4 passed, surely it's done? The record says otherwise. The "done"/"not done" loop — where the agent reports done, the human tests and finds it broken, the agent fixes, and the cycle repeats — traces almost entirely to skipping Gate 5. Three rounds of "done"/"not done" cost more time than every Gate 5 verification ever will.

**Never tag a release without explicit human confirmation.**

---

## Gate Summary

| Gate | Runs When | Who Runs It | Catches |
|------|-----------|-------------|---------|
| 1 — Preflight | Before code | Orchestrator | Wrong field names, spec/reality mismatch |
| 2 — Atomic Commits | During code | Specialist | Scope creep, parallel-session interference |
| 3 — Self-Verify | After code | Specialist | Build failures, test regressions, stale cache |
| 4 — Orchestrator Smoke | After report | Orchestrator | Drift from spec, regressions in other endpoints |
| 5 — Human Smoke | After Gate 4 | Human | Intent drift, real-world behaviour mismatch |

---

## Crystallised Principle

**Every gate catches a different class of problem. Skip any gate and that class of problem passes silently — accumulating until the debug round is measured in hours, not minutes.**

The gates are not overhead. They are the mechanism that keeps velocity high over time. Without them, velocity looks high early and collapses mid-project as drift compounds into a codebase nobody trusts.
