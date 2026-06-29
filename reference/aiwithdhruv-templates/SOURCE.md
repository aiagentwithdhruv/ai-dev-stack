# reference/aiwithdhruv-templates

**Origin:** Distilled and de-identified from a private "workspace templates hub" — a
boilerplate repo used to scaffold a new team member's coding workspace in minutes (folder
skeleton + `CLAUDE.md` anchors + named agent personas + role briefs + dispatch templates +
onboarding checklists). Most of that repo was identity-bearing (named people, named products,
a specific GitHub org, a specific secrets vault, internal revenue tasks) and was **not** folded.

**Why anything is here:** Two artifacts in the source were genuinely generic, reusable, and
**not already covered** by the flagship or earlier reference folds:

1. The flagship's `pillars/agents/patterns/` describes the *agent-as-markdown* pattern in four
   lines (role + tools + constraints as a versioned file). The source operationalised that
   pattern into a concrete, repeatable **role-agent profile** with a distinctive shape — an
   explicit *"what this agent does NOT do"* boundary list and a *good-prompt-vs-bad-prompt*
   contrast that teaches the dispatcher how to hand off. That template is worth keeping.
2. The flagship's `pillars/automation/` is a **pointer** to a companion repo (`ai-automation-kit`)
   and ships no depth. The source carried a real **automation operations playbook** — the
   seven-step workflow shape, an idempotency checklist, backoff rules, a secret-handling
   do/don't, observability requirements, a failure-mode table, and a Definition of Done. That
   playbook is generic and fills the gap. (Its natural long-term home is `ai-automation-kit`;
   it is parked here as a curated reference.)

## What's in this folder

| File | What it is |
|------|------------|
| `role-agent-profile-template.md` | A vendor-neutral template for defining a single narrow-scope agent: what it does / does NOT do / hard rules / how to dispatch (good vs bad prompt) / output report format / context-load order. Includes one worked example. |
| `automation-playbook.md` | Generic operations playbook for deterministic workflow automation: the "automate if a human would do it twice" decision tree, the 7-step flow shape, idempotency + backoff + secret handling, observability requirements, a failure-mode/defence table, and a Definition of Done. |

## What was deliberately NOT folded (leak-safety)

- **All person names** and the team roster (founder, PM agent, peers).
- **All named agent personas** (the source's backend / frontend / automation / QA / content /
  sourcing personas) — replaced with generic role names.
- **All product and project names**, and the GitHub org / private repo names.
- **The four-hub `sync.sh` / `scaffold.sh` workspace-bootstrap machinery** — too tied to the
  source's specific repo layout, secrets vault, and central agent archive to generalise cleanly.
  The *idea* (a scaffold script that stamps `{{NAME}}/{{ROLE}}` placeholders to mint one
  per-person workspace from a template, then syncs shared "doctrine" hubs into a gitignored
  `.shared/`) is noted here but the script itself was not copied.
- **The `dispatch-templates/REV-*` files** — 100% internal revenue tasks with real first names,
  rupee compensation figures, dated deadlines, geographic targeting, and product-specific ICP
  definitions. Pure internal; excluded entirely.
- **The onboarding checklists** — referenced a specific secrets vault, a private central archive,
  and a named founder onboarding call. Excluded.
- A specific secrets-vault brand was generalised to "secrets manager / vault"; a specific
  transactional-email vendor to "transactional email provider".

If you adopt these, swap the generic role/product placeholders for your own and pick your own
workflow engine and secrets manager.
