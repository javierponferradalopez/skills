---
name: code-standards
description: A language-agnostic quality bar for generating and validating good code, focused on what models get wrong by default — deep modules, designing errors out of existence, behavior-driven tests that mock only at boundaries, and restraint against speculative abstraction. Use when writing, reviewing, refactoring, or judging code in any language, or when the user references coding standards, clean code, deep modules, or asks whether code is clean, maintainable, or well designed.
---

# Code Standards

## Reconcile with the repo first

This is the universal floor. Layer the repo's own rules on top — on conflict, the repo
wins. Read `AGENTS.md` / `CLAUDE.md`, and any `CONTEXT.md` or `docs/adr/`, before judging.
Team-specific rules added to this file take priority over everything below.

## Interface design

**Deep modules** — small interface, deep implementation: a few methods with simple
params hiding complex logic behind them. Avoid shallow modules (a large interface that
just forwards to a thin implementation) and pass-through classes. When designing, ask:
can I reduce the number of methods? Simplify the params? Hide more complexity inside?

**Design for testability**:

1. **Accept dependencies, don't create them** — pass external deps in rather than
   constructing them internally.
2. **Return results, don't produce side effects** — a function that returns a value is
   easier to reason about and test than one that mutates state.
3. **Small surface area** — fewer methods = fewer tests; fewer params = simpler setup.

**Scrutinize optional parameters** — a major source of bugs by omission. Prefer
correctness over backwards compatibility.

## Design errors out of existence

Prefer designs that remove special cases over code that handles them. Return an empty
collection instead of a null/nil sentinel; where the language allows, make invalid states
unrepresentable (sum types, enums, required fields that travel together) instead of
guarding against them at every call site.

## Restraint

- **No speculative generality.** No config, layers, or abstraction "just in case." Build
  for the case in front of you, not an imagined future one.
- **Don't force DRY.** Two fragments that look alike today but change for different
  reasons should stay separate. The wrong abstraction costs more than duplication.
- **Conceptual integrity.** Solve the same kind of problem the same way sibling modules
  do. Coherence across the system beats any single clever feature.

## Comments

Comments earn their place by explaining **why**, not narrating **what**. The default is
*no comment* — the code itself is the documentation, so make it read clearly instead of
annotating it.

Before writing any comment, run this gate: **can a better name or a smaller function
remove the need?** If yes, do that and write no comment. Only when the reasoning still
isn't recoverable from the code does a comment belong — and only for one of these:

- a non-obvious constraint or invariant,
- a workaround and the cause that forces it,
- a deliberate trade-off or a rejected obvious alternative,
- a link to a spec, issue, or external reference.

That list is exhaustive. If a comment doesn't fit it, delete it.

Never add:

- **Narration** that restates the next line (`// increment counter`, `// loop over users`).
- **Change/process markers** — `// added`, `// new`, `// fixed`, `// was: ...`,
  `// TODO(me)` left from your own edit. History lives in git, not the source.
- **Section banners and decorative dividers** that just label structure the code already shows.
- **Restated signatures** — docstrings that repeat the parameter list in prose without
  adding meaning.

Match the file's existing comment density and style. When in doubt, delete the comment and
let a better name or a smaller function carry the intent instead.

## Testing

Tests verify **behavior through public interfaces, not implementation details**. Code can
change entirely; tests shouldn't break unless behavior changed.

- Test what callers care about, through the public API only.
- One logical assertion per test.
- Mock only at **system boundaries** (external APIs, time/randomness, FS/DB when no real
  instance is practical). **Never mock your own modules or internal collaborators** — if
  something is hard to test without that, redesign the interface.
- Don't test trivial one-liners or thin delegation; the test just mirrors the code.

See [references/testing.md](references/testing.md) for GOOD/BAD examples and the full
red-flag list.

## When reviewing

When this skill is used to review rather than write, it is **read-only**: report what
violates the bar, why it matters, and the specific fix — but don't edit the code unless
the user asks afterward. Don't report noise: only flag what genuinely affects
correctness, maintainability, or design, and acknowledge what's done well.
