# Multi-Agent Team Prompt Templates

Four condensed team archetypes you can paste into the lead and adapt. Each shows the **roster**,
the **handoff graph** (who messages whom), and the **deliverables** — the reusable skeleton, not
a verbatim mega-prompt. Fill the bracketed parts and add your project's specifics.

**Common shape every template follows:**
- One sentence of goal + the concrete artifact you expect at the end.
- `Create a team called "<name>" with N teammates. Use <model> for each.`
- Per agent: a one-line **role**, a short **persona** (optional but sharpens output), **tasks**,
  the explicit **"when done, message X"** handoff, and a single **deliverable file**.
- A final **deliverables table** so you can check completion.

---

## 1. Full-stack build (8 agents) — "ship a working app"

Goal: a running full-stack app plus its docs, tests, and a build summary.

Roster and handoff graph:

```
Product Manager ─┐
                 ├─→ System Architect ─┬─→ Backend Dev ──┐
BRD Manager ─────┘                     ├─→ Frontend Dev ─┼─→ QA Engineer ─→ DevOps/Integration
                                       └─→ QA (test plan)┘
Docs Agent ← (PRD+BRD)  builds traceability matrix + exec summary in parallel
```

| Agent | Owns / deliverable |
|-------|--------------------|
| Product Manager | `docs/PRD.md` — vision, personas, prioritized features, ≥15 user stories, acceptance criteria |
| BRD Manager | `docs/BRD.md` — business objectives, scope, constraints (stack), risks, compliance |
| System Architect | `docs/SYSTEM-DESIGN.md` — architecture, DB schema, full REST contract, auth flow, folder layout |
| Docs Agent | `docs/TRACEABILITY-MATRIX.md`, `docs/EXECUTIVE-SUMMARY.md` |
| Backend Dev | working API in `src/api/` |
| Frontend Dev | working UI in `src/client/` |
| QA Engineer | `tests/` + `tests/report.md` (pass/fail counts) |
| DevOps / Integration | root config, `docs/build-summary.md`, a running app |

Key ordering: architect **waits** for both PM (features) and BRD (constraints) before designing;
backend and frontend run in parallel off the shared API contract; QA depends on shipped code.

---

## 2. Research & strategy (6 agents) — "validate an idea"

Goal: a decision-ready strategy package with an adversarial review baked in.

```
Market Researcher ─┐
Tech Analyst ──────┼─→ Product Strategist ─→ GTM Planner ─┐
                   │                                       ├─→ Devil's Advocate ─→ Report Synthesizer
                   └───────────────────────────────────────┘
```

| Agent | Deliverable |
|-------|-------------|
| Market Researcher | `research/MARKET-RESEARCH.md` — landscape, personas, signals |
| Technical Feasibility Analyst | `research/TECHNICAL-FEASIBILITY.md` — architecture, build-vs-buy, verdicts |
| Product Strategist | `research/PRODUCT-STRATEGY.md` — positioning, pricing, MVP scope, wedge |
| GTM Planner | `research/GTM-PLAYBOOK.md` — 90-day plan, channels, content calendar |
| Devil's Advocate | `research/DEVILS-ADVOCATE-REVIEW.md` — risk heat map, killer questions, go/no-go |
| Report Synthesizer | `research/STRATEGY.md` (master doc) + `research/DECISION-BRIEF.md` (1-page) |

The Devil's Advocate is the load-bearing role: it reviews the other five before synthesis, so the
final brief survives contact with hard questions.

---

## 3. Repo publisher (6 agents) — "make a workspace shareable"

Goal: turn a messy workspace into a clean, documented, public-ready repository.

```
Repo Researcher ─→ Repo Architect ─┬─→ README Writer ─┐
                                   └─→ Docs Writer ────┼─→ Quality Reviewer ─→ Publisher
```

| Agent | Deliverable |
|-------|-------------|
| Repo Researcher | `docs/REPO-RESEARCH.md` — workspace audit + best-practice research |
| Repo Architect | reorganized structure + scaffolding + an index README |
| README Writer | hero `README.md` + per-section READMEs |
| Docs Writer | `GETTING-STARTED`, `ARCHITECTURE`, `FAQ`, `GLOSSARY`, `TROUBLESHOOTING`, `CONTRIBUTING` |
| Quality Reviewer | `docs/QA-REVIEW.md` + fixes applied |
| Publisher | the live repo + `docs/PUBLISH-REPORT.md` (verification + URL) |

Publish step should be gated: nothing goes public until the Quality Reviewer signs off.

---

## 4. Security audit (10 agents) — "red/blue team a system"

Goal: an enterprise-grade security posture package, cross-validated by an adversarial red team.

```
Threat Intel ─┬─→ Security Architect ─┐
              ├─→ Pentester           ├─→ (Code Auditor, Infra, Data Protection, Compliance run in parallel)
              └─→ Red Team Lead ──────┘                         │
                         Red Team Lead challenges every finding ─┴─→ CISO Synthesizer (exec brief + roadmap + register)
```

| Agent | Deliverable |
|-------|-------------|
| Threat Intelligence Analyst | `security/01-THREAT-INTELLIGENCE.md` — attack surface, actor profiles, MITRE ATT&CK map, CVE inventory |
| Security Architect | `security/02-SECURITY-ARCHITECTURE.md` — defense-in-depth, zero-trust, assume-breach controls |
| Code Security Auditor | `security/03-CODE-AUDIT.md` |
| Infra & Cloud Security | `security/04-INFRASTRUCTURE-SECURITY.md` |
| Data Protection & Privacy | `security/05-DATA-PROTECTION.md` |
| Compliance & Governance | `security/06-COMPLIANCE-GOVERNANCE.md` (SOC 2 / ISO 27001 / NIST 800-53 mapping) |
| Penetration Tester | `security/07-PENETRATION-TEST.md` |
| SecOps & Incident Response | `security/08-SECOPS-INCIDENT-RESPONSE.md` |
| Red Team Lead / Adversarial Reviewer | `security/09-RED-TEAM-REVIEW.md` — challenges every other finding |
| CISO Synthesizer | `10-CISO-EXECUTIVE-BRIEF.md` + `SECURITY-ROADMAP.md` + `MASTER-SECURITY-REGISTER.md` + `README.md` |

The differentiator vs. a single security pass: **adversarial validation** — a dedicated red-team
role exists to attack every assumption and contest every control before the CISO brief is written.

---

## Adapting these

- Keep the **handoff messages explicit** ("when done, message X with Y") — that's what turns a
  pile of agents into a pipeline.
- Keep **one deliverable file per agent** — it makes ownership and completion checkable.
- Right-size: most of these compress to 3–5 agents fine. Drop the synthesizer and merge adjacent
  roles when the scope is small (see `patterns-and-best-practices.md` on team sizing).
- Enforce gates with `team-hooks.md` (e.g. block "build" agents from idling until tests pass).
