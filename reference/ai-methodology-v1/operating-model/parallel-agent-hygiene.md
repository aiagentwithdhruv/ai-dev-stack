# Parallel Agent Hygiene

Running 2 or more agents on the same git repository simultaneously multiplies velocity. It also introduces a class of failure that doesn't exist in single-agent work: commit contamination, where one agent's commit absorbs another agent's pre-staged files.

The failure is silent. The commit looks normal. The commit message says "backend route implementation." The diff includes a 731-line frontend file that has nothing to do with backend routes. Neither agent notices. The orchestrator catches it at Gate 4 — or it ships.

These rules exist to prevent that failure. They cost each agent 20 seconds per commit. They prevent hours of untangling.

---

## The Core Rule: Explicit Paths Only

When 2 or more agents are committing in the same repository:

```bash
# NEVER
git add -A
git add .

# ALWAYS
git add backend/routes/orders.py backend/services/order_service.py
```

`git add -A` and `git add .` collect ALL untracked and modified files in the repository — including files another agent has staged but not yet committed. One session's pre-staged work becomes another session's accidental commit.

This is not theoretical. It happened on a live sprint: one agent had staged a 731-line service file but hadn't committed. Another agent ran `git add -A`, absorbed the staged file, and committed it under the wrong task. The file was now in the wrong commit, associated with the wrong task, and the actual owning agent had nothing to commit when it finished.

**There is no safe use of `git add -A` or `git add .` in a parallel-agent environment.**

---

## Before Every Commit: Verify the Staged Set

After `git add <explicit-paths>` and before `git commit`:

```bash
git diff --cached --stat
```

Read the output. Every file listed should belong to the current task. If a foreign file appears:

```bash
git restore --staged path/to/foreign/file
```

Then re-verify with `git diff --cached --stat` before committing.

This takes 10 seconds. It is the difference between a clean commit and a contaminated one.

---

## Scope Lock Files

When 2 or more agents are working the same repository, each agent should declare its file scope upfront — before writing any code. Use a scope lock file in `/tmp/`:

```bash
# Agent session A (backend)
cat > /tmp/scope-backend.txt << 'EOF'
Session: backend-task-02
Owner: Backend Specialist
Files:
  backend/routes/orders.py
  backend/services/order_service.py
  backend/tests/test_orders.py
  backend/supabase/migrations/072_orders_table.sql
EOF

# Agent session B (frontend)
cat > /tmp/scope-frontend.txt << 'EOF'
Session: frontend-task-02
Owner: Frontend Specialist
Files:
  frontend/src/pages/Orders.tsx
  frontend/src/components/OrderForm.tsx
  frontend/src/hooks/useOrders.ts
EOF
```

The scope lock file is not enforced by git — it's a coordination artifact. Its purpose: when the orchestrator writes both prompt files, file ranges are declared explicitly and non-overlapping. If two sessions would touch the same file, the orchestrator sequences them (session A finishes and commits; session B starts) rather than running them in parallel.

**Two sessions should never write the same file at the same time.** The scope lock makes this violation visible before it happens.

---

## Sequencing vs Parallelising

Not all work can be parallelised safely.

**Safe to parallelise:**
- Backend endpoint + corresponding frontend component, if the API contract is already fixed and both agents have read-only access to it
- Two independent backend endpoints in different route files
- Two independent frontend pages that share no components

**Must be serialised:**
- Shared utility files (a constants file, a base model, a shared hook)
- Migration files (SQL migrations must have sequential numbers — two agents cannot both write `migration_072.sql`)
- Any file where both sessions would write different changes

The orchestrator decides the parallelisation boundary. When in doubt, serialise. The time saved by parallelising a shared file is always less than the time lost untangling the merge conflict or the overwrite.

---

## When Hijack Happens Anyway

If an agent commits a foreign file (caught at Gate 4 or later):

1. **Do not rebase, cherry-pick, or reset mid-sprint.** The risk of creating a worse state is high.
2. Document in the next commit's message: `Note: [foreign-file.py] absorbed from parallel session — will separate at sprint end`
3. Flag it explicitly in the agent's report to the orchestrator
4. At sprint end, the orchestrator and human review the contaminated commits, decide whether to split or accept, and clean up in a dedicated commit

This is a last-resort. The rules above exist to make it unnecessary. If it happens more than once, the scope lock process wasn't being followed.

---

## Migration File Discipline

Migration files require extra care in parallel-agent environments because they have sequential naming requirements that git cannot enforce.

The rule: **only one agent may write a new migration at a time.**

Before writing a migration:

```bash
ls backend/supabase/migrations/ | tail -5
```

Take the next sequential number. If you're unsure what the current highest number is — check before writing, not after.

If two agents both write `migration_072.sql` with different content, one of them will fail to apply. The failure mode is not always immediately obvious — it may surface only when the migration is run against a database that already has `072` from the other session.

The orchestrator serialises migration work: session A writes and commits its migration, session B verifies the commit exists, then takes the next number.

---

## Branch Discipline in Parallel Work

All parallel agent work runs on the same branch (`dev` by convention). Separate feature branches per agent introduce merge complexity that costs more than the isolation gains.

The discipline that makes single-branch parallel work safe:
- Atomic commits (Gate 2)
- Explicit git add paths
- Scope lock files
- The orchestrator serialising shared-file work

These compensate for the lack of branch isolation. They're cheaper than merge management.

---

## Crystallised Principle

**Parallel velocity is only real if parallel commits are clean. `git add -A` in a multi-agent session is not a shortcut — it's deferred debugging.**

Declare scope upfront. Add explicit paths. Verify `git diff --cached --stat` before every commit. Serialise shared files. The 30 seconds this costs per commit is paid back the first time it prevents a contaminated commit.
