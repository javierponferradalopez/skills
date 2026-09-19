---
name: implement
description: Build one issue end-to-end and hold it to the standards bar — stops with the tree dirty, no commit, push, branch, or issue close.
argument-hint: "#N (passes an issue URL/path)"
disable-model-invocation: true
---

# Implement

Build **one** issue end-to-end, then **stop and leave the working tree dirty**.
This is one deliberate step in a human-in-the-loop flow.

**Argument:** an issue reference — `/implement #N`, a URL, or a path,
depending on the repo's tracker. Implement **only** that issue.

## 1. Fetch the issue

The issue tracker convention should already be in your context — run
`/setup-skills` if not. Fetch the given issue **with its full body
and comments**, and pull in its parent PRD if it has one.

## 2. Load context

Before writing code, read the project's own bar and shape: `CONTEXT.md`,
`docs/`, `CLAUDE.md` / `AGENTS.md`.

When the issue carries **Bearings**, read there first — they are an estimate of
where the work lands, so they spare you the search, not the reading.

Orient in the repo **surgically**: grep for the seam, read the ranges the grep
points at, and open a whole file when you'll edit it. Nothing you read leaves
this window, so read what you'll use.

The tests already covering the area are material you'll use: they carry the
conventions the tests you're about to write have to match.

Done when nothing about the repo is left to find out and you can start editing.

## 3. Implement (TDD where feasible)

Use `/tdd` where possible, at pre-agreed seams.

Done when every acceptance criterion is built, and each one that went through a
seam went **red** before it went green.

## 4. Autonomy & escalation

Work autonomously — no plan-approval gate. Escalate to the user (**in prose, no
interactive prompts**) **only** for a blocking ambiguity that neither the issue,
its PRD, `CONTEXT.md`, nor the ADRs resolve. Don't guess blindly; don't ask
about everything either.

## 5. Feedback loop

Before stopping, run the repo's **real** typecheck and test commands and get them
green. Get them from where the repo documents them — `CLAUDE.md` / `AGENTS.md`,
project memory, a `docs/` runbook. Only if they aren't written down anywhere, fall
back to discovering them (`package.json` scripts, `Makefile`, README); don't assume
`npm`, and don't spelunk in a loop.

## 6. Hold the bar

The code works; now make it hold. **The diff is the only evidence** — you wrote these
lines, so you carry every assumption that went into them, and the assumptions are what
a bar exists to catch. Judging from memory judges your intent, not the code. So the
judging goes to a **read-only sub-agent** that has seen nothing but the diff.

Give it:

- The diff: `git diff HEAD`, plus `git status` for the untracked files the diff misses.
- The repo's own standards sources — anything documenting how code should be written
  here, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.
- The **absolute path to `STANDARDS.md`**, resolved from this skill's own directory.
  The sub-agent reads it itself — this window never loads it.
- The brief: "Read the standards file at the path given, then report — per file/hunk
  where relevant — every place the diff violates (a) a documented repo standard: cite
  the file + the rule; or (b) a rule from that file: name it and quote the hunk. A
  documented repo standard overrides it. Skip anything tooling enforces. Report only
  what genuinely bears on correctness, maintainability, or design, and say what the
  diff does well. Under 400 words."

**Then fix what it found, here.** Reduce nesting, eliminate redundancy, sharpen names,
consolidate logic. **Preserve behavior** — change only *how* the code works, never
*what* it does. Re-run typecheck and tests and get back to green.

A report that finds nothing worth changing is a valid outcome. Only touch what
genuinely needs it.

## 7. Prune the comments

Invoke **`/prune-comments`** on the change. Done when every comment in the diff has
faced its verdict.

## 8. Stop — leave it dirty

When the issue is done:

- **Do NOT** commit, push, create a branch, or close the issue. Work on the
  current branch; branches are the user's concern.
- End with a short summary: what you built, key decisions, what the standards pass
  changed, and the typecheck / test status.
