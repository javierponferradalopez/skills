#!/usr/bin/env bash
#
# Install the Claude Code harness into ~/.claude/.
#
# Properties:
#   - Idempotent: re-running is safe.
#   - Non-destructive: extends rather than replaces. If a skill
#     with the same name already exists, it is skipped (your version wins).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$SCRIPT_DIR"
TARGET_DIR="$HOME/.claude"

if [[ ! -d "$PACKAGE_DIR/skills" ]]; then
    echo "error: package skills/ not found at $PACKAGE_DIR" >&2
    exit 1
fi

step() { printf "\n\033[1;34m==>\033[0m %s\n" "$1"; }
ok()   { printf "  \033[0;32m✓\033[0m %s\n" "$1"; }
skip() { printf "  \033[0;33m⊘\033[0m %s\n" "$1"; }

link_if_safe() {
    local src="$1" target="$2" label="$3"
    if [[ -L "$target" ]]; then
        local current
        current="$(readlink "$target")"
        if [[ "$current" == "$src" ]]; then
            ok "$label (already linked)"
        else
            skip "$label (points elsewhere: $current)"
        fi
    elif [[ -e "$target" ]]; then
        skip "$label (exists, not a symlink — your version wins)"
    else
        ln -s "$src" "$target"
        ok "$label"
    fi
}

step "Ensuring ~/.claude/ structure"
mkdir -p "$TARGET_DIR/skills"
ok "$TARGET_DIR"

step "Installing skills"
# In this repo skills are organized into category folders for browsing:
#   skills/<category>/<name>/SKILL.md   (e.g. skills/engineer/tdd/SKILL.md).
# Claude Code requires a FLAT layout, so we flatten the categories away and
# link every skill into ~/.claude/skills/<name>/. Categories are purely an
# authoring convenience and never reach the install target. Skill names are
# intent-based (no category prefixes), so they stay unique across categories.
if [[ -d "$PACKAGE_DIR/skills" ]]; then
    for skill_md in "$PACKAGE_DIR/skills"/*/*/SKILL.md; do
        [[ -f "$skill_md" ]] || continue
        skill_dir="$(dirname "$skill_md")"
        skill_name="$(basename "$skill_dir")"
        category="$(basename "$(dirname "$skill_dir")")"
        link_if_safe "$skill_dir" "$TARGET_DIR/skills/$skill_name" "$category/$skill_name"
    done
fi

step "Done."
echo
echo "Next steps:"
echo "  - Open a new Claude Code session for the skills to be discovered."
