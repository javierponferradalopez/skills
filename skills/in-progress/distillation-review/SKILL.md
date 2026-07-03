---
name: distillation-review
description: Map and explain the changes in a long PR (or a remote branch, or the current local diff) as a navigable, self-contained HTML distillation — file map, per-change explanations, annotated diffs, an optional dependency/flow diagram, and a curated set of key-change tabs. Use when a reviewer needs to grasp what a large PR does and where the important changes are — fast, without reading all the code or building the mental map by hand. Also covers "review/recap this PR", "what does this PR do", "visual diff/PR overview".
disable-model-invocation: true
---

# Distillation Review

Produce a read-only distillation of a set of changes, opened as a local HTML file. The source can be
the current branch's **local** changes, a **GitHub PR**, or a **remote branch** —
the last two without any checkout. A bundled script extracts the diff; you add the
prose; the page renders it — no network beyond two CDN enhancements, nothing
written to the repo.

**Core principle — true by construction.** The diff hunks, file tree, and stats are
produced by the script and are copied verbatim from `git` (local) or `GitHub` (PR /
branch). You author *only* prose (narrative, diagram, curated key-change tabs).
Never rewrite a diff line: if a hunk looks wrong, that is the real code — say so in
a summary.

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

It prints JSON with `reviewDir`, `dataFile`, `htmlFile`, `source`, and change counts.
- If it exits non-zero, surface the exact message (not a git repo / on the base
  branch / no merge-base → suggest `git fetch origin`; PR or branch not found; `gh`
  not installed or unauthenticated) and stop. Don't fabricate a review.

**Done when** you have the `dataFile` and `htmlFile` paths.

### 2. Fill the prose

Read `dataFile` (`review-data.js`) — it holds every diff hunk and the file tree,
with `narrative`, `diagram`, and `keyChanges` set to `null`. Read
[`references/blocks.md`](references/blocks.md) for the exact shapes, then Edit the
file in place to fill those three nulls:

- **`narrative`** — 1–3 paragraphs on what the branch does and why.
- **`diagram`** — one Mermaid diagram if a graph/flow earns it, else leave `null`.
- **`keyChanges`** — 3–8 curated tabs, most-important first, each classified
  (`diff` / `data-model` / `api-endpoint` / `wireframe`) with a title (<70 chars) and summary.

Edit **only** those three fields. Leave `files`, `meta`, and every diff line untouched.

**Done when** no prose field is still `null` (a deliberate `diagram: null` is fine),
`keyChanges` has 3–8 entries each pointing at a `path` present in `files`, and the
`.js` file is still valid JavaScript (the `window.REVIEW_DATA = {…};` assignment parses).

### 3. Open it

Open the `htmlFile` in the browser — `open` (macOS), `xdg-open` (Linux), `start`
(Windows) — and tell the user the absolute path. The page loads the now-complete
`review-data.js` and renders. Open only after step 2, so the user never sees a
half-filled review.

**Done when** the browser is opened and the user has the path.

## Anti-patterns

- ❌ Editing a diff line, hunk header, or the `files`/`meta` blocks — breaks *true by construction*.
- ❌ More than 8 key-change tabs, or one per changed file — curate; the reader drowns otherwise.
- ❌ Restating diff lines in prose instead of explaining intent and risk.
- ❌ Opening the browser before the prose is filled.
- ❌ Inventing a review when the script errored — surface the error and stop.
