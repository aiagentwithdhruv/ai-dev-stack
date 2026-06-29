# Prompt template — add one backend endpoint

A parameterized prompt for dispatching a backend agent to add a **single** REST endpoint to
an existing service. Scope-limited on purpose: one endpoint, not greenfield, not a complex
orchestration.

## When to use
- Adding one CRUD/action endpoint to an existing backend.
- Framework already chosen (don't use this to stand up a new service).

## Parameters
- `{FRAMEWORK}` — e.g. FastAPI (Python) or Next.js API routes (TypeScript)
- `{ENDPOINT_PATH}` — e.g. `/api/orders/{id}/pdf`
- `{METHOD}` — GET / POST / PUT / DELETE
- `{INPUT_SCHEMA}` — Pydantic model (Python) or Zod schema (TS)
- `{OUTPUT_SCHEMA}` — return type + example response
- `{RELATED_FILES}` — existing files to read first (models, sibling endpoints)
- `{AUTH_REQUIRED}` — Yes (which auth) / No (public)
- `{SIDE_EFFECTS}` — DB writes / external calls / file generation / queue enqueues

## The prompt

```markdown
# Task: Add {METHOD} {ENDPOINT_PATH}

## Context
- Framework: {FRAMEWORK}
- Why now: [trigger / user story]

## Read first
- the project's rules/conventions file
- {RELATED_FILES}

## Expected output
- Endpoint: {METHOD} {ENDPOINT_PATH}
- File: [specific path]
- Input schema: {INPUT_SCHEMA}
- Output schema: {OUTPUT_SCHEMA}
- Auth: {AUTH_REQUIRED}
- Side effects: {SIDE_EFFECTS}

## Must include
- Input validation (Pydantic / Zod) — never trust raw bodies
- Structured JSON error responses: 400 / 401 / 404 / 500
- Structured logging on errors (never silent)
- External calls: timeout + retry + fallback
- DB writes: idempotent where possible, explicit unique constraint otherwise

## Do not
- Don't add UI code (separate lane)
- Don't change existing endpoints — only ADD the new one
- Don't skip auth if {AUTH_REQUIRED} is Yes
- Don't log sensitive inputs (passwords, tokens, PII)
- Don't hardcode config — use env variables

## Tests
- Manual: curl the endpoint → expected output
- Error paths: verify 400/401/404/500 each return structured JSON
- Add a unit test if a test scaffold exists
```

## Known gotchas
1. **Path conflicts** — grep for overlapping route prefixes before adding.
2. **Transaction scope** — multiple DB writes must be wrapped in one transaction.
3. **Streaming** — for large file/PDF downloads use a streaming response
   (e.g. `FileResponse` in FastAPI, a streamed `NextResponse` in Next.js).
4. **CORS** — if called cross-origin, add the CORS headers/middleware.
