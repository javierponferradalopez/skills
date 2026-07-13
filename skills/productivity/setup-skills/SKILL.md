---
name: setup-skills
description: Sets up an `## Agent skills` block in AGENTS.md/CLAUDE.md and `docs/agents/` so the engineering skills know this repo's issue tracker (GitHub, GitLab, ClickUp, or local markdown), domain doc layout, and error tracking. Run as a first-time bootstrap for a repo, or if engineering skills appear to be missing context about the issue tracker, domain docs, or error tracker.
disable-model-invocation: true
---

# Setup Skills

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker** — where issues live (GitHub by default; GitLab, ClickUp, and local markdown are also supported out of the box)
- **Domain docs** — where `CONTEXT.md` and ADRs live, and the consumer rules for reading them
- **Error tracker** — which error-tracking tool this repo talks to, so skills like `diagnose` can pull production error signal over MCP. Optional — skip it for repos with no error tracking.
- **Code standards** — a fixed rule telling agents to load the `code-standards` skill so all generated code meets the project's quality bar

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

### 2. Present findings and ask

Summarise what's present and what's missing. Then walk the user through the decisions **one at a time** — present a section, get the user's answer, then move to the next. Don't dump them all at once.

Assume the user does not know what these terms mean. Each section starts with a short explainer (what it is, why the engineering skills need it, what changes if they pick differently). Then show the choices and the default.

**Section A — Issue tracker.**

> Explainer: The "issue tracker" is where issues live for this repo. Skills like `to-tickets`, `to-spec`, and `qa` read from and write to it — they need to know whether to call `gh issue create`, write a markdown file under `.scratch/`, or follow some other workflow you describe. Pick the place you actually track work for this repo.

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

### 3. Confirm and edit

Show the user a draft of:

- The `## Agent skills` block to add to whichever of `CLAUDE.md` / `AGENTS.md` is being edited (see step 4 for selection rules)
- The contents of `docs/agents/issue-tracker.md` and `docs/agents/domain.md`, plus each error-tracker doc (one at the root, or one per subproject) if a tool was picked

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

### Code standards

Before writing or modifying code, load the `code-standards` skill and hold all generated code to it.
```

Omit the `### Error tracker` sub-section entirely when no error tracker was picked — don't leave an empty heading.

Then write the docs files using the seed templates in this skill folder as a starting point:

- [issue-tracker-github.md](./issue-tracker-github.md) — GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md) — GitLab issue tracker
- [issue-tracker-clickup.md](./issue-tracker-clickup.md) — ClickUp issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md) — local-markdown issue tracker
- [domain.md](./domain.md) — domain doc consumer rules + layout
- [error-tracker-sentry.md](./error-tracker-sentry.md) — Sentry error tracking

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

**Error-tracker doc(s).** Write one doc **per place** picked in Section C — at the root, `docs/agents/error-tracker.md`; per-subproject, one `src/<context>/docs/agents/error-tracker.md` per subproject. Each doc holds a single `# Error tracker: <tool>` section built from that place's seed template, filling the `<...>` scope placeholders with that place's org/project and leaving the MCP connection wording as-is. For an **Other** tool, write the section from scratch using the user's description. A place that picked **None** gets no doc.

### 5. Done

Tell the user the setup is complete. Mention they can edit `docs/agents/*.md` directly later — re-running this skill is only necessary if they want to switch issue trackers, change the error tracker, or restart from scratch.
