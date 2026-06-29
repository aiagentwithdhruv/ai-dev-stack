#!/usr/bin/env bash
# Command Center safe regenerator.
# Backs up current HTML, generates to temp, validates size delta,
# promotes if safe, prunes old backups.
#
# Usage: ./regen.sh [--output PATH]
#
# Safety rules:
#   - Aborts if new HTML would be >20% smaller than existing HTML.
#   - Keeps last 10 backups, auto-prunes oldest.
#   - Never overwrites with an empty or tiny file.

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
YAML="$HERE/data/tasks.yaml"
BACKUP_DIR="$HERE/backups"
TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)

# Read slug from tasks.yaml to build output filename.
# Requires python3 (already a dependency of generate.py).
if [ -f "$YAML" ]; then
  SLUG=$(python3 -c "
import yaml, sys
try:
    d = yaml.safe_load(open('$YAML'))
    print(d.get('meta', {}).get('slug', 'PROJECT'))
except Exception as e:
    print('PROJECT')
" 2>/dev/null || echo "PROJECT")
else
  echo "ERROR: $YAML not found. Cannot determine output filename." >&2
  exit 1
fi

OUTPUT="${1:-$HOME/Downloads/${SLUG}-COMMAND-CENTER.html}"
NEW_TMP="/tmp/${SLUG}-COMMAND-CENTER.new.${TIMESTAMP}.html"

mkdir -p "$BACKUP_DIR"

# 1. Capture pre-state
OLD_SIZE=0
OLD_LINES=0
if [ -f "$OUTPUT" ]; then
  OLD_SIZE=$(stat -f%z "$OUTPUT" 2>/dev/null || stat -c%s "$OUTPUT" 2>/dev/null || echo 0)
  OLD_LINES=$(wc -l < "$OUTPUT" 2>/dev/null || echo 0)
fi

# 2. Backup current HTML (if it exists)
if [ -f "$OUTPUT" ] && [ "$OLD_SIZE" -gt 0 ]; then
  cp "$OUTPUT" "$BACKUP_DIR/${SLUG}-COMMAND-CENTER.${TIMESTAMP}.html"
  echo "Backup: $BACKUP_DIR/${SLUG}-COMMAND-CENTER.${TIMESTAMP}.html"
fi

# 3. Generate to temp
python3 "$HERE/generate.py" --output "$NEW_TMP"

# 4. Validate
NEW_SIZE=$(stat -f%z "$NEW_TMP" 2>/dev/null || stat -c%s "$NEW_TMP" 2>/dev/null || echo 0)
NEW_LINES=$(wc -l < "$NEW_TMP" 2>/dev/null || echo 0)

if [ "$NEW_SIZE" -eq 0 ]; then
  echo "ABORT: generator produced an empty file." >&2
  rm -f "$NEW_TMP"
  exit 1
fi

if [ "$OLD_SIZE" -gt 0 ]; then
  # Integer arithmetic: (old - new) * 100 / old = shrink percentage
  SIZE_DROP=$(( (OLD_SIZE - NEW_SIZE) * 100 / OLD_SIZE ))
  if [ "$SIZE_DROP" -gt 20 ]; then
    echo "ABORT: new HTML is ${SIZE_DROP}% smaller than existing." >&2
    echo "  Old: ${OLD_LINES} lines / ${OLD_SIZE} bytes" >&2
    echo "  New: ${NEW_LINES} lines / ${NEW_SIZE} bytes" >&2
    echo "  Suspect: a module was removed from $YAML" >&2
    echo "  Inspect the rejected file: $NEW_TMP" >&2
    exit 1
  fi
fi

# 5. Promote temp to output
mv "$NEW_TMP" "$OUTPUT"

# 6. Prune — keep last 10 backups
if [ -d "$BACKUP_DIR" ]; then
  ls -t "$BACKUP_DIR"/*.html 2>/dev/null | tail -n +11 | xargs rm -f 2>/dev/null || true
fi

# 7. Report
DELTA_LINES=$(( NEW_LINES - OLD_LINES ))
DELTA_SIGN=""
[ "$DELTA_LINES" -gt 0 ] && DELTA_SIGN="+"
echo "Generated: $OUTPUT"
echo "  ${OLD_LINES} -> ${NEW_LINES} lines (${DELTA_SIGN}${DELTA_LINES})"
echo "  ${OLD_SIZE} -> ${NEW_SIZE} bytes"
