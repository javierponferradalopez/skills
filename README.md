<div align="center">

<pre>
 ____              __      _       ____  _    _ _ _     
|  _ \ ___  _ __  / _| ___( )___  / ___|| | _(_) | |___ 
| |_) / _ \| '_ \| |_ / _ \// __| \___ \| |/ / | | / __|
|  __/ (_) | | | |  _|  __/ \__ \  ___) |   &lt;| | | \__ \
|_|   \___/|_| |_|_|  \___| |___/ |____/|_|\_\_|_|_|___/
</pre>

**A personal development harness for Claude Code.**

A curated set of independent skills that turn vague tasks into shipped code with a disciplined, conscious workflow — _no vibe coding_.

</div>

---

Every skill here is a **self-contained capability**, invoked by intent. Skills live entirely in the conversation: each one runs its single procedure and stops. No skill depends on a file another skill left behind, none writes to your repo unless you explicitly ask — so the projects you point them at stay clean. That independence is exactly why you can install **one skill or many**, and take only what you need.

## Installation

Install straight from GitHub with the [skills](https://github.com/vercel-labs/skills) CLI — no clone, no setup:

```bash
npx skills@latest add javierponferradalopez/skills
```

The command opens an **interactive selector** listing every skill in this repo. Pick exactly the ones you want — one or many — with the skill's description shown as you browse, then confirm. The CLI installs each selected skill together with all the resources it bundles (scripts, templates, references), so it works with no manual follow-up. Skills that mention a companion skill still install cleanly on their own.

## Skill catalog

Skills fall into two families: **engineer** — the disciplined inner loop from a vague task to committed code (align → plan → build → commit), plus the handoff skills that pause and resume that loop — and **productivity** — everything around that loop: diagnosis, domain modeling, architecture, code navigation, PR workflow, harness tooling, and learning.

### Engineer

| Skill                                              | Use when                                                                                                                                  |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| [`grill-me`](./skills/engineer/grill-me/SKILL.md)           | Interrogating an idea until every ambiguity is resolved — walking down each branch of the design tree, one question at a time.            |
| [`grill-with-docs`](./skills/engineer/grill-me-with-docs/SKILL.md) | Running a `grill-me` session that also drives `domain-modeling` — so the interrogation simultaneously sharpens terminology and writes the glossary/ADRs down as decisions crystallise. |
| [`to-prd`](./skills/engineer/to-prd/SKILL.md)               | Turning the current conversation into a PRD and publishing it to the project issue tracker — synthesises what's known, no interview.       |
| [`to-issues`](./skills/engineer/to-issues/SKILL.md)         | Breaking a plan, spec, or PRD into independently-grabbable issues on the tracker using tracer-bullet vertical slices.                      |
| [`wayfinder`](./skills/engineer/wayfinder/SKILL.md)         | Planning a chunk of work too big for one agent session — charting it as a shared map of investigation tickets on the issue tracker, then resolving them one at a time until the route to the destination is clear. |
| [`tdd`](./skills/engineer/tdd/SKILL.md)                     | Building a feature or fixing a bug test-first — a disciplined red-green-refactor loop in vertical slices, with behavior-driven integration tests. |
| [`implement`](./skills/engineer/implement/SKILL.md)         | Implementing a single issue end-to-end and stopping with the tree dirty — fetches the issue, loads project context, applies the code-standards bar and red-green-refactor; no commit, push, branch, or issue close. |
| [`validate`](./skills/engineer/validate/SKILL.md)           | Reviewing one issue's uncommitted implementation pre-commit in a fresh session — fixes bugs/edge-cases/quality in place, writes tests to break the code, flags spec gaps and scope creep; leaves the tree green, never commits. |
| [`code-review`](./skills/engineer/code-review/SKILL.md)     | Reviewing the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards and Spec — run as parallel sub-agents and reported side by side. Use to review a branch, a PR, or work-in-progress. |
| [`code-standards`](./skills/engineer/code-standards/SKILL.md) | Writing or reviewing code in any language against a thin quality bar focused on what models get wrong by default — deep modules, errors designed out of existence, behavior-driven tests, restraint.   |
| [`commit`](./skills/engineer/commit/SKILL.md)               | Splitting a dirty working tree into an ordered list of atomic conventional commits — plans from `git diff HEAD`, commits only on an explicit literal OK. |
| [`handoff`](./skills/engineer/handoff/SKILL.md)             | Compacting the current conversation into a handoff document (saved to the OS temp dir) so a fresh agent can continue the work — references existing artifacts rather than duplicating them. |
| [`handoff-grill`](./skills/engineer/handoff-grill/SKILL.md) | Pausing a `grill-me` session into a resumable handoff that preserves the open branches of the decision tree, not just the closed decisions — to continue later or hand to a teammate. |
| [`domain-modeling`](./skills/engineer/domain-modeling/SKILL.md) | Actively building and sharpening the project's domain model — challenging terms and writing the glossary (`CONTEXT.md`) and decisions (ADRs) down the moment they crystallise. |

### Productivity

| Skill                                              | Use when                                                                                                                                  |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| [`diagnose`](./skills/productivity/diagnose/SKILL.md)           | Hard bugs, unclear regressions, perf problems: reproduce → minimise → hypothesise → instrument → fix → regression-test.                   |
| [`improve-codebase-architecture`](./skills/productivity/improve-codebase-architecture/SKILL.md) | Finding deepening opportunities in a codebase — turning shallow modules into deep ones for testability and AI-navigability, presented as a visual before/after HTML report informed by `CONTEXT.md` and ADRs. |
| [`zoom-out`](./skills/productivity/zoom-out/SKILL.md)           | Stepping back for broader context or a higher-level perspective on an unfamiliar section of code.                                         |
| [`validate-business-idea`](./skills/productivity/validate-business-idea/SKILL.md) | Validating a business idea before building — a bounded grill extracts the idea, mandatory multi-angle web research checks whether it already exists and who the competitors are, and it ships a shadcn/ui HTML report with an existence verdict, differentiation axes, and a pursue/pivot/abandon call. |
| [`github-pr`](./skills/productivity/github-pr/SKILL.md)         | Preparing and opening a PR for the current branch — Conventional-Commits title + why-focused description, approved before `gh pr create`. |
| [`suggest-reviewers`](./skills/productivity/suggest-reviewers/SKILL.md) | Suggesting GitHub reviewers for the current branch's PR — ranked from git history + CODEOWNERS, kept out of context via an aggregating script. |
| [`setup-skills`](./skills/productivity/setup-skills/SKILL.md)   | Scaffolding a repo's `## Agent skills` block in `AGENTS.md`/`CLAUDE.md` plus `docs/agents/` so the engineering skills know its issue tracker and domain-doc layout. |
| [`write-a-skill`](./skills/productivity/write-a-skill/SKILL.md) | Adding, writing, or reworking a harness skill; formalizing a procedure you keep repeating by hand.                                        |
| [`teach`](./skills/productivity/teach/SKILL.md)                 | Learning a topic over multiple sessions — turns the current directory into a teaching workspace with a mission, citation-backed HTML lessons, reference cheat-sheets, and learning records. |

---

## Credits

Many of these skills are based on [Matt Pocock's skills](https://github.com/mattpocock/skills), adapted to my own needs.

> **Maintaining or forking this repo?** The machinery for keeping forked skills in sync with their upstreams, the local-development symlink tool, and the repository layout all live in [`MAINTAINING.md`](./MAINTAINING.md).

## License

Released under the [MIT License](./LICENSE).

---
