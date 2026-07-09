---
name: validate
description: Review one issue's uncommitted implementation locally, pre-commit, in a clean-room subagent that never sees how the ticket was built — for zero implementer bias. It reads the issue spec and `git diff HEAD`, applies the code-standards bar, actively fixes bugs/edge-cases/quality in place and writes tests to break the code, then flags spec-coverage gaps and scope creep for the human instead of silently filling them. Leaves the tree green and never commits, pushes, branches, or touches GitHub.
argument-hint: "#N (passes an issue URL/path)"
disable-model-invocation: true
---

# Validate

Review the uncommitted changes in the working tree against an issue —
**locally, before any commit**. This is one deliberate step in a
human-in-the-loop flow.

**Argument:** an issue reference — `/validate #N`, a URL, or a path, depending
on the repo's tracker. Review **only** that issue's work.

## Run the review clean-room

A reviewer who watched the ticket get built inherits the implementer's
assumptions — the exact bias this review exists to remove. So the review never
runs in this conversation. It runs in a **clean-room** subagent that has never
seen how the code was written — every run, no matter where you launch it from,
including the very session that built the ticket.

Launch one `general-purpose` subagent and hand it:

- the issue reference (`#N`, URL, or path) **exactly as given**, and
- the absolute path to `REVIEW.md` in this skill's directory.

Instruct it to follow `REVIEW.md` to the letter against the current working
tree (`git diff HEAD`), and to end with the prose report that file describes.

The subagent shares this working tree, so its fixes and new tests land here
uncommitted — the review's whole output. When it returns, **relay its report to
the human verbatim** and add nothing of your own: you launched the review, the
clean-room performed it.
