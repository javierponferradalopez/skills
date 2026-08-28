---
name: what-it-took
description: Diagnose how much context window this session needed to do what it did, what got buried along the way, and what would have made it cheaper — a throwaway HTML report.
disable-model-invocation: true
---

# What it took

The human just felt this session getting expensive and wants to know where the
window went. The unit is **footprint** — what is *resident* in the window right
now — not the tokens billed along the way. A search repeated twelve times barely
moves the footprint; one 900-line file read moves it once and forever.

The whole analysis runs in a **subagent**, because a transcript runs to hundreds
of thousands of tokens and the point of this skill is to spend the window, not
fill it. Your own job is three steps long.

## 1. Locate this session's transcript

The session id is the last path segment of the scratchpad directory named in
your system prompt (`.../<project-slug>/<session-id>/scratchpad`). The transcript
is `~/.claude/projects/<project-slug>/<session-id>.jsonl`.

Confirm the file exists. If it doesn't, say so and stop — the diagnosis is
evidence-driven, and there is nothing to read.

## 2. Dispatch the subagent

Give it exactly three things: the absolute path to the transcript, the absolute
path to this skill's directory, and the instruction to read
`ANALYSIS.md` in that directory and follow it end to end.

Ask it to return **one line**: the headline figure and the path to the report it
wrote. Everything else it learns stays in its own window, which is the point.

## 3. Hand over the report

Relay that line and open the report (`open <path>` on macOS, `xdg-open` on
Linux). One line in the conversation, the detail on
the page — repeating the findings here would spend the window this skill exists
to protect.
