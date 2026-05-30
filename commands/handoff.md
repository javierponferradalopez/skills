---
description: Compresses the state of the current task into a self-contained markdown to resume it later (you or someone else). It's the only point of the system that persists anything to disk.
---

# /handoff

Pickle of the state of an in-progress task so a fresh session — you or someone else — can resume it without losing context. It's the only point of the system that persists anything to disk: everything else lives in the conversation.

## Inputs

- The current conversation (the main thing): what's been discussed, decided, what `<!-- GRILL RESULT -->` blocks, plans or subtask lists have been emitted.
- Repo state: `git status`, `git diff`, `git log` since the merge-base.
- Whatever the user considers relevant that isn't in the above.

## Procedure

1. Compute `$HARNESS` and ask the user for the `<task-id>` (or suggest one from the branch / current task title: `YYYYMMDD-HHMM-<slug>`).
2. Walk the conversation and identify:
   - What the original task was and why it exists.
   - Decisions made and the reason (especially the non-obvious ones).
   - Current state: what's done, what's half-done, what's pending.
   - The concrete next step on resume.
   - Open risks or doubts.
3. Collect from the repo: current branch, last commit, uncommitted modifications, tests green/red.
4. Write the handoff following the Output format. Be dense, not prose.
5. Redact any secrets (keys, passwords, PII).
6. Ask the user whether they want to review the handoff before writing it. After their OK, write `$HARNESS/<task-id>/handoff.md`.

## Output

`~/harness/<slug>/<task-id>/handoff.md`:

````markdown
# Handoff: <task title>

**Task ID**: <task-id>
**Date**: <YYYY-MM-DD>
**Branch**: <git branch>
**Who takes over**: <future me | someone else>

## 1-minute summary
[What the task is, why it exists, where you are. 3-5 sentences.]

## Current state
- Done: …
- Half-done: …
- Pending: …

## Concrete next step
[Exactly what to do when opening the next session. Zero friction. Example: "open src/foo.ts line 42 and finish the missing branch of the switch".]

## Decisions that matter
- <decision + why> — only if not already in an ADR or a commit message.

## Open risks / doubts
- …

## Repo state
- Branch: `<branch>`
- Last commit: `<sha> — <subject>`
- Uncommitted modifications: <short list>
- Tests: <green/red/not run>

## References
- Ticket / origin: <URL if any>
- Related ADRs: `docs/adr/NNNN-*.md`
- Relevant commits: `<sha>`, `<sha>`, …
````

## Anti-patterns

- ❌ Vague handoff like "I'm halfway". The next step must be concrete: "open file X, finish Y".
- ❌ Restating what's already in commits or ADRs. Link it instead of copying.
- ❌ Assuming you'll remember the context in a week. You won't.
- ❌ Suggesting which skill to run next. That decision is the user + agent's in the next session.
