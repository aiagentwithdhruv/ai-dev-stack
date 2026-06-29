# Sub-agent role definitions

Ten ready-to-drop sub-agent files. Each is a self-contained role brief with YAML frontmatter
(`name`, `description`, `model`, `tools`, optional `permissionMode` / `isolation` / `memory`)
followed by the system prompt for that role. They complement the flagship's `docs/AGENTS.md`
(when-to-use prose) and `pillars/agents` by giving you concrete, installable specialists.

| File | Role | Default model | Writes code? |
|------|------|---------------|--------------|
| `code-reviewer.md` | Quality/security review, PASS/FAIL verdict | opus | no (review only) |
| `security-auditor.md` | OWASP Top 10 + AI-specific audit + hardening | opus | no (audit only) |
| `researcher.md` | Codebase exploration + web research, cited findings | sonnet | notes only |
| `backend-builder.md` | APIs/services/DB logic (routes→services→repos) | opus | yes (worktree) |
| `frontend-builder.md` | UI components, pages, styling | sonnet | yes (worktree) |
| `db-architect.md` | Schemas, migrations, indexes, RLS | sonnet | yes |
| `api-integrator.md` | OAuth, webhooks, REST/GraphQL clients | sonnet | yes |
| `test-runner.md` | Run + write tests, lint, validate | sonnet | yes |
| `mcp-builder.md` | Build MCP servers (tools/resources/prompts) | sonnet | yes |
| `deployer.md` | CI/CD, containers, env/secrets, domains | sonnet | yes |

**Usage:** drop the files into your agent host's sub-agent directory (e.g. `.claude/agents/`),
adjust the `tools` and `model` to your host, and reference the role by `name`. The two
review/audit roles are deliberately read-only — keep them that way so their verdicts stay
unbiased. The tech stacks named inside (FastAPI, Next.js, Postgres, Supabase, Vercel, etc.) are
illustrative defaults — swap them for your own.
