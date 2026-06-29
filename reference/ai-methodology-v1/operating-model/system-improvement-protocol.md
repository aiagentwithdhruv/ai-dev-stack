# System Improvement Protocol

> *Improve, don't replace. The system is alive. Your job is to strengthen it, not rebuild it.*

When the human asks the orchestrator to "improve" an existing folder, project, or workspace, this protocol is the discipline. Six phases. Each phase produces a concrete artefact. Nothing happens in production until the human approves.

---

## The cardinal rule

**Additive first, structural second, destructive never without explicit approval.**

You are walking into a living system. People are working in it. Rules exist that you don't know the history of. Files that look stale may be load-bearing. Your default is to add guardrails around what exists, not replace what exists.

---

## The six phases

### Phase 1 — Survey (read-only, zero edits)

Walk the scope without changing a single file. Produce a mental map:

- `ls -la` every folder in scope.
- Read every file briefly — enough to understand its purpose, not enough to critique it.
- Map each file to one of the seven hygiene categories (see `04-rules/file-type-hygiene.md`).
- Check `git log` history per file: has it been edited line-by-line, or rewritten whole-cloth?
- Note candidates for drift: multiple files claiming the same authority, overlapping purposes, dead links, stale timestamps, copy-paste duplicates.

**Deliverable:** `SURVEY.md` — a flat list of every file in scope with category + purpose + one-line observation.

**What NOT to do:** do not edit, do not delete, do not reorganise. Observation only.

### Phase 2 — Diagnose

For each file in `SURVEY.md`, ask three questions:

1. What hygiene category does it fit?
2. Which hygiene rule is being violated (if any)?
3. What's the highest-leverage improvement — the one that, if applied, prevents the most future failures?

Rank improvements by leverage-per-effort. An XS fix that prevents a weekly recurring failure beats an M fix that prevents a rare edge case.

**Deliverable:** `IMPROVEMENT-AUDIT.md` — for each file needing improvement, a row with: file · current problem · proposed fix · effort (XS / S / M / L) · reversibility (high / medium / low) · risk of breaking the existing system.

**What NOT to do:** do not propose refactors, do not propose consolidations that merge multiple files, do not propose deletions. Stay additive.

### Phase 3 — Propose (for human approval)

Hand `IMPROVEMENT-AUDIT.md` to the human. Do not start applying fixes yet. The human's job is to:

- Confirm the diagnosis matches their mental model.
- Prioritise which improvements go first.
- Flag any file that looks stale but is actually load-bearing.
- Approve the first batch (never the whole list at once).

**Deliverable:** the human returns the audit with a batch marked "approved — start here."

**What NOT to do:** do not proceed to Phase 4 without explicit approval. Silent application is how systems break.

### Phase 4 — Apply (incremental, reversible)

Execute one improvement at a time. For each:

1. Backup the target file (`cp file file.bak.<timestamp>`) if it exists.
2. Apply the fix. Use `Edit`, not `Write`, unless creating a new file.
3. Run a minimal smoke check — does the system still load the file correctly? Does the existing workflow still work?
4. Commit atomically: one improvement = one commit. Commit message format: `improve(<scope>): <one-line summary> [per improvement-audit.md row N]`.
5. Move to the next improvement only after the previous one is verified.

**Deliverable:** a chain of atomic commits, each reversible by `git revert`.

**What NOT to do:** do not batch multiple improvements into one commit. Do not skip the smoke check. Do not proceed if one fix broke something — stop, investigate, revert.

### Phase 5 — Verify

After the approved batch is applied:

- Run full smoke on the affected system (whatever "smoke" means in this project — tests, build, browser check).
- Run any existing regression scripts (`uat-smoke.sh` equivalent).
- Check that files the improvements didn't touch still behave identically.

If any smoke fails, `git revert` the most recent commit, diagnose why, and report back to the human before trying again.

**Deliverable:** a short verification report inside `IMPROVEMENT-AUDIT.md` — which rows from the batch were applied successfully, which got reverted, which need re-thinking.

### Phase 6 — Document

After verification:

- Update the canonical `STATE.md` (or equivalent) with the new state.
- Append a dated entry to the project's `LEARNING-ZONE.md` describing what was improved and why.
- If any hygiene rule needed adjustment during the work, update `04-rules/file-type-hygiene.md` (or the project's analogous file) with the new sub-rule.

**Deliverable:** a closing-loop summary that makes this improvement visible to future agent sessions.

---

## Per-folder template

When the improvement scope is a single folder, repeat the six phases at folder level. Produce:

- `<folder>/SURVEY.md`
- `<folder>/IMPROVEMENT-AUDIT.md`
- One commit per applied improvement
- A closing entry in the folder's `LEARNING-ZONE.md` or project-level equivalent

Larger scopes (whole workspace) fan out into per-folder surveys first, then a cross-folder audit that rolls them up.

---

## Worked example

**Scope:** a project's `docs/` folder is "messy and has too many files."

- **Phase 1 — Survey:** 47 markdown files. 23 are technique references. 11 are dated meeting notes. 8 are agent loadouts. 5 are unrelated drafts.
- **Phase 2 — Diagnose:** The 23 technique references have no backlinks — category 7 violation (knowledge hub without active links). The 11 meeting notes are append-only but live in the same folder as config files — category boundary violation. The 8 loadouts are duplicated across `docs/agents/` and `agents/`. The 5 drafts are 3 months old.
- **Phase 3 — Propose:** Add backlinks from the project's active prompt-files to the 23 techniques (XS effort, reversible). Move meeting notes to `docs/meetings/` (S effort, reversible via `git mv`). Resolve the duplicate loadouts (M effort, needs human to pick canonical location). Archive or delete the drafts (needs human decision).
- **Phase 4 — Apply:** Human approves the backlinks batch first. Apply one technique at a time, commit per backlink added.
- **Phase 5 — Verify:** Prompt-files still parse. Techniques still render. Smoke clean.
- **Phase 6 — Document:** `LEARNING-ZONE.md` gets a new entry: *"2026-MM-DD — 23 technique files linked from active prompt-files. 4 files surfaced as unused and queued for review."*

Second batch (meeting-note move) proposed next week, not now.

---

## Red flags — stop and escalate

- A file's purpose is unclear and git log doesn't explain it. Stop. Ask the human.
- Two files claim the same authority and both have recent commits. Stop. Ask the human which wins.
- A file references a path that doesn't exist. Note in `SURVEY.md`; do not fix until you understand the history.
- Your improvement would delete content visible to stakeholders or clients. Stop. Ask the human.

---

## What this protocol is NOT

- Not a refactor pass. Don't restructure.
- Not a consolidation sprint. Don't merge files.
- Not automation. This is deliberate human-approved work.
- Not a rewrite. The system is alive; respect it.

---

## Principle

*Strong systems get stronger when you add guardrails. They get weaker when you rebuild them. Pick the first path.*
