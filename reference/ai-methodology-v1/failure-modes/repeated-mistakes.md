# Repeated Mistakes

## What happens

A bug is found. The code is fixed. The sprint moves on. Three sprints later, the same bug appears again. Someone says "we fixed this before." The fix is re-applied. Two sprints after that, the bug appears again.

The code was fixed. The system was not.

## Why it happens

A code fix changes the code. It does not change the prompts that produce the code, the rules that govern the agent, or the agent's understanding of why the fix was necessary.

The next time a similar task is assigned, the agent writes new code without the constraint the fix implied. The prompt didn't mention it. The rule file didn't include it. The lesson existed only in a commit message no one reads before writing new code.

The fix is local. The bug is systemic.

## How it escalates

1. Sprint 1: agent produces code with bug. Bug is fixed manually.
2. Sprint 2: new agent session. Writes similar code without knowing about the bug from Sprint 1. Bug reappears.
3. Sprint 3: the pattern is noticed. "This keeps happening." Time is spent tracing the history.
4. Every recurrence costs the same time as the original fix. The cumulative cost grows linearly with recurrences.

Born from: the same field-naming mismatch appeared in 3 consecutive sprints. Each time, an agent wrote spec-imagined field names instead of real schema names. The fix was in the code each time. The prompt was never updated to say "grep the schema before listing fields." The lesson only lived in commit messages.

## Defence

**1. Eval-loop rule: fix code and fix the prompt in the same commit.**

Any commit that fixes an agent-caused error must include:
- The code fix
- The prompt-file update (or rule-file update) that prevents the same error

These are committed together. The rule and the fix are inseparable in git history.

**2. Rule files are the durable layer.**

Lessons go in `04-rules/`. Prompt-specific pitfalls go in the spec file or CLAUDE.md for that module. The agent reads these files before starting work. The lesson is activated by the work itself.

**3. Post-sprint retrospective rule extraction.**

After every sprint, review the commits that contained bug fixes. For each fix: is there a rule that, if the agent had known it, would have prevented the bug? If yes: write the rule now.

**4. Boot sequence reads rule files.**

Every agent boot sequence explicitly reads `04-rules/` files. This is not optional. A lesson in a rule file that isn't in the boot sequence is a lesson that will be forgotten.

**5. "Born from" annotations on every rule.**

Every rule in the rule library includes a "Born from" line: a one-sentence description of the incident that produced the rule. This context tells future agents and humans why the rule exists — and makes it harder to dismiss the rule as bureaucratic overhead.

**6. Three-strikes extract.**

If the same pattern appears in 3 or more places in the codebase, extract it to a shared utility. If the same mistake happens 3 or more times, extract it to a rule and link it from every prompt that could trigger it.

Three is the threshold for "this is now a system problem, not an individual error."
