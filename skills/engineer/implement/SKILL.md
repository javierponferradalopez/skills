---
name: implement
description: Build one issue through three fresh-eyes phases — build, harden, gaps — write its docs with you, and report only what needs your eye; stops with the tree dirty.
argument-hint: "#N [what to complete] (passes an issue URL/path)"
disable-model-invocation: true
---

# Implement

You are the **orchestrator**. You build **one** issue in four steps. Three of them
are phases, and each phase is a sub-agent with **fresh eyes**: it sees the shared
pack and the code, never the thinking of the phase before it. Your window holds
pointers and short returns only — that is where the tokens are saved. The fourth
step is the **docs**: you write them yourself, with the user, before the last phase.

**Argument:** an issue reference — `/implement #N`, a URL, or a path, depending on the
repo's tracker — plus optional **extra instructions**, such as `completa los huecos 1
y 3`. Numbers refer to the last report of this session.

## 1. Write the pack

The **pack** is the material all three phases share. Write it once, as one Markdown
file in a temporary directory outside the repo: the session scratchpad when one
exists, else `mktemp -d`. Outside the repo, it never enters the diff.

The issue tracker convention should already be in your context — run `/setup-skills`
if not. Put in the pack one section per heading, so a phase can read only the ones it
needs:

- `## Issue` — the issue, with its full body and comments.
- `## Spec` — when the issue is a ticket cut from a spec: the spec, and its other
  tickets with their state.
- `## Commands` — the repo's **real** typecheck, test and mutation commands. Get
  them from where the repo documents them — `CLAUDE.md` / `AGENTS.md`, project
  memory, a `docs/` runbook. Only if they aren't written down anywhere, fall back to
  `package.json` scripts, a `Makefile`, the README; don't assume `npm`. A repo that
  documents no mutation command gets `none` on that line.
- `## Extra instructions` — when given, with each gap number resolved to the
  requirement text it names.

Then check the start state:

- Run typecheck and tests; read only the exit status and the failure summary. **Red**
  → say what fails and stop. Work built on a red base cannot tell who broke what.
- A **dirty** tree with no extra instructions → ask whether the diff is earlier work
  on this issue, and stop. With extra instructions, the diff is the base the build
  phase completes.

Done when the pack file exists and the start state is green.

## 2. Run the phases

Run each phase as a foreground `general-purpose` sub-agent, one after the other, on
the current working tree. Pass **pointers, not content**: the brief names the
absolute path of the pack and of the phase file, resolved from this skill's
directory, and restates neither.

1. **Build** — brief: "Read the pack at `<pack>`, then follow `<BUILD.md>`."
   - Returns **blocked** → stop the flow, put its question to the user in prose, and
     send the answer to the **same** sub-agent (`SendMessage`), so it keeps the
     context it loaded.
   - Returns **red** → stop and report what fails. Hardening red code hides the cause.
2. **Harden** — brief: "The pack is at `<pack>`. Follow `<HARDEN.md>`. The standards
   file is `<STANDARDS.md>`." It runs whatever state it leaves.
3. **Docs** — in this window, with the user, for each doc build returned as
   **owed**. This is the human-in-the-loop step, so it runs where the user is.
   Invoke the skill of its kind before you write it:
   - a `CONTEXT.md` term or an ADR — `/domain-modeling`;
   - a skill, an `AGENTS.md` / `CLAUDE.md`, a doc a pointer names —
     `/writing-for-agents`;
   - any other kind a skill in your list or the repo's `CLAUDE.md` / `AGENTS.md`
     covers — that skill.

   Put to the user every question those skills raise, and wait for the answer. Done
   when each owed doc is written, or the user dropped it.
4. **Gaps** — invoke **`/gaps`** with the pack path, on the dirty tree. It judges the
   final diff, so it runs last and runs even when harden ended red.

The orchestrator never fills a gap: a requirement that is missing stays missing until
the user names it in the extra instructions of a later run.

## 3. Report — filter for attention

End with the report the user reads, in their configured language. It is a filter,
not a log: it holds only what the user must decide or look at.

- **One status line**: typecheck / test / mutation (green, red, or mutation skipped),
  plus counts — tests added, standards fixes, deferred requirements.
- **Look closer** — only when there is something, one line each with `file:line`:
  - each **bug harden fixed**: a behavior change nobody asked for;
  - each **real gap** — an owned requirement that is missing, partial or wrong —
    numbered, so the user can name it in the next run;
  - **unasked** behavior, **unowned** spec requirements and **ambiguous** ones;
  - what is still **red**.

An empty **Look closer** leaves the status line as the whole report. What was built,
the standards fixes and the deferred list stay out of it.

## What this does not do

Commit, push, create a branch, or close the issue. Work on the current branch and
leave the tree dirty; `/commit` is the next deliberate step.
