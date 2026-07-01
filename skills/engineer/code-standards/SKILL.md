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

**Do not add comments. Code must be self-explanatory.** A comment you're about to
write is a signal the code isn't clear enough — fix the code, don't annotate it.

When you feel the urge to comment, do one of these instead:

- **Rename** the variable, function, or type so the intent lives in the name.
- **Extract** the block into a well-named function that says what the comment would have.
- **Restructure** so the control flow makes the reasoning obvious.

This is absolute for production code. Never emit narration (`// increment counter`),
change/process markers (`// added`, `// fixed`, `// was: ...`, `// TODO(me)`), section
banners, restated signatures, or docstrings that paraphrase the code. Delete any comment
you'd otherwise write, and never carry comments over from examples, scaffolding, or the
surrounding file into the code you produce.

**Test files are the exception**: comments are fine there as long as they follow the
project's own testing convention (if one exists) and stay consistent with the existing
tests. Be continuist — match the style, wording, and density the surrounding tests
already use, and never introduce a commenting pattern they don't. When the existing
tests carry no comments, add none.

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
