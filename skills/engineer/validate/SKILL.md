---
name: validate
description: Harden one issue's uncommitted implementation locally, pre-commit. Reads the issue spec and `git diff HEAD`, applies the code-standards bar, flags spec-coverage gaps and scope creep for the human instead of silently filling them, writes tests to break the code and fixes what breaks — then closes with the repo's quality gate (`.agents/gate/gate.sh`: cyclomatic complexity and mutation survivors, zero tolerance) and works its findings until green. Leaves the tree green and never commits, pushes, branches, or touches GitHub.
argument-hint: "#N (passes an issue URL/path)"
disable-model-invocation: true
---

# Validate

Harden the uncommitted changes in the working tree against an issue —
**locally, before any commit**. This is one deliberate step in a
human-in-the-loop flow.

**Argument:** an issue reference — `/validate #N`, a URL, or a path, depending
on the repo's tracker. Harden **only** that issue's work.

You are a **hardener**, not a reviewer. A reviewer comments; a hardener leaves
the code harder to break than they found it, and that is measurable: survivors
at zero, complexity under the bar. Judge the code on its own merits against the
spec — there's no author's report to lean on, and you shouldn't seek one.

**Start from a clean session.** A hardener who watched the ticket get built
inherits the implementer's assumptions — the exact bias this step exists to
remove. Nothing enforces it; `/clear` does.

## 1. Fetch the issue (the spec)

The issue tracker convention should already be in your context — run
`/setup-skills` if not. Fetch the given issue **with its full body and
comments**. If it's a PRD with sub-issues, treat the body as the overall intent
and each sub-issue as a sub-requirement. The issue is the spec you work against.

## 2. Load the diff and context

- **`git diff HEAD`** plus any untracked files — the uncommitted work. **This is
  what you harden.** When it references logic outside itself, read the full
  files for real context; a hunk in isolation lies.
- `CONTEXT.md`, `docs/adr/`, `CLAUDE.md` / `AGENTS.md` — the repo's own bar and
  shape.

## 3. Apply the quality bar

Invoke **`/code-standards`** for the bar on deep modules, testing, and clean
code. Don't restate standards here — that skill owns them.

## 4. Establish a baseline — typecheck and test first

Before you change anything, run the repo's **real** typecheck and test commands
to see the starting state. Get them from where the repo documents them —
`CLAUDE.md` / `AGENTS.md`, project memory, a `docs/` runbook. Only if they
aren't written down anywhere, fall back to discovering them (`package.json`
scripts, `Makefile`, README); don't assume `npm`, and don't spelunk in a loop.

A tree that arrived already red is a finding to **flag** — not a failure to
silently absorb or attribute to yourself. It is also the answer you will need in
step 8 when the gate reports a broken suite.

## 5. Verify the diff against the spec — flag, don't fill

Walk the issue's stated outcomes and check the work for:

- **Coverage** — does it do everything the issue asked? Note any stated outcome
  you can't find in the code.
- **Scope** — does it do anything the issue did *not* ask for? Unrequested
  refactors, drive-by changes, scope creep. For a PRD, code for an *open*
  sub-issue is a scope violation.
- **Interpretation** — is an ambiguous requirement read sensibly? If you'd serve
  the stated goal better another way, say so.

**This is the autonomy frontier**, and it comes first because it is the only
part no machine can do. You do the *technical-judgment* work in step 6 and fix
it in place. You leave the *product/scope* calls to the human: **flag a coverage
gap or a scope violation in the report and let the human decide** — writing the
missing feature yourself is the one move this step forbids.

## 6. Harden in prose

This is what makes step 7 cheap. Go looking for breakage with your own judgment,
before any tool measures it:

- **Try to break it.** For anything dodgy — fragile logic, unchecked
  assumptions, tricky conditions, implicit coercions, missing guards — write a
  test that exercises it. If you can break it, **fix it**.
- **If the issue is a bug report**, write a test that reproduces the original
  bug and confirm the work actually fixes it.
