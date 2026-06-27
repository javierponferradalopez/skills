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
