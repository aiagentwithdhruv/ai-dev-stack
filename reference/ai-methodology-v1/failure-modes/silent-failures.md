# Silent Failures

## What happens

The backend tests pass. The type-checker shows no errors. The agent reports "done." The human opens the browser and the feature is broken. The failure was invisible to every automated check that ran.

Variants:
- Tests pass, browser shows blank page
- curl returns 200, but the response body is missing expected fields
- Build succeeds, but a circular import produces a runtime error on first render
- Smoke script all-green, but a new POST endpoint returns an IntegrityError on real data

## Why it happens

Each check validates a subset of the system. Passing all checks means the system passed all subsets — not that the system works end-to-end.

Common gaps:

| Check | What it catches | What it misses |
|-------|----------------|----------------|
| `tsc --noEmit` | Type errors | Circular imports, duplicate exports, bundler resolution |
| `pytest` with real DB | Logic errors in tested paths | Untested paths, integration with real request headers |
| `curl GET /health` | Server is alive | Whether the endpoint returns correct data |
| Regression smoke (GET endpoints) | Existing GET endpoint regressions | POST round-trips, response shape of new endpoints |

Silent failures happen at the boundaries between these checks — in the gaps where no single check reaches.

## How it escalates

1. Agent commits a new feature.
2. Orchestrator runs regression smoke: 17/17 green. Reports "verified clean."
3. Human opens the browser: blank page.
4. 20 minutes of back-and-forth to establish that the browser is receiving a 200 with malformed JSON.
5. The POST endpoint was never actually exercised by any check.
6. Trust in the verification process is reduced.

Or:

1. A new import endpoint is added. GET smoke: passes. curl GET: passes.
2. First real POST to the endpoint: IntegrityError on a unique constraint.
3. The constraint is triggered by a combination of real data that the smoke script never sent.

Born from: a new endpoint passed GET regression smoke and was declared clean. The first real POST from a real client returned a constraint violation. The smoke script only checked GET endpoints. A round-trip POST test would have caught the violation in 10 seconds.

## Defence

**1. Run `npx vite build`, not just `tsc --noEmit`.**

The bundler catches what the type-checker misses. Every frontend commit verification runs the full build.

**2. Orchestrator-side feature smoke: real POST with round-trip payload.**

After every backend commit that adds or modifies a write endpoint:

```bash
TOKEN=$(cat /tmp/project-token.txt)
curl -sS -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}' \
  http://localhost:PORT/api/endpoint | python3 -m json.tool
```

Inspect the response. Confirm every field the frontend expects is present.

**3. Regression smoke script after every backend commit.**

The script covers all existing endpoints. It runs in under 30 seconds. It is not optional.

**4. Click-script for UI changes.**

The orchestrator provides the human with a numbered click-script for every UI change. The human runs it before the orchestrator reports clean.

**5. No "done" without the human's explicit visual confirmation.**

Backend-only changes: human spot-checks curl output. UI changes: human walks the click-script in a browser. The human's confirmation is Gate 5 — the final gate. No gate is skipped.

**6. Browser smoke in incognito, not cached tabs.**

Chrome caches aggressively. "Still broken" after a fix is often a cache issue. The orchestrator instructs the human to test in incognito or to clear site data before concluding the fix is wrong. curl the server first to confirm the fix is deployed — if the server returns correct HTML, the cache is the problem.