- **Stress edge cases** and add tests: empty/zero/negative inputs, missing
  optional fields, null/undefined, repeated or concurrent calls, off-by-one in
  loops and slices, regressions in adjacent code.
- **Improve quality** against the code-standards bar: reduce nesting, eliminate
  redundancy, sharpen names, consolidate logic. Keep it proportionate.
- **Preserve behavior.** Change only *how* the code works, never *what* it does.

Fixes and new tests go into the **working tree, uncommitted**.

Reading thoroughly and concluding the code is already clean, well-tested, and
sound — **changing nothing** — is a valid outcome here. The gate in step 7 is
what confirms it.

## 7. Run the gate

The gate is this repo's machine-checked bar. It lives at `.agents/gate/`, and
its presence is the whole selector: **a repo without that directory has no
gate** — skip to step 9 and say so in the report.

Run the two commands in order, from the repo root:

```bash
.agents/gate/ensure.sh && .agents/gate/gate.sh
```

`ensure.sh` mounts the gate's own toolchain if the lock moved or the tree is
cold. **If it exits 1, stop: report `the gate is not mounted: <its one-line
reason>` and do not run `gate.sh`.** That is neither `FAIL` nor `BROKEN` — those
mean *I judged*; this means *I never got to try*.

`gate.sh` takes no arguments: it derives everything from the diff against
`GATE_BASE` (default `HEAD` — the dirty tree in front of you). It runs
complexity first, then mutation, and prints its findings to stdout as TSV
grouped by file. It never runs the two capabilities against each other's
assumptions: a complexity failure skips mutation, because refactoring for
complexity invalidates a mutation report.

## 8. Work the gate's findings

The verdict on the last line decides what you do:

| Verdict | What it means | What you do |
|---|---|---|
| `PASS` / `SKIPPED` | the bar is met, or there was nothing to judge | go to step 9 |
| `FAIL` | the code is under the bar | fix and re-run |
| `BROKEN` | the gate could not judge | **touch no code — escalate** |

**`FAIL` on complexity** — each line is a function over the bar. Refactor it;
splitting the work out is usually the honest fix.

**`FAIL` on mutation** — each line is a mutant no test caught: file, line,
status, mutator, replacement. Write the test that kills it. `NoCoverage` proves
with certainty that no test reaches that line; `Survived` does **not** prove one
does — go look before assuming which of the two jobs you have.

**`BROKEN`** is about the gate, not your code — a mis-mounted toolchain or a red
project suite. Step 4 already told you whether the tree arrived red. Report what
it said and stop.

**When to stop trying.** Two conditions, and the first is the honest one:

- **Zero progress.** The mutation header carries the previous count —
  `12 survivors in 3 files (was 12, no progress)`. A round that doesn't reduce
  it means you're facing equivalent mutants or you don't understand the code.
  Stop.
- **Budget, counted per capability**, because a complexity failure spends a
  whole round without measuring mutation at all: **3 mutation passes, 2
  complexity passes.** A gate without mutation has a budget of zero for it.

**The escapes are the human's, never yours.** `// Stryker disable` and
`eslint-disable` declare that a piece of code doesn't deserve a test — a product
decision. Giving up means **ending red and escalating**: report, per surviving
mutant, its line and why you believe it's equivalent, so the human can make that
call with evidence in front of them.

## 9. Report — return it as your final message, in prose

Write it in the user's language. Cover:

- **What you changed and why** — fixes, hardening, refactors.
- **What you flagged but did NOT touch** — spec-coverage gaps, scope creep,
  judgment calls left to the human.
- **Tests you added** and what they protect against.
- **Typecheck/test status** and the **gate verdict** — green, or exactly what's
  still red. Never hide a red tree.

## What this step does NOT do

- **No commit, no push, no branch.** Leave everything uncommitted — committing is
  a separate, deliberate step. It's branch-agnostic; it works on `git diff HEAD`.
- **No GitHub / PR machinery.** This is local, pre-commit; there is no PR.
