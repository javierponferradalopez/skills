---
name: which-skill
description: Ask which skill or flow fits your situation. A router over the skills in this harness.
disable-model-invocation: true
---

# Which skill

You don't remember every skill, so ask.

A **flow** is a path through the skills. Most paths run along one **main flow**, and three **on-ramps** merge onto it. Everything else is standalone, or a vocabulary layer that runs underneath.

## The main flow: idea → ship

The route most work travels. You have an idea and want it built.

1. **`/grill-with-docs`** sharpens the idea by interview. Start here whenever you are **working in a working directory**: it's stateful, retaining what it learns in `CONTEXT.md` and ADRs. (No working directory? Use `/grill-me` instead, covered under Standalone. Both run the same relentless interview; `grill-with-docs` is the one that leaves a paper trail, which makes it the better of the two whenever a repo is there to leave it in.)

2. **Branch: is this a multi-session build?**
   - **Yes** → **`/to-spec`** (turn the thread into a spec on the tracker), then **`/to-tickets`** to split it into tracer-bullet tickets, each declaring its **blocking edges**. On a local tracker the edges are text in one file per ticket, worked blockers-first by hand; on a real tracker they become native blocking links, so any ticket whose blockers are done can be grabbed: take one ticket at a time through step 3, **`/clear`ing context between each one**. Each ticket is self-contained, so the last one's context is disposable.
   - **No** → step 3, right here in the same context window.

3. **Build and ship it.** Four deliberate steps, each stopping exactly where the next begins:
   - **`/implement`** builds one issue: fetches it, loads the project's context, holds the **`/code-standards`** bar and drives **`/tdd`** internally one red-green slice at a time. It **stops with the tree dirty** — no commit, no push, no branch, no issue closed.
   - **`/validate`** then reviews that uncommitted diff with **fresh eyes**: the diff is the only evidence, never how the ticket was built, so none of the implementer's bias survives. It fixes bugs, edge cases and quality in place and writes tests to break the code, then flags spec-coverage gaps and scope creep for you instead of silently filling them. It leaves the tree green and never commits.
   - **`/commit`** splits the dirty tree into an ordered list of atomic conventional commits, and commits only on an explicit literal OK.
   - **`/done`** pushes the branch and closes the issue it finishes. When the work ships through review instead, that's **`/github-pr`**, which closes out by running **`/suggest-reviewers`**.

   Three of these are worth reaching for on their own: **`/tdd`** when you just want a concrete behaviour built test-first with no ticket behind it, **`/code-review`** whenever you want the two-axis review (Standards + Spec) of a branch, a PR or work in progress against a fixed point, and **`/walkthrough`** when you'd rather read a set of changes yourself than have them judged for you.

### Context hygiene

