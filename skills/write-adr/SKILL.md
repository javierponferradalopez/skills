---
name: write-adr
description: Creates a lightweight Architecture Decision Record (ADR) when a non-trivial technical decision is made: choosing between libraries, change of architectural pattern, decision affecting multiple modules, decision whose "why" won't be obvious in 3 months. Standalone — invoke it whenever you detect a decision that deserves to be remembered.
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

1. Locate the project's ADR folder (`docs/adr/`, or create it).
2. Find the next sequential number: `NNNN`.
3. Create `docs/adr/NNNN-kebab-title.md`:

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

## Anti-patterns

- ❌ 3-page ADR. If it doesn't fit on one screen, too big.
- ❌ Skipping the discarded options. Their value is for future
  lookups: "why aren't we using X?".
- ❌ ADRs for decisions no longer valid. If a decision changes,
  mark the old ADR as "Superseded by NNNN" and create a new one.
