---
name: harden
description: Harden — try to break a change that already works, by hand, and write the test that catches each break; leaves the tree green and dirty. Fires on an explicit ask to harden or break a change, and from `/implement`.
argument-hint: "[#N ticket]"
---

# Harden

Take a change that already works and see whether it **holds**: attack it until your
suite catches every break. The standards bar belongs to `/build`, and the check
against the ticket belongs to `/gaps`.

## 1. Pin the diff

Harden attacks the **dirty tree**: `git diff HEAD`, plus `git status` for the
untracked files the diff misses. A clean tree has nothing to attack: say so, and
stop.

When the diff references logic outside it, read the full files for real context.

## 2. Fetch the ticket

The issue tracker convention should already be in your context — run `/setup-skills`
if not. The ticket is the reference in the argument; with none, attack without it,
and say so in the report.

Fetch it **with its full body and comments**. When it is cut from a spec, read the
spec too. Read both for their **rules**: how the code and the tests must be written
here — for example, which kinds of code get no unit test of their own. A test you add
follows them. Scope is not your job: a requirement the diff does not cover is a
finding for `/gaps`.

## 3. Baseline

Find the repo's **real** typecheck, lint and test commands. Get them from where the
repo documents them — `CLAUDE.md` / `AGENTS.md`, project memory, a `docs/` runbook.
Only if they are not written down, fall back to `package.json` scripts, a
`Makefile`, the README; do not assume `npm`.

Run them before you change anything. A tree that arrived red is a finding to
**flag** — not a failure to absorb in silence or to take as yours.

## 4. Attack

Break the code on purpose. For anything dodgy — fragile logic, unchecked
assumptions, tricky conditions, implicit coercions, missing guards — write a test
that exercises it. Stress the edges: empty, zero, negative, missing optional fields,
null/undefined, repeated or concurrent calls, off-by-one in loops and slices,
regressions in adjacent code. When the ticket is a bug report, write the test that
reproduces the original bug and confirm the diff fixes it. The suite is a safety
net: aim first at the paths the existing tests leave uncovered.

When a test breaks the code, **fix it**, and record the fix as a **bug**: it changes
what the code does.

While you iterate, run only the tests of the area you attack. The tests you add
follow `/tdd` and match the comment convention of the tests around them — where those
carry no comments, yours carry none.

Done when nothing dodgy is left untested.

## 5. Leave the tree green

Run the full test suite, typecheck and lint, one time each, and leave them green. If
you cannot, say exactly what still fails.

## 6. Report

Report in the user's configured language; under `/implement`, return it in under 200
words:

- **Bugs** — each one you fixed: `file:line` and the behavior before and after.
- **Tests added** — how many, and what they protect against.
- **State** — typecheck, lint and test: green, or what fails. Say when the tree
  arrived red, and when no ticket was found.

## What this does not do

Commit, push, or create a branch. Leave everything uncommitted.
