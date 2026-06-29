# 05-failure-modes — Scar Ledger

These are the failure patterns this methodology was built to prevent. Each one is a real incident, distilled into a named pattern. Each has a defence.

## How to read this ledger

Every file covers one failure mode. The format is:

- **What happens** — the observable symptom
- **Why it happens** — the root cause
- **How it escalates** — how the problem gets worse before anyone notices
- **Born from** — a one-sentence generic description of the real incident that produced this pattern
- **Defence** — the specific changes to process or tooling that prevent recurrence

Read the defences as rules, not suggestions. Each one was bought with real time.

## How to add a new failure mode

1. A failure happens (agent error, lost work, production incident, client trust event).
2. After the incident is resolved: write a new file here.
3. Name it after the pattern, not the incident: `context-rot.md`, not `the-april-sprint-thing.md`.
4. Follow the format above.
5. Update the relevant rule file in `04-rules/` with the resulting rule.
6. Commit both files together: the scar and the rule live or die together.

## Index

| File | Pattern | Likelihood |
|------|---------|-----------|
| `parallel-agent-collision.md` | 2 agents on 1 tree, `git add -A` hijacks work | High |
| `context-rot.md` | Long session forgets early constraints | High |
| `notes-nobody-reads.md` | Lesson written but never loaded | High |
| `render-vs-save-confusion.md` | Output treated as source of truth | Medium |
| `silent-failures.md` | Tests green, browser broken | High |
| `repeated-mistakes.md` | Same bug three sprints in a row | Medium |
| `destructive-ops-no-safeguard.md` | Overwrite with no backup, content lost | Medium |
| `context-compaction-drop.md` | Compaction summarises away critical state | Medium |

## On likelihood

"Likelihood" is the probability of recurrence without the defence in place. High means it has happened more than twice. Medium means it has happened once with potential to recur. Low means it happened once in unusual circumstances.

Defences for High-likelihood patterns are mandatory. Defences for Medium-likelihood patterns are strongly recommended.
