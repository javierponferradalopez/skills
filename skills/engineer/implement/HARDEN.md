# Harden phase

Take a change that already works and make it **hold**: hold it to the standards bar,
then attack it until your suite catches every break.

## Fresh eyes

From the pack, read only the `Issue` and `Commands` sections. The spec and its
sibling tickets judge scope, and scope is not your job.

You did not write this code, so you carry none of the assumptions that went into it.
**The diff is the only evidence**: `git diff HEAD`, plus `git status` for the
untracked files the diff misses. When the diff references logic outside it, read the
full files for real context.

Your scope is the behavior the diff already has. A requirement the diff does not
cover is a finding for `/gaps`, which runs after you.

## 1. Hold the bar

Read the standards file named in your brief, and the repo's own standards sources —
anything documenting how code should be written here, such as `CODING_STANDARDS.md`
or `CONTRIBUTING.md`. A documented repo standard overrides the standards file. Skip
anything tooling enforces.

Judge every hunk against them, then fix what genuinely bears on correctness,
maintainability or design: reduce nesting, eliminate redundancy, sharpen names,
consolidate logic, and stop short of over-simplifying. **Preserve behavior** —
change only *how* the code works, never *what* it does. Re-run typecheck and tests
and get back to green.

A diff with nothing worth changing is a valid outcome.

## 2. Prune the comments

Invoke **`/prune-comments`** on the change. Done when every comment in the diff has
faced its verdict.

## 3. Attack

Two ways to find a hole; both end the same way — *your suite lets a behavior through,
so write the test that catches it*.

**By hand.** For anything dodgy — fragile logic, unchecked assumptions, tricky
conditions, implicit coercions, missing guards — write a test that exercises it. If
you can break it, **fix it**, and record the fix as a **bug**: it changes what the
code does. Stress the edges: empty, zero, negative, missing optional fields,
null/undefined, repeated or concurrent calls, off-by-one in loops and slices,
regressions in adjacent code. When the issue is a bug report, write the test that
reproduces the original bug and confirm the diff fixes it. The suite is a safety
net: aim first at the paths the existing tests leave uncovered.

**By tooling.** Run the mutation command from the pack on the green suite and kill
every survivor: a mutant that lives is a behavior change your tests let through, so
each one earns the test that catches it. A pack with `none` skips this.

The tests you add match the comment convention of the tests around them — where those
carry no comments, yours carry none.

Done when every mutant is dead and nothing dodgy is left untested.

## 4. Leave the tree green

Re-run the typecheck and test commands from the pack and leave them green. If you
genuinely can't, say exactly what still fails.

## 5. Return

Return, under 200 words:

- **Bugs** — each one you fixed: `file:line` and the behavior before and after.
- **Counts** — tests added, standards fixes.
- **State** — typecheck, test and mutation: green, red with what fails, or mutation
  skipped.
