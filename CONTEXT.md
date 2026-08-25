# Glossary

The ubiquitous language for this skills harness. Glossary only — no implementation details.

- **Skill** — a self-contained capability under `skills/<category>/<name>/`, invoked by its `name:` frontmatter. The unit that gets installed and synced.
- **Fork** — a skill in this repo that was adopted from someone else's repo and may have been edited. Tracked in `upstream.lock.json`. Contrast with a **self-authored** skill, which has no upstream.
- **Upstream** — a named external repository this harness borrows skills from. Each upstream has a `url` and a `ref` (the git ref to compare against). Today there is one (`matt`); the model supports many. An upstream is a *source of ideas*, never a hard dependency.
- **Upstream key** — the short name a fork uses to point at its upstream (e.g. `matt`). Lives in the `upstreams` catalog and is referenced by each fork's `upstream` field.
- **Source** — the path a fork occupies *inside its upstream* (`source` field). May differ from `mine` because upstreams rename/move things.
- **Mine** — the path the fork occupies *in this repo* (`mine` field). The copy I actually run.
- **Base** — the upstream commit my copy is currently synced from (`base` field). The merge ancestor for 3-way merges. Per-fork, lives in the upstream's history.
- **Mode** — how an update is applied: `pure` (take upstream verbatim) or `modified` (3-way merge preserving my edits).
- **Provenance** — the full record of where a fork came from and how it syncs: `{ upstream, source, base, mode }`.
- **Manifest key** — the tool-facing handle for a fork, `<upstream>:<name>` (e.g. `matt:tdd`). Used by commands (`update matt:tdd`). Distinct from the *invocable* name, which comes from the skill's `SKILL.md` frontmatter.
- **Sync-remotes** — reconciling the local git remotes from the `upstreams` catalog: add missing, fix changed URLs, fetch, set default HEAD. The catalog is the source of truth; remotes are derived.
- **Detach** — dropping a fork's manifest entry while leaving its `mine/` copy intact, turning it back into a self-authored skill. The safe way to stop tracking an upstream without losing work.

## Quality gate

The machine-checked half of the quality bar. Materialised by `setup-skills` in the target repo, run by `validate`.

- **Gate** — the quality bar expressed as commands rather than prose: `<repo>/.agents/gate/`, versioned with the repo, carrying **its own dependency tree** so nothing of it ever enters the project's `node_modules`. Its presence is the whole selector: no directory, no gate.
- **Capability** — one thing the gate measures. Two today: **complexity** (cyclomatic, ESLint, max 10, judged on the function *head* inside the diff) and **mutation** (Stryker, zero surviving mutants). A capability either sinks the gate or isn't in it — there is no informative mode.
- **Verdict** — what a capability or the run as a whole reports. `PASS` / `FAIL` / `SKIPPED` judge the **code**; **`BROKEN`** judges the **gate** — *"I could not judge"*, not *"your code is wrong"*. Exit `0` for `PASS`/`SKIPPED`, `1` for anything else.
- **Pass** (*pasada*) — one run of one capability. The correction loop's budget is counted in passes per capability (3 mutation, 2 complexity), never in invocations of the gate.
- **Escape** — an annotation that exempts code from a capability (`// Stryker disable`, `eslint-disable`). Visible in the diff, and **the human's alone**: an agent that can write one turns zero tolerance into theatre.
- **Hardener** — `validate`'s posture in its first half: leave the code harder to break than you found it, measured rather than commented. Its second half, spec conformance, is judgment and stays human-facing.
- **`$GATE_BASE`** — the revision the gate diffs against; default `HEAD`, the dirty pre-commit tree. The whole branch is asked for explicitly.
- **Seal** — `.agents/gate/.installed`, the hash of the `package-lock.json` the toolchain was installed from. `ensure.sh` compares it and reinstalls when it moves, which makes a cold start and a drifted lock the same event.
- **Full form / short form** — the two shapes of gate. Full has tests behind it and runs both capabilities; short has none and runs complexity only. They differ by the presence of `stryker.config.json` and nothing else: composition is declared by which configs are there, never by what got installed, so both forms share one `package.json` and one lock.
- **Baked template** — the gate ships with its lock committed, so the versions it was verified against are properties of the gate rather than luck of the install date.
