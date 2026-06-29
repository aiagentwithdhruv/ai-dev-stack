# reference/agent-session-archive

**Origin:** Folded from a private internal repo that scaffolded a central archive for
multi-agent coding sessions. The source was ~90% empty stubs (placeholder `README.md`
files per folder) plus three process docs and one prompt template.

**Why it's here:** The *idea* is reusable and is not covered elsewhere in this stack —
flagship `prompts/` and `rules/` cover how to drive agents, but nothing covers the
**learning loop**: capturing every prompt+response, promoting what works into templates,
and naming failure modes with concrete defences so they stop recurring. That loop is the
unique, generic contribution. Everything identity-bearing was dropped.

## What's in this folder

| File | What it is |
|------|------------|
| `agent-session-archive-method.md` | The methodology: log → review → promote loop, session-log template, pattern template, naming/redaction rules |
| `failure-mode-ledger.md` | "Scar ledger" format — name a failure mode once it recurs, attach a concrete defence; includes generic seed failures |
| `prompt-template-backend-endpoint.md` | A parameterized prompt template for "add one backend endpoint" (sanitized) |

## What was deliberately NOT folded (leak-safety)

- All person names and the team roster.
- All internal agent code-names — replaced with generic roles (pm-agent, backend-agent,
  frontend-agent, content-agent, outreach-agent, finance-agent, qa-agent, ops-agent).
- All product / project names and the GitHub org.
- Revenue targets, deadlines, "north-star" numbers, and the bootstrap session list.
- Names of connected private repos and individual workspaces.
- Company/brand name and any contact details.

If you adopt this, swap the generic roles/products for your own.
