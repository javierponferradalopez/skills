# Personal Development Harness

A set of independent Claude Code skills that turn vague tasks into shipped code with a disciplined, conscious workflow. No vibe coding.

The harness lives in `~/.claude/`. Skills run entirely in the conversation and write nothing to disk unless you explicitly ask, so client repositories stay completely clean.

---

## Installation

From the root of this repo:

```bash
./install.sh
```

When run in a terminal, the script opens an **interactive selector** so you can choose exactly which skills to install. Nothing is selected by default — toggle the **Select all** row at the top to grab everything, or use `space` to pick individual skills:

```
==> Select skills to install
    ↑/↓ move · space toggle · a all · enter confirm · q quit

  ◯ Select all

  engineer
    ◯ code-standards
    ◉ commit
    ...
  productivity
    ◉ diagnose
    ◯ handoff
    ...

    Split a dirty working tree into an ordered list of atomic
    conventional commits, then commit them only on an explicit OK.

  2 of 18 selected
```

The line under the list shows the **description of the highlighted skill** (taken from its `SKILL.md`), so you can tell what each one does before choosing.

| Key            | Action                          |
| -------------- | ------------------------------- |
| `↑`/`↓` or `k`/`j` | Move the cursor             |
| `space`        | Toggle the row under the cursor (incl. **Select all**) |
| `a`            | Shortcut to toggle all on/off   |
| `enter`        | Install the selected skills     |
| `q` / `esc`    | Abort without installing anything |

To install everything without prompting (e.g. in a pipe or CI), pass `--all`:

```bash
./install.sh --all
```

If stdin is not a terminal, `--all` is assumed automatically.

The script is **non-destructive and idempotent**:

| Situation                                            | Behavior                                                          |
| ---------------------------------------------------- | ---------------------------------------------------------------- |
| Empty `~/.claude/skills/`                            | Symlinks every skill cleanly.                                    |
| You already have a skill with the same name          | Skips it with a log line. Your version wins.                     |
| You have skills in unrelated categories              | They coexist — the script only touches paths inside this package.|
| Re-running the script                                | Detects what's already linked; no duplicates, no errors.         |

Personal state (`memory/`, `projects/`, `todos/`, `sessions/`, credentials, local settings) is never touched: the script only creates symlinks for the files in this package.

### Uninstall

The script doesn't ship an uninstaller. To remove the harness:

```bash
# Remove the harness symlinks; your real files and other skills stay.
find ~/.claude -maxdepth 2 -type l -lname "*/skills/*" -delete
```

---

## Stateless skills, conversational orchestration

Skills are independent units invoked by intent. They live in the conversation: each one executes its single procedure and stops. No skill requires any prior file to exist, none reads files left by other skills, none writes files of its own.

When a skill produces a reusable artifact (a plan, a list of subtasks, a verification summary), it **asks the user where to deposit it** — the project's task manager, a local markdown, the original ticket, or just-conversation. The skill does not decide where things go.

The agent in the conversation (with the user) decides which skill to invoke next — never hardcoded inside a skill. Skills must not suggest "next, run skill X" nor "skip if Y". Those decisions belong to the conversation.

---

## Skill catalog

> In this repo skills are organized into category folders for browsing — `skills/<category>/<name>/`. Claude Code requires a flat layout, so the installer flattens the categories away and links each skill into `~/.claude/skills/<name>/`. Categories are an authoring convenience only; names are **intent-based** and stay unique across categories, with no category prefixes.

Skills fall into two categories: **engineer** — the disciplined inner loop from a vague task to committed code (align → plan → build → commit) — and **productivity** — everything around that loop: diagnosis, architecture, code navigation, PR workflow, harness tooling, and learning.

### Engineer

