---
name: handoff-grill
description: Pause a grill-me session into a resumable handoff that preserves the open branches of the decision tree, not just the closed decisions. Use when pausing or parking a grill-me / design interrogation to continue later or hand to a teammate.
---

Produce a handoff document following the `handoff` skill's mechanics (save to the OS temp directory, redact secrets, add a suggested-skills section, reference rather than duplicate existing artifacts). Specialise it for **resuming a grill-me**: structure the body around the state of the decision tree.

- **Closed decisions** — what was decided and *why*; for each, the alternatives discarded and the reason. If any have already landed in an ADR or CONTEXT.md, reference them by path instead of restating.
- **Open branches** — every branch of the decision tree left unresolved, each with the context for why it matters. This is the section that lets the next session resume the interrogation instead of reopening it; capture every open branch, not a sample.
- **Provisional assumptions** — what was taken as true to keep moving, still pending validation.
- **Stopping point** — the **frontier** the session paused on: every question of the last round left unanswered, each with its recommended answer, so the next session re-asks that round instead of rebuilding it.

In suggested skills, include `grill-me` to resume the interrogation and `grill-with-docs` if closed decisions still need to land in an ADR / CONTEXT.md.
