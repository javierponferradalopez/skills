# Personal Development Harness

A set of independent Claude Code skills, commands, and subagents that turn vague tasks into shipped code with a disciplined, conscious workflow. No vibe coding.

The harness lives in `~/.claude/`. The only thing it ever writes to disk is a handoff document, under `~/harness/<project-slug>/<task-id>/handoff.md`, so client repositories stay completely clean.

> Working philosophy lives in [`WORK_PHILOSOPHY.md`](./WORK_PHILOSOPHY.md).
> See [Why `WORK_PHILOSOPHY.md` instead of `CLAUDE.md`](#why-work_philosophymd-instead-of-claudemd).

---

## Installation

From the root of this repo:

```bash
./install.sh
```

The script is **non-destructive and idempotent**:

| Situation | Behavior |
|---|---|
| Empty `~/.claude/` | Symlinks everything cleanly. Creates `CLAUDE.md` with `@WORK_PHILOSOPHY.md`. |
| You already have `~/.claude/CLAUDE.md` | Prepends `@WORK_PHILOSOPHY.md` to it. Your existing content stays intact. |
| You already have a skill/command/agent with the same name | Skips it with a log line. Your version wins. |
| You have skills in unrelated categories | They coexist — the script only touches paths inside this package. |
| Re-running the script | Detects what's already linked; no duplicates, no errors. |

Personal state (`memory/`, `projects/`, `todos/`, `sessions/`, credentials, local settings) is never touched: the script only creates symlinks for the files in this package.

### Uninstall

The script doesn't ship an uninstaller. To remove the harness:

```bash
# Remove the harness symlinks; your real files and other skills stay.
find ~/.claude -maxdepth 2 -type l -lname "*/skills/*" -delete
# Optionally remove the import line from CLAUDE.md
sed -i '' '/^@WORK_PHILOSOPHY\.md$/d' ~/.claude/CLAUDE.md
```

---

## Why `WORK_PHILOSOPHY.md` instead of `CLAUDE.md`?

Claude Code loads `~/.claude/CLAUDE.md` as the **global instructions for every session**. If this package shipped its own `CLAUDE.md`, installing it would either overwrite yours or refuse to install.

Instead:

- The harness's philosophy ships as [`WORK_PHILOSOPHY.md`](./WORK_PHILOSOPHY.md).
- The installer ensures your `~/.claude/CLAUDE.md` imports it with a single line: `@WORK_PHILOSOPHY.md`.
- Your `CLAUDE.md` stays yours — add personal rules above or below the import, mix in other imports (`@other-file.md`), comment the line out to temporarily disable the harness.

This way the harness's rules come along for the ride without conflicting with whatever you already had.

---

## Stateless skills, conversational orchestration

Skills are independent units invoked by intent. They live in the conversation: each one executes its single procedure and stops. No skill requires any prior file to exist, none reads files left by other skills, none writes files of its own.

When a skill produces a reusable artifact (a plan, a list of subtasks, a verification summary), it **asks the user where to deposit it** — the project's task manager, a local markdown, the original ticket, or just-conversation. The skill does not decide where things go.

The single point of persistence is the `/handoff` command, which collapses the current task into a markdown when the user asks for it.

The agent in the conversation (with the user) decides which skill to invoke next — never hardcoded inside a skill. Skills must not suggest "next, run skill X" nor "skip if Y". Those decisions belong to the conversation.

---

## Skill catalog

> Skills live flat at `~/.claude/skills/<name>/` (Claude Code requirement). Names are **intent-based**, no category prefixes.

| Skill | Use when |
|---|---|
| [`ingest`](./skills/ingest/SKILL.md) | Capturing a task from any source (ClickUp/Linear/Jira ticket, email, voice notes, free-form) into a normalized block in the conversation. |
| [`grill`](./skills/grill/SKILL.md) | Interrogating an idea until every ambiguity is resolved — corner cases, implicit assumptions, conflicts with what exists. |
| [`plan`](./skills/plan/SKILL.md) | Producing a structured technical plan — affected modules, decisions, risks, side effects, rough effort. |
| [`subtasks`](./skills/subtasks/SKILL.md) | Splitting a plan into vertical, independently-closable slices. |
| [`verify`](./skills/verify/SKILL.md) | Comparing delivered work against acceptance criteria, leaving technical debt explicit, producing a PR-ready summary. |
| [`diagnose`](./skills/diagnose/SKILL.md) | Hard bugs, unclear regressions, perf problems: reproduce → minimise → hypothesise → instrument → fix → regression-test. |
| [`write-adr`](./skills/write-adr/SKILL.md) | A non-trivial, hard-to-reverse technical decision deserves a lightweight ADR. |
| [`write-a-skill`](./skills/write-a-skill/SKILL.md) | Adding, writing, or reworking a harness skill; formalizing a procedure you keep repeating by hand. |

### Commands

> Live at `~/.claude/commands/<name>.md`, invoked as `/name`. Explicit, user-triggered actions.

| Command | Use when |
|---|---|
| [`/handoff`](./commands/handoff.md) | End of day, context switch, multi-day pause. Writes a self-contained `handoff.md` outside the repo. |
| [`/github-pr`](./commands/github-pr.md) | You want to draft and open a PR for the current branch with `gh pr create`. |
| [`/project-init`](./commands/project-init.md) | Configure this project — currently just the task manager. Writes `~/harness/<slug>/config.json`. |

### Subagents

| Agent | Purpose |
|---|---|
| [`code-explorer`](./agents/code-explorer.md) | Map a repo without polluting main context. Delegate to it whenever loading files yourself would saturate context. |
| [`adversarial-reviewer`](./agents/adversarial-reviewer.md) | Critical external reviewer. Finds problems, doesn't propose solutions. Run it on a plan or on a finished result. |

---

## Per-project state

The harness keeps state **outside the project tree** so client repos stay clean. The harness root is derived from the project's git root:

```bash
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SLUG="$(printf '%s' "$ROOT" | sed 's/[/.]/-/g')"
HARNESS="$HOME/harness/$SLUG"
```

Each project lands in its own folder under `~/harness/`, with no collisions:

```
~/harness/
└── -Users-me-Documents-clientA/        # slug of the git root
    ├── config.json                     # optional, created by /project-init
    └── <task-id>/                      # YYYYMMDD-HHMM-<slug>
        └── handoff.md                  # only when /handoff is invoked
```

`config.json` is optional metadata (currently just the task manager) read by skills to tailor their prompts. ADRs, when created, live in the project's own `docs/adr/`.

---

## Invariants

1. **Alignment before plan, plan before code.** Reach for `grill` and `plan` when the task isn't already crystal-clear — but they're invoked by need, not forced order.
2. **Stateless, never blocking.** Any skill runs on its own; it reads the conversation and asks the user for what it needs. Nothing is a hard stop.
3. **Client repos stay clean.** Per-project state lives under `~/harness/`, never inside the working tree.
4. **Technical debt is never silent.** Every shortcut leaves a tracked trail.
5. **The project always wins.** Skills read `AGENTS.md` first; they never assume stack or architecture.
6. **The user orchestrates, not the skills.** Each skill executes its single procedure and stops; it does not suggest the next step.

---

## Extending the harness

Rules of thumb:

- One skill = one procedure. If you're doing two things, they're two skills.
- The name is the intention, verb-first where natural. No category prefixes.
- Description is intent-based: lead with what it does, then `Use when …` with concrete triggers. The description is the only thing the agent sees when deciding whether to load the skill.
- Keep `SKILL.md` short (aim < 100 lines). Push detail into sibling files and reference them (progressive disclosure).
- If a skill produces a reusable artifact, end with the destination question — never persist unilaterally.
- Prefer a **command** over a skill when the action is an explicit, conscious one-shot the user triggers themselves (like `/handoff` or `/github-pr`).
- Don't create a skill until you've done the procedure by hand 2–3 times.
