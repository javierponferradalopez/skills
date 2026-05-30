#!/usr/bin/env bash
#
# Install the Claude Code harness into ~/.claude/.
#
# Properties:
#   - Idempotent: re-running is safe.
#   - Non-destructive: extends rather than replaces. If a skill/agent
#     with the same name already exists, it is skipped (your version wins).
#   - For CLAUDE.md: if it already exists, prepends an
#     @WORK_PHILOSOPHY.md import line so the harness's philosophy is
#     loaded alongside whatever you already had.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$SCRIPT_DIR"
TARGET_DIR="$HOME/.claude"
IMPORT_LINE="@WORK_PHILOSOPHY.md"

if [[ ! -d "$PACKAGE_DIR/skills" ]]; then
    echo "error: package skills/ not found at $PACKAGE_DIR" >&2
    exit 1
fi

step() { printf "\n\033[1;34m==>\033[0m %s\n" "$1"; }
ok()   { printf "  \033[0;32m✓\033[0m %s\n" "$1"; }
skip() { printf "  \033[0;33m⊘\033[0m %s\n" "$1"; }
warn() { printf "  \033[0;33m!\033[0m %s\n" "$1"; }

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
mkdir -p "$TARGET_DIR/skills" "$TARGET_DIR/agents" "$TARGET_DIR/commands"
ok "$TARGET_DIR"

step "Installing WORK_PHILOSOPHY.md"
link_if_safe "$PACKAGE_DIR/WORK_PHILOSOPHY.md" "$TARGET_DIR/WORK_PHILOSOPHY.md" "WORK_PHILOSOPHY.md"

step "Ensuring ~/.claude/CLAUDE.md imports $IMPORT_LINE"
CLAUDE_MD="$TARGET_DIR/CLAUDE.md"
if [[ ! -e "$CLAUDE_MD" && ! -L "$CLAUDE_MD" ]]; then
    printf '%s\n' "$IMPORT_LINE" > "$CLAUDE_MD"
    ok "Created CLAUDE.md with $IMPORT_LINE"
elif [[ -L "$CLAUDE_MD" ]]; then
    warn "CLAUDE.md is a symlink; not touching. Ensure its target imports $IMPORT_LINE."
elif grep -qxF "$IMPORT_LINE" "$CLAUDE_MD"; then
    ok "CLAUDE.md already imports WORK_PHILOSOPHY.md"
else
    tmp="$(mktemp)"
    printf '%s\n\n' "$IMPORT_LINE" > "$tmp"
    cat "$CLAUDE_MD" >> "$tmp"
    mv "$tmp" "$CLAUDE_MD"
    ok "Prepended $IMPORT_LINE to existing CLAUDE.md"
fi

step "Installing skills"
# Claude Code requires a flat layout: ~/.claude/skills/<name>/SKILL.md.
# Each folder under skills/ here is one skill (with SKILL.md). Skill names
# are intent-based (no category prefixes).
if [[ -d "$PACKAGE_DIR/skills" ]]; then
    for skill_dir in "$PACKAGE_DIR/skills"/*/; do
        [[ -d "$skill_dir" ]] || continue
        [[ -f "${skill_dir}SKILL.md" ]] || continue
        skill_name="$(basename "$skill_dir")"
        link_if_safe "${skill_dir%/}" "$TARGET_DIR/skills/$skill_name" "skills/$skill_name"
    done
fi

step "Installing agents"
if [[ -d "$PACKAGE_DIR/agents" ]]; then
    for agent_file in "$PACKAGE_DIR/agents"/*.md; do
        [[ -f "$agent_file" ]] || continue
        agent_name="$(basename "$agent_file")"
        link_if_safe "$agent_file" "$TARGET_DIR/agents/$agent_name" "agents/$agent_name"
    done
fi

step "Installing commands"
# Slash commands live flat at ~/.claude/commands/<name>.md and are invoked as
# /<name>. Each .md here is one command.
if [[ -d "$PACKAGE_DIR/commands" ]]; then
    for command_file in "$PACKAGE_DIR/commands"/*.md; do
        [[ -f "$command_file" ]] || continue
        command_name="$(basename "$command_file")"
        link_if_safe "$command_file" "$TARGET_DIR/commands/$command_name" "commands/$command_name"
    done
fi

step "Done."
echo
echo "Next steps:"
echo "  - Open a new Claude Code session for the skills to be discovered."
echo "  - Review ~/.claude/CLAUDE.md if you had personal content there."
