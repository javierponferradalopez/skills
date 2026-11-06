---
name: implement-spec
description: Implement every ticket of a spec in parallel, through `/build`, `/harden` and `/gaps`, as one GitButler stack of draft PRs — one branch per ticket.
argument-hint: "#N (the spec: an issue reference, URL or path)"
disable-model-invocation: true
---

# Implement spec

You are the **orchestrator**. Carry every open ticket of a spec through `/build`,
`/harden` and `/gaps` sub-agents to atomic commits on its own branch of one
GitButler **stack**, then open the stack as draft PRs assigned to the user.

You are the **sole writer**: sub-agents implement, attack, judge and plan; you run
every `but` write, one at a time, always naming file or hunk IDs. `/branch`,
`/commit` and `/github-pr` give the plan only — the branch name, the commits, the
PR text — and you execute it with `but`. Invoking this skill is the user's explicit
authorization for this run's `but` writes, tracker assignments and PRs: the user
reviews the draft PRs. The official `but` skill owns command syntax and IDs.

**Argument:** the spec reference, as `docs/agents/issue-tracker.md` defines it.

## 1. Preflight

Any failed check stops the run:

1. `but --version` runs, and the `but` skill is in your skill list. If not, tell the
   user to install them (`but skill install`).
2. `git status --porcelain --untracked-files=all` lists only **hook files**: files
   whose content contains `GITBUTLER_MANAGED_HOOK_V1`.
3. [`scripts/check-stale-stacks`](scripts/check-stale-stacks), run from the repo
   root, prints nothing. Else name each stack it lists.
4. Run `but config forge github-stacks enable`, `but setup` and `but pull`.
5. The base is green: the repo's documented typecheck and test commands, scoped to
   the apps and packages the tickets' Bearings name — the full commands when they
   name none.

## 2. Stack

Fetch the spec, its tickets and the blockers of each ticket, as
`docs/agents/issue-tracker.md` defines them. Sort each ticket:

- **closed**, or **with an open PR** → done. It is a **satisfied** blocker.
- **with a branch and no PR** → earlier work of a previous run: resume it from its
  branch.
- **open**, with no branch → new.

A blocker is **satisfied** once it is done, or once its ticket has its atomic
commits in this run. A ticket with an open blocker outside the spec, or in a blocker
cycle, stops (step 5) before any branch exists.

Order the remaining tickets topologically, ties broken by tracker order. Name each
new branch by step 1 of the `/branch` skill — read its `SKILL.md`: when more than
one type fits, take the dominant one. Then build the stack:

- When the open PRs of this spec already form a stack, `but apply` its top branch,
  and anchor the first branch on it.
- Create each new branch with `but branch new <branch> -A <previous-branch>`; the
  first one with no anchor, `but branch new <branch>`.
- `but apply` each branch to resume, and `but move <branch> --above
  <previous-branch>`.

Done when `but status` shows a single stack holding every branch in that order.

## 3. Schedule

A ticket is **ready** when every blocker is satisfied. Launch the pipeline of every
ready ticket at once, with no concurrency cap: each sub-agent runs in the background,
and a ticket moves to its next step when its sub-agent returns. A ticket is **in
flight** from its launch until its atomic commits, and **claims** every path in the
`Files:` lists it reports.

At launch, assign the ticket to the user, as `docs/agents/issue-tracker.md` defines
it — on GitHub, `gh issue edit <n> --add-assignee @me`.

An escalated **overlap** makes the ticket **wait on** the in-flight ticket whose
`Files:` list claims that path, as one more blocker. If its branch sits below the
blocker's, `but move <branch> --above <blocker-branch>`. Once that blocker is
satisfied, resume the same sub-agent with "Overlap resolved: build on top." and its
pipeline continues.

An escalated **environment need** (an install, a build, the apps running) is yours
to meet: do it, then resume the same sub-agent with "Environment ready."

Done when every ticket has its atomic commits or is stopped.

## 4. Ticket pipeline

**Matching** a `Files:` list: every listed path shows in `but diff`, and no other
ticket in flight claims it. A failed match stops the ticket.
[`scripts/cli-ids`](scripts/cli-ids) `<path>...` prints the IDs of matched paths.

### 4.1 Build

Launch a sub-agent that can edit, with [`briefs/build.md`](briefs/build.md); add its
resume line for a ticket with earlier work. Its return starts with **done**,
**blocked** or **red**: **blocked** and **red** stop the ticket. Keep the report.

### 4.2 WIP commit

Match the `Files:` list. For a new ticket, `but commit -b <branch> -m
"wip(#<ticket-number>)" <hunk-ids>`, and keep the change ID it prints. For a resumed
ticket, `but amend -t <wip-change-id> <hunk-ids>`.

Done when no listed path remains in `but diff`.

### 4.3 Harden

