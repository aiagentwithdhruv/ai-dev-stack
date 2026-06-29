# The Loadout Framework — portable, self-updating agent context packs

> Context beats prompts. A well-equipped agent — one that already knows the architecture, the domain,
> the procedures, and the failure modes — outperforms a cleverly-prompted one that knows none of it.
> A **loadout** packages that context so it's portable across tools, composable, and kept fresh.

---

## 1. Pack anatomy

Every loadout is a folder with a predictable shape. Agents read top-down: manifest → master context →
the specific skill/runbook/test they need.

| File | Type | Purpose | Auto-loaded? |
|------|------|---------|--------------|
| `LOADOUT.md` | Manifest | Identity, version, dependencies, tier, refresh cadence, supported platforms | No (read on demand) |
| `.claude/CLAUDE.md` | Context | Master context — what it is, what's built, architecture, instructions. Keep < ~200 lines | Yes, in Claude Code |
| `skills/*/SKILL.md` | Skill | Per-system deep context: codebase map, recipes, known issues, typed Schema | On demand |
| `knowledge/*.md` | Knowledge | Domain expertise — glossary, market/domain facts, best practices | On demand |
| `runbooks/*.md` | Runbook | Step-by-step procedures (deploy, configure, recover) | On demand |
| `tests/*.md` | Tests | Validation scenarios that prove the agent knows the domain | On demand |
| `memory/MEMORY.md` | Memory | Rolling state the agent appends to across sessions | On demand |
| `workflows/*.json` | Workflow | Optional automation exports (e.g. n8n) | Imported by the tool |

Keep the master context small so it loads cheaply on every turn; push depth into `skills/`, `knowledge/`,
and `runbooks/` that are pulled in only when relevant.

---

## 2. Cross-platform mapping

The same loadout works across AI coding tools — only the entry point changes:

| Platform | How to use |
|----------|------------|
| Claude Code | Drop in project root — `.claude/CLAUDE.md` auto-loads. |
| Cursor | Copy the master context into `.cursor/rules/*.mdc`; add knowledge files as extra context. |
| Codex / AGENTS.md tools | Use the master context as `AGENTS.md` (compatible structure). |
| Any LLM | Feed the master context as the system prompt; attach knowledge files for depth. |
| n8n / automation | Import workflow JSON from `workflows/`. |

---

## 3. Self-update + staleness (keep packs alive, not rotting)

A loadout that never updates becomes a liability — confidently wrong. Bake refresh rules into the files:

**Self-update triggers** (put a small table in `LOADOUT.md` and each master context):

| Event | Update | Section |
|-------|--------|---------|
| New feature shipped | Add to features list | What's Built |
| API endpoint added | Update codebase map | Codebase Map |
| Architecture changed | Update the diagram | Architecture |
| Bug fixed | Mark resolved | Known Issues |
| Pricing / external fact changed | Update the relevant table | Domain Knowledge |

**Verification cadence + staleness markers:** stamp each major section with `last_verified: YYYY-MM-DD`
and a `refresh_cadence` (monthly / quarterly / yearly). When an agent reads a section whose
`last_verified` is older than its cadence, it should flag:
*"This section may be stale (last verified: {date}). Verify before relying on it."*

A simple **staleness checker** can scan every `LOADOUT.md`, compare `last_verified + refresh_cadence`
against today, and report which packs are overdue. Wire the report wherever you want (stdout, CI, a chat
webhook) — keep any webhook URL/token in env vars, never in the script.

---

## 4. Principles

1. **Context > prompts** — equip the agent, don't out-clever it.
2. **Self-updating** — every file carries rules for when and how to refresh itself.
3. **Verifiable** — `tests/` prove the agent actually knows what it claims.
4. **Portable** — one pack, many tools (Claude / Cursor / Codex / any LLM).
5. **Composable** — loadouts can depend on other loadouts; skills can chain (see §6).
6. **Domain-first** — the templates are a starting point, not the destination. Fill them with real depth.
7. **Public-safe by construction** — credentials and any identifying data live only in *private* packs;
   public/shared versions are sanitized (the context template flags this explicitly).

---

## 5. Managing a library — generic tool surface

When you maintain many loadouts, a thin CLI + MCP layer makes them discoverable and verifiable. The
*interface* below is the reusable part; implement it against your own workspace layout and keep all paths
configurable via an env var (e.g. `LOADOUT_WORKSPACE`) rather than hardcoded.

**CLI commands:**

| Command | Purpose |
|---------|---------|
| `init <name>` | Scaffold a new loadout from the templates. |
| `verify [path]` | Check a loadout's structure + staleness. |
| `list` | List all loadouts in the workspace with version/status. |
| `schema <skill>` | Show a skill's typed Schema (see `schema-section-convention.md`). |
| `search <query>` | Find skills by keyword. |
| `chains` | Show pre-defined skill composition chains. |
| `doctor` | Full workspace health check (structure, staleness, missing schemas). |

**MCP tool surface** (so an agent can discover loadouts at runtime over stdio):

| Tool | Purpose |
|------|---------|
| `list_loadouts` | Enumerate available loadouts. |
| `get_skill` | Return a skill's content + Schema. |
| `search_skills` | Keyword search across skills. |
| `get_routing` | Map an intent ("send a message", "research X") to the right skill(s). |
| `check_staleness` | Report overdue packs. |
| `get_schema` | Return the typed Schema for a named skill. |

Configure such a server with a workspace path supplied via env, e.g.:

```json
{
  "mcpServers": {
    "AgentLoadout": {
      "command": "python3",
      "args": ["loadouts/tools/loadout_mcp.py"],
      "env": { "LOADOUT_WORKSPACE": "/path/to/workspace" }
    }
  }
}
```

---

## 6. Composition chains

Because every skill declares a typed Schema (Inputs / Outputs / Composable-With), skills chain into
pipelines where one's output feeds the next. Define named chains so an agent can run a whole workflow:

```
# generic example
fetch-records → classify-records → enrich-records → draft-outreach → send-message
```

Document each chain as: name · ordered skills · the use case it serves. A chain is valid when each
step's declared Outputs satisfy the next step's required Inputs.
