---
name: setup-skills
description: Sets up an `## Agent skills` block in AGENTS.md/CLAUDE.md, `docs/agents/`, and the quality gate in `.agents/gate/`, so the engineering skills know this repo's issue tracker (GitHub, GitLab, ClickUp, or local markdown), domain doc layout, error tracking, and machine-checked quality bar. Run as a first-time bootstrap for a repo, or if engineering skills appear to be missing context about the issue tracker, domain docs, error tracker, or quality gate.
disable-model-invocation: true
---

# Setup Skills

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker** — where issues live (GitHub by default; GitLab, ClickUp, and local markdown are also supported out of the box)
- **Domain docs** — where `CONTEXT.md` and ADRs live, and the consumer rules for reading them
- **Error tracker** — which error-tracking tool this repo talks to, so skills like `diagnose` can pull production error signal over MCP. Optional — skip it for repos with no error tracking.
- **Quality gate** — the machine-checked quality bar `validate` runs, materialised in `.agents/gate/` with its own dependency tree. Optional — skip it for repos that aren't JS/TS.

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config` — is this a GitHub repo? Which one?
- `AGENTS.md` and `CLAUDE.md` at the repo root — does either exist? Is there already an `## Agent skills` section in either?
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root
- `docs/adr/` and any `src/*/docs/adr/` directories
- `docs/agents/` — does this skill's prior output already exist?
- `.scratch/` — sign that a local-markdown issue tracker convention is already in use
- `.agents/gate/` — does a gate already exist here?
- **Does this repo have tests, and what runs them?** Look in that order of authority: a declared script, then a config file, then an installed dependency. `vitest` in `devDependencies` plus files matching `*.test.*` / `*.spec.*` is the signal that decides Section D.
- Monorepo signals — a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. Present only in a genuinely large multi-package repo; their absence means single-context, which is almost every repo.

### 2. Present findings and ask

Summarise what's present and what's missing. Then take the sections in order — one section, one answer, then the next.

Lead each section with the recommended answer so the user can accept it in a word. Give a one-line explainer only when the choice genuinely branches; skip the section entirely when exploration already settled it (Section B when there's no monorepo).

**Section A — Issue tracker.**

> Explainer: The "issue tracker" is where issues live for this repo. Skills like `to-tickets` and `to-spec` read from and write to it — they need to know whether to call `gh issue create`, write a markdown file under `.scratch/`, or follow some other workflow you describe. Pick the place you actually track work for this repo.

Default posture: these skills were designed for GitHub. If a `git remote` points at GitHub, propose that. If a `git remote` points at GitLab (`gitlab.com` or a self-hosted host), propose GitLab. Otherwise (or if the user prefers), offer:

- **GitHub** — issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **GitLab** — issues live in the repo's GitLab Issues (uses the [`glab`](https://gitlab.com/gitlab-org/cli) CLI)
- **ClickUp** — issues live as ClickUp tasks (uses the ClickUp MCP tools)
- **Local markdown** — issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, Linear, etc.) — ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

**Section B — Domain docs.**

> Explainer: Some engineering skills read a `CONTEXT.md` file to learn the project's domain language, and `docs/adr/` for past architectural decisions. They need to know whether the repo has one global context or multiple (e.g. a monorepo with separate frontend/backend contexts) so they look in the right place.

Confirm the layout:

- **Single-context** — one `CONTEXT.md` + `docs/adr/` at the repo root. Most repos are this.
- **Multi-context** — `CONTEXT-MAP.md` at the root pointing to per-context `CONTEXT.md` files (typically a monorepo).

**Section C — Error tracker.** Optional.

> Explainer: The "error tracker" is the error-tracking tool this repo talks to. When configured, skills like `diagnose` can pull an error's stack trace, breadcrumbs, and frequency from it — instead of working blind. This is distinct from the **issue tracker** in Section A: the issue tracker is where *work* lives (GitHub Issues, etc.); the error tracker is where *runtime errors* are captured. Skip this section entirely for a repo with no error tracking; nothing downstream depends on it.

Ask **where** the error tracker lives first — it decides how many times you ask the rest:

- **Root** — one `docs/agents/error-tracker.md` for the whole repo. Most repos.
- **Per-subproject** — each context keeps its own `src/<context>/docs/agents/error-tracker.md`, so a monorepo where subprojects wire to different projects (or different tools) declares each one separately.

This is independent of the domain-doc layout — a single-context repo can still split its error tracking per subproject, and a multi-context one can still share one root doc.

Then, for **each place** (once at root, or once per subproject the user names), pick its **one** error tracker — each place declares a single tool:

- **Sentry** — errors / exceptions (stack traces, breadcrumbs, frequency). The tool shipped with a seed template.
- **Other** — a different error tracker (Rollbar, Bugsnag, …). Ask the user to describe in one paragraph what it returns and how it's reached over MCP; the skill records that as freeform prose.
- **None** — skip this place; write no doc for it.

Connection is **MCP-only** — the user authenticates the MCP server themselves; the skill never handles credentials. For the tool picked, collect its **scope** to bake into that place's doc so skills query the right target, not credentials:

- **Sentry** — the org slug and the project slug(s) this place maps to.

**Section D — Quality gate.** Optional.

> Explainer: The "quality gate" is the machine-checked half of this repo's quality bar. `validate` runs it after its own work and fixes what it reports. It measures two things on **the lines your diff touched**, with zero tolerance: cyclomatic complexity over 10, and mutants that no test kills. It installs into `.agents/gate/` with its **own** `node_modules` — nothing of the gate ever enters the project's, and no version of anything the project installed is touched or bumped.

