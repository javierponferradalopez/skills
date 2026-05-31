---
name: write-adr
description: Creates a lightweight Architecture Decision Record (ADR) in the conversation when a non-trivial technical decision is made: choosing between libraries, change of architectural pattern, decision affecting multiple modules, decision whose "why" won't be obvious in 3 months. On close, asks the user where to deposit it (ADR folder, markdown, ticket, conversation). Standalone — invoke it whenever you detect a decision that deserves to be remembered.
---

# Write ADR

Lightweight ADRs (10-30 lines), not full architecture documents.

## When to write an ADR

DO write:
- Choice among multiple reasonable libraries
- Pattern change (e.g., from transactional script to domain model)
- Decision that breaks a project convention (and why we break it)
- Trade-off that sacrifices something (perf for simplicity, etc.)

DO NOT write:
- Trivial decisions (variable naming)
- Decisions affecting only one file
- "How to do X" (that's documentation, not an ADR)

## Procedure

1. Draft the ADR in the conversation using the template below. Keep it 10-30 lines.
2. For the number, reuse the project's existing ADR sequence if one is already in the conversation or obvious from context; otherwise leave it as `NNNN` and let the user assign it on deposit.
3. Present the draft and wait for the user's reaction before continuing.
4. When the user approves, **ask where to deposit the ADR**. The skill writes nothing on its own — see "Where to deposit" below.

## ADR template

```markdown
# NNNN. <Imperative title: "Use X for Y">

Date: <YYYY-MM-DD>
Status: Accepted | Proposed | Superseded by NNNN

## Context
[Why something needs to be decided. 2-3 sentences.]

## Options considered
- **A**: <description> — pros: ... | cons: ...
- **B**: <description> — pros: ... | cons: ...
- **C**: <description> — pros: ... | cons: ...

## Decision
<Which one we choose>

## Why
[1-2 sentences. What weighed more.]

## Consequences
- Positive: [...]
- Negative: [...]
- To watch: [if something changes, this ADR may become obsolete]
```

## Where to deposit

The ADR lives in the conversation by default. After the user approves it, ask where it should go. Suggest options based on the project's setup, e.g.:

- An ADR folder if the project already keeps one (`docs/adr/`, `adr/`, `decisions/`, …) — confirm the path and the next sequential number before writing.
- A markdown file at a path the user gives.
- The original ticket / PR description / task manager where the decision came from.
- Only the conversation, no persistence.

Only write to disk if the user picks a file destination. Never assume a `docs/adr/` folder exists or create one unprompted.

## Anti-patterns

- ❌ Assuming the project has a `docs/adr/` folder, or writing the file without the user asking. Render in the conversation first.
- ❌ Closing the skill without the explicit destination question.
- ❌ 3-page ADR. If it doesn't fit on one screen, too big.
- ❌ Skipping the discarded options. Their value is for future
  lookups: "why aren't we using X?".
- ❌ ADRs for decisions no longer valid. If a decision changes,
  mark the old ADR as "Superseded by NNNN" and create a new one.
