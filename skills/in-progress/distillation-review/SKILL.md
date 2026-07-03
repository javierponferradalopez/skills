---
name: distillation-review
description: Map and explain the changes in a long PR (or a remote branch, or the current local diff) as a navigable, self-contained HTML distillation — a project-grouped file map, a problem→approach→impact mental map, typed dependency/relationship diagrams, per-change tabs ranked by disruption, and a direct link on every referenced file (GitHub diff anchor for a PR, blob for a branch, copy-path for local). Use when a reviewer needs to grasp what a large PR does, which projects it touches, and where the risky changes are — fast, without reading all the code or building the mental map by hand. Also covers "review/recap this PR", "what does this PR do", "visual diff/PR overview".
disable-model-invocation: true
---

# Distillation Review

Produce a read-only distillation of a set of changes, opened as a local HTML file. The source can be
the current branch's **local** changes, a **GitHub PR**, or a **remote branch** —
the last two without any checkout. A bundled script extracts the diff, groups files
by project, and precomputes a per-file link; you read the repo's context and add the
prose; the page renders it — no network beyond two CDN enhancements, nothing
written to the repo.

**Core principle — true by construction.** The diff hunks, file tree, stats, project
grouping, and per-file links are produced by the script and are copied/derived
verbatim from `git` (local) or `GitHub` (PR / branch). You author *only* prose (mental
map, per-project role, diagrams, curated key-change tabs). Never rewrite a diff line:
if a hunk looks wrong, that is the real code — say so in a summary.

## Steps

### 0. Pick the source

Decide, from the conversation context, which diff the user wants:

- **A GitHub PR** — they gave a PR number or a `github.com/.../pull/N` URL, or say
  "review the PR" → use `--pr <number|url>`.
- **A remote branch** — they name a branch on origin (e.g. `feature/x`, "the branch
  from Marta") → use `--branch <name>`.
- **Their own local changes** — "my changes", "this branch", "what I've got", or no
  source mentioned → run with no flags.

If the source is genuinely ambiguous, **ask the user in prose** which one they mean
before running the script (do not use the `AskUserQuestion` tool).

### 1. Extract the diff

Run the bundled generator by its **absolute** path, from the **target repository's
working directory** — do NOT `cd` into the skill's directory. Every mode (including
`--pr` / `--branch`) resolves the repo from the current directory via `gh`'s cwd
context, so running from the wrong directory targets the wrong repo (a 404 on a PR
that exists). Invoke it as:

```bash
# stay in the repo; point node at the script by its absolute path
node "$SKILL_DIR/generate.mjs"                 # local: merge-base(base, HEAD) → working tree
node "$SKILL_DIR/generate.mjs" --pr <n|url>    # a GitHub PR — no checkout (gh pr diff)
node "$SKILL_DIR/generate.mjs" --branch <name> # a remote branch — no checkout (GitHub compare)
```

where `$SKILL_DIR` is this skill's directory (the folder holding `generate.mjs`).

Pass `--base <ref>` only if the user names a base other than the repo default (the
script auto-detects `origin/HEAD` otherwise). Local mode includes uncommitted
tracked changes; `--pr` / `--branch` reflect exactly what is on GitHub. The `--pr`
and `--branch` modes require the `gh` CLI, authenticated (`gh auth status`).

It prints JSON with `reviewDir`, `dataFile`, `htmlFile`, `source`, `projects`, and
change counts.
- If it exits non-zero, surface the exact message (not a git repo / on the base
  branch / no merge-base → suggest `git fetch origin`; PR or branch not found; `gh`
  not installed or unauthenticated) and stop. Don't fabricate a review.

**Done when** you have the `dataFile` and `htmlFile` paths and the list of `projects`.

### 2. Gather project context

Before writing any prose, ground yourself in the repo's own language — the mental
map must describe the *problem*, not paraphrase the diff. Read, best-effort:

- `CONTEXT.md` and `docs/adr/` at the repo root (the domain model and decisions).
- The `README` and/or manifest of **each project reported in step 1** (e.g. the
  `packages/api` README + `package.json`), to learn what each touched project is for.

If a file is absent, skip it — don't invent it. Local mode reads these from disk;
for `--pr` / `--branch` fetch what you need with `gh api .../contents/<path>` (or skip
if unavailable and lean on the diff).

**Done when** you can state, in the repo's own terms, the problem the change solves
and the role each touched project plays.

### 3. Fill the prose

Read `dataFile` (`review-data.js`) — it holds every diff hunk, the file tree, the
`projects` grouping, and each file's precomputed `link`, with `mentalMap`, `diagrams`,
and `keyChanges` set to `null`. Read [`references/blocks.md`](references/blocks.md)
for the exact shapes, then Edit the file in place to fill:

- **`mentalMap`** — `{ problem, approach, impact }`: what hurt, how the change attacks
  it, what changes for the user/system. Grounded in step 2, not a diff recap.
- **`projects[].role`** — one line per touched project on its role in this change.
  Add a `role` field to each entry; leave `name`/`path`/counts untouched. If the
  manifest-based grouping mis-split an unusual architecture, you may correct a file's
  `project` field — but only then.
- **`diagrams`** — 1–4 typed Mermaid diagrams (`kind`: `inheritance` / `relationship`
  / `types` / `flow` / `state`) when a graph earns it (complex hierarchies, relations,
  type shapes, flows). Set `[]` when none does.
- **`keyChanges`** — 3–8 curated tabs, **ordered by disruption** (most disruptive
  first). Each classified (`diff` / `data-model` / `api-endpoint` / `wireframe`), tagged
  with its `project`, and given an `impact` (`breaking` / `risky` / `safe`) + a short
  `impactWhy`, a title (<70 chars), and a summary.

Edit **only** the prose fields (`mentalMap`, `diagrams`, `keyChanges`, and
`projects[].role`). Leave `files`, `meta`, `projects` name/path/counts, and every
diff line and `link` untouched.

**Done when** no prose field is still `null` (deliberate `diagrams: []` is fine),
`keyChanges` has 3–8 entries each pointing at a `path` present in `files`, and the
`.js` file is still valid JavaScript (the `window.REVIEW_DATA = {…};` assignment parses).

### 4. Open it

Open the `htmlFile` in the browser — `open` (macOS), `xdg-open` (Linux), `start`
(Windows) — and tell the user the absolute path. The page loads the now-complete
`review-data.js` and renders. Open only after step 3, so the user never sees a
half-filled review.

**Done when** the browser is opened and the user has the path.

## Anti-patterns

- ❌ Editing a diff line, hunk header, a `link`, or the `files`/`meta`/`projects` counts — breaks *true by construction*.
- ❌ Writing the mental map from the diff alone, skipping step 2 — it reads as a line-by-line recap, not the problem solved.
- ❌ More than 8 key-change tabs, or one per changed file — curate; the reader drowns otherwise.
- ❌ More than 4 diagrams, or a diagram of two files — a graph must earn its place.
- ❌ Restating diff lines in prose instead of explaining intent and risk.
- ❌ Opening the browser before the prose is filled.
- ❌ Inventing a review when the script errored — surface the error and stop.
