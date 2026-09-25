# ADR Format

ADRs live in `docs/adr/` and use sequential numbering: `0001-slug.md`, `0002-slug.md`, etc.

Create the `docs/adr/` directory lazily — only when the first ADR is needed.

## Template

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

That's it. An ADR can be a single paragraph. The value is in recording *that* a decision was made and *why* — not in filling out sections.

## Optional sections

Only include these when they add genuine value. Most ADRs won't need them.

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`) — useful when decisions are revisited
- **Considered Options** — only when the rejected alternatives are worth remembering
- **Consequences** — only when non-obvious downstream effects need to be called out

## Numbering

Scan `docs/adr/` for the highest existing number and increment by one.

## When to offer an ADR

All three of these must be true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will look at the code and wonder "why on earth did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If a decision is easy to reverse, skip it — you'll just reverse it. If it's not surprising, nobody will wonder why. If there was no real alternative, there's nothing to record beyond "we did the obvious thing."

### What qualifies

- **Architectural shape.** "We're using a monorepo." "The write model is event-sourced, the read model is projected into Postgres."
- **Integration patterns between contexts.** "Ordering and Billing communicate via domain events, not synchronous HTTP."
- **Technology choices that carry lock-in.** Database, message bus, auth provider, deployment target. Not every library — just the ones that would take a quarter to swap out.
- **Boundary and scope decisions.** "Customer data is owned by the Customer context; other contexts reference it by ID only." The explicit no-s are as valuable as the yes-s.
- **Deliberate deviations from the obvious path.** "We're using manual SQL instead of an ORM because X." Anything where a reasonable reader would assume the opposite. These stop the next engineer from "fixing" something that was deliberate.
- **Constraints not visible in the code.** "We can't use AWS because of compliance requirements." "Response times must be under 200ms because of the partner API contract."
- **Rejected alternatives when the rejection is non-obvious.** If you considered GraphQL and picked REST for subtle reasons, record it — otherwise someone will suggest GraphQL again in six months.

## Decisions and conventions

This section applies only when the repo's `docs/agents/domain.md` has a section **Decision or convention**. Otherwise each ADR is a decision, and the rest of this file applies as it is.

In such a repo, each rule of the project is an ADR, of one of two kinds. The frontmatter gives the kind and the status:

```md
---
kind: decision | convention
status: accepted | superseded by ADR-NNNN
---
```

### Which kind

Ask one question: **can a find-and-replace or a codemod revert the rule, with no change to what the system does?**

- **Yes → convention.** Names, suffixes, the factories of a value object, the base class of an aggregate, folders, the shape of a test.
- **No → decision.** To revert it changes the behaviour, the stored data, a contract with the outside, or the flow between modules.

Two checks support the answer:

- **No real alternative was refused** → convention.
- **A reader would "fix" it** → decision, even when it is small.

One topic can have a part of each kind. For a handler, the errors it catches are a decision, and its name and its folder are a convention.

### A decision

Everything above this section applies to it: the three conditions of *When to offer an ADR*, and the file `NNNN-slug.md`. To change it, a new decision amends or supersedes it.

### A convention

- **Offer one each time the session settles a rule on the shape of the code.** The three conditions do not apply.
- **Its file is `NNNN-convention-<topic>.md`.** In a monorepo it is `NNNN-convention-<package>-<topic>.md`, with a package from the list in `docs/agents/domain.md`. The topic is the kind of class or file that it governs: `0033-convention-backend-handler.md`.
- **It holds the rule and its example.** It gives a why only when a real one exists.
- **It is complete in itself.** It links to no decision, so the agent that writes the code reads the convention and nothing more. A decision can link to the convention that applies it.
- **To change it, supersede it whole.** Write a new ADR with the same package and topic that restates the whole convention, and set the old one to `superseded by ADR-NNNN`. So one package and topic always have one `accepted` ADR, and the superseded one still explains the code that follows it.
