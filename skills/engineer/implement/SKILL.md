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

1. **Build** — Brief: "Invoke `/build #N` `<extra instructions>`. You run under
   `/implement`." Its return starts with one of:
   - **blocked** → put its question to the user in prose, and send the answer to the
     **same** sub-agent, so it keeps the context it loaded.
   - **red** → stop and report what fails. Hardening red code hides the cause.
   - **done** → keep its **decisions** for the report.
2. **Harden** — Brief: "Invoke `/harden #N` on the dirty tree. You run under
   `/implement`." Skip it when the diff holds no code — only docs, ADRs, or config
   with no logic.
3. **Gaps** — Brief: "Invoke `/gaps #N` on the dirty tree. You run under
   `/implement`." It judges the final diff, so it runs last and runs even when harden
   ended red.

The orchestrator never fills a gap: a requirement that is missing stays missing until
the user names it in the extra instructions of a later run.

## 2. Report — filter for attention

End with the report the user reads, in their configured language. It is a filter,
not a log: it holds only what the user must decide or look at.

- **One status line**: typecheck / lint / test (green or red), plus counts — tests
  harden added, deferred requirements.
- **Look closer** — only when there is something, one line each with `file:line`:
  - each **decision** build made, with its reason;
  - each **bug harden fixed**: a behavior change nobody asked for;
  - each **real gap** — an owned requirement that is missing, partial or wrong —
    numbered, so the user can name it in the next run;
  - **unasked** behavior, **unowned** spec requirements and **ambiguous** ones;
  - what is still **red**.

An empty **Look closer** leaves the status line as the whole report. What was built
and the deferred list stay out of it.

## What this does not do

Commit, push, create a branch, or close the issue. Work on the current branch and
leave the tree dirty.
