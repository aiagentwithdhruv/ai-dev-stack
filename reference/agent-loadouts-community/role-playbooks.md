# Role Playbooks — Starter Loadouts by Use Case

A playbook is a short doc that lists which context, skills, and tools to combine for a
specific role, so you go from zero to a working AI setup in minutes. Each one below is
a vendor-neutral starting point — fill in your own details.

Common shape for every playbook:

```
my-loadout/
├── .claude/CLAUDE.md   # context: who you are, rules, current state
├── skills/<task>/SKILL.md
└── LOADOUT.md          # manifest: what's included + self-update rules
```

---

## 1. Freelancer / Consultant

**Goal:** proposals, pricing, pipeline, outreach in your own voice.

Context to capture: services + pricing table, your tone ("never say…"), current
pipeline (client / project / status / value), monthly revenue target.

Starter skills:

| Skill | Does |
|-------|------|
| `write-proposal` | Reads your pricing, drafts a proposal in your voice + follow-up email |
| `outreach` | Personalized cold outreach sequences |
| `generate-report` | Client deliverable reports |
| `manage-pipeline` | Track leads, clients, revenue |

Proposal skill rule that matters: **always use your actual pricing, never invent
numbers**; reference relevant past projects; end with one specific next step.

---

## 2. Sales Team

**Goal:** lead gen, qualification, outreach, pipeline.

Context to capture: what you sell, ICP, ACV, sales cycle length, pricing tiers,
objection-handling table, competitor table (their price / your advantage).

Starter skills + chain:

```
scrape-leads → classify-leads → personalize → outreach → follow-up
```

`scrape-leads` declares a schema (inputs: query, location, max_results; outputs:
leads_csv, summary) so it chains cleanly into `classify-leads`. Scoring uses the ICP
from context. Track: leads/week, open rate, reply rate, demos/week, close rate.

---

## 3. Content Creator

**Goal:** idea research, scripts, titles, thumbnails, editing, calendar.

Context to capture: platform + niche, cadence, your style ("signature phrases",
"never do"), what's performed best (title / views / why), competitor table.

Pipeline:

```
find-outliers → generate-titles → write-script → thumbnail-concept → edit-video
```

`find-outliers` rule: pull recent videos in your niche, find ones that beat channel
average ~10x, extract title pattern + hook + format + why it spread, then adapt ideas
to **your** style rather than copying.

---

## 4. Developer

**Goal:** code review, tests, deploy, docs — with full project context.

Context to capture (`.claude/CLAUDE.md`): architecture (FE/BE/DB/host), key-files
table, conventions (branch naming, commit style, test framework, linter), known-issues
table, environment versions, **self-update rules** (new endpoint → update API table;
bug fixed → drop from known issues).

Skill vs agent split:
- `code-review` **skill** = fixed checklist (security/OWASP, perf, error handling,
  missing tests, convention violations) → PASS/FAIL with line numbers.
- `code-reviewer` **agent** = judgment: reads intent, decides PASS/FAIL, but **never
  fixes** code (separation of concerns).

Deploy skill: run tests → build → push image → deploy → verify health check →
report; with an explicit rollback path on failure.

---

## 5. Agency Owner

**Goal:** onboarding, multi-client ops, reporting, renewals.

Context to capture: services (price / delivery / margin), active clients (service /
MRR / start / health), team (role / capacity), processes, MRR + churn.

Structure adds per-client context folders:

```
agency-loadout/
├── skills/{create-proposal,onboarding,generate-report,pipeline-tracker,renewal-reminder}/
└── clients/<client>/CONTEXT.md
```

Onboarding skill output: filled client `CONTEXT.md`, welcome email draft, milestone
timeline, first report template.

Scaling adds skills by stage: solo (proposal, report) → small team (onboarding,
pipeline) → agency (renewal, capacity-planning) → scaled (white-label, dashboards).

---

## 6. Student / Researcher

**Goal:** research, note-taking, project organization, literature review.

Context to capture: subjects/courses, current projects + deadlines, preferred note
format, citation style.

Starter skills: `literature-research` (gather + summarize sources with citations),
note organization, and a project tracker. Keep findings in `memory/` so prior reading
carries across sessions (see `memory-vs-context.md`).

---

## Writing your own playbook

A playbook just lists: which context files to create, which skills to include, which
tools to set up, and a step-by-step setup guide. Start from the closest role above,
strip what you don't need, and add the one skill you repeat most. Add more as the
repetition reveals them — the loadout compounds.
