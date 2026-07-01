<div align="center">

<pre>
 ____              __      _       ____  _    _ _ _     
|  _ \ ___  _ __  / _| ___( )___  / ___|| | _(_) | |___ 
| |_) / _ \| '_ \| |_ / _ \// __| \___ \| |/ / | | / __|
|  __/ (_) | | | |  _|  __/ \__ \  ___) |   &lt;| | | \__ \
|_|   \___/|_| |_|_|  \___| |___/ |____/|_|\_\_|_|_|___/
</pre>

**A personal development harness for Claude Code.**

A curated set of independent skills that turn vague tasks into shipped code with a disciplined, conscious workflow — _no vibe coding_.

</div>

The harness lives in `~/.claude/`. Skills run entirely in the conversation and write nothing to disk unless you explicitly ask, so client repositories stay completely clean. Many skills are **adopted from other creators and adapted to my own needs** — with tooling to keep them in sync without ever losing my changes (see [Why this exists](#why-this-exists)).

---

## Contents

- [Why this exists](#why-this-exists) — the philosophy: own your skills, borrow the best, stay in control
- [Installation](#installation) — get the skills into `~/.claude/`
  - [Quick reference](#quick-reference--find-your-need) · [Uninstall](#uninstall)
- [Maintenance — syncing with upstreams](#maintenance--syncing-with-upstreams) — pull other creators' updates without losing your edits
  - [Quick reference](#quick-reference--find-your-need-1) · [How provenance is recorded](#how-provenance-is-recorded) · [One-time setup](#one-time-setup-fresh-clones) · [The `skills-upstream` tool](#the-tool-binskills-upstream) · [Registering an upstream & adopting skills](#registering-an-upstream--adopting-skills) · [Common scenarios](#common-scenarios)
- [Stateless skills, conversational orchestration](#stateless-skills-conversational-orchestration) — how the skills are designed
- [Skill catalog](#skill-catalog) — every skill and when to use it
- [Credits](#credits) · [License](#license)

---

## Why this exists

Skills are quickly becoming one of the highest-leverage ways to shape how Claude Code works. Brilliant people are publishing their own — but a raw fork has a problem: the moment you tweak someone's skill to fit your workflow, you either freeze it (and miss their improvements) or keep pulling (and clobber your edits). You end up depending 100% on an external source you can't safely change.

This repo is built around a different stance: **borrow the best, but own what you run.**

- **Adopt from anyone.** Skills here are adopted from other creators — today [Matt Pocock](https://github.com/mattpocock/skills), more in the future — and the [`skills-upstream`](#the-tool-binskills-upstream) tool makes adding a new one a single command.
- **Adapt to your needs.** Every adopted skill is _my_ copy. I translate it, retune it, split it, or extend it freely — it's just files in this repo.
- **Stay in sync without losing control.** Provenance is tracked per skill, so the tool can pull only what the original author changed and **3-way-merge** it into my version — surfacing real conflicts instead of overwriting my work. I decide, per skill, what to take and what to keep.
- **Never depend 100% on something external.** If an upstream skill is renamed, deleted, or goes in a direction I don't like, my copy keeps working. Upstream is a source of ideas, not a dependency I'm chained to.

The result: a harness that grows with the wider community **and** stays fully under my control. The [Maintenance](#maintenance--syncing-with-upstreams) section is where that machinery lives.

---

## Installation

> Just want the skills as they are today? This section is all you need. If you later want to pull other creators' newest changes into the skills forked from them, see [Maintenance](#maintenance--syncing-with-upstreams).

### Quick reference — find your need

Run everything from the root of this repo.

| I want to…                                              | Run                                                                 |
| ------------------------------------------------------- | ------------------------------------------------------------------- |
| **Pick exactly which skills to install** (interactive)  | `./install.sh`                                                       |
| **Install everything**, no prompts (CI, pipes)          | `./install.sh --all`                                                 |
| **Add skills I just adopted/updated** (re-run, safe)    | `./install.sh` — idempotent: links new ones, skips what's there      |
| **Update a skill's content** after editing it           | nothing — skills are symlinks, edits in the repo apply instantly     |
| **Keep my own version of a same-named skill**           | nothing — the installer skips it and leaves yours in place           |
| **See the options**                                     | `./install.sh --help`                                               |
| **Uninstall the harness**                               | see [Uninstall](#uninstall) below                                   |

The rest of this section explains each of these in detail.

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
    ◯ domain-modeling
    ...

    Split a dirty working tree into an ordered list of atomic
    conventional commits, then commit them only on an explicit OK.

  2 of 20 selected
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

## Maintenance — syncing with upstreams

Many skills here are **forked from other creators** — today [Matt Pocock's skills](https://github.com/mattpocock/skills), more in the future — but this is not a git fork: the repos share no common history, and each upstream renames and moves skills freely. So a plain `git merge` is not an option. Instead, every origin is registered once in an **upstreams catalog**, provenance is tracked **per fork** in [`upstream.lock.json`](./upstream.lock.json), and a small tool brings over only the changes you want — without clobbering your local edits.

Each origin is an **upstream** with a short **key** (e.g. `matt`). Every fork records which key it came from and is addressed by a namespaced **manifest key** `<upstream>:<name>` (e.g. `matt:teach`) — so two creators can ship a skill of the same name without colliding. That manifest key is tool-facing only; the name you *invoke* a skill with still comes from its `SKILL.md` frontmatter.

You only need this section if you want to keep your forked skills up to date. Skills you authored yourself (`implement`, `validate`, `handoff-grill`, `github-pr`, `code-standards`, `commit`, `suggest-reviewers`, `zoom-out`, `validate-business-idea`) are **not** tracked and are never touched. To see this split at any time, run `bin/skills-upstream doctor`.

### Quick reference — find your need

Start here. Match what you want to do, run the command, and follow the deep-dive section below if you need the details. Refresh your origins first with `sync-remotes` so every comparison is against each creator's latest.

| I want to…                                                  | Run                                                            | Example                                                          |
| ----------------------------------------------------------- | ------------------------------------------------------------- | --------------------------------------------------------------- |
| **Set up a fresh clone / refresh all origins**              | `bin/skills-upstream sync-remotes`                            | `bin/skills-upstream sync-remotes`                              |
| **Check everything is healthy**                             | `bin/skills-upstream doctor`                                  | `bin/skills-upstream doctor`                                    |
| **See which forks their upstreams touched**                 | `bin/skills-upstream sync-remotes && … status`                | `bin/skills-upstream sync-remotes && bin/skills-upstream status`|
| **Focus on one creator**                                    | `bin/skills-upstream status <key>`                            | `bin/skills-upstream status matt`                               |
| **Review what changed in one fork** before pulling         | `bin/skills-upstream diff <upstream>:<name>`                  | `bin/skills-upstream diff matt:teach`                           |
| **Pull an upstream's changes into one fork**                | `update <upstream>:<name>` → resolve → `pin <upstream>:<name>`| `bin/skills-upstream update matt:teach` → resolve → `pin matt:teach` |
| **Register a new creator's repo**                           | `bin/skills-upstream upstream-add <key> <url> [branch]`       | `bin/skills-upstream upstream-add alice https://github.com/alice/skills.git` |
| **Adopt a skill from a registered upstream**                | `bin/skills-upstream add <key> <source> [mine]`               | `bin/skills-upstream add alice skills/agents/prototype skills/utils/prototype` |
| **Stop tracking one fork** (keep your copy as your own)     | `bin/skills-upstream detach <upstream>:<name>`                | `bin/skills-upstream detach matt:teach`                         |
| **Drop a whole upstream** (keep its forks as self-authored) | `bin/skills-upstream upstream-remove <key>`                   | `bin/skills-upstream upstream-remove alice`                     |
| **List all forks grouped by origin** (source, base, mode)   | `bin/skills-upstream list`                                    | `bin/skills-upstream list`                                      |
| **Something looks broken / cryptic error**                  | `bin/skills-upstream doctor`                                  | `bin/skills-upstream doctor`                                    |

> `<key>` is an upstream's short name (e.g. `matt`). `<upstream>:<name>` is a fork's manifest key from the left column of `list` (e.g. `matt:teach`). `<source>` is a path inside that upstream's repo (e.g. `skills/engineering/prototype`). `[mine]` is where it lands in *your* tree — pick any category, independent of the author's path; omit it and it defaults to `skills/productivity/<name>`.

### How provenance is recorded

`upstream.lock.json` has two parts: the `upstreams` catalog of origins, and one `skills` entry per tracked fork.

```jsonc
{
  "upstreams": {
    "matt": { "url": "https://github.com/mattpocock/skills.git" }
    //         "branch" is optional — when absent, the ref follows the remote's default HEAD
  },
  "skills": {
    "matt:teach": {
      "upstream": "matt",                     // which catalog origin this fork came from
      "mine":     "skills/productivity/teach",// your copy
      "source":   "skills/productivity/teach",// the equivalent path in that upstream (may be renamed/moved)
      "base":     "6eeb81b",                  // the upstream commit you are synced from
      "mode":     "modified"                  // "modified" = 3-way merge · "pure" = take upstream verbatim
    }
  }
}
```

The catalog stores each URL **once**; every fork references its origin by key. The `base` commit is what makes selective updates possible: it lets the tool compute *exactly* what that upstream changed since your last sync and three-way-merge only that delta into your copy — even when the paths differ. `mode` decides how an update is applied:

- **`modified`** — your copy has intentional local changes (e.g. translations, tweaks). Updates are a **3-way merge** that preserves your edits and only flags real conflicts.
- **`pure`** — you track the upstream's version verbatim. Updates **overwrite** your copy with upstream.

### One-time setup (fresh clones)

The catalog is the single source of truth for your git remotes. After cloning, one command derives them all:

```bash
bin/skills-upstream sync-remotes   # creates an `upstream-<key>` remote per catalog entry, fetches, records each default branch
bin/skills-upstream doctor         # confirms the manifest, paths and remotes are all healthy
```

`sync-remotes` is idempotent — run it any time to add a newly-registered origin, fix a changed URL, and re-fetch everyone. `doctor` is the first thing to run whenever something looks off; it works even before the remotes exist (it skips the upstream-only checks and tells you to run `sync-remotes`).

### The tool: `bin/skills-upstream`

It runs only in this authoring repo (it needs `jq` and the git history); it never ships to `~/.claude`. Each origin maps to a git remote `upstream-<key>`, and the compare ref is `upstream-<key>/<branch>` (the catalog branch, or the remote's default HEAD when none is pinned).

| Command                                            | What it does                                                                 |
| -------------------------------------------------- | ---------------------------------------------------------------------------- |
| `bin/skills-upstream sync-remotes`                 | Reconciles git remotes from the catalog: adds missing `upstream-<key>` remotes, fixes changed URLs, fetches all, records each default HEAD. Idempotent. |
| `bin/skills-upstream upstream-add <key> <url> [branch]` | Registers an origin in the catalog. Adopts nothing — run `sync-remotes` next, then `add`. |
| `bin/skills-upstream upstream-remove <key>`        | Drops an origin and its remote. If forks still reference it, lists them and asks whether to keep them as self-authored. |
| `bin/skills-upstream status [<key>]`               | Walks every upstream (or just `<key>`), grouped by origin: which forks the upstream touched since each `base`. Degrades gracefully on a missing remote. |
| `bin/skills-upstream diff <upstream>:<name>`       | Shows that fork's upstream changes (`base..upstream-<key>/<branch>`).        |
| `bin/skills-upstream update <upstream>:<name>`     | Applies the upstream's changes to your copy (3-way merge, or overwrite if `pure`). |
| `bin/skills-upstream pin <upstream>:<name>`        | Records that fork's current upstream ref as the new `base`, once you're happy. |
| `bin/skills-upstream add <key> <source> [mine] [mode]` | Adopts a skill from an **already-registered** upstream and registers the fork. |
| `bin/skills-upstream detach <upstream>:<name>`     | Stops tracking one fork — drops its manifest entry, leaves `mine/` intact (becomes self-authored). |
| `bin/skills-upstream list`                         | Dumps the manifest, forks grouped under their origin (source, base, mode).   |
| `bin/skills-upstream doctor`                       | Sanity-checks everything: valid JSON, every `mine` path exists, no installer name collisions, untracked folders, and per-upstream that the remote/ref resolves and every `source`/`base` is still alive. |

### Registering an upstream & adopting skills

Borrowing from a new creator is two deliberate steps — register the origin once, then adopt skills from it. Keeping them separate means a URL typo can never spawn a near-duplicate origin.

```bash
# 1. register the origin (branch optional; omit to follow the repo's default branch)
bin/skills-upstream upstream-add alice https://github.com/alice/skills.git
bin/skills-upstream sync-remotes                      # create the upstream-alice remote + fetch

# 2. adopt skills from it — <key> is required and must already be registered
bin/skills-upstream add alice skills/agents/prototype                         # -> skills/productivity/prototype, mode "pure"
bin/skills-upstream add alice skills/agents/prototype skills/engineer/prototype modified
```

- `<key>` is the upstream's catalog key. `add` fails clearly if it isn't registered yet, pointing you to `upstream-add`.
- `<source>` is the path **in that upstream's repo** (find it with `git ls-tree -r --name-only upstream-<key>/HEAD | grep <name>`).
- `[mine]` is where it lands in *your* tree (default `skills/productivity/<name>`). Pick any category folder — the installer flattens it to `~/.claude/skills/<name>/` anyway.
- `[mode]` defaults to `pure` (track the upstream verbatim). If you plan to customize it, pass `modified`, or flip its `mode` in the manifest once you start editing — otherwise the next `update` will overwrite your changes.

`add` copies **all** of the skill's files (e.g. `SKILL.md` plus any `UI.md`, `GLOSSARY.md`, `scripts/`), registers it as `<key>:<name>`, pins `base` to the current upstream ref, and refuses to clobber an existing skill or folder-name collision. In the rare case where one upstream has two sources sharing a basename, `add` asks for an explicit suffix to disambiguate the key. The new skill's invocation name comes from its `SKILL.md` frontmatter `name:`, exactly as the author wrote it.

### Common scenarios

Every flow starts the same way — refresh your origins and see what moved, grouped by creator:

```bash
bin/skills-upstream sync-remotes && bin/skills-upstream status
```

**1. Pull an upstream's changes into one forked skill** — the everyday case:

```bash
bin/skills-upstream diff matt:teach          # review what the upstream changed
bin/skills-upstream update matt:teach        # 3-way merge into your copy
# resolve any conflict markers (<<<<<<<), then test the skill
bin/skills-upstream pin matt:teach           # lock in the new base
```

**2. Catch up several skills at once** — `status` listed more than one:

```bash
for s in matt:tdd matt:to-prd matt:handoff; do bin/skills-upstream update "$s"; done
# review/resolve each, then pin the ones you're happy with
for s in matt:tdd matt:to-prd matt:handoff; do bin/skills-upstream pin "$s"; done
```

**3. Borrow from a new creator** — register, sync, adopt:

```bash
bin/skills-upstream upstream-add alice https://github.com/alice/skills.git
bin/skills-upstream sync-remotes
git ls-tree -r --name-only upstream-alice/HEAD | grep prototype   # find its path
bin/skills-upstream add alice skills/agents/prototype             # copy + register (mode pure)
```

**4. You've started customizing a `pure` skill** — stop future overwrites by switching its mode to `modified` in `upstream.lock.json`, so the next `update` does a 3-way merge instead:

```jsonc
"alice:prototype": { ..., "mode": "modified" }
```

**5. An upstream renamed or deleted a skill** — `status` flags it as `GONE from <key>`. Decide per skill: `detach <upstream>:<name>` to keep your copy as your own, or repoint `source` to its new path if it just moved.

**6. You no longer follow a creator** — `upstream-remove <key>` drops the origin and its remote. If forks still point at it, it lists them and asks whether to detach each (keeping every `mine/` copy as self-authored); answer `n` or empty and it touches nothing.

**7. "Did I miss anything?"** — `bin/skills-upstream status` is the single source of truth: green means your copy is synced to its `base`, yellow means the upstream moved on since then.

`update` only touches the one fork you name, so you upgrade exactly what you want and leave the rest frozen. On a `modified` skill, expect conflicts where your local edits overlap the upstream's — that's the safety net working; resolve them by hand. Heavily diverged skills (`grill-me`, `teach`, `grill-with-docs`, `improve-codebase-architecture`) will conflict more often; near-identical ones (`tdd`, `handoff`, `to-prd`, `to-issues`) usually merge clean.

---

## Stateless skills, conversational orchestration

Skills are independent units invoked by intent. They live in the conversation: each one executes its single procedure and stops. No skill requires any prior file to exist, none reads files left by other skills, none writes files of its own.

When a skill produces a reusable artifact (a plan, a list of subtasks, a verification summary), it **asks the user where to deposit it** — the project's task manager, a local markdown, the original ticket, or just-conversation. The skill does not decide where things go.

The agent in the conversation (with the user) decides which skill to invoke next — never hardcoded inside a skill. Skills must not suggest "next, run skill X" nor "skip if Y". Those decisions belong to the conversation.

---

## Skill catalog

> In this repo skills are organized into category folders for browsing — `skills/<category>/<name>/`. Claude Code requires a flat layout, so the installer flattens the categories away and links each skill into `~/.claude/skills/<name>/`. Categories are an authoring convenience only; names are **intent-based** and stay unique across categories, with no category prefixes.

Skills fall into two categories: **engineer** — the disciplined inner loop from a vague task to committed code (align → plan → build → commit), plus the handoff skills that pause and resume that loop — and **productivity** — everything around that loop: diagnosis, domain modeling, architecture, code navigation, PR workflow, harness tooling, and learning.

### Engineer

| Skill                                              | Use when                                                                                                                                  |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| [`grill-me`](./skills/engineer/grill-me/SKILL.md)           | Interrogating an idea until every ambiguity is resolved — walking down each branch of the design tree, one question at a time.            |
| [`grill-with-docs`](./skills/engineer/grill-me-with-docs/SKILL.md) | Running a `grill-me` session that also drives `domain-modeling` — so the interrogation simultaneously sharpens terminology and writes the glossary/ADRs down as decisions crystallise. |
| [`to-prd`](./skills/engineer/to-prd/SKILL.md)               | Turning the current conversation into a PRD and publishing it to the project issue tracker — synthesises what's known, no interview.       |
| [`to-issues`](./skills/engineer/to-issues/SKILL.md)         | Breaking a plan, spec, or PRD into independently-grabbable issues on the tracker using tracer-bullet vertical slices.                      |
| [`tdd`](./skills/engineer/tdd/SKILL.md)                     | Building a feature or fixing a bug test-first — a disciplined red-green-refactor loop in vertical slices, with behavior-driven integration tests. |
| [`implement`](./skills/engineer/implement/SKILL.md)         | Implementing a single issue end-to-end and stopping with the tree dirty — fetches the issue, loads project context, applies the code-standards bar and red-green-refactor; no commit, push, branch, or issue close. |
| [`validate`](./skills/engineer/validate/SKILL.md)           | Reviewing one issue's uncommitted implementation pre-commit in a fresh session — fixes bugs/edge-cases/quality in place, writes tests to break the code, flags spec gaps and scope creep; leaves the tree green, never commits. |
| [`code-standards`](./skills/engineer/code-standards/SKILL.md) | Writing or reviewing code in any language against a thin quality bar focused on what models get wrong by default — deep modules, errors designed out of existence, behavior-driven tests, restraint.   |
| [`commit`](./skills/engineer/commit/SKILL.md)               | Splitting a dirty working tree into an ordered list of atomic conventional commits — plans from `git diff HEAD`, commits only on an explicit literal OK. |
| [`handoff`](./skills/engineer/handoff/SKILL.md)             | Compacting the current conversation into a handoff document (saved to the OS temp dir) so a fresh agent can continue the work — references existing artifacts rather than duplicating them. |
| [`handoff-grill`](./skills/engineer/handoff-grill/SKILL.md) | Pausing a `grill-me` session into a resumable handoff that preserves the open branches of the decision tree, not just the closed decisions — to continue later or hand to a teammate. |
| [`domain-modeling`](./skills/engineer/domain-modeling/SKILL.md) | Actively building and sharpening the project's domain model — challenging terms and writing the glossary (`CONTEXT.md`) and decisions (ADRs) down the moment they crystallise. |

### Productivity

| Skill                                              | Use when                                                                                                                                  |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| [`diagnose`](./skills/productivity/diagnose/SKILL.md)           | Hard bugs, unclear regressions, perf problems: reproduce → minimise → hypothesise → instrument → fix → regression-test.                   |
| [`improve-codebase-architecture`](./skills/productivity/improve-codebase-architecture/SKILL.md) | Finding deepening opportunities in a codebase — turning shallow modules into deep ones for testability and AI-navigability, presented as a visual before/after HTML report informed by `CONTEXT.md` and ADRs. |
| [`zoom-out`](./skills/productivity/zoom-out/SKILL.md)           | Stepping back for broader context or a higher-level perspective on an unfamiliar section of code.                                         |
| [`validate-business-idea`](./skills/productivity/validate-business-idea/SKILL.md) | Validating a business idea before building — a bounded grill extracts the idea, mandatory multi-angle web research checks whether it already exists and who the competitors are, and it ships a shadcn/ui HTML report with an existence verdict, differentiation axes, and a pursue/pivot/abandon call. |
| [`github-pr`](./skills/productivity/github-pr/SKILL.md)         | Preparing and opening a PR for the current branch — Conventional-Commits title + why-focused description, approved before `gh pr create`. |
| [`suggest-reviewers`](./skills/productivity/suggest-reviewers/SKILL.md) | Suggesting GitHub reviewers for the current branch's PR — ranked from git history + CODEOWNERS, kept out of context via an aggregating script. |
| [`setup-skills`](./skills/productivity/setup-skills/SKILL.md)   | Scaffolding a repo's `## Agent skills` block in `AGENTS.md`/`CLAUDE.md` plus `docs/agents/` so the engineering skills know its issue tracker and domain-doc layout. |
| [`write-a-skill`](./skills/productivity/write-a-skill/SKILL.md) | Adding, writing, or reworking a harness skill; formalizing a procedure you keep repeating by hand.                                        |
| [`teach`](./skills/productivity/teach/SKILL.md)                 | Learning a topic over multiple sessions — turns the current directory into a teaching workspace with a mission, citation-backed HTML lessons, reference cheat-sheets, and learning records. |

---

## Credits

Many of these skills are based on [Matt Pocock's skills](https://github.com/mattpocock/skills), adapted to my own needs.

---

## License

Released under the [MIT License](./LICENSE).

---
