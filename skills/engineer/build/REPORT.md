# Build report

Write it in the user's configured language. Under an orchestrator, return it in under
200 words, and start it with **done**, **blocked** or **red**.

## Full report

- the criteria you built, one line each;
- the **decisions**, each with its `file:line` and reason;
- the docs you wrote, one line each: the file, and the term, decision or requirement
  it holds;
- the typecheck, lint and test state: green, or what still fails and what you tried.

## For attention

The part of the report that an orchestrator puts in front of the user:

- **Status** — typecheck, lint and test: green or red.
- **Look closer** — each **decision** with its `file:line` and reason, and what is
  still **red**.
