# Setup — get the rules into your editor

The fastest way to make an AI coding tool behave like a senior engineer is to give it the rules before it writes a line. This page is the install path. It does not redefine the rules — the canonical rule files already live in this kit, and this page points you at them.

## Canonical sources (do not duplicate these)

| What | Where | Read by |
|------|-------|---------|
| Combined rule file | [`../../claude/CLAUDE.md`](../../claude/CLAUDE.md) | Claude Code (loaded from project root) |
| Per-rule composer | [`../../claude/compose.sh`](../../claude/compose.sh) | You — build a custom `CLAUDE.md` |
| Permission template | [`../../claude/.claude/settings.json`](../../claude/.claude/settings.json) | Claude Code (tool permissions) |
| Individual rule files | [`../../rules/`](../../rules/) | Cursor (`.mdc` with frontmatter) |

One rule corpus, two surface formats: Cursor reads the numbered `.mdc` files; Claude Code reads `CLAUDE.md`. Same content, no conflict. Keep them in sync by editing the rule source, not the rendered copy.

## One-line install recap

From a cloned copy of this kit:

```bash
# Cursor — runs the installer, drops the .mdc rules into .cursor/rules/
bash install.sh

# Claude Code — copy the combined rule file to your project root
cp claude/CLAUDE.md ~/your-project/CLAUDE.md
```

Run both in the same project — zero conflict. The network one-liner (a single `curl … | bash`) and the canonical repo URLs live in the [root README](../../README.md) quick-start — use that as the source of truth so this page never drifts from it.

## Compose only what you need

Most projects don't want all 15 rules. Use the composer to assemble a focused `CLAUDE.md`:

```bash
cd ../../claude
./compose.sh 00 10 30 70 80 99 > ~/project/CLAUDE.md    # backend only
./compose.sh 00 20 70 80 99    > ~/project/CLAUDE.md    # frontend only
./compose.sh 00 50 55 60 70 99 > ~/project/CLAUDE.md    # AI/ML only
./compose.sh                   > ~/project/CLAUDE.md    # everything
```

Rule `00` (Global Architect) belongs in every build — it sets the architect-first default and auto-references your `docs/`.

## Verify the install

A rules install is only real if the tool actually loads it. Confirm before you trust it:

- [ ] **Cursor** — open Settings → Rules and confirm the `.mdc` files appear under project rules.
- [ ] **Claude Code** — `CLAUDE.md` sits at the project root (or the directory you launch from). Ask the model "what rules are you following?" and check it echoes them back.
- [ ] **Permissions** — if you copied `settings.json`, confirm the allowed/denied tool lists match your intent before running anything destructive.
- [ ] **Docs present** — rule `00` references [`../../docs/`](../../docs/) (PRD, architecture, API spec, DB schema). Stub these even briefly so the model has a contract to align to.

## Other editors

Windsurf, Cline, GitHub Copilot, and Gemini-based assistants take the same rule corpus with a different file name and location. See **[other-editors.md](./other-editors.md)** for the per-editor drop-in mapping.

## How to use

1. Install once per project (the two curl lines above).
2. Compose a focused `CLAUDE.md` if the full set is too broad.
3. Run the verify checklist — an unloaded rule file is worse than none, because you'll assume coverage you don't have.
4. Stub the [`../../docs/`](../../docs/) templates so the architect rule has something to anchor on.