Skip it when the branch holds no code — only docs, ADRs, or config with no logic.

Launch a fresh sub-agent that can edit, with [`briefs/harden.md`](briefs/harden.md).
Match its `Files:` list, an empty list included, and `but amend -t <wip-change-id>
<hunk-ids>` when there are changes. A return that starts with **red** stops the
ticket. Keep the report.

Done when no listed path remains in `but diff`.

### 4.4 Gaps

Launch a fresh read-only sub-agent with the review message of
[`briefs/gaps.md`](briefs/gaps.md). Keep the report. A gap never stops the ticket,
and you never fill one: it goes to the PR comment.

### 4.5 Commit plan

Resume the gaps sub-agent with the plan message of [`briefs/gaps.md`](briefs/gaps.md).

Done when every change in `but diff <branch>` belongs to exactly one planned commit.

### 4.6 Replace the WIP

`but uncommit <wip-change-id>`, then one `but commit -b <branch> -m "<message>"
<hunk-ids>` per planned commit, in plan order.

Done when `but status -fv` shows the branch carrying exactly the planned commits in
order and no WIP, and none of the ticket's paths remain in `but diff`.

## 5. Stopping a ticket

A ticket stops when:

- a sub-agent escalates a question about the product, the spec or another ticket —
  the run never waits for the user;
- a sub-agent returns **red** or fails;
- a match fails, or one of its `but` writes fails.

For each stopped ticket:

1. Stop its running sub-agent, if any, and stop every ticket that depends on it,
   transitively.
2. If it has a branch, put its claimed paths still in `but diff` into its WIP —
   `but amend -t <wip-change-id>`, or `but commit -b <branch> -m
   "wip(#<ticket-number>)"` when it has none — then `but move <branch> --unstack`.
3. Record the ticket, its branch, and the reason; an escalated question verbatim.

The rest of the spec keeps running. The next run of this skill resumes the ticket
from its branch, once the user has answered on the tracker.

## 6. Gate

`but unapply` every stopped ticket's branch, so the working tree is the top of the
stack. Build the packages the stack touches, then run the repo's documented
typecheck and test commands, scoped to the apps and packages it touches.

Done when every command is green. A red gate skips step 7.

## 7. Pull requests

Resume every stack ticket's gaps sub-agent at once with the PR message of
[`briefs/gaps.md`](briefs/gaps.md): the base is the branch below it, or the target
branch for the bottom one.

Then, bottom-up, for each branch:

1. Write its PR message as the title line, a blank line and the description to a
   file outside the repo, so it never lands in `but diff`.
2. `but pr new <branch> -F <file>`, as a draft. When `but pr new` has no draft
   option, run `gh pr ready <branch> --undo` after it.
3. `gh pr edit <branch> --add-assignee @me`.
4. Compose the ticket's report from the **For attention** section of each step that
   ran — [`build`](../build/REPORT.md), [`harden`](../harden/REPORT.md),
   [`gaps`](../gaps/REPORT.md) — as one status line, the **Status** of each step
   joined, then **Look closer**, the items of each step in step order. Write it to a
   file outside the repo, and `gh pr comment <branch> --body-file <file>`.

Done when `gh pr view <branch> --json isDraft,assignees,baseRefName,comments` shows
every stack branch as a draft, assigned to the user, with the branch below it as
base and its report as a comment.

## 8. Summary

Report, in the user's configured language:

- the stack bottom-up, the order to review it in, each branch with its PR link;
- a red gate's failing command and its errors, in place of the links;
- every stopped ticket with its unapplied branch and reason;
- every path left in `but diff` other than hook files.

## 9. Feedback

The repo stays in workspace mode. For each piece of feedback on a PR:

1. Launch a sub-agent that can edit, with [`briefs/feedback.md`](briefs/feedback.md).
2. Match its `Files:` list, then `but commit -b <branch> -m "<message>" <hunk-ids>`:
   always a new commit on top of the branch, leaving published commits untouched.
3. `but push <top-branch>`, without `--with-force` or `--skip-force-push-protection`.
4. Resume that ticket's gaps sub-agent with the PR message of
   [`briefs/gaps.md`](briefs/gaps.md) — when it is gone, launch a fresh read-only
   sub-agent with that message — write its answer to a file outside the repo,
   and `gh pr edit <branch> --title "<title>" --body-file <file>`.

Done when `but status -fv` shows the new commit on its branch, the branches above
restacked on it, nothing left unpushed, and the PR's description covering the fix.

## 10. Teardown

Offer the teardown whenever the review looks finished. On the user's go-ahead,
`but unapply` every applied stack, then run `but teardown --checkout-to
<top-branch>`, so no stack stays marked in the workspace, and `git branch -D
gitbutler/workspace gitbutler/target`. Report the stack branches left behind.
