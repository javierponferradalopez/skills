---
name: done
description: Push the branch and close the issue it finishes — one approval gate, then push, then close.
argument-hint: "[#N] (optional; inferred from the session)"
disable-model-invocation: true
---

# Done

Push what's committed and close the issue it finishes — the last deliberate step
of `implement` → `validate` → `commit` → **`done`**.

No Pull Request: when the work ships through review, that's `/github-pr`.

## 1. Resolve the issue

`/done #N` names it. Without an argument, the issue is the one **this
conversation** already worked (`/implement #N`, `/validate #N`), most recent
winning — the session is the only signal, so when it names none, ask and stop.

Fetch it: the gate needs its **title**, the close comment its **language**.

## 2. Propose push and close together

A dirty tree means the chain skipped `/commit` — name what's uncommitted and stop
there.

Derive the push command from the real state (`git status -sb`). When local history
was rewritten, the command is `git push --force-with-lease` and the proposal
**says that it rewrites remote history**. When nothing is ahead, the proposal
covers the close alone.

Show one proposal — command, the commits that travel, and the issue **by title**,
since a wrong issue is invisible as a bare `#7`:

```
**Push** `git push -u origin HEAD` — no upstream; 2 commits → `origin/feature/x`
- 1a2b3c4 feat(auth): add token refresh endpoint

**Close** #7 «Migración de esquema multi-upstream»
```

Then **stop**. Only the literal `OK` (or `ok`) runs it; anything else → adjust,
re-show, wait.

## 3. Push, then close

The approved command is the only one that runs. A rejected push means the remote
holds commits you lack: report it verbatim and leave the issue open for the human
to resolve — forcing would destroy that work.

A successful push earns the close, commented with the SHAs and branch **in the
issue's language** — without a PR, that line is the only trail from issue to code:

```bash
gh issue close 7 --comment "Cerrada por 1a2b3c4, 5d6e7f8 en master."
```
