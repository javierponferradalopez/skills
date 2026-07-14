---
name: catch-up
description: Catch up on the state of delegated work — recurse a ticket's subtasks, match each to its PRs and branches, and report what changed since a chosen date.
disable-model-invocation: true
---

# Catch-up

Brief the user on work they left in the team's hands — reconstructing the state of a task from what the team did across the tracker and the code host.

Three leading ideas run through the skill:

- **Anchor** — the date the catch-up counts from. In **delta** mode it filters every source to what changed since; in **full** mode there is no filter and you report the whole state from the start.
- **State ladder** — each task sits on one rung: _nothing_ → _branch, no PR_ → _open PR_ → _merged PR_. The ladder is the spine of the report.
- **Delegate the noise** — the main agent only orchestrates and synthesises. Every noisy search, match, and read happens in a subagent that returns a distilled finding, so the main context never fills with raw PR lists, diffs, or comment threads.

## Step 1 — Frame the catch-up

Establish three things before touching any source:

- **Identifier** — the user gives a reference or link to a ticket. Derive its identifier (e.g. `PD-123`) from that reference; it's the string you'll match PRs and branches against. Don't ask for it — read it off what they gave you.
- **Tracker access** — the `## Agent skills` block points at the issue-tracker doc `/setup-skills` wrote. That doc is the source of truth for which tracker is configured and how to reach it (`gh`, `glab`, ClickUp MCP, local markdown…). Never assume a specific tracker.
- **Anchor** — ask: _full catch-up from the start, or the delta since a date?_ For delta, **propose a date** from the user's last git activity in the repo (`git log --author=<them> -1`) and let them confirm or override; if there's no such activity, just ask for the date. Full mode = no date filter.

Done when you hold `(identifier, tracker access, anchor)`.

## Step 2 — Map the work tree

Read the ticket via the configured tracker and **recurse its hierarchy** (epic → subtasks) into a flat list of task identifiers to resolve. Follow the tracker's own subtask convention; if the tracker has no subtask concept, the single ticket *is* the tree — say so and move on.

## Step 3 — Resolve each task in a subagent

**Fan out one subagent per task**, in parallel. The main agent assembles nothing itself here — it only dispatches and collects distilled findings.

Each subagent, for its identifier, must:

1. Search the code host for **PRs *and* branches** whose name, title, or body cite the identifier — including **branches with no PR yet** (in-flight work that hasn't surfaced). Matching by identifier string is deliberate: it stays independent of any tracker's PR integration.
2. Place the task on the **state ladder** (_nothing_ / _branch, no PR_ / _open PR_ / _merged PR_).
3. Compute the **delta against the anchor**: commits, PR events, review discussion, tracker comments, decisions, blockers, and scope changes since the date (in full mode, the whole history).
4. Return a **distilled finding** — the rung, the PRs/branches/commits/ticket **each with its full URL**, and a short prose delta. Not raw command output. Carry the URLs through: the synthesis can only link what the finding hands it.

**Degrade gracefully.** A source it can't reach (no matching branch, unauthenticated MCP, a tracker with no comments) is a note in the finding, not a failure. Matching by string has a blind spot — if the team never cited the identifier, its PRs won't be found; the finding must say so.

## Step 4 — Synthesise the briefing

Write a markdown file to the **OS temp directory** — never into the repo, and don't write back to the tracker.

**Every reference is a link.** Each PR, commit, branch, and ticket named in the report renders as a clickable markdown link to its URL (`[PD-123](…)`, `[#482](…)`, `[a1b2c3d](…)`) — never a bare identifier. A reference whose URL the finding didn't carry stays plain text and is called out under blind spots.

**Draw the tree when it beats prose.** For an epic with several subtasks, a Mermaid diagram of the subtask tree coloured by rung shows the overall state faster than a list can — put one under the headline. For a single ticket or a handful, prose is clearer; skip it. Same restraint for any graphic: it earns its place only when it reads faster than the words it replaces. Note that Mermaid renders only in Mermaid-aware viewers (VS Code, Obsidian, GitHub preview); in a plain viewer it shows as a code block.

Structure it:

1. **Headline** — the overall state of the epic in a sentence or two.
2. **Per-subtask breakdown** — each task on its rung, with its PRs/branches linked.
3. **What changed since `<anchor>`** — decisions, blockers, scope changes, who did what. This is the point of a delta catch-up; lead with the change, not the static state.
4. **Blind spots** — sources not reached, tasks with no cited identifier, anything the report can't vouch for.

Then show the user a short summary and the file path, and **stop**. Read-only, one-shot.
