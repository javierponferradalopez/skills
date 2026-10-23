# Build phase

Build the issue in the pack until it works. The bar and the attack belong to the
phases after you; your job ends at **green**.

## 1. Load context

Read the pack first: the issue, its spec and siblings, the commands, and any extra
instructions. Then read the project's own bar and shape: `CONTEXT.md`, `docs/`,
`CLAUDE.md` / `AGENTS.md`.

When the issue carries **Bearings**, read there first — they are an estimate of where
the work lands, so they spare you the search, not the reading.

Orient in the repo **surgically**: grep for the seam, read the ranges the grep points
at, and open a whole file when you'll edit it. The tests already covering the area
carry the conventions your tests have to match.

When the pack carries **extra instructions**, the dirty tree is earlier work on this
issue: read `git diff HEAD` and `git status`, and build only what the instructions
name, on top of that diff.

Done when nothing about the repo is left to find out and you can start editing.

## 2. Implement

Use `/tdd` where possible, at pre-agreed seams.

The **docs** — the glossary, the ADRs, and the documents agents read — wait for the
orchestrator, which writes them with the user at the end. Leave those files as they
are and record each one as **owed**: each doc the issue asks for, and each term or
decision your code introduces that the glossary or the ADRs do not hold yet.

Done when every acceptance criterion is built — or, with extra instructions, every
item they name — except the owed docs, and each one that went through a seam went
**red** before it went green.

## 3. Escalate only when blocked

Work autonomously. Return **blocked** only for an ambiguity that neither the issue,
its spec, `CONTEXT.md`, nor the ADRs resolve: quote the line that is ambiguous and
give the readings you see. The orchestrator puts it to the user and sends you the
answer; then continue from where you stopped.

## 4. Get to green

Run the typecheck and test commands from the pack and get them green.

## 5. Return

Return one of these, under 150 words:

- **done** — the criteria you built, one line each; then the **owed** docs, one line
  each: the file, and the term, decision or requirement it holds.
- **blocked** — the question, with its quote and readings.
- **red** — what still fails, and what you tried.
