# Code Standards

## Interface design

**Deep modules** — small interface, deep implementation: a few methods with simple
params hiding complex logic behind them. Avoid shallow modules (a large interface that
just forwards to a thin implementation) and pass-through classes. When designing, ask:
can I reduce the number of methods? Simplify the params? Hide more complexity inside?

**A name is a contract**, and the two sides of a module answer to different forces:

- **Public** — name the caller's intention and hide the how, so the name survives new
  rules landing inside it. Then make the body cover what the name promises: if it promises
  more than it checks, either reduce the name or complete the body. A public name that
  over-promises is the defect; a broad public name backed by a body that honours it is not.
- **Private** — there is no contract to keep stable and the only reader is reading this
  file, so the name serves its call site: it reads as one line of the narrative there.
  Name what the result is, not what was done to get it, and let the signature declare
  the types. A helper that returns nothing takes its action as its name.

**Fail fast** — validate where the value is born, in the constructor. A separate
`validate()` someone must remember to call is a rule that ships switched off.

**Tell, don't ask** — no public setters. State changes only through methods named for the
domain change they perform, so the rules travel with the data instead of living at every
call site.

**Design for testability**:

1. **Accept dependencies, don't create them** — pass external deps in rather than
   constructing them internally.
2. **Return results, don't produce side effects** — a function that returns a value is
   easier to reason about and test than one that mutates state.
3. **Small surface area** — fewer methods = fewer tests; fewer params = simpler setup.

**Scrutinize optional parameters** — a major source of bugs by omission. Prefer
correctness over backwards compatibility.

## Atomicity

The counterpart of _Interface design_, pointed inward: private scope only. A public module
with seven methods is an API, not fragmentation.

Logic used once stays where it is. One call site is one function.

Extracting single-use logic is defensible in exactly one shape: you extract **every** phase,
and the base function is left as a list of named steps carrying no logic of its own. The
half-way state is the forbidden one — one helper pulled out and the rest inline leaves the
function half narrative and half mechanics, so the reader hops to follow one idea.

## Design errors out of existence

Prefer designs that remove special cases over code that handles them. Return an empty
collection instead of a null/nil sentinel; where the language allows, make invalid states
unrepresentable (sum types, enums, required fields that travel together) instead of
guarding against them at every call site.

**Close the set.** Write the guard that rejects over the **allowed** state, never over the
forbidden one: reject what is not uploaded, rather than rejecting what is pending. A state
added later is then refused by default instead of slipping through in silence. The trap
lives in the two-valued enum, where negating one value happens to equal the other today.
Make the bad guard unwritable rather than remembered: the type exposes the closing
predicate only. Exposing the open predicate to _display_ state is fine — the ban is on
guards.

## Restraint

- **No speculative generality.** No config, layers, or abstraction "just in case." Build
  for the case in front of you, not an imagined future one.
- **Don't force DRY.** Extract a repeated shape when both sites change for the **same**
  reason; two fragments that look alike today but change for different reasons should stay
  separate. The wrong abstraction costs more than duplication.
- **Conceptual integrity.** Solve the same kind of problem the same way sibling modules
  do. Coherence across the system beats any single clever feature.
