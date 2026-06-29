# {PROMPT_FILE_TITLE} — {PROMPT_CODE}

> **ACTIVE PROJECT: {PROJECT_NAME}**
> **Issued by:** {ORCHESTRATOR_NAME}
> **Assigned to:** {SPECIALIST_NAME}
> **Date:** {DATE}
> **Scope:** {SMALL | MEDIUM | LARGE}

---

## WORKSPACE

```
cwd:        {ABSOLUTE_REPO_PATH}
branch:     {GIT_BRANCH}
backend:    {BACKEND_DEV_URL}   e.g. http://localhost:8000
frontend:   {FRONTEND_DEV_URL}  e.g. http://localhost:5173
token:      {TOKEN_PATH}        e.g. /tmp/project.token
```

Verify branch before touching a single file:
```bash
git -C {ABSOLUTE_REPO_PATH} branch --show-current
# must print: {GIT_BRANCH}
```

---

## CONTEXT

{2-3 sentences of why this task exists. What broke, what changed in the spec, what the
 human asked for. Link to the spec section if relevant: "per spec §{SECTION}."}

---

## OBJECTIVE

{One sentence. What is done when this task is done? Frame as an observable outcome,
 not an action. "The user can create X and see Y" not "implement X."}

---

## SCOPE — DO THIS

{Numbered list of exactly what to build. Be explicit about files to touch.
 Reference spec sections. Use exact field names from the schema.}

1. {STEP_1}
2. {STEP_2}
3. {STEP_3}

---

## NON-GOALS — DO NOT DO THIS

{Explicit list of what is out of scope. Without this, specialists drift into adjacent work.}

- Do NOT touch `{OUT_OF_SCOPE_FILE_1}`.
- Do NOT refactor `{OUT_OF_SCOPE_MODULE}` — that is a separate task.
- Do NOT add {OUT_OF_SCOPE_FEATURE} — that is deferred to {FUTURE_PROMPT_CODE}.

---

## GATE 1 — PREFLIGHT (complete before writing code)

Cross-check and confirm in the REPORT:

1. **Schema truth:** `grep "CREATE TABLE {TABLE_NAME}" {MIGRATIONS_PATH}` — paste actual column list.
2. **Existing code:** `grep -rn "{FUNCTION_OR_CLASS}" {SRC_PATH}` — does it already exist?
3. **API smoke (if touching an existing endpoint):**
   ```bash
   curl -sS -H "Authorization: Bearer $(cat {TOKEN_PATH})" \
        {BACKEND_DEV_URL}/api/v1/{ENDPOINT_PATH} | python3 -m json.tool
   ```
   Paste the response shape.
4. **Spec section:** confirm `{SPEC_SECTION}` says `{EXPECTED_BEHAVIOR}`.

If any check reveals a mismatch with this prompt — STOP and report before writing code.

---

## STEPS

### Step 1 — {STEP_1_TITLE}

{Precise instructions. Reference file paths. State what the expected output is.}

**Gate 2 check:** commit with message `{TYPE}({SCOPE}): {DESCRIPTION} ({PROMPT_CODE} S1)`.
Verify `git diff --cached --stat` shows only the files you intended.

---

### Step 2 — {STEP_2_TITLE}

{Precise instructions.}

**Gate 2 check:** commit `{TYPE}({SCOPE}): {DESCRIPTION} ({PROMPT_CODE} S2)`.

---

### Step 3 — {STEP_3_TITLE}

{Precise instructions.}

**Gate 2 check:** commit `{TYPE}({SCOPE}): {DESCRIPTION} ({PROMPT_CODE} S3)`.

---

## GATE 3 — VERIFICATION (complete before writing REPORT)

1. **Build:** {BUILD_COMMAND} — paste exit code and last 5 lines.
2. **API smoke:** curl the new endpoint, paste response body.
3. **Browser smoke:** open `{FRONTEND_DEV_URL}/{ROUTE}`, confirm `{EXPECTED_UI_STATE}`.
4. **Restart:** if backend changed, kill + restart the server now.

---

## ROLLBACK

If anything goes wrong:
```bash
git revert HEAD    # one commit at a time — never reset --hard
# repeat until you are before the first commit of this task
```
Do NOT mass-reset. Revert one commit at a time. Report which commit introduced the failure.

---

## SUCCESS CRITERIA

All of the following must be true before writing REPORT:

- [ ] Gate 1 preflight passed — all checks match expectations.
- [ ] {N} commits on `{GIT_BRANCH}`, each atomic, message includes `({PROMPT_CODE} S{N})`.
- [ ] Build passes with zero errors.
- [ ] API smoke: `{ENDPOINT}` returns `{EXPECTED_STATUS}` with `{EXPECTED_FIELD}` in body.
- [ ] Browser: `{UI_ELEMENT}` visible at `{ROUTE}`.
- [ ] No `console.log` debug lines in committed code.
- [ ] No hardcoded localhost in env vars.

---

## REPORTING FORMAT

```
## REPORT — {PROMPT_CODE}

**Status:** DONE | BLOCKED | PARTIAL
**Commits:** {N} on {BRANCH}
  - {SHA_1}: {MESSAGE_1}
  - {SHA_2}: {MESSAGE_2}

**Gate 1 preflight:**
  - Schema: {RESULT}
  - Existing code: {RESULT}
  - API smoke: {HTTP_STATUS} {ENDPOINT}

**Gate 3 verification:**
  - Build: {PASS/FAIL} — {EXIT_CODE}
  - API smoke: {HTTP_STATUS} — {KEY_FIELD}: {VALUE}
  - Browser: {PASS/FAIL} — {WHAT_WAS_SEEN}

**Blockers / deviations from scope:**
  {NONE or description}

**Next recommended prompt:**
  {PROMPT_CODE_NEXT} — {ONE_LINE_DESCRIPTION}
```
