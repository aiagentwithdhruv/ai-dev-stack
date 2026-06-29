---
name: your-loadout-name
version: 0.1.0
description: One-line description of what this loadout equips an AI agent to do
author: YourName
license: proprietary  # or MIT, Apache-2.0
tier: free  # free | premium | enterprise
last_verified: YYYY-MM-DD
refresh_cadence: monthly  # monthly | quarterly | yearly
dependencies: []  # other loadouts required
platforms: [claude-code]  # claude-code, cursor, codex, openai, etc.
---

# {Loadout Name} — Agent Loadout

> One paragraph describing what this loadout does and who it's for.

---

## What's Included

| File | Type | Purpose |
|------|------|---------|
| `.claude/CLAUDE.md` | Context | Auto-loaded master context |
| `skills/*/SKILL.md` | Skill | Specialized skill files |
| `knowledge/*.md` | Knowledge | Domain knowledge files |
| `runbooks/*.md` | Runbook | Step-by-step procedures |
| `tests/*.md` | Tests | Validation test cases |
<!-- Add all files in this loadout -->

---

## Quick Start

### For Claude Code
1. Open this folder as project root
2. `.claude/CLAUDE.md` auto-loads — agent has full context
3. For specific tasks, agent reads relevant `skills/` or `runbooks/`

### For Cursor
1. Copy CLAUDE.md into `.cursor/rules/context.mdc`
2. Add knowledge files as additional context

### For Any AI Agent
1. Feed CLAUDE.md as system prompt
2. Feed relevant knowledge files for domain expertise

### Via MCP Server
1. Add to Claude Desktop / Cursor MCP config:
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
2. Use tools: `list_loadouts`, `get_skill`, `search_skills`, `get_routing`

### Via CLI
```bash
python3 loadouts/tools/loadout_cli.py verify .
python3 loadouts/tools/loadout_cli.py doctor
```

---

## Self-Update Schedule

| Component | Refresh | How | Last Verified |
|-----------|---------|-----|---------------|
| Core context | Monthly | Review for accuracy | YYYY-MM-DD |
| Market data | Quarterly | Web search for updates | YYYY-MM-DD |
| Credentials | On failure | Test and update | YYYY-MM-DD |
<!-- Add all components that need refreshing -->

---

## Changelog

### v0.1.0 (YYYY-MM-DD)
- Initial loadout creation
- List what's included
