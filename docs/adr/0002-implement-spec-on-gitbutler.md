# 2. `implement-spec` builds tickets in parallel on GitButler

Date: 2026-11-06

## Status

Accepted

## Context

`implement-spec` builds every ticket of a spec in parallel and opens them as one
**stack** of PRs. Parallel agents need isolation. The obvious path is one git
worktree per ticket. But some of the repos we work in are very large monorepos, where
a worktree per ticket costs too much: each one needs its own install and build.

## Decision

- **GitButler, one shared working tree.** Each ticket is a GitButler branch in the
  same directory. No worktrees.
- **The orchestrator is the sole writer.** Sub-agents edit files only. The
  orchestrator runs every `but` write, naming the file or hunk IDs of one ticket.
  Each sub-agent reports the paths it changed (`Files:`). A path that one ticket
  **claims** makes any other ticket that must change it wait.
- **`/branch`, `/commit` and `/github-pr` plan only.** They give the branch name, the
  commit plan and the PR text. Their git writes (`git switch`, `git commit`,
  `gh pr create`) break a GitButler workspace or its stack metadata, so the
  orchestrator runs `but` in their place.
- **The briefs adapt the leaf skills.** `/build`, `/harden` and `/gaps` stay
  unchanged for the shared tree. The brief gives each sub-agent the diff to read
  and the checks to skip.
- **No approval gates.** Invoking the skill authorizes its writes. The user reviews
  the draft PRs. An escalated question stops its ticket and the tickets that depend
  on it, and the run goes on.

## Considered options

- **One worktree per ticket**, with `/branch`, `/commit` and `/github-pr` as they are
  and `gh stack` for the native stack. Rejected: too expensive in a large monorepo.
- **One ticket after another**, in one working tree. Rejected: no parallelism.

## Consequences

- `implement-spec` needs the `but` CLI and its official skill. Repos with no
  GitButler cannot use it; `/implement` stays the flow for one ticket.
- Agents share dependencies, builds and running apps. The orchestrator owns the
  environment, and each agent scopes its test runs to what it touches.
- The shared-tree rules live in the briefs, so a change to `/build`, `/harden` or
  `/gaps` that reads the diff another way must be checked against the briefs.