The gate is JS/TS only today. For anything else, skip this section — write no `.agents/gate/`, and the repo simply has no gate.

**The detection is your judgment, not a ladder in bash.** Look at what step 1 found and propose the form:

- **Full form** — the repo has tests. Complexity **and** mutation.
- **Short form** — the repo has no tests. Complexity only. The honest default for an untested repo, and it still gives a real bar today.

**The two forms differ by one file**, `stryker.config.json`: copy it and the gate mutates, leave it out and it doesn't. There is one `package.json` and one lock, so the toolchain a repo installs never depends on which form it picked — and turning mutation on later is copying that one file, with nothing to reinstall.

**Offer the full form to an untested repo anyway — with its price said out loud.** This is the *greenfield* case: with no tests at all, every mutant survives and the gate reports `N Survived` when the truth is *there are no tests*. `validate` will end red until the first test exists, because the agent is forbidden from writing escapes. Some people want exactly that — a forcing function, and this repo has a `tdd` skill. What you must not do is let them discover it on their first `/validate`.

Ask nothing about thresholds, `ignorePatterns`, or how tests are launched. Complexity 10 and zero tolerance are fixed; the mutation runner finds the project's own test runner by itself. Those are dials to turn later, in the repo, with evidence in front of you.

### 3. Confirm and edit

Show the user a draft of:

- The `## Agent skills` block to add to whichever of `CLAUDE.md` / `AGENTS.md` is being edited (see step 4 for selection rules)
- The contents of `docs/agents/issue-tracker.md` and `docs/agents/domain.md`, plus each error-tracker doc (one at the root, or one per subproject) if a tool was picked
- Which gate form lands in `.agents/gate/`, if one was picked

Let them edit before writing.

### 4. Write

**Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create — don't pick for them.

Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa) — always edit the one that's already there.

If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The block:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Domain docs

[one-line summary of layout — "single-context" or "multi-context"]. See `docs/agents/domain.md`.

### Error tracker

[one-line summary of the tool picked — e.g. "Sentry (errors)"]. [If root: `See docs/agents/error-tracker.md`.] [If per-subproject: `Configured per-subproject — each context declares its own tool in src/<context>/docs/agents/error-tracker.md`.]

### Quality gate

[one-line summary — e.g. "`.agents/gate/` (complexity + mutation on the diff). `validate` runs it."]
```

Omit a sub-section entirely when its section was skipped — don't leave an empty heading.

The `### Quality gate` line is the only block here no skill parses. It earns its place because `## Agent skills` is this repo's declaration of what agent machinery it carries: a human or an agent opening `CLAUDE.md` should see there's a bar `validate` will enforce, rather than discovering it from a hidden directory.

Then write the docs files using the seed templates in this skill folder as a starting point:

- [issue-tracker-github.md](./issue-tracker-github.md) — GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md) — GitLab issue tracker
- [issue-tracker-clickup.md](./issue-tracker-clickup.md) — ClickUp issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md) — local-markdown issue tracker
- [domain.md](./domain.md) — domain doc consumer rules + layout
- [error-tracker-sentry.md](./error-tracker-sentry.md) — Sentry error tracking

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

**Error-tracker doc(s).** Write one doc **per place** picked in Section C — at the root, `docs/agents/error-tracker.md`; per-subproject, one `src/<context>/docs/agents/error-tracker.md` per subproject. Each doc holds a single `# Error tracker: <tool>` section built from that place's seed template, filling the `<...>` scope placeholders with that place's org/project and leaving the MCP connection wording as-is. For an **Other** tool, write the section from scratch using the user's description. A place that picked **None** gets no doc.

**The gate.** Copy the template from [`gate/`](./gate/) in this skill's folder into `<repo>/.agents/gate/`, then mount it:

```bash
mkdir -p .agents/gate
cp <skill>/gate/gate.sh <skill>/gate/ensure.sh <skill>/gate/eslint.complexity.config.mjs \
   <skill>/gate/package.json <skill>/gate/package-lock.json .agents/gate/
cp <skill>/gate/stryker.config.json .agents/gate/     # full form only
cp <skill>/gate/gitignore .agents/gate/.gitignore
chmod +x .agents/gate/gate.sh .agents/gate/ensure.sh
.agents/gate/ensure.sh
```

`gate.sh`, `ensure.sh`, the configs, the `package.json`, **the lock** and the `.gitignore` are versioned with the repo; `node_modules/`, the seal and the reports are not. The toolchain is the same either way — composition is declared by which configs are present, never by what got installed, so `ensure.sh` has exactly one lock to reason about. The lock is baked: the gate installs the exact versions this template was verified against, so its guarantees stay properties of the gate rather than luck of the install date. `ensure.sh` reinstalls whenever that lock moves — a cold start and a lock that drifted are the same event, and it settles both.

**The gate can fall behind the skill.** `ensure.sh` only compares what's local: the tree against the lock beside it. Updating the machinery itself means re-running this skill. That's deliberate — the meeting point between skills is the project, not another skill, because skills install selectively and `validate` may be here without this one.

### 5. Done

Tell the user the setup is complete. Mention they can edit `docs/agents/*.md` and the gate's configs directly later — re-running this skill is only necessary if they want to switch issue trackers, change the error tracker, change the gate's form, or pick up a newer version of the gate.
