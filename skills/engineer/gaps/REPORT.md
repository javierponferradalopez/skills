# Gaps report

Write it in the user's configured language. Under an orchestrator, return it in under
400 words.

## Full report

Every status and list of the judgement, grouped. Where an ambiguous requirement could
be read another way that serves the stated goal better, say so. The calls are the
human's: a gap stays a gap, and unasked code stays in the diff.

## For attention

The part of the report that an orchestrator puts in front of the user:

- **Status** — the count of **deferred** requirements.
- **Look closer** — each **real gap**, numbered: a requirement this ticket owns that
  is **missing**, **partial** or **wrong**; then each **unasked**, **unowned** and
  **ambiguous** finding. Each one keeps its spec quote and its `file:line`.