| Skill                                              | Use when                                                                                                                                  |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| [`grill-me`](./skills/engineer/grill-me/SKILL.md)           | Interrogating an idea until every ambiguity is resolved — walking down each branch of the design tree, one question at a time.            |
| [`grill-with-docs`](./skills/engineer/grill-with-docs/SKILL.md) | Stress-testing a plan against the project's documented domain — sharpens terminology and updates `CONTEXT.md`/ADRs inline as decisions crystallise. |
| [`to-prd`](./skills/engineer/to-prd/SKILL.md)               | Turning the current conversation into a PRD and publishing it to the project issue tracker — synthesises what's known, no interview.       |
| [`to-issues`](./skills/engineer/to-issues/SKILL.md)         | Breaking a plan, spec, or PRD into independently-grabbable issues on the tracker using tracer-bullet vertical slices.                      |
| [`tdd`](./skills/engineer/tdd/SKILL.md)                     | Building a feature or fixing a bug test-first — a disciplined red-green-refactor loop in vertical slices, with behavior-driven integration tests. |
| [`implement`](./skills/engineer/implement/SKILL.md)         | Implementing a single issue end-to-end and stopping with the tree dirty — fetches the issue, loads project context, applies the code-standards bar and red-green-refactor; no commit, push, branch, or issue close. |
| [`validate`](./skills/engineer/validate/SKILL.md)           | Reviewing one issue's uncommitted implementation pre-commit in a fresh session — fixes bugs/edge-cases/quality in place, writes tests to break the code, flags spec gaps and scope creep; leaves the tree green, never commits. |
| [`code-standards`](./skills/engineer/code-standards/SKILL.md) | Writing or reviewing code in any language against a thin quality bar focused on what models get wrong by default — deep modules, errors designed out of existence, behavior-driven tests, restraint.   |
| [`commit`](./skills/engineer/commit/SKILL.md)               | Splitting a dirty working tree into an ordered list of atomic conventional commits — plans from `git diff HEAD`, commits only on an explicit literal OK. |

### Productivity

| Skill                                              | Use when                                                                                                                                  |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| [`diagnose`](./skills/productivity/diagnose/SKILL.md)           | Hard bugs, unclear regressions, perf problems: reproduce → minimise → hypothesise → instrument → fix → regression-test.                   |
| [`improve-codebase-architecture`](./skills/productivity/improve-codebase-architecture/SKILL.md) | Finding deepening opportunities in a codebase — turning shallow modules into deep ones for testability and AI-navigability, presented as a visual before/after HTML report informed by `CONTEXT.md` and ADRs. |
| [`zoom-out`](./skills/productivity/zoom-out/SKILL.md)           | Stepping back for broader context or a higher-level perspective on an unfamiliar section of code.                                         |
| [`github-pr`](./skills/productivity/github-pr/SKILL.md)         | Preparing and opening a PR for the current branch — Conventional-Commits title + why-focused description, approved before `gh pr create`. |
| [`suggest-reviewers`](./skills/productivity/suggest-reviewers/SKILL.md) | Suggesting GitHub reviewers for the current branch's PR — ranked from git history + CODEOWNERS, kept out of context via an aggregating script. |
| [`setup-skills`](./skills/productivity/setup-skills/SKILL.md)   | Scaffolding a repo's `## Agent skills` block in `AGENTS.md`/`CLAUDE.md` plus `docs/agents/` so the engineering skills know its issue tracker and domain-doc layout. |
| [`write-a-skill`](./skills/productivity/write-a-skill/SKILL.md) | Adding, writing, or reworking a harness skill; formalizing a procedure you keep repeating by hand.                                        |
| [`handoff`](./skills/productivity/handoff/SKILL.md)             | Compacting the current conversation into a handoff document so a fresh agent can continue the work.                                       |
| [`teach`](./skills/productivity/teach/SKILL.md)                 | Learning a topic over multiple sessions — turns the current directory into a teaching workspace with a mission, citation-backed HTML lessons, reference cheat-sheets, and learning records. |

---

## Credits

Many of these skills are based on [Matt Pocock's skills](https://github.com/mattpocock/skills), adapted to my own needs.

---

## License

Released under the [MIT License](./LICENSE).

---
