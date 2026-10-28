---
name: build
description: Build one ticket alone, to green, held to the standards bar — no harden, no gaps. Fires on an explicit ask to build a ticket alone, and from `/implement`. The full flow is `/implement`.
argument-hint: "#N [what to complete]"
---

# Build

Build **one** ticket until it works and holds the standards bar, then stop with the
tree dirty. Harden and gaps are separate skills; `/implement` runs all three.

**Argument:** a ticket reference — `#N`, a URL, or a path, depending on the repo's
tracker — plus optional **extra instructions**, such as "complete the validation of
the title". Build only that ticket.

**Under `/implement`** the brief says so. Then you are a sub-agent with no user: you
return your questions, and the orchestrator takes them to the user.

## 1. Fetch the ticket

The issue tracker convention should already be in your context — run `/setup-skills`
if not. Fetch the ticket **with its full body and comments**. When it is cut from a
spec, read the spec too.

## 2. Check the start state

Find the repo's **real** typecheck, lint and test commands. Get them from where the
repo documents them — `CLAUDE.md` / `AGENTS.md`, project memory, a `docs/` runbook.
Only if they are not written down, fall back to `package.json` scripts, a
`Makefile`, the README; do not assume `npm`.

- Run typecheck and tests; read only the exit status and the failure summary. **Red**
  → say what fails and stop. Work built on a red base cannot tell who broke what.
- A **dirty** tree with no extra instructions → ask whether the diff is earlier work
  on this ticket, and stop. With extra instructions, the diff is the base you
  complete: read `git diff HEAD` and `git status`.

## 3. Load context

Read the project's own bar and shape: `CONTEXT.md`, `docs/`, `CLAUDE.md` /
`AGENTS.md`.

When the ticket carries **Bearings**, read there first — they are an estimate of
where the work lands, so they spare you the search, not the reading.

Orient in the repo **surgically**: grep for the seam, read the ranges the grep points
at, and open a whole file when you will edit it. The tests already covering the area
carry the conventions your tests must match.

Done when nothing about the repo is left to find out and you can start editing.

## 4. Implement

Use `/tdd` where possible, at pre-agreed seams. While you iterate, run only the tests
of the area you touch.

Write the **docs** the change needs: each doc the ticket asks for, and each term or
decision your code introduces that the glossary or the ADRs do not hold yet. Invoke
the skill of its kind before you write it:

- a `CONTEXT.md` term or an ADR — `/domain-modeling`;
- a skill, an `AGENTS.md` / `CLAUDE.md`, a doc a pointer names —
  `/writing-for-agents`;
- any other kind a skill in your list or the repo's `CLAUDE.md` / `AGENTS.md`
  covers — that skill.

Where those skills ask for the user's answer, take your recommended answer and go on.

Record each **decision** too: a choice that takes the code away from what the repo
already does — a new dependency, a pattern unlike its neighbours, a port you go
around. Note its `file:line` and a one-line reason.

Done when every acceptance criterion is built — or, with extra instructions, every
item they name — with its docs written, and each one that went through a seam went
**red** before it went green.

## 5. Escalate only when blocked

Work autonomously. Stop only for an ambiguity that neither the ticket, its spec,
`CONTEXT.md`, nor the ADRs resolve: quote the line that is ambiguous and give the
readings you see. Put it to the user in prose and wait; under `/implement`, return
**blocked** with it, and continue when the answer comes back.

## 6. Hold the bar

The code works; now make it hold. **The diff is the only evidence** — you wrote these
lines, so you carry every assumption that went into them. So the judging goes to a
**read-only sub-agent** that has seen nothing but the diff.

Give it:

- The diff: `git diff HEAD`, plus `git status` for the untracked files the diff
  misses.
- The repo's own standards sources — anything documenting how code should be written
  here, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.
- The **absolute path to `STANDARDS.md`**, resolved from this skill's directory.
- The brief: "Read the standards file at the path given, then report — per file/hunk
  where relevant — every place the diff violates (a) a documented repo standard: cite
  the file and the rule; or (b) a rule from that file: name it and quote the hunk. A
  documented repo standard overrides it. Skip anything tooling enforces. Report only
  what bears on correctness, maintainability, or design. Under 400 words."

Then fix what it found, here. **Preserve behavior** — change only *how* the code
works, never *what* it does. A report with nothing worth changing is a valid outcome.

Then invoke **`/prune-comments`** on the change.

## 7. Get to green

Run the full test suite, typecheck and lint, one time each, and get them green.

## 8. Report

Report in the user's configured language; under `/implement`, return it in under 200
words, and start with **done**, **blocked** or **red**:

- the criteria you built, one line each;
- the **decisions**, each with its `file:line` and reason;
- the docs you wrote, one line each: the file, and the term, decision or
  requirement it holds;
- the typecheck, lint and test state: green, or what still fails and what you tried.

## What this does not do

Commit, push, create a branch, or close the ticket. Work on the current branch and
leave the tree dirty.
