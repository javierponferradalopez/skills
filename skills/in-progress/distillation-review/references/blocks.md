# Block schema — what the agent fills in `review-data.js`

`generate.mjs` writes `window.REVIEW_DATA = {…}` with `mentalMap`, `diagrams`, and
`keyChanges` set to `null` (plus a `role` to add on each project). Fill **only those**,
in place. Everything else is **true by construction** — the diff hunks, the `files`
tree, the `projects` grouping (name/path/counts), and every file's `link` are
derived verbatim from `git`/`GitHub`. Never edit `files`, `meta`, `projects` counts,
a `link`, or any diff line.

## What the script already computed (do not edit)

- `meta.source` — `"local" | "pr" | "branch"` (drives the header badge).
- `files[].projectHint` — deepest package-manifest dir above the file, or `null`.
- `files[].project` — the resolved grouping key (`projectHint` or top path segment).
- `files[].link` — the reviewer's jump target: `{ mode:"href", href }` for a PR
  (anchored diff URL) or branch (blob URL), `{ mode:"copy", path }` for local.
- `projects[]` — `{ name, path, fileCount, added, removed }` per touched project,
  sorted by churn. **You add `role`** (see below); leave the rest alone.

## The prose fields

### `mentalMap` — `{ problem, approach, impact }`
The mental map of the problem solved, grounded in the repo context you read (step 2),
**not** a diff recap. Three short strings:
- `problem` — what hurt / what was missing / why this exists.
- `approach` — how the change attacks it (the shape of the solution).
- `impact` — what changes for the user or the system (behaviour, contracts, risk).

### `projects[].role` — string (one per touched project)
Add a `role` field to each entry in the existing `projects[]` array — one line on the
part this project plays in the change (e.g. `"api"` → "adds the /invites endpoint",
`"ui"` → "consumes it", `"shared"` → "new Invite type"). Do not touch `name`, `path`,
or the counts. Only correct a file's `project` field if the manifest heuristic
mis-split an unusual architecture.

### `diagrams` — array of 1–4 typed diagrams, or `[]`
Draw a diagram when a graph reliably communicates something the prose can't — a
class/inheritance hierarchy, entity relations, a type graph, a request flow, a state
machine. Each entry:

```js
{
  kind: "inheritance",           // "inheritance" | "relationship" | "types" | "flow" | "state"
  title: "Policy resolution order",
  mermaid: "graph TD; A-->B"     // valid Mermaid source; keep node labels short
}
```

Use `[]` (not `null`) when no diagram earns its place — a diagram of two files is
noise. Cap at **4**; prefer fewer, purposeful diagrams over many decorative ones.

### `keyChanges` — array of 3–8 curated tabs
The heart of the review. Each entry promotes one changed file to a tab. **Curate**:
pick the 3–8 changes that matter and **order them by disruption, most disruptive first**.
Skip trivial files.

```js
{
  path: "src/auth/policy.ts",   // MUST match a file in REVIEW_DATA.files — the diff & link are pulled from there
  project: "packages/auth",      // the project this change belongs to (match files[].project)
  blockType: "diff",             // "diff" | "data-model" | "api-endpoint" | "wireframe"
  impact: "breaking",            // "breaking" | "risky" | "safe" — your judgement, read the diff + context
  impactWhy: "Removes the public canEdit() export; downstream callers must migrate.",
  title: "Tighten viewer permissions",   // < 70 chars
  summary: "Viewers can no longer edit shared docs; the check moved to the policy layer.",
  wireframeHtml: "<div>…</div>"  // ONLY for blockType "wireframe" — optional inline HTML mockup
}
```

## Choosing `blockType`

Classify by what the change *is*, not just the filename. `files[].hint` is a cheap
path-based guess — trust your reading of the diff over it.

- **`data-model`** — schema/migration/entity/persistence shape changes.
- **`api-endpoint`** — API surface: routes, controllers, request/response contracts, GraphQL/OpenAPI.
- **`wireframe`** — user-facing UI. Optionally add `wireframeHtml`: a small, self-contained HTML sketch of the affected screen/component (inline styles only). It renders inside a dashed box above the diff.
- **`diff`** — everything else (logic, config, tests, tooling). The default.

The rendered tab always shows the real diff hunks for `path` regardless of block
type — the block type drives the label and (for wireframe) the optional mockup.
It never replaces the diff.

## Choosing `impact`

Your judgement after reading the diff and the context — the script does **not** guess
this. Order `keyChanges` by it.

- **`breaking`** — removes/changes a public contract, deletes a used symbol, a
  migration that isn't backward-compatible, anything that forces callers to change.
- **`risky`** — behaviour changes in a hot path, tricky logic, wide blast radius, but
  no hard break.
- **`safe`** — additive, isolated, well-tested, or mechanical.

`impactWhy` is one line: *who* it affects and *why it could hurt* — the reviewer's
"look here first".

## Budget

- 3–8 key-change tabs. More than 8 → the reader drowns; curate harder.
- 1–4 diagrams, or `[]`. Titles under 70 characters.
- One `role` line per project; keep each tab focused on one file's story.

## Grounding

Prose explains *intent, the problem, and risk*. Structured content (diff lines, file
tree, stats, project grouping, links) is already true by construction. Do not restate
diff lines in prose, and never edit them — if a hunk looks wrong, that is the real
code, report it in the summary.
