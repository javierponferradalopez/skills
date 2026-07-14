---
name: catch-up
description: Catch up on the state of delegated work — recurse a ticket's subtasks, match each to its PRs and branches, and report what changed since a chosen date.
disable-model-invocation: true
---

# Catch-up

Brief the user on work they left in the team's hands — reconstructing the state of a task from what the team did across the tracker and the code host.

Three leading ideas run through the skill:

- **Anchor** — the date the catch-up counts from. In **delta** mode it filters every source to what changed since; in **full** mode there is no filter and you report the whole state from the start.
- **State ladder** — each task sits on one rung: _nothing_ → _branch, no PR_ → _open PR_ → _merged PR_. The ladder is how the briefing renders where each task rests now.
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

Synthesise the findings into a **self-contained HTML briefing** written to the **OS temp directory** — never into the repo, and don't write back to the tracker. It's an ephemeral, read-only artifact: one scroll the user reads once.

Follow [`BRIEFING-FORMAT.md`](BRIEFING-FORMAT.md) for structure and house style. Its spine is a **timeline** of what changed since the anchor — the point of a delta catch-up is the change, not the static state — and every beat is a sourced event, so the storytelling never outruns what a finding can prove.

Then open it for the user with a single command (`open <path>`), show a short summary, and **stop**. Read-only, one-shot.
