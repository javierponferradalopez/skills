# 1. Support multiple upstreams

Date: 2026-06-27

## Status

Accepted

## Context

The harness adopts skills from external repos and syncs them with a 3-way merge.
The original design hard-wired a **single** upstream (Matt Pocock's repo): one
top-level `"upstream"` URL in `upstream.lock.json`, one git remote named
`upstream`, and one global `SKILLS_UPSTREAM_REF`. Every fork was implicitly
"from matt", so forks carried no record of *which* upstream they came from.

We want to borrow from more than one creator without that single-source
assumption leaking through the schema and the tool.

## Decision

- **Named upstream catalog.** A top-level `upstreams` map keys each origin by a
  short name (`matt`, `foo`) to `{ url, branch? }`. Each fork references its
  origin by that key via an `upstream` field. The URL lives in exactly one place.
- **`branch` is optional.** Omitted means "follow the remote's default branch",
  resolved at sync time (`git remote set-head … -a` + `symbolic-ref`). Set it
  only to pin a non-default branch.
- **One remote per upstream**, named `upstream-<key>`. The prefix avoids
  clobbering remotes the user already has. The ref is derived as
  `upstream-<key>/<branch>`; `SKILLS_UPSTREAM_REF` is no longer global.
- **The catalog is the source of truth for remotes.** A `sync-remotes` command
  reconciles git remotes from the catalog (add missing, fix changed URLs, fetch
  all, set default HEAD). Fresh clones stop hand-adding remotes.
- **Namespaced manifest keys: `<upstream>:<name>`.** The key is tool-facing only
  (the *invocable* name comes from `SKILL.md` frontmatter, not the key). This
  structurally eliminates cross-upstream key collisions (`matt:tdd` ≠ `foo:tdd`)
  with no manual disambiguation.
- **Two-command adoption.** `upstream-add <key> <url> [branch]` registers an
  origin; `add <key> <source> [mine] [mode]` adopts a skill from an already
  registered origin. Registering an origin and adopting a skill are separate
  concerns.
- **Clean migration, no dual-format support.** The legacy single-`upstream`
  schema is converted once (`upstream` → `upstreams.matt`, every fork gains
  `upstream: "matt"`); the tool only understands the new schema and fails loudly
  on the old one.

## Consequences

- The URL and branch of each origin are DRY; adding an origin is one catalog
  entry plus `sync-remotes`.
- Commands grow an upstream dimension (`update matt:tdd`), which is more verbose
  but unambiguous.
- `status`/`doctor`/`diff`/`update`/`pin` must iterate or resolve per-upstream
  refs instead of a single global ref.
- The `install.sh` flatten-by-folder-name collision is unchanged and still needs
  its own check — namespaced manifest keys do not fix folder-name clashes.
- A residual within-one-upstream basename collision (`matt:eng/tdd` vs
  `matt:prod/tdd`) still requires an explicit suffix at `add` time.
