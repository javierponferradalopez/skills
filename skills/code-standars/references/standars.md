# JS/TS code standards

Catalogue of rules for the review. Each category groups rules with their **default severity**
and the **source** of the principle. The default severity is a starting point: adjust it to
the real impact in the context you're reviewing.

> How to read it: for each rule, "Flag when…" describes the symptom to look for in the code.

## Index
1. Naming
2. Functions
3. Comments and documentation
4. Structure and formatting
5. Error handling
6. Complexity and module design
7. Duplication (DRY)
8. Coupling and dependencies
9. TypeScript: types and safety
10. Async and side effects
11. Testability
12. Conceptual integrity
13. Team-specific standards

---

## 1. Naming
*(Source: Clean Code; Domain-Driven Design)*

- **Intention-revealing names.** Flag when a name forces you to read the implementation to
  know what it is (`data`, `tmp`, `info`, `handle`, `doStuff`, `x`). Severity: 🟡 Minor
  (🟠 if it's in a public API or a core domain name).
- **Names that don't mislead.** Flag when a name promises something different from what it
  does (a `getUser` that also writes to the DB; an `isValid` that throws). Severity: 🟠.
- **Domain language.** Flag when the code invents terms instead of using the business
  vocabulary, or mixes languages/synonyms for the same concept
  (`client`/`customer`/`user` interchangeably). Severity: 🟡.
- **Lexical consistency.** One verb per concept (`get` vs `fetch` vs `retrieve` mixed without
  criteria). Severity: 🟡.

## 2. Functions
*(Source: Clean Code; Refactoring; Code Complete)*

- **Single responsibility / single level of abstraction.** Flag when a function mixes
  high-level decisions with low-level details, or does several separable things joined by
  "and" ("validate **and** save **and** notify"). Severity: 🟠.
- **Size.** Long functions are a smell, not a rigid numeric limit. Flag functions that don't
  fit in your head at a glance (rough guide: >40–50 lines, or many responsibilities).
  Severity: 🟠 (🔴 if it's also untestable and unintelligible).
- **Few parameters.** Flag long parameter lists (rough guide: >3–4), especially control
  booleans (`render(true, false, true)`). Suggest an options object or grouping into a type.
  Severity: 🟡 (🟠 with multiple boolean flags).
- **No hidden side effects.** Flag functions that promise one thing and mutate external state
  along the way. Severity: 🟠.
- **Command/query separation.** A function either returns a value or changes state, not both
  without need. Severity: 🟡.

## 3. Comments and documentation
*(Source: Clean Code; A Philosophy of Software Design)*

- **A comment is no substitute for clear code.** Flag comments that explain what a line does
  when it would be better understood by renaming or extracting. Severity: 🟡.
- **Comments that provide the "why".** Good: comments that explain decisions, trade-offs, or
  non-obvious context. That's what code can't capture. Don't flag.
- **No stale or dead comments.** Flag commented-out code, old ownerless TODOs, or comments
  that no longer describe the code. Severity: 🟡 (🟠 if the comment lies about current
  behavior).
- **Interface documentation.** For public/exported APIs, flag a missing description of the
  contract (what it expects, what it returns, what errors it throws). Severity: 🟡.

## 4. Structure and formatting
*(Source: Clean Code; Code Complete)*

- **Deep nesting.** Flag pyramids of nested `if`/`for`/`try` (rough guide: >3 levels). Suggest
  early returns or guard clauses. Severity: 🟡 (🟠 if it seriously hurts readability).
- **Vertical proximity.** Things used together should sit together; related things, close.
  Flag variables declared far from their use. Severity: 🔵.
- **Formatting consistency.** Assume there is a linter/formatter (ESLint/Prettier). Don't
  report style that a tool fixes automatically unless there clearly is no formatter.
  Severity: 🔵.

## 5. Error handling
*(Source: Clean Code; A Philosophy of Software Design; Code Complete)*

- **Don't swallow errors.** Flag empty `catch` blocks or ones that only `console.log` and
  carry on as if nothing happened. Severity: 🔴.
- **Don't use errors for normal control flow.** Flag exceptions thrown and caught like a
  `goto`. Severity: 🟠.
- **Fail early and with context.** Flag missing validation at boundaries (user input, external
  data) or generic errors with no context (`throw new Error("error")`). Severity: 🟠.
- **Don't return `null`/`undefined` as a silent sentinel** where a value is expected; or
  failing to check it in the consumer. Prefer types that make the invalid state impossible.
  Severity: 🟠.
- **Promises without rejection handling.** Flag `async`/promises with no `catch` and no clear
  propagation. Severity: 🟠 (🔴 if it silences critical failures).

## 6. Complexity and module design
*(Source: A Philosophy of Software Design; The Pragmatic Programmer)*

- **Deep modules, not shallow ones.** Flag modules/classes whose interface is almost as complex
  as their implementation (lots of surface, little hidden value), or "passthrough classes" that
  only forward calls. Severity: 🟠.
- **Information hiding.** Flag implementation details that leak through the interface and force
  the caller to know the internals. Severity: 🟠.
- **Accidental complexity.** Flag solutions more complicated than the problem requires:
  unnecessary layers, premature abstractions, indirection with no payoff. Severity: 🟠.
- **"Errors that shouldn't exist".** Where possible, flag designs that force handling many
  special cases that a different design would eliminate (e.g. returning an empty list instead
  of `null`). Severity: 🟡.
- **Design patterns with judgment.** Flag patterns (Factory, Singleton, Observer…) applied
  where a simple function would do. The pattern is a means, not an end. Severity: 🟡.
  *(Source: Design Patterns — over-application caveat)*

## 7. Duplication (DRY)
*(Source: The Pragmatic Programmer; Refactoring)*

- **Duplicated knowledge.** Flag the same logic/business rule repeated in several places (not
  mere textual coincidence). Severity: 🟠 (🔴 if it's critical logic that will diverge).
- **No DRY by force.** Careful: two chunks that look alike today but respond to different
  reasons to change should NOT be unified. Flag forced abstractions just like duplication.
  Severity: 🟡.

## 8. Coupling and dependencies
*(Source: The Pragmatic Programmer; Working Effectively with Legacy Code)*

- **Law of Demeter.** Flag long chains that dig into other objects' internals
  (`a.b().c().d().e`). Severity: 🟡.
- **High coupling.** Flag modules that know too much about one another or depend on concrete
  details instead of abstractions. Severity: 🟠.
- **Injectable dependencies / seams.** Flag hard dependencies (side-effect imports, `new`-ing
  heavy services inside the logic, direct access to `Date.now()`, network or DB with no
  substitution point) that prevent testing. Severity: 🟠.

## 9. TypeScript: types and safety
*(Source: idiomatic TS + A Philosophy of Software Design + Clean Code applied to types)*

- **Avoidable `any`.** Flag `any` that voids type checking, especially at public boundaries.
  Suggest `unknown` + narrowing, generics, or concrete types. Severity: 🟠
  (🔴 in a public API or an external-data boundary).
- **Dangerous type assertions.** Flag `as` that lies to the compiler (`as unknown as X`,
  non-null `!` with no real guarantee). Severity: 🟠.
- **Model impossible states out of existence.** Flag loose types that allow invalid states
  (optional fields that actually go together). Suggest discriminated unions. Severity: 🟡.
- **No implicit types on exports.** Flag exported functions/objects without an explicit return
  type when the inferred one is fragile or unclear. Severity: 🔵.
- **`strict` assumed.** If the code relies on `null`/`undefined` without checking, note that it
  should compile in strict mode. Severity: 🟡.

## 10. Async and side effects
*(Source: idiomatic JS/TS + Clean Code)*

- **`async/await` over nested, unreadable `.then` chains.** Severity: 🔵.
- **Wasted or mishandled concurrency.** Flag serial `await` inside a loop when the calls could
  run in parallel (`Promise.all`), or `Promise.all` where a partial failure matters and you
  need `allSettled`. Severity: 🟡.
- **Pure functions where possible.** Flag business logic intertwined with I/O that could be
  separated to be testable and predictable. Severity: 🟡.
- **No obvious race conditions** and no shared mutable state without control. Severity: 🟠 when
  you spot it.

## 11. Testability
*(Source: Working Effectively with Legacy Code)*

- **The code is testable.** Flag logic that's hard to test due to hard dependencies, lack of
  seams, or functions that mix decision and effect. Severity: 🟠.
- **Important logic without tests.** If the scope includes tests, flag business logic or error
  branches without coverage. Severity: 🟠 (don't invent missing tests if you can't see them).

## 12. Conceptual integrity
*(Source: The Design of Design / The Mythical Man-Month — Fred Brooks)*

- **Design coherence.** Flag when the code solves the same kind of problem in different ways
  for no reason (three error-handling styles, two ways of injecting dependencies, inconsistent
  conventions between sibling modules). A system's coherence is worth more than any single
  loose feature. Severity: 🟠.
- **Second-system effect.** Flag over-engineering: generality and configurability built "just
  in case" with no real use case. Severity: 🟡.

---

## 13. Team-specific standards

> Section reserved for team/user-specific rules. They **take priority** over the canon if they
> conflict. Keep the same format: rule statement, "Flag when…", and default severity. A rule you
> can't verify is useless for reviewing: make it concrete before saving it.

*(Empty for now — add your rules here.)*

<!--
Template:
- **<Rule name>.** Flag when <observable symptom in the code>. Severity: <🔴/🟠/🟡/🔵>.
  Rationale: <why your team decided it this way>.
-->
