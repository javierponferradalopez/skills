# Maintaining this repo

This document is for the **owner and forkers** of this repo — not for people who
just want to use a skill. If you only want to install skills, see the
[README](./README.md): `npx skills@latest add javierponferradalopez/skills`.

Here lives everything that never ships to a user's `~/.claude`: why the repo is
shaped the way it is, how forked skills are kept in sync with their upstreams,
the local-development symlink tool, and the repository layout.

## Contents

- [Why this exists](#why-this-exists) — the philosophy: own your skills, borrow the best, stay in control
- [Repository layout](#repository-layout) — categories and how they map to `~/.claude`
- [Local development — `bin/dev-link`](#local-development--bindev-link) — symlink the repo into your live harness
  - [Uninstall the symlinks](#uninstall-the-symlinks)
- [Syncing with upstreams](#syncing-with-upstreams) — pull other creators' updates without losing your edits
  - [How provenance is recorded](#how-provenance-is-recorded) · [One-time setup](#one-time-setup-fresh-clones) · [The `skills-upstream` tool](#the-tool-binskills-upstream) · [Registering an upstream & adopting skills](#registering-an-upstream--adopting-skills) · [Common scenarios](#common-scenarios)

---

## Why this exists

Skills are quickly becoming one of the highest-leverage ways to shape how Claude Code works. Brilliant people are publishing their own — but a raw fork has a problem: the moment you tweak someone's skill to fit your workflow, you either freeze it (and miss their improvements) or keep pulling (and clobber your edits). You end up depending 100% on an external source you can't safely change.

This repo is built around a different stance: **borrow the best, but own what you run.**

- **Adopt from anyone.** Skills here are adopted from other creators — today [Matt Pocock](https://github.com/mattpocock/skills), more in the future — and the [`skills-upstream`](#the-tool-binskills-upstream) tool makes adding a new one a single command.
- **Adapt to your needs.** Every adopted skill is _my_ copy. I translate it, retune it, split it, or extend it freely — it's just files in this repo.
- **Stay in sync without losing control.** Provenance is tracked per skill, so the tool can pull only what the original author changed and **3-way-merge** it into my version — surfacing real conflicts instead of overwriting my work. I decide, per skill, what to take and what to keep.
- **Never depend 100% on something external.** If an upstream skill is renamed, deleted, or goes in a direction I don't like, my copy keeps working. Upstream is a source of ideas, not a dependency I'm chained to.

The result: a harness that grows with the wider community **and** stays fully under my control. The [Syncing with upstreams](#syncing-with-upstreams) section is where that machinery lives.

---

## Repository layout

In this repo skills are organized into category folders for browsing:
`skills/<category>/<name>/` (e.g. `skills/engineer/tdd/SKILL.md`). Claude Code
requires a **flat** layout, so anything that places a skill flattens the
categories away and lands it at `<agent>/skills/<name>/`. Categories are an
authoring convenience only; names are **intent-based** and stay unique across
categories, with no category prefixes.

Two consumers rely on this layout:

- The public `npx skills add` path — the skills.sh CLI natively understands this
  "catalog layout" and flattens each skill's container as it installs.
- `bin/dev-link` — flattens the categories into symlinks under `~/.claude/skills/`
  (see below).

---

## Local development — `bin/dev-link`

`bin/dev-link` is the **maintainer's local-development tool**. It symlinks the
skills in this repo into `~/.claude/skills/` so that edits made here apply
instantly in your live harness — no re-link between changes. It is **not** the
public install path; end users install individual skills with `npx skills add`.

Run everything from the root of this repo.

| I want to…                                              | Run                                                                 |
| ------------------------------------------------------- | ------------------------------------------------------------------- |
| **Pick exactly which skills to link** (interactive)     | `bin/dev-link`                                                       |
| **Link everything**, no prompts (CI, pipes)             | `bin/dev-link --all`                                                 |
| **Add skills I just adopted/updated** (re-run, safe)    | `bin/dev-link` — idempotent: links new ones, skips what's there      |
| **Update a skill's content** after editing it           | nothing — skills are symlinks, edits in the repo apply instantly     |
| **Keep my own version of a same-named skill**           | nothing — the tool skips it and leaves yours in place               |
| **See the options**                                     | `bin/dev-link --help`                                                |
| **Uninstall the symlinks**                              | see [Uninstall the symlinks](#uninstall-the-symlinks) below         |

When run in a terminal, `bin/dev-link` opens an **interactive selector** so you can choose exactly which skills to link. Nothing is selected by default — toggle the **Select all** row at the top to grab everything, or use `space` to pick individual skills:

```
==> Select skills to link
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

  2 of 21 selected
```

The line under the list shows the **description of the highlighted skill** (taken from its `SKILL.md`), so you can tell what each one does before choosing.

| Key            | Action                          |
| -------------- | ------------------------------- |
| `↑`/`↓` or `k`/`j` | Move the cursor             |
| `space`        | Toggle the row under the cursor (incl. **Select all**) |
| `a`            | Shortcut to toggle all on/off   |
| `enter`        | Link the selected skills        |
| `q` / `esc`    | Abort without linking anything  |

To link everything without prompting (e.g. in a pipe or CI), pass `--all`:

```bash
bin/dev-link --all
```

If stdin is not a terminal, `--all` is assumed automatically.

The tool is **non-destructive and idempotent**:

| Situation                                            | Behavior                                                          |
| ---------------------------------------------------- | ---------------------------------------------------------------- |
| Empty `~/.claude/skills/`                            | Symlinks every skill cleanly.                                    |
| You already have a skill with the same name          | Skips it with a log line. Your version wins.                     |
| You have skills in unrelated categories              | They coexist — the tool only touches paths inside this package.  |
| Re-running the tool                                  | Detects what's already linked; no duplicates, no errors.         |

Personal state (`memory/`, `projects/`, `todos/`, `sessions/`, credentials, local settings) is never touched: the tool only creates symlinks for the files in this package.

### Uninstall the symlinks

`bin/dev-link` doesn't ship an uninstaller. To remove the symlinks it created:

```bash
# Remove the harness symlinks; your real files and other skills stay.
find ~/.claude -maxdepth 2 -type l -lname "*/skills/*" -delete
```

---

## Syncing with upstreams

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
| **Register a new creator's repo**                           | `bin/skills-upstream upstream-add <key> <url> [<branch>]`     | `bin/skills-upstream upstream-add alice https://github.com/alice/skills.git` |
| **Adopt a skill from a registered upstream**                | `bin/skills-upstream add <key> <source> [<mine>]`             | `bin/skills-upstream add alice skills/agents/prototype skills/engineer/prototype` |
| **Stop tracking one fork** (keep your copy as your own)     | `bin/skills-upstream detach <upstream>:<name>`                | `bin/skills-upstream detach matt:teach`                         |
| **Drop a whole upstream** (keep its forks as self-authored) | `bin/skills-upstream upstream-remove <key>`                   | `bin/skills-upstream upstream-remove alice`                     |
| **List all forks grouped by origin** (source, base, mode)   | `bin/skills-upstream list`                                    | `bin/skills-upstream list`                                      |
| **Something looks broken / cryptic error**                  | `bin/skills-upstream doctor`                                  | `bin/skills-upstream doctor`                                    |

> `<key>` is an upstream's short name (e.g. `matt`). `<upstream>:<name>` is a fork's manifest key from the left column of `list` (e.g. `matt:teach`). `<source>` is a path inside that upstream's repo (e.g. `skills/engineering/prototype`). `[<mine>]` is where it lands in *your* tree — pick any category, independent of the author's path; omit it and it defaults to `skills/productivity/<name>`.

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
| `bin/skills-upstream upstream-add <key> <url> [<branch>]` | Registers an origin in the catalog. Adopts nothing — run `sync-remotes` next, then `add`. |
| `bin/skills-upstream upstream-remove <key>`        | Drops an origin and its remote. If forks still reference it, lists them and asks whether to keep them as self-authored. |
| `bin/skills-upstream status [<key>]`               | Walks every upstream (or just `<key>`), grouped by origin: which forks the upstream touched since each `base`. Degrades gracefully on a missing remote. |
| `bin/skills-upstream diff <upstream>:<name>`       | Shows that fork's upstream changes (`base..upstream-<key>/<branch>`).        |
| `bin/skills-upstream update <upstream>:<name>`     | Applies the upstream's changes to your copy (3-way merge, or overwrite if `pure`). |
| `bin/skills-upstream pin <upstream>:<name>`        | Records that fork's current upstream ref as the new `base`, once you're happy. |
| `bin/skills-upstream add <key> <source> [<mine>] [<mode>]` | Adopts a skill from an **already-registered** upstream and registers the fork. |
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
- `[<mine>]` is where it lands in *your* tree (default `skills/productivity/<name>`). Pick any category folder — the layout is flattened to `~/.claude/skills/<name>/` anyway.
- `[<mode>]` defaults to `pure` (track the upstream verbatim). If you plan to customize it, pass `modified`, or flip its `mode` in the manifest once you start editing — otherwise the next `update` will overwrite your changes.

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
for s in matt:tdd matt:to-spec matt:handoff; do bin/skills-upstream update "$s"; done
# review/resolve each, then pin the ones you're happy with
for s in matt:tdd matt:to-spec matt:handoff; do bin/skills-upstream pin "$s"; done
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

`update` only touches the one fork you name, so you upgrade exactly what you want and leave the rest frozen. On a `modified` skill, expect conflicts where your local edits overlap the upstream's — that's the safety net working; resolve them by hand. Heavily diverged skills (`grill-me`, `teach`, `grill-with-docs`, `improve-codebase-architecture`) will conflict more often; near-identical ones (`tdd`, `handoff`, `to-spec`, `to-tickets`) usually merge clean.
