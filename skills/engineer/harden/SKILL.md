---
name: harden
description: Break a change on purpose and check it against its issue — leaves the tree green and dirty.
argument-hint: "#N | <fixed-point> (an issue ref, a commit/branch/tag, or both)"
disable-model-invocation: true
---

# Harden

Take a change that already works and see whether it **holds**. Two questions, and
neither is about craft — `implement` already held the change to the standards bar:

- **Does it survive attack?** Tests for the holes the building left, and the
  mutants the suite lets live.
- **Is it what was asked for?** A read-only **Spec sub-agent** judges the diff
  against the originating issue.

## Fresh eyes

Judge the code against the spec on its own merits. **The diff is the only
evidence.** A reviewer who leans on how the ticket got built inherits the
implementer's assumptions — the exact bias this pass exists to remove. So even in
the session that wrote the code, and even where you remember why a line reads the
way it does, that line has to defend itself in the diff: no author's report or
commit message to lean on, and none to go looking for.

## 1. Pin what you attack

The working tree picks the diff. Capture the command once — the sub-agent gets the
same one.

- **Dirty tree** → `git diff HEAD`, plus `git status` for the untracked files the
  diff misses. This is the pre-commit pass over work just built.
- **Clean tree, with a fixed point** → `git diff <fixed-point>...HEAD` (three-dot,
  so the comparison is against the merge-base), plus `git log <fixed-point>..HEAD
  --oneline` for the commits that travel. Confirm the ref resolves
  (`git rev-parse`) and the diff is non-empty **here**, not inside a sub-agent.
- **Clean tree, no fixed point** → ask which one, and stop.

When the diff references logic outside it, read the full files for real context.

## 2. Fetch the issue (the spec)

The issue tracker convention should already be in your context — run
`/setup-skills` if not. Find the spec in this order:

1. The issue reference passed as an argument.
2. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`),
   fetched through the tracker workflow.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch or feature.
4. Nothing found → ask where the spec is. If there is none, the spec check skips
   and the report says so.

Fetch it **with its full body and comments**. A PRD with sub-issues reads as
overall intent plus one sub-requirement per sub-issue.

## 3. Baseline — typecheck and test first

Before you change anything, run the repo's **real** typecheck and test commands to
see the starting state. Get them from where the repo documents them — `CLAUDE.md` /
`AGENTS.md`, project memory, a `docs/` runbook. Only if they aren't written down
anywhere, fall back to discovering them (`package.json` scripts, `Makefile`,
README); don't assume `npm`, and don't spelunk in a loop.

Pick up the **mutation** command here too, from the same places — step 5 needs it,
and a repo documenting none skips that half of the attack.

A tree that arrived already red is a finding to **flag** — not a failure to
silently absorb or attribute to yourself.

## 4. Spawn the Spec sub-agent

It is a **read-only reporter**: it reads, it reports, it edits nothing. Every fix
belongs in this window. Give it the diff command from step 1, the commit list where
there is one, and the path or fetched contents of the spec.

The brief: "Report: (a) requirements the spec asked for that are missing or
partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c)
requirements that look implemented but where the implementation looks wrong. Quote
the spec line for each finding. Under 400 words."

Its report has no bearing on the attack, so **start step 5 while it runs**.

## 5. Attack

Two ways to find a hole; both end the same way — *your suite lets a behaviour
through, so write the test that catches it*.

**By hand.** For anything dodgy — fragile logic, unchecked assumptions, tricky
conditions, implicit coercions, missing guards — write a test that exercises it.
If you can break it, **fix it**. Stress the edges: empty, zero, negative, missing
optional fields, null/undefined, repeated or concurrent calls, off-by-one in loops
and slices, regressions in adjacent code. When the issue is a bug report, write
the test that reproduces the original bug and confirm the diff actually fixes it.

**By tooling.** Run the mutation command from step 3 on the green suite and kill
every survivor: a mutant that lives is a behavior change your tests let through,
so each one earns the test that catches it. A repo documenting no mutation command
skips this — say which of the two happened, so a silent skip never reads as a
clean run.

The tests you add match the comment convention of the tests around them — where
those carry no comments, yours carry none.

Done when every mutant is dead and nothing dodgy is left untested.

## 6. Spec findings — flag, never fill

A coverage gap stays a gap and scope creep stays in the diff, both named in the
report for the human to decide. For a PRD, code belonging to an *open* sub-issue is
a scope violation. Where an ambiguous requirement could be read another way that
serves the stated goal better, say so.

This is the frontier: you own the attack, the human owns the product calls.

## 7. Leave the tree green

Re-run the **same** typecheck and test commands from step 3 and leave them green.
If you genuinely can't get there, say so clearly in the report — never hide a red
tree.

## 8. Report — end with it, in prose

Close with the report the human reads, in their configured language. Cover: **what
you broke and fixed**; **tests you added** and what they protect against; **the
spec findings you flagged but did NOT touch** (coverage gaps, scope creep, calls
left to the human); and the **typecheck / test / mutation status** (green, or
exactly what's still failing).

## What this does NOT do

- **No standards review.** The bar belongs to `/implement`, which holds the change
  to it before this pass ever runs.
- **No commit, no push, no branch.** Leave everything uncommitted — committing is a
  separate, deliberate step.
- **No GitHub / PR machinery.** This is local; there is no PR.
