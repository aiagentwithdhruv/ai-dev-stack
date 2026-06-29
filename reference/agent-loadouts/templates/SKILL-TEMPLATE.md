# {System Name} — AI Skill Context

> Everything an AI agent needs to work on, improve, or extend this system.
> Includes: architecture, codebase map, domain knowledge, technical recipes, and best practices.

---

## System Identity

**What:** {One-line description}
**Who:** {Target users / company}
**Status:** {BUILT / IN DEVELOPMENT / DEPLOYED}
**Blockers:** {Current blockers, if any}

---

## Architecture

```
{ASCII diagram showing:
- Frontend (framework, port)
- Backend (framework, port)
- Database (type, key tables)
- External services (APIs, CRM, etc.)
- Data flow arrows}
```

---

## Codebase Map

### {Layer} (`path/`)

| File | What It Does |
|------|-------------|
| `{file}` | {description} |

<!-- Repeat for each layer: core, routes, services, agents, frontend, database -->

---

## Known Issues & Tech Debt

| Issue | Severity | Fix |
|-------|----------|-----|
| {issue} | {High/Medium/Low/Cosmetic} | {known fix or workaround} |

---

## Domain Knowledge

<!-- Link to knowledge/ files or include key domain info inline -->

### {Topic 1}
{Key facts, formulas, or patterns the AI needs to know}

### {Topic 2}
{Key facts, formulas, or patterns}

---

## Technical Recipes

### {Recipe 1: Common Pattern}
```{language}
{Code snippet or configuration that's reusable}
```

### {Recipe 2: Integration Pattern}
```{language}
{Code snippet}
```

---

## Next Steps (Prioritized)

### Phase 1: {Name} (Week 1-2)
1. {Step}
2. {Step}

### Phase 2: {Name} (Week 3-4)
3. {Step}
4. {Step}

---

## Schema

> Typed schema for programmatic discovery and composition.
> This section is required for all skills. Used by the Loadout MCP Server and CLI.

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `{param_name}` | string/integer/boolean/array/object/file_path | Yes/No | {What this parameter does} |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `{output_name}` | string/file_path/array/boolean | {What this output contains} |

### Credentials
| Name | Source |
|------|--------|
| `{ENV_VAR_NAME}` | .env / file / dashboard / secrets manager |

### Composable With
Skills that chain well with this one: `{skill-1}`, `{skill-2}`

### Cost
{Free / $X per run / API credits}

---

## Self-Update Rules

### After Every Coding Session
1. If you fixed a bug → add to Known Issues with fix description
2. If you added an endpoint → update Codebase Map
3. If you changed architecture → update Architecture diagram
4. If you discovered a pattern → add to Technical Recipes

### After Every Deployment
1. Update status from development → deployed
2. Update blockers (remove resolved, add new)
3. Update LOADOUT.md changelog

### Cross-File Updates
When updating this file, also check:
- `../LOADOUT.md` — version, changelog
- `../.claude/CLAUDE.md` — if architecture changed
- `../knowledge/*.md` — if domain info changed
