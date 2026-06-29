#!/bin/bash
# Install ai-dev-stack into your project
# Usage: curl -fsSL https://raw.githubusercontent.com/aiagentwithdhruv/ai-dev-stack/main/install.sh | bash

set -e

REPO="https://github.com/aiagentwithdhruv/ai-dev-stack.git"
RULES_DIR=".cursor/rules"
DOCS_DIR="docs"
TEMP_DIR=$(mktemp -d)

echo "Installing ai-dev-stack..."
echo ""

# Clone repo
git clone --depth 1 "$REPO" "$TEMP_DIR" 2>/dev/null

# Create directories
mkdir -p "$RULES_DIR"
mkdir -p "$DOCS_DIR"

# Copy Cursor rules
cp "$TEMP_DIR/rules/"*.mdc "$RULES_DIR/"

# Copy Claude Code instructions
if [ ! -f "CLAUDE.md" ]; then
  cp "$TEMP_DIR/claude/CLAUDE.md" "CLAUDE.md"
  echo "  Created CLAUDE.md"
else
  echo "  Skipped CLAUDE.md (already exists)"
fi

# Copy docs (don't overwrite existing)
for doc in PRD.md ARCHITECTURE.md API_SPEC.md DB_SCHEMA.md DEPLOYMENT.md SKILLS.md AGENTS.md LOADOUT.md MCP.md; do
  if [ -f "$TEMP_DIR/docs/$doc" ] && [ ! -f "$DOCS_DIR/$doc" ]; then
    cp "$TEMP_DIR/docs/$doc" "$DOCS_DIR/$doc"
  fi
done

# Cleanup
rm -rf "$TEMP_DIR"

RULE_COUNT=$(ls -1 "$RULES_DIR"/*.mdc 2>/dev/null | wc -l | tr -d ' ')
DOC_COUNT=$(ls -1 "$DOCS_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ')

echo ""
echo "  $RULE_COUNT rules  → $RULES_DIR/"
echo "  $DOC_COUNT docs    → $DOCS_DIR/"
echo "  CLAUDE.md → project root"
echo ""
echo "Next steps:"
echo "  1. Edit docs/ with your product details"
echo "  2. Open Cursor or Claude Code — rules are active"
echo ""
echo "Done."
