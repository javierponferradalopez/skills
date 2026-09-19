---
name: prune-comments
description: Prune comments — every comment in scope faces one test, and the ones carrying no why go; survivors compress to one line. Fires on a freshly implemented or reviewed change, on a path or glob of older code, and on any ask to clean up or audit comments.
---

# Prune Comments

Give every comment in the change a verdict, and prune the ones that haven't earned
their place.

**Scope** — the recent change. Work from what you already hold this session,
otherwise read `git diff HEAD`. An argument overrides it: a path, a glob, a
directory of older code.

**Before judging** — layer the repo's own comment rules on top of the bar below
(`CLAUDE.md` / `AGENTS.md`); on conflict the repo wins. Run the repo's typecheck
and lint once now, so a tree that arrived red is not mistaken for yours.

## The test

> Would a competent reader of this code, without this comment, lose information?

Lost information means a **why** the code cannot express and that is worth knowing:
a workaround, a constraint from outside the file, a decision whose discarded
alternative looks better than it is. Whatever the code already says, the reader
already has.

Three verdicts. **Keep** — the reader would lose something, and the comment is
already tight. **Reduce** — a why sits buried in prose that restates the code;
compress it to the why alone. **Delete** — the reader loses nothing.

A survivor is **one line**; more than one needs a reason you can state.

When deleting leaves the code unclear, **fix the code** — a sharper name, an
extracted function — so there is nothing left to explain.

## The reader already has the repo

Three places outside the file carry what a comment may be restating. Where they
carry it, the comment fails the test: it is a second copy, and the copy goes stale
alone.

- **`CONTEXT.md`** — the glossary. A comment explaining a domain term the glossary
  defines is a duplicate; delete it and let the term do the work. A concept the
  code needs and the glossary lacks is a gap to report, not a comment to keep.
- **`docs/adr/`** — the decisions. A comment arguing why one approach beat another
  is an ADR wearing comment syntax. Where the ADR exists, the survivor is a
  one-line citation of it. Where it doesn't, the decision is worth one — report it.
- **Git** — the history. "now uses X instead of Y", "added to support Z".

## Patterns that fail on sight

- **Narrated preamble** — a block of prose above a method, class, or type telling
  in words what the unit does.
- **Step narration** — `// 1. validate`, `// 2. save`, over code that already reads
  in that order.
- **Restatement** — the line's own logic, said again in words.
- **Obvious docblock** — JSDoc/TSDoc repeating the signature.
- **Section banner** — a ruled comment dividing one file into named regions.

## Judged apart

- **Public API docblocks** — an exported library API is judged by what it gives the
  consumer (autocomplete, generated docs), not by inferability. Keep the ones that
  serve the consumer, pruned to what the consumer needs.
- **Test files** — judged by the tests around them, not by this bar. Match the
  style, wording, and density the surrounding tests already use; where they carry
  no comments, the bar above applies unchanged.
- **`TODO` and `FIXME`** — one the implementation wrote about its own work goes,
  and gets reported: it usually marks work left half-done that belongs in a ticket.
  One older than the scope stays as it is.
- **Functional comments** — `@ts-expect-error`, `eslint-disable*`, `biome-ignore`,
  `prettier-ignore`, `/// <reference>`, `// @vite-ignore`, shebangs, license
  headers, codegen markers. Code wearing a comment's syntax; no verdict.

Every file with comment syntax is in scope — TypeScript, YAML, SQL, Dockerfile,
CSS. A config option's why earns its place through the same test as any other.

## Close

Re-run typecheck and lint. Pruning prose leaves behavior identical, so red means a
functional comment left with the prose — restore that comment.

Then say what you did, in prose, as short as the sweep was. A sweep that changed
nothing says so in one line. Beyond that, only what the human cannot see without
you: **the survivors and the why each carries** — that is what makes the sweep
auditable — plus **code you changed** to absorb a deletion, since that is a code
change and not a comment change, and the **`TODO`s and ADR gaps** you found.
