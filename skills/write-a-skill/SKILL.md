---
name: write-a-skill
description: Create or rework an agent skill so it fits the harness — single procedure, intent-based description, progressive disclosure. Use when the user wants to add, write, or improve a skill, or formalize a procedure they keep doing by hand.
---

# Write a Skill

Create a new skill (or rework one) so it fits the harness: small, composable,
intent-triggered. Reach for this once a manual procedure has been repeated 2–3
times and is worth formalizing.

## Process

1. **Gather requirements** — one question at a time, proposing your recommended
   answer each time:
   - What single procedure does it cover? One skill = one procedure; two things
     means two skills.
   - When should it trigger — what words, contexts, file types?
   - Does it write artifacts or just guide? Persisted or ephemeral?
   - Any reference material, or a deterministic step worth a script?
2. **Name it** following the harness convention (below).
3. **Draft** the SKILL.md from the template. Keep it short; split detail out.
4. **Review with the user**, then **install** (below).

## Name it — intent only, no prefixes

The name is the **intention** of the skill, verb-first where natural (`grill`, `plan`, `subtasks`, `verify`, `ingest`, `write-adr`, `diagnose`). One intent, one skill, one name. Do NOT use prefixes like `workflow-` or `quick-` to encode persistence or mode of work — those are properties of the procedure, not of the name.

If two skills feel like they need the same name with a modifier, they probably want to be a single skill with a question in step 1 ("¿quieres persistir esto?") rather than two skills.

## Stateless by default

Skills are stateless by default: they live in the conversation and write nothing to disk. If a skill needs to produce a reusable artifact (a plan, a list of subtasks, a verification summary, etc.), it must **ask the user where to deposit it** (ClickUp, markdown, original ticket, just-conversation) instead of persisting unilaterally.

## SKILL.md template

Start from [`TEMPLATE.md`](TEMPLATE.md) — copy it to `skills/<name>/SKILL.md` and
fill in each section. Drop `## Output` if the skill writes nothing.

## The description is everything

It's the only thing the agent sees when deciding whether to load the skill.

- Third person, ≤ 1024 chars.
- First sentence: what it does. Then `Use when [specific triggers]`.
- Good: "Extract text and tables from PDFs, fill forms. Use when working with
  PDF files or when the user mentions PDFs or forms."
- Bad: "Helps with documents." — nothing to disambiguate it from other skills.

## Keep it small (progressive disclosure)

- Aim under 100 lines in SKILL.md.
- Push detail into sibling files (`REFERENCE.md`, `FORMAT.md`, `EXAMPLES.md`)
  and link them — they load only when needed.
- Add a script only for deterministic steps (validation, formatting); it saves
  tokens and is more reliable than regenerated code.

## Install (this dotfiles setup)

Skills live in the dotfiles repo and are symlinked into the agent's skills
directory:

1. Create `skills/<name>/SKILL.md` inside the harness package in the dotfiles repo.
2. Run the package's `install.sh` to symlink it into place (idempotent), or
   create the symlink by hand.
3. Add a catalog row for it in the package `README.md`.
4. Open a new session for the skill to be discovered.

## Anti-patterns

- A skill that bundles two procedures. Split it.
- A description without "Use when …". The agent won't know when to fire it.
- Writing the skill before doing the procedure by hand 2–3 times.
- A 500-line SKILL.md. Move the detail into reference files.
- A skill that decides "skip if X" or "next, run skill Y". Orchestration is the user + agent's job, not the skill's. The skill executes its single procedure and stops.
- A skill that persists to disk silently. If the output is reusable, ask where to deposit it.
- Prefixes (`workflow-`, `quick-`) in the name. Use intent only.
