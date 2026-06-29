# Source: Obsidian AI Knowledge Vault (PARA + Claude Code via MCP)

**Origin:** Adapted from a public Obsidian vault template repo (a GitHub
"Use this template" starter). Sanitized and made vendor/employer-neutral for
inclusion in this kit.

**What this folds into the flagship:** The flagship covers AI *engineering*
(prompting, RAG, agents, deploy, evals). It has generic MCP-server docs
(`docs/MCP.md`) but nothing on using a **local knowledge vault as Claude Code's
long-term memory**. This reference adds that missing piece: a plain-Markdown,
local-first knowledge base, organized with the PARA method, that Claude Code
reads and writes over MCP so the assistant "thinks with" your whole knowledge
base instead of starting cold every session.

## What's here

| File | What it is |
|------|-----------|
| `README.md` | The pattern: why a local Markdown vault, PARA layout, Claude Code MCP wiring, recommended plugins. Vendor-neutral. |
| `templates/` | 6 reusable Obsidian note templates (Client, Project, Daily Note, Skill, Meeting, Research). Plain frontmatter + headings — drop-in. |
| `dashboards/` | 4 Dataview-powered dashboards (Home, Client Pipeline, Skills Index, Projects Map). Live queries over the vault. |

## What was deliberately NOT folded (leak-safety)

- The original author's name, brand handle, and YouTube/LinkedIn links from the
  README "Built By" block.
- Two research notes from the source vault (an "AI landscape snapshot" and a
  personal philosophy note). Both were dropped: the landscape note is a
  time-stamped snapshot that goes stale and overlaps the kit's existing
  model/pricing material, and both contained personal/project-specific
  references (specific side projects, private workflow counts, named third-party
  MCP integrations). Generic templates + the pattern are the durable, reusable
  IP; the notes were not.
