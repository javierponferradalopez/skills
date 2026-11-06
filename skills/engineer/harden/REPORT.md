# Harden report

Write it in the user's configured language. Under an orchestrator, return it in under
200 words, and start it with **done** or **red**.

## Full report

- **Bugs** — each one you fixed: `file:line` and the behavior before and after.
- **Tests added** — how many, and what they protect against.
- **State** — typecheck, lint and test: green, or what fails. Say when the tree
  arrived red, and when no ticket was found.

## For attention

The part of the report that an orchestrator puts in front of the user:

- **Status** — typecheck, lint and test: green or red; the count of tests added.
- **Look closer** — each **bug** you fixed, as a behavior change nobody asked for,
  with its `file:line`; what is still **red**; a tree that arrived red.
