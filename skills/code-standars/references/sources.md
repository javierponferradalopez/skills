# The canon — sources behind the standards

This is the bibliographic basis from which the rules in `standards.md` are derived. The rules
are written in original wording: this file summarizes what principles each work contributes,
so they can be cited precisely in reports.

## Clean Code — Robert C. Martin (2008)
Contributes the bulk of the day-to-day tactical rules: intention-revealing names, small
functions that do one thing at a single level of abstraction, comments as a last resort (code
should explain itself), error handling with exceptions instead of return codes, clean
boundaries with third-party code, and the "Boy Scout Rule" (leave the code cleaner than you
found it).

## The Pragmatic Programmer — Andrew Hunt & David Thomas (1999 / 2019 ed.)
Principles of attitude and design: **DRY** (don't repeat knowledge), **orthogonality**
(independent components), "don't leave broken windows" (don't tolerate small decay),
decoupling, the **Law of Demeter** (talk only to your immediate neighbors), and favoring
reversible, decoupled solutions.

## A Philosophy of Software Design — John Ousterhout (2018)
The most useful framework for reasoning about complexity in modules. Key ideas: **complexity**
is the enemy and accumulates incrementally; **deep modules** (a simple interface hiding a lot
of implementation) versus shallow modules; **information hiding**; "define errors out of
existence" (eliminate special cases by design instead of handling a thousand of them); and
that comments should capture what the code cannot.

## Refactoring — Martin Fowler (2nd ed., 2018, JavaScript examples)
The catalogue of **code smells** (long function, long parameter list, large class, feature
envy, primitive obsession, duplicated code, etc.) and the refactorings that resolve them.
Useful for naming precisely what smells.

## Code Complete — Steve McConnell (2nd ed., 2004)
Low-level software construction: defensive programming, reducing control-flow complexity
(nesting, number of paths), pseudocode first, and managing essential vs. accidental complexity.

## Working Effectively with Legacy Code — Michael Feathers (2004)
Testability and dependencies: the notion of **seams** (places where you can change behavior
without editing in that spot), and the idea that code without tests is legacy code. Useful for
assessing whether something is testable.

## The Design of Design / The Mythical Man-Month — Fred Brooks (2010 / 1975)
Design as a process and at the macro level: **conceptual integrity** (a system should reflect
one coherent set of design ideas; coherence matters more than piling on features), the
**second-system effect** (the tendency to over-design the second system), and that design is
iterative and rarely right on the first try.

## Domain-Driven Design — Eric Evans (2003)
**Ubiquitous language** (the code speaks the language of the domain) and context boundaries.
Useful for assessing whether names and abstractions reflect the business domain.

## Design Patterns — Gamma, Helm, Johnson, Vlissides "GoF" (1994)
A vocabulary of patterns. Caveat baked into the rules: patterns are a tool, not a goal —
over-applying them creates accidental complexity.
