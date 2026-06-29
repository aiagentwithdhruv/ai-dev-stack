# Switch 1 — Eval Loop

> **Status:** PROVISIONAL — designed, not yet validated across 2+ projects.
> **Category:** Error prevention
> **Cost:** low — adds one file edit per mistake caught
> **Benefit:** lessons live inside the prompt that caused them; can't skip

---

## The Rule

When a specialist makes a mistake that requires a code fix, the orchestrator MUST:

1. Write a `## Lessons` section at the bottom of the prompt-file that produced the error.
2. Add a `DO NOT` line for each mistake found.
3. Commit the updated prompt-file in the same commit as the hotfix — not separately.

---

## Why

The standard approach: log the mistake in ERRORS.md, which is read at session start.

The problem: ERRORS.md is read once per session. If the same specialist is re-issued
the same prompt (or a close variant) in a later session, they read ERRORS.md at startup
and may not connect the general lesson to the specific prompt pattern that triggered it.

The eval loop places the lesson inside the artifact that caused the error.
Next time the orchestrator uses this prompt-file as a template, the `DO NOT` block
is right there — impossible to miss, impossible to mentally decouple.

---

## Implementation

**Before (prompt-file, no eval loop):**

```markdown
## STEPS

### Step 1 — Write the import parser

Parse the uploaded Excel file row by row.
For each row, create a new material record via the service layer.
```

**After (hotfix was needed because the parser fabricated barcode values):**

```markdown
## STEPS

### Step 1 — Write the import parser

Parse the uploaded Excel file row by row.
For each row, create a new material record via the service layer.

---

## Lessons

Appended 2024-02-14 after HOTFIX-2.

- DO NOT fabricate or generate barcode values in the import path.
  Pass `barcode=None` to let the database trigger assign the correct format.
  Passing a value short-circuits the trigger and produces wrong output.
  (Root cause: parser built a MAT-{hash} string; trigger saw non-null and skipped.)
```

---

## Commit pattern

```bash
git add path/to/hotfix-file.py path/to/prompt-file.md
git commit -m "hotfix(import): fix barcode trigger short-circuit + add DO-NOT lesson"
```

The lesson and the fix land together. The git diff shows both.

---

## Tradeoffs

- Prompt-files grow over time. Acceptable — lessons are worth the length.
- Requires discipline from the orchestrator to update the file mid-sprint, not "later."
  "Later" means it doesn't happen.
- Does not replace ERRORS.md — both get the entry.
  ERRORS.md for global pattern; prompt-file for prompt-specific context.
