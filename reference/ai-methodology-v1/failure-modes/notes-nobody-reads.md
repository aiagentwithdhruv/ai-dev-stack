# Notes Nobody Reads

## What happens

A lesson is learned. Someone writes it down: in Obsidian, in a shared doc, in a team wiki, in a Slack message, in the project README. The note is accurate. It is well-written. It will never be read again.

The next sprint starts. A fresh agent session opens with no knowledge of the note. The same pitfall is encountered. The same 30 minutes are lost. The fix is applied again. No one updates the note because no one checked the note.

The lesson exists. It is just stored in a location that no active process ever reads.

## Why it happens

Notes are written in a moment of pain. The team is motivated to document. They document in the most natural location — a wiki, a README, a shared document. Then they move on.

The problem is activation. A wiki is passive. It answers questions when queried. Agent sessions don't query wikis on startup; they load their context window from the files the system directs them to read.

If the lesson is not in a file that the agent reads as part of its standard boot sequence, the lesson is not accessible to the agent.

## How it escalates

1. Bug fixed. Lesson written. In Obsidian.
2. Next sprint: fresh agent session. Boot sequence reads CLAUDE.md and a few spec files. Does not read Obsidian.
3. Agent encounters the same pitfall. Makes the same fix.
4. Human notices. "We documented this." No one can find the note quickly.
5. The note is rediscovered. Someone says "we need a better system." The note is copied somewhere else. The cycle restarts.

Born from: a database field naming mismatch was discovered and documented in the project wiki. The next sprint, a fresh agent used the spec-imagined field name again, not the real schema name. The wiki note had never been loaded into any agent's boot sequence.

## Defence

**1. Passive documentation → active prompt-file.**

The lesson must live inside the file the agent must read to do the work. Not in a parallel location. Inside the spec file, inside the CLAUDE.md, inside the prompt itself.

Structure:
```markdown
## Known pitfalls for this module

- Field name: the spec calls this `warehouse_name`. The actual schema column is `name`. Always grep the migration before using a field name.
- Validation: the create endpoint rejects requests where `code` contains spaces. Sanitise before sending.
```

This section is read every time the spec is read. The lesson is activated by the work itself.

**2. Commit the rule in the same commit as the fix.**

When a bug is fixed that reveals a lesson:
- Update the relevant rule file in `04-rules/`
- Update the relevant spec or CLAUDE.md with the pitfall note
- Commit both in the same commit as the fix

The rule and the fix live together in git history. They are inseparable.

**3. Eval-loop rule.**

Any commit that fixes an agent-caused error must include a prompt-file update in the same commit. The prompt that caused the error must be modified so that if an agent reads it again, it will not make the same error.

**4. Boot sequence reads rule files.**

Every agent's boot sequence explicitly lists the rule files to read before starting work. The rule files are in `04-rules/` or equivalent. This is not optional — it is the first step of every session.

**5. Weekly lint.**

Once per week (or per sprint): read each lesson in the rule files and ask: is this lesson still being applied? Has any recent commit violated it? If so: the lesson needs to move closer to where the work happens.
