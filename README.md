# Personal Development Harness

A set of independent Claude Code skills that turn vague tasks into shipped code with a disciplined, conscious workflow. No vibe coding.

The harness lives in `~/.claude/`. Skills run entirely in the conversation and write nothing to disk unless you explicitly ask, so client repositories stay completely clean.

> Working philosophy lives in [`WORK_PHILOSOPHY.md`](./WORK_PHILOSOPHY.md).
> See [Why `WORK_PHILOSOPHY.md` instead of `CLAUDE.md`](#why-work_philosophymd-instead-of-claudemd).

---

## Installation

From the root of this repo:

```bash
./install.sh
```

The script is **non-destructive and idempotent**:

| Situation                                            | Behavior                                                                     |
| ---------------------------------------------------- | ---------------------------------------------------------------------------- |
| Empty `~/.claude/`                                   | Symlinks everything cleanly. Creates `CLAUDE.md` with `@WORK_PHILOSOPHY.md`. |
| You already have `~/.claude/CLAUDE.md`               | Prepends `@WORK_PHILOSOPHY.md` to it. Your existing content stays intact.    |
| You already have a skill with the same name          | Skips it with a log line. Your version wins.                                 |
| You have skills in unrelated categories              | They coexist — the script only touches paths inside this package.            |
| Re-running the script                                | Detects what's already linked; no duplicates, no errors.                     |

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

The agent in the conversation (with the user) decides which skill to invoke next — never hardcoded inside a skill. Skills must not suggest "next, run skill X" nor "skip if Y". Those decisions belong to the conversation.

---

## Skill catalog

> Skills live flat at `~/.claude/skills/<name>/` (Claude Code requirement). Names are **intent-based**, no category prefixes.

| Skill                                              | Use when                                                                                                                                  |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| [`grill-me`](./skills/grill-me/SKILL.md)           | Interrogating an idea until every ambiguity is resolved — walking down each branch of the design tree, one question at a time.            |
| [`plan`](./skills/plan/SKILL.md)                   | Producing a structured technical plan — affected modules, decisions, risks, side effects, rough effort.                                   |
| [`diagnose`](./skills/diagnose/SKILL.md)           | Hard bugs, unclear regressions, perf problems: reproduce → minimise → hypothesise → instrument → fix → regression-test.                   |
| [`code-standards`](./skills/code-standards/SKILL.md) | Writing or reviewing code in any language against a thin quality bar focused on what models get wrong by default — deep modules, errors designed out of existence, behavior-driven tests, restraint.   |
| [`write-adr`](./skills/write-adr/SKILL.md)         | A non-trivial, hard-to-reverse technical decision deserves a lightweight ADR.                                                             |
| [`write-a-skill`](./skills/write-a-skill/SKILL.md) | Adding, writing, or reworking a harness skill; formalizing a procedure you keep repeating by hand.                                        |
| [`github-pr`](./skills/github-pr/SKILL.md)         | Preparing and opening a PR for the current branch — Conventional-Commits title + why-focused description, approved before `gh pr create`. |
| [`suggest-reviewers`](./skills/suggest-reviewers/SKILL.md) | Suggesting GitHub reviewers for the current branch's PR — ranked from git history + CODEOWNERS, kept out of context via an aggregating script. |
| [`zoom-out`](./skills/zoom-out/SKILL.md)           | Stepping back for broader context or a higher-level perspective on an unfamiliar section of code.                                         |
| [`handoff`](./skills/handoff/SKILL.md)             | Compacting the current conversation into a handoff document so a fresh agent can continue the work.                                       |

---

## Invariants

1. **Alignment before plan, plan before code.** Reach for `grill-me` and `plan` when the task isn't already crystal-clear — but they're invoked by need, not forced order.
2. **Stateless, never blocking.** Any skill runs on its own; it reads the conversation and asks the user for what it needs. Nothing is a hard stop.
3. **Client repos stay clean.** Skills write nothing to the working tree unless you ask them to deposit an artifact there.
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
- Don't create a skill until you've done the procedure by hand 2–3 times.
