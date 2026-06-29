# Memory vs Context — Persistent Recall Across Sessions

Without memory, every AI session starts from zero. With memory, the assistant
recalls what happened yesterday, last week, last month. This is the piece most
loadouts miss.

## The distinction

| | Context | Memory |
|---|---------|--------|
| What it is | Who you are and what you're working on **now** | What **happened** in past sessions |
| Changes | Weekly (priorities) to quarterly (stack) | Every session (new entries appended) |
| Format | Structured template, fixed sections | Chronological log of events and decisions |
| Size | Stays small (trim old projects) | Grows over time (organize by topic) |
| Analogy | Your resume (current state) | Your journal (history of what happened) |
| File | `context/CONTEXT.md` | `memory/MEMORY.md` |

## What to save in memory

Save things you'll need to recall in future sessions — decisions, outcomes, and
hard-won knowledge.

| Category | Example |
|----------|---------|
| Decisions and why | "Chose Postgres-backed auth over a 3rd-party SaaS because we need row-level security and SQL queries." |
| Problems solved | "Fixed CORS by adding `credentials: 'include'` on the client AND `allow_credentials=True` in middleware." |
| Architecture choices | "API uses path-based routing behind a load balancer. Frontend must use relative URLs, not a hardcoded host." |
| Things that broke | "Webhook stopped working after redeploy because the platform reassigned the port. Fixed by reading `$PORT`." |
| Key numbers | "Launch: 47 signups, 12 activated, 3 pilots. Activation rate 25%." |
| Conventions established | "All migrations go through the CLI, never the dashboard UI." |
| Milestones | "First paying customer signed after a 15-minute demo." |

## What NOT to save

| Don't save | Why | Where it goes instead |
|------------|-----|----------------------|
| Generic knowledge | The model already knows how hooks work | Nowhere — it's built-in |
| Temporary notes | "Call X at 3pm" | Calendar / todo app |
| Secrets and credentials | Security risk if shared/committed | Secret manager / vault |
| Opinions and speculation | Memory should be facts | Personal notes |
| Duplicate of context | Don't repeat what's in CONTEXT.md | `context/CONTEXT.md` |
| Entire code files | Memory is for decisions about code, not code | The source files |
| Step-by-step procedures | These belong in skills | `skills/<name>/SKILL.md` |

## Entry format

Every entry answers: **what happened, when, and why it matters for future sessions.**

```markdown
## Topic Name (Date)
- **What:** Brief description of what happened
- **Decision:** What was decided (if applicable)
- **Why:** The reasoning behind it
- **Key detail:** The specific technical thing to remember
- **Files:** Relevant file paths (if applicable)
- **Status:** Current state (if ongoing)
```

Compact form for quick entries:

```markdown
## Topic (Date)
- One-liner about what happened. Key detail: the specific thing. Files: `path/to/file`
```

### Example entries (illustrative)

```markdown
## Auth Migration (Date)
- **What:** Moved from custom JWT to a managed auth flow
- **Why:** Custom JWT had session-refresh bugs on mobile
- **Key detail:** Must enable auto-refresh + persist-session in the client config
- **Files:** `src/lib/auth.ts`, `src/middleware.ts`

## Port Bug (Date)
- **What:** Webhook returned 502 after a redeploy
- **Root cause:** Platform assigns a dynamic port; config was hardcoded
- **Fix:** Read `process.env.PORT`; never hardcode the port
```

## Organizing memory

- **Single file** for most projects: one `MEMORY.md`, sections by topic with a
  "Last updated" date per section.
- **Split by domain** once it passes ~500 lines:

```
memory/
  MEMORY.md                  # recent, cross-cutting
  deployment-notes.md
  architecture-decisions.md
  bug-fixes.md
```

Reference the split files from the main `MEMORY.md` with a one-line pointer + the
most recent fact.

## Searching memory

```bash
grep -i "authentication" memory/MEMORY.md      # by topic
grep -ri "postgres" memory/                    # across all memory files
```

Or just ask the assistant: "Check memory — what did we decide about auth?"

## Maintaining it over time

**Add** after: solving a hard problem, a significant decision, a deployment that
went sideways, establishing a convention, hitting a milestone.

**Clean up:** split at ~500 lines; move dead projects to an Archive section at the
bottom; when entries contradict, keep the latest and delete the old; skim quarterly.

```markdown
## Archive (No Longer Active)
### Old Project (Killed Date)
- Built X. Killed because Y. Lesson: validate Z before building.
```

### Loading memory in different tools

- **Claude Code:** has a built-in memory file auto-loaded per project; you can also
  keep `memory/MEMORY.md` in the repo.
- **Other IDE assistants:** add a rule like "Read `memory/MEMORY.md` at the start of
  every session."
- **Chat-only tools:** upload `memory/MEMORY.md` as a project file, or paste the
  relevant section into the conversation.

> Chat logs are noisy — 95% is exploration and false starts. Memory is the distilled
> 5% that matters for future work.
