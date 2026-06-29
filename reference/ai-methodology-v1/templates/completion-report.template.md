# Completion Report Template (Master Rule §7)

After every code wave, the agent posts this verbatim. The orchestrator archives it to `docs/agent-reports/{date}-{wave}-{agent}-{chat}.md` BEFORE updating CC / tags / tasks.

```
=== COMPLETION REPORT (MANDATORY) ===

FEATURE IMPLEMENTED:
[One-line description of what was built]

COMMITS:
1. [SHA] [subject line]
2. [SHA] [subject line]
...

FILES CHANGED:
1. [path/to/file.ext] — [what changed and why, line range if relevant]
2. ...

FILES CREATED:
1. [path/to/new-file.ext] — [purpose]

LOCKED AREAS VERIFICATION:
[ ] Authentication — NOT MODIFIED
[ ] Permissions — NOT MODIFIED
[ ] API contracts — NOT MODIFIED
[ ] Database schema — NOT MODIFIED
[ ] Routing — NOT MODIFIED
[ ] Global CSS / Tailwind config — NOT MODIFIED
[ ] Shared components — NOT MODIFIED (or list each + reason if touched)
[ ] Existing validations — NOT MODIFIED
[ ] Existing UI elements — NOT MODIFIED
[ ] tenant_id present on all new queries (multi-tenant projects)
[ ] No center-overlay-with-backdrop modal added (project standard)

NEW FEATURE TEST CASES (orchestrator test plan):
1. [Step-by-step action] → Expected: [outcome]
2. ...

REGRESSION AREAS TO VERIFY (QA / orchestrator):
1. [Module / screen] — [what to spot-check]
2. ...

API SMOKE (backend tasks only):
- [ ] uat-smoke: 17/17 PASS
- [ ] curl on the new endpoint: [paste response]

KNOWN RISKS:
1. [Risk + mitigation, or "None"]

ANOMALIES (if any deviated from prompt):
1. [What was different + why + what was actually shipped]

SELF-CONFIRMATION:
I confirm no existing working functionality was intentionally broken or modified.
All changes are additive and isolated to the requested scope.
=========================================
```

## Why this format works

- **Commit SHAs at top**: revert path is one `git revert <SHA>` per atomic commit
- **Files changed/created sections**: orchestrator can verify scope without re-reading the diff
- **Locked-areas checklist**: forces the agent to consciously confirm each area; missed checks surface as obvious omissions
- **Test plan written by the agent**: agent knows what they changed best; their test plan is the ground truth
- **Anomalies section**: deviations stop being silent. Documented deviation = known debt.
- **Self-confirmation**: forces the agent to assert "I did not break anything" — psychological gate against half-finished work being declared complete.

## Production validation

This format was proven across 25+ code waves on a multi-tenant SaaS project: zero silent regressions, with multiple anomalies (a UI-framework reconciliation footgun caught during impact analysis, a shared-primitive change halted before it spread, a missing-field bug stopped at report time) caught and escalated cleanly. Orchestrator review time dropped from ad-hoc grep + diff inspection to a consistent scan of a known structure.
