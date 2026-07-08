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

## Code smells

A checklist to sweep changed code against (Fowler, _Refactoring_, ch.3). Each smell is a
labelled judgement call — flag it as _possible_ X, never a hard violation — and skip
anything tooling already enforces. Three of these already live above: **Mysterious Name**
is the naming demand of _Interface design_ (a name that doesn't reveal what it does or
holds → rename; if no honest name comes, the design's murky); **Speculative Generality**
and **Duplicated Code** are the two halves of _Restraint_ — extract a repeated shape when
both sites change for the **same** reason, but leave look-alikes that change for
**different** reasons alone (the wrong abstraction costs more than duplication).

The rest:

- **Feature Envy** — a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps** — the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession** — a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches** — the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery** — one logical change forces scattered edits across many files. → gather what changes together into one module.
- **Divergent Change** — one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Message Chains** — long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man** — a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest** — a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

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

See the `tdd` skill for GOOD/BAD examples and the full
red-flag list.

## When reviewing

When this skill is used to review rather than write, it is **read-only**: report what
violates the bar, why it matters, and the specific fix — but don't edit the code unless
the user asks afterward. Don't report noise: only flag what genuinely affects
correctness, maintainability, or design, and acknowledge what's done well.
