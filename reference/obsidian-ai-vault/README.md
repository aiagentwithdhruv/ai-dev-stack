# Obsidian Knowledge Vault for AI Developers (PARA + Claude Code via MCP)

A local-first, plain-Markdown knowledge base that Claude Code can search, read,
and write over MCP. Instead of the assistant starting cold every session, it
reasons over your whole vault — projects, clients, skills, research, and memory.

> The idea: **one vault, everything linked, AI reads it all.** Code that lives
> next to your knowledge beats an assistant that forgets everything between chats.

## Why a local Markdown vault

| Property | Why it matters |
|----------|----------------|
| Local-first | Your files, your disk. Works offline. No vendor lock-in. |
| Plain `.md` | Greppable, diffable, future-proof. Any tool can read it. |
| Git-backed | Full version history; recover anything. |
| AI-connected | Claude Code reaches it over MCP and reasons across notes. |
| Graph + backlinks | Knowledge connects instead of siloing in folders. |

## Folder structure (PARA method)

PARA = Projects, Areas, Resources, Archive (Tiago Forte). A flat, proven layout.

```
vault/
├── 00-Inbox/        # Quick capture — dump ideas, process later
├── 01-Projects/     # Time-bound goals (build X by Y date)
├── 02-Areas/        # Ongoing responsibilities
│   ├── Clients/     # One note per client (CRM)
│   ├── Revenue/     # Pricing, proposals, pipeline
│   └── Content/     # Content calendar & ideas
├── 03-Resources/    # Reference material
│   ├── Skills/      # Reusable automation patterns
│   ├── Agents/      # AI sub-agent definitions
│   └── Research/    # Deep research notes
├── 04-Archive/      # Done / inactive
├── Context/         # AI context files (CLAUDE.md, brand, preferences)
├── Memory/          # Persistent AI memory across sessions
├── Templates/       # Note templates (see templates/)
└── Dashboard/       # Dataview dashboards (see dashboards/)
```

`Inbox` is the only entry point — capture fast, then file each item into a
Project, Area, Resource, or Archive.

## Connect Claude Code over MCP

1. Install an Obsidian MCP server (any maintained one works), e.g.:
   ```bash
   npm install -g obsidian-mcp
   ```
2. Register it in your Claude Code project's MCP config
   (`.claude/mcp_servers.json` or `settings.json`):
   ```json
   {
     "mcpServers": {
       "vault": {
         "command": "obsidian-mcp",
         "args": ["/absolute/path/to/your/vault"]
       }
     }
   }
   ```
3. (Optional) Add a maintained Obsidian skill so the assistant writes
   Obsidian-flavored Markdown correctly (frontmatter, `[[wikilinks]]`, callouts).

Once wired, you can ask naturally:

- "Search my vault for everything about lead generation."
- "Create a client note for Acme Corp, $5000 project."
- "What skills do I have for email automation?"
- "Update today's daily note with these wins."

```
  ┌──────────────── VAULT ────────────────┐
  │  Skills · Clients · Projects · Memory  │
  │  Context · Research   ┌─────────┐      │
  │                       │  Graph  │      │
  └───────────────────────┴────┬────┘──────┘
                               │ MCP
                               ▼
                  ┌────────────────────────┐
                  │      CLAUDE CODE       │
                  │  read · write · search │
                  └────────────────────────┘
```

## Recommended plugins

| Plugin | Purpose |
|--------|---------|
| Dataview | Query the vault like a database — powers every dashboard here |
| Templater | Templates with date math and logic |
| Tasks | Due dates and task filters |
| Kanban | Visual pipeline boards (clients, projects) |
| Calendar | Daily notes / content calendar |
| Git | Auto-backup the vault to a remote |
| Smart Connections *(optional)* | Local semantic search across notes |

## How to use the included files

- **Templates** (`templates/`): six starting points. Pair with Templater so
  `{{title}}` / `{{date:YYYY-MM-DD}}` placeholders fill automatically.
- **Dashboards** (`dashboards/`): drop into `Dashboard/`; they query the folders
  above via Dataview. Start at `Home.md`.

## Daily loop

1. Capture into `00-Inbox` all day.
2. Once a day, file inbox items into Projects / Areas / Resources / Archive.
3. Create a daily note (template) — tasks, wins, tomorrow.
4. Let Claude Code query and update the vault as you work.
