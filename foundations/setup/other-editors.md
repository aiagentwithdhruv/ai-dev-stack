# Other editors — same rules, different file

The rule corpus in [`../../rules/`](../../rules/) and [`../../claude/CLAUDE.md`](../../claude/CLAUDE.md) is plain markdown. That portability is the point: almost every AI coding tool loads a project-level instruction file, only the **name and location** differ. Pick the row for your editor, drop the same content in, done.

## Drop-in map

| Editor / assistant | File it loads | Where it goes | Notes |
|--------------------|---------------|---------------|-------|
| **Windsurf** | `.windsurfrules` (or `.windsurf/rules/*.md`) | Project root | Single-file form takes the combined `CLAUDE.md`. The folder form mirrors the numbered `.mdc` split — drop the rule bodies, the frontmatter is ignored. |
| **Cline** | `.clinerules` (file) or `.clinerules/*.md` (folder) | Project root | Folder form lets you keep one file per rule, same numbering as `../../rules/`. |
| **GitHub Copilot** | `.github/copilot-instructions.md` | `.github/` | One file only. Use the combined `CLAUDE.md`. Keep it tight — long instruction files get truncated in some surfaces. |
| **Gemini-based assistants** | `GEMINI.md` (CLI) / settings "custom instructions" (IDE) | Project root or settings | CLI reads a root markdown file much like Claude Code; IDE plugins paste the same body into a settings field. |
| **Generic / unknown tool** | whatever its docs name | Project root | If it loads a markdown instruction file at all, give it `CLAUDE.md`. |

## The one transformation that matters

Cursor `.mdc` files carry YAML frontmatter:

```yaml
---
description: Global default behavior for the entire repository
alwaysApply: true
---
```

Every other editor on this page ignores or rejects frontmatter. When you port a rule out of `../../rules/`, **strip the `---` block** and keep the body. That's the only edit. The combined `CLAUDE.md` is already frontmatter-free, so for single-file editors just copy it as-is.

## Keep one source of truth

Do not hand-maintain five divergent rule files. Pick the rule corpus as canonical (the `.mdc` set or `CLAUDE.md`), and render the others from it:

- **Single-file editors** (Copilot, Windsurf single-file, Gemini): symlink or copy `CLAUDE.md` to the editor's filename.
- **Folder editors** (Cline, Windsurf folder form): copy the rule bodies, frontmatter stripped.

A small generation step beats silent drift. When the rules change, regenerate — never edit the rendered copies by hand.

## Verify per editor

Same discipline as the [setup checklist](./README.md#verify-the-install): an unloaded rule file is worse than none.

- [ ] The file is at the **exact** path the editor documents — a near-miss path loads nothing, silently.
- [ ] Frontmatter stripped for every non-Cursor target.
- [ ] Ask the assistant to restate its active rules and confirm it echoes them.
- [ ] If the tool has a context/rules inspector panel, confirm the file shows as loaded.

## How to use

1. Find your editor in the drop-in map.
2. Copy the combined `CLAUDE.md` (or the folder-split rules) to the named path, stripping frontmatter where required.
3. Wire a one-line copy/symlink so the rendered file stays downstream of the canonical corpus.
4. Run the per-editor verify checklist before you rely on it.
