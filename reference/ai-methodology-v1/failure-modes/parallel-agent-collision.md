# Parallel Agent Collision

## What happens

Two specialist agents work concurrently on the same git repository. Agent A pre-stages files for its task but hasn't committed yet. Agent B runs `git add -A` to stage its own files. Agent B's commit absorbs all of Agent A's pre-staged files. The commit is now a mix of two unrelated changes. The work is not lost, but it is entangled.

The entanglement compounds: subsequent commits from both agents now build on an incorrect baseline. The sprint ends with a git history that cannot be cleanly read or rolled back by change.

## Why it happens

`git add -A` is the path of least resistance. It stages everything and asks no questions. In a single-agent environment it is usually harmless. In a parallel-agent environment it is a trap.

The pre-staged files from Agent A look, to Agent B, identical to Agent B's own files: they are unstaged changes in the working tree. `git add -A` cannot distinguish them.

## How it escalates

1. Agent B commits 731 lines of Agent A's code under its own commit message.
2. Agent B's commit message ("feat: add UI component") now describes a subset of what's in the commit.
3. Agent A commits later, but its files are already in Agent B's commit. Agent A's commit now has nothing, or worse, has a conflicting version.
4. The orchestrator's diff review sees a commit that doesn't match its title.
5. At sprint end, cleaning up requires git bisect, cherry-pick, or manual re-application of the correct changes.

Born from: two agents working the same repository during a concurrent sprint. One agent pre-staged a 731-line service file. The other ran `git add -A` before committing a UI component. The service file appeared in the UI commit. Discovered at sprint end.

## Defence

**1. Explicit paths only. `git add <specific-paths>` always.**

Every prompt for every specialist agent must include:
```
Use `git add <explicit paths>` (never `-A` or `.`).
Verify `git diff --cached --stat` shows only your files before committing.
```

**2. Verify staged files before committing.**

After every `git add`, run:
```bash
git diff --cached --stat
```
Read every line. If any file listed does not belong to this task: `git restore --staged <path>`.

**3. Scope-lock in every prompt.**

Every prompt includes a `DO NOT TOUCH` list: files owned by other agents in this sprint. This makes foreign files recognisable during staging.

**4. If hijack is discovered after commit: document, don't rebase.**

Annotate the commit body:
```
Note: also includes foreign-file.py from parallel session — clean up at sprint end.
```

Report to the orchestrator immediately. Do not attempt rebase mid-sprint — rebase on a shared branch with parallel work creates divergence that is harder to resolve than the original collision.

**5. Orchestrator verifies each commit's diff stat against its title.**

After parallel batches, the orchestrator checks: does this commit's diff contain only files consistent with its commit message? A mismatch is a collision signal.