Keep steps 1–2 in **one unbroken context window** (don't compact or clear until after `/to-tickets`) so the grilling, spec, and tickets all build on the same thinking. Each `/implement` then starts fresh, working from the ticket.

The limit on this is the **[smart zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone)**: the window (~150k tokens on state-of-the-art models) within which the model still reasons sharply. If a session approaches it before `/to-tickets`, don't push on degraded; `/compact` at the nearest phase boundary and carry on (see Phase boundaries). **`/what-it-took`** is the retrospective on that budget: run it on a session that felt expensive and it reports where the window actually went, what got buried, and what would have made it cheaper.

## On-ramps

A starting situation that generates work, then merges onto the main flow.

- **Something's broken** → **`/diagnose`**. For the hard ones: the bug that resists a first glance, the intermittent flake, the regression that crept in between two known-good states. It refuses to theorise until it has a **tight feedback loop** (one command that already goes red on *this* bug), then fixes with a regression test. Its post-mortem hands off to **`/improve-codebase-architecture`** when the real finding is that there's no good seam to lock the bug down.

- **Review comments piling up** → **`/grill-me-comments`**. The ones you left in the code, a PR's unresolved threads, or feedback someone pasted you: it sorts them by whether the implementation is obvious, settles that list on a single OK, grills you one at a time on the rest, then hands back the agreed batch and asks what becomes of it — nothing written, no comment deleted, no thread answered until you say. What comes back merges onto the main flow at step 3.

- **A huge, foggy effort: a greenfield project or a huge feature build, too big for one session** → **`/wayfinder`**, the most cognitively demanding flow here. When the way from here to the destination isn't visible yet, it charts a **shared map** of **decision tickets** on the issue tracker and resolves them one at a time, producing **decisions, not deliverables**, until the fog is pushed back and the way is clear. Where **`/grill-with-docs`** sharpens an idea you can hold in one session, wayfinder is for the idea you can't, and it's slower and denser, so save it for exactly that, never a well-scoped feature.

  When the map clears, **it hands off, it doesn't build**: merge onto the main flow at **`/to-spec`**, which collapses the map's linked decisions into a buildable plan, then `/to-tickets` and `/implement` as usual. Looping the map straight into `/implement` skips that collapse and throws the linked detail away, so go straight there only when the effort turned out genuinely small.

## Codebase health

Not feature work, just upkeep.

- **`/improve-codebase-architecture`** runs whenever you have a spare moment to keep the codebase good for agents to operate in. It surveys for **deepening opportunities**, informed by `CONTEXT.md` and the ADRs, and reports them as a before/after HTML report; picking one _generates an idea_ you can take into the main flow at `/grill-with-docs`. It finds the candidates; **`/code-standards`** (below) is the vocabulary you design the chosen one in.

## Vocabulary underneath

Two model-invoked references that run *beneath* the other skills, each the single source of truth for its vocabulary — so the skills above pull them in unasked. Reach for them directly when the **words**, not the process, are the problem.

- **`/domain-modeling`**: sharpen the project's *domain* language: challenge a fuzzy term, resolve an overloaded word ("account" doing three jobs), record a hard-to-reverse decision as an ADR. It's the active discipline `/grill-with-docs` drives to keep `CONTEXT.md` a clean glossary.
- **`/code-standards`** is the quality bar for the code itself, and the vocabulary for arguing about it: deep modules, errors designed out of existence, behaviour-driven tests that mock only at boundaries, restraint against speculative abstraction — language-agnostic, and aimed at what models get wrong by default. `/implement`, `/validate` and `/code-review` all speak it.

## Phase boundaries

A **phase** is a chunk of work inside a session: the grilling, the implementation, the QA. At the **boundary** between two of them you have five options, and picking between them is the fuzziest decision in this whole map:

- **Continue**: stay put. Costs nothing, loses nothing.
- **`/clear`**: empty the window, when nothing here matters to what's next.
- **`/handoff`** writes a portable markdown file. Narrow: only for a **new harness**, a **new directory**, a **colleague**, or forking a side task **mid-phase**. What it buys is portability.
- **Subagent**: send a tightly-scoped task to its own window and get a report back.
- **`/compact`** compresses this context and seeds a fresh session with it. The **default**, at the bottom of the tree rather than the first reach.

Read [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md) for the ordered tree: the five questions, the reasoning behind each branch, and why the primary-source cost makes **Continue** the one to rule out first. Make the decision **at** a boundary; mid-phase, continue or split the rest into subagents.

## Standalone

Off the main flow entirely.

- **`/grill-me`**: the same relentless interview as `/grill-with-docs`, but **stateless**: it saves nothing locally and builds no `CONTEXT.md`. Reach for it when you are **not working in a working directory** (sharpening a plan, a design, a piece of writing, anything with no repo under it). If you are in a working directory, use `/grill-with-docs` instead: it runs the same interview and leaves a paper trail, so it is strictly the better one.
- **`/handoff-grill`** is the pause button on either interview: it preserves the **open branches** of the decision tree, not just the closed decisions, so a later session — or a teammate — resumes the grilling where it stopped rather than restarting it. Plain **`/handoff`** flattens a conversation into a portable file for a fresh agent to continue; use it for everything that isn't a grill, on the terms in Phase boundaries above.
- **`/zoom-out`**: you're deep in an unfamiliar section of code and need the level above it — what this fits into, why it exists. Cheap, mid-conversation, no output but the explanation.
- **`/catch-up`**: you delegated work and were away, or you lead the people doing it. It recurses a ticket's subtasks, matches each to its PRs and branches by identifier, and reports what changed since a date you pick as a throwaway briefing.
- **`/research`**: delegate reading legwork to a **background agent**: it investigates a question against **primary sources**, then leaves a cited Markdown file in the repo. Keep working while it reads. The file it produces is something to take *into* the main flow at `/grill-with-docs`, since research feeds the thinking rather than replacing it.
- **`/teach`**: learn a concept over multiple sessions, using the current directory as a stateful workspace.
- **`/writing-for-agents`** is the reference for writing documents agents consume: skills, `AGENTS.md`/`CLAUDE.md`, pointed-at docs.

## Precondition

**`/setup-skills`**: run before your first engineering flow to configure the issue tracker, the domain-doc layout and the error tracker the other skills assume. Custom issue trackers also work.
