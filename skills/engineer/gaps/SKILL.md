---
name: gaps
description: Gaps — judge a change against its ticket, read-only: what it meets, misses, gets wrong, adds unasked, and leaves to a sibling ticket. Fires on a dirty tree, a branch, commit or tag, or a PR, and on any ask whether a change does what its ticket asks.
argument-hint: "[#N ticket] [<fixed-point> | PR #N/URL] [pack path]"
---

# Gaps

Judge a change against the ticket it answers, and report. You are a **reporter**:
every finding stays a finding for the human, and the code stays as it is.

## 1. Pin the diff

Pick the **origin** of the diff, and capture its command once — the judge gets the
same one.

- **PR** (a URL, or a number that `gh pr view` resolves to a PR) → `gh pr diff <N>`,
  plus `gh pr view <N> --json title,body,commits` for the body and the commits.
- **Fixed point** (a commit, branch or tag) → `git diff <fixed-point>...HEAD`
  (three-dot, against the merge-base), plus `git log <fixed-point>..HEAD --oneline`.
  Confirm the ref resolves (`git rev-parse`).
- **Dirty tree**, nothing else given → `git diff HEAD`, plus `git status` for the
  untracked files the diff misses.
- **Clean tree**, nothing given → ask which change to judge, and stop.

Confirm the diff is non-empty **here**, not inside the judge.

## 2. Fetch the ticket and its owners

A **pack path** in the argument (from `/implement`) holds the ticket, its spec and
its siblings: use it, and go to step 3.

Else, the issue tracker convention should already be in your context — run
`/setup-skills` if not. Find the ticket in this order:

1. The ticket reference in the argument.
2. References in the PR body or the commit messages (`#123`, `Closes #45`).
3. Nothing found → ask which ticket the change answers, and stop.

Fetch it **with its full body and comments**. When it is a ticket cut from a spec,
also read the spec and list its other tickets with their state. Together they give
each spec requirement an **owner**: this ticket owns its acceptance criteria, and
each sibling owns the requirements it carries. A requirement that an open sibling
owns is **deferred** — planned for that ticket, so it is not a gap in this one.

## 3. Judge with fresh eyes

**The diff is the only evidence.** A judge that leans on how the change got built
inherits the author's assumptions, so the judging goes to a **read-only sub-agent**
that has seen nothing but the diff — even in the session that wrote the code.

Give it the diff command from step 1, the commit list where there is one, and the
pack path or the fetched ticket, spec and siblings with their state.

The brief: "Judge the diff against the requirements this ticket owns. Give each one a
status: **met**; **missing** or **partial**; **wrong** (it looks implemented, but the
implementation looks wrong). Then list: **unasked** — behavior in the diff that no
requirement of this ticket asks for, including code an open sibling owns; **deferred**
— each spec requirement an open sibling owns, with that sibling; **unowned** — spec
requirements no ticket owns; **ambiguous** — requirements that can be read another
way, with that reading. Quote the spec line for each finding and give `file:line` for
each one the diff touches. Under 400 words."

Done when the judge has returned and every finding carries its quote.

## 4. Report

Report every status and list from the judge, grouped, in the user's configured
language. Where an ambiguous requirement could be read another way that serves the
stated goal better, say so. The calls are the human's: a gap stays a gap, and
unasked code stays in the diff.
