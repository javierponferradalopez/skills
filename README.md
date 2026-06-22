# Personal Development Harness

A set of independent Claude Code skills that turn vague tasks into shipped code with a disciplined, conscious workflow. No vibe coding.

The harness lives in `~/.claude/`. Skills run entirely in the conversation and write nothing to disk unless you explicitly ask, so client repositories stay completely clean.

---

## Installation

> Just want the skills as they are today? This section is all you need. If you later want to pull Matt Pocock's newest changes into the skills forked from him, see [Maintenance](#maintenance--syncing-with-upstream).

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

## Maintenance — syncing with upstream

Many skills here are **forked from [Matt Pocock's skills](https://github.com/mattpocock/skills)**, but this is not a git fork: the two repos share no common history, and upstream renames and moves skills freely. So a plain `git merge` is not an option. Instead, provenance is tracked **per skill** in [`upstream.lock.json`](./upstream.lock.json), and a small tool brings over only the changes you want — without clobbering your local edits.

You only need this section if you want to keep your forked skills up to date with upstream. Skills you authored yourself (`implement`, `validate`, `github-pr`, `code-standards`, `commit`, `suggest-reviewers`, `zoom-out`) are **not** tracked and are never touched.

### How provenance is recorded

`upstream.lock.json` holds one entry per tracked fork:

```jsonc
"teach": {
  "mine":   "skills/productivity/teach",        // your copy
  "source": "skills/productivity/teach",        // the equivalent path in Matt's repo (may be renamed/moved)
  "base":   "6eeb81b",                          // the upstream commit you are synced from
  "mode":   "modified"                          // "modified" = 3-way merge · "pure" = take upstream verbatim
}
```

The `base` commit is what makes selective updates possible: it lets the tool compute *exactly* what Matt changed since your last sync and three-way-merge only that delta into your copy — even when the paths differ. `mode` decides how an update is applied:

- **`modified`** — your copy has intentional local changes (e.g. translations, tweaks). Updates are a **3-way merge** that preserves your edits and only flags real conflicts.
- **`pure`** — you track Matt's version verbatim. Updates **overwrite** your copy with upstream.

### One-time setup (fresh clones)

The tool compares against the `upstream` remote. If you cloned this repo, add it once:

```bash
git remote add upstream https://github.com/mattpocock/skills.git
git fetch upstream
```

### The tool: `bin/skills-upstream`

It runs only in this authoring repo (it needs `jq` and the git history); it never ships to `~/.claude`.

| Command                       | What it does                                                                 |
| ----------------------------- | ---------------------------------------------------------------------------- |
| `bin/skills-upstream status`  | For each tracked fork, shows whether Matt changed it since your `base`.       |
| `bin/skills-upstream list`    | Dumps the manifest (source path, base, mode per skill).                       |
| `bin/skills-upstream diff <skill>`   | Shows Matt's changes for that fork (`base..upstream/main`).            |
| `bin/skills-upstream update <skill>` | Applies Matt's changes to your copy (3-way merge, or overwrite if `pure`). |
| `bin/skills-upstream pin <skill>`    | Records the current upstream as the new `base`, once you're happy.    |
| `bin/skills-upstream add <source> [mine] [mode]` | Adopts a **new** skill from Matt and registers it in the manifest. |

### Adopting a brand-new skill from Matt

When Matt ships a skill you don't have yet, `add` copies it into your structure and starts tracking it — no manual copy/paste:

```bash
git fetch upstream
bin/skills-upstream add skills/engineering/prototype          # -> skills/productivity/prototype, mode "pure"
bin/skills-upstream add skills/engineering/prototype skills/engineer/prototype modified
```

- `<source>` is the path **in Matt's repo** (find it with `git ls-tree -r --name-only upstream/main | grep <name>`).
- `[mine]` is where it lands in *your* tree (default `skills/productivity/<name>`). Pick any category folder — the installer flattens it to `~/.claude/skills/<name>/` anyway.
- `[mode]` defaults to `pure` (track Matt verbatim). If you plan to customize it, pass `modified`, or flip its `mode` in the manifest once you start editing — otherwise the next `update` will overwrite your changes.

It copies **all** of the skill's files (e.g. `SKILL.md` plus any `UI.md`, `GLOSSARY.md`, `scripts/`), pins `base` to the current upstream, and refuses to clobber an existing skill or name collision. The new skill's invocation name comes from its `SKILL.md` frontmatter `name:`, exactly as Matt wrote it.

### Common scenarios

Every flow starts the same way — pull Matt's latest and see what moved:

```bash
git fetch upstream && bin/skills-upstream status
```

**1. Pull Matt's changes into one forked skill** — the everyday case:

```bash
bin/skills-upstream diff teach          # review what Matt changed
bin/skills-upstream update teach        # 3-way merge into your copy
# resolve any conflict markers (<<<<<<<), then test the skill
bin/skills-upstream pin teach           # lock in the new base
```

**2. Catch up several skills at once** — `status` listed more than one:

```bash
for s in tdd to-prd handoff; do bin/skills-upstream update "$s"; done
# review/resolve each, then pin the ones you're happy with
for s in tdd to-prd handoff; do bin/skills-upstream pin "$s"; done
```

**3. Adopt a brand-new skill Matt just shipped:**

```bash
git ls-tree -r --name-only upstream/main | grep prototype   # find its path
bin/skills-upstream add skills/engineering/prototype        # copy + register (mode pure)
```

**4. You've started customizing a `pure` skill** — stop future overwrites by switching its mode to `modified` in `upstream.lock.json`, so the next `update` does a 3-way merge instead:

```jsonc
"prototype": { ..., "mode": "modified" }
```

**5. Matt renamed or deleted a skill** — `status` flags it as `GONE from matt`. Decide per skill: drop tracking (delete its entry from `upstream.lock.json`, keep your copy as your own), or repoint `source` to its new path if he just moved it.

**6. "Did I miss anything?"** — `bin/skills-upstream status` is the single source of truth: green means your copy is synced to its `base`, yellow means Matt moved on since then.

`update` only touches the one skill you name, so you upgrade exactly what you want and leave the rest frozen. On a `modified` skill, expect conflicts where your local edits overlap Matt's — that's the safety net working; resolve them by hand. Heavily diverged skills (`grill-me`, `teach`, `grill-with-docs`, `improve-codebase-architecture`) will conflict more often; near-identical ones (`tdd`, `handoff`, `to-prd`, `to-issues`) usually merge clean.

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
| [`handoff-grill`](./skills/productivity/handoff-grill/SKILL.md) | Pausing a `grill-me` session into a resumable handoff that preserves the open branches of the decision tree, not just the closed decisions — to continue later or hand to a teammate. |
| [`teach`](./skills/productivity/teach/SKILL.md)                 | Learning a topic over multiple sessions — turns the current directory into a teaching workspace with a mission, citation-backed HTML lessons, reference cheat-sheets, and learning records. |

---

## Credits

Many of these skills are based on [Matt Pocock's skills](https://github.com/mattpocock/skills), adapted to my own needs.

---

## License

Released under the [MIT License](./LICENSE).

---
