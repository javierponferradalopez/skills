---
name: implement
description: Build one issue through `/build`, `/harden` and `/gaps`, each in its own sub-agent for fresh eyes, and report only what needs your eye; stops with the tree dirty.
argument-hint: "#N [what to complete] (passes an issue URL/path)"
disable-model-invocation: true
---

# Implement

You are the **orchestrator**. You build **one** issue with three skills — `/build`,
`/harden`, `/gaps` — one after the other. Each one runs in its own sub-agent, so it
has **fresh eyes**: it never sees the thinking of the step before it. Your window
holds short returns only.

**Argument:** an issue reference — `/implement #N`, a URL, or a path, depending on the
repo's tracker — plus optional **extra instructions**, such as `completa los huecos 1
y 3`. Numbers refer to the last report of this session: resolve each one to the
requirement text it names.

## 1. Run the steps

Each step runs in a new **foreground** sub-agent that can edit files, and you wait
for its return. Send the user one short line as each step starts.

1. **Build** — Brief: "Invoke `/build #N` `<extra instructions>`. You run under an
   orchestrator." Its return starts with one of:
   - **blocked** → put its question to the user in prose, and send the answer to the
     **same** sub-agent, so it keeps the context it loaded.
   - **red** → stop and report what fails. Hardening red code hides the cause.
   - **done** → keep its **decisions** for the report.
2. **Harden** — Brief: "Invoke `/harden #N` on the dirty tree. You run under an
   orchestrator." Skip it when the diff holds no code — only docs, ADRs, or config
   with no logic.
3. **Gaps** — Brief: "Invoke `/gaps #N` on the dirty tree. You run under an
   orchestrator." It judges the final diff, so it runs last and runs even when harden
   ended red.

The orchestrator never fills a gap: a requirement that is missing stays missing until
the user names it in the extra instructions of a later run.

## 2. Report — filter for attention

End with the report the user reads, in their configured language. It is a filter,
not a log: it holds only what the user must decide or look at. Each step defines its
own part in the **For attention** section of its `REPORT.md`:
[`build`](../build/REPORT.md), [`harden`](../harden/REPORT.md),
[`gaps`](../gaps/REPORT.md).

- **One status line** — the **Status** of each step that ran, joined.
- **Look closer** — the **Look closer** items of each step, one line each, in step
  order. The gap numbers let the user name a gap in the next run.

An empty **Look closer** leaves the status line as the whole report.

## What this does not do

Commit, push, create a branch, or close the issue. Work on the current branch and
leave the tree dirty.
