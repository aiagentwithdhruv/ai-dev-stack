# Source: product-rules dashboard (folded extract)

This folder is a **curated, sanitized extract** from a personal product-development
rules dashboard (an interactive single-file HTML of ~57 rules across Personal /
Agent-Team / Coding / Marketing tabs). The original was authored for one engineer's
internal product project, so most of it was personal, brand-specific, or team-specific and
was **not** folded.

## What was kept (and why)

Only the **language-level bug cures** and a small set of **vendor-neutral workflow
gotchas** were folded. These are concrete, reproducible engineering lessons that
the flagship `rules/` corpus (which is high-level architectural convention) does not
capture at this granularity. They read as "things that silently break and how to
avoid them" — useful to any team on a Python + Postgres + FastAPI/Pydantic +
React/Next.js stack.

- `engineering-bug-cures.md` — concrete bug cures (Python / SQLAlchemy / Postgres /
  Pydantic / React / multi-tenant / build hygiene).
- `workflow-discipline.md` — generic shipping discipline distilled to neutral rules.

## What was deliberately excluded (leak-safety)

- All personal mindset / "how I work" content (the **Personal** tab) — identifying.
- The entire **Agent-Team** tab and the agent **rewards/credit ledger** — names
  individual AI agents and an internal team process.
- The entire **Marketing** tab — personal outbound brand voice + approval flow.
- All person names, lab/brand names, course-instructor attributions.
- Internal product specifics: the CRM's module chain, table/column names, internal
  tenant names, client/example company names, internal modal/component names,
  internal log/file paths, and any backend-provider project identifiers.

The patterns below were rewritten to be employer-neutral and example-free where the
original used real internal identifiers.
