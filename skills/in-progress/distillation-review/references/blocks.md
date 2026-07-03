# Block schema — what the agent fills in `review-data.js`

`generate.mjs` writes `window.REVIEW_DATA = {…}` with three fields set to `null`.
Fill **only those nulls**, in place. Everything else is **true by construction** —
copied verbatim from `git`. Never edit `files`, `meta`, or any diff line.

## The three prose fields

### `narrative` — string | string[]
1–3 short paragraphs: what this branch does and why it exists. Intent and risk,
not a line-by-line recap of the diff. A string with `\n\n` splits into paragraphs;
an array is one entry per paragraph.

### `diagram` — `{ title, mermaid }` | leave `null`
One diagram when a graph/flow reliably communicates the change (dependencies
between touched modules, a request flow, a state machine). `mermaid` is valid
Mermaid source (e.g. `graph TD; A-->B`). Omit (`null`) when no diagram earns its
place — a diagram of two files is noise. Keep node labels short.

### `keyChanges` — array of 3–8 curated tabs
The heart of the review. Each entry promotes one changed file to a tab. **Curate**:
pick the 3–8 changes that matter, ordered most-important first. Skip trivial files.

```js
{
  path: "src/auth/policy.ts",   // MUST match a file in REVIEW_DATA.files — the diff is pulled from there
  blockType: "diff",             // "diff" | "data-model" | "api-endpoint" | "wireframe"
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

## Budget

- 3–8 key-change tabs. More than 8 → the reader drowns; curate harder.
- Titles under 70 characters.
- Keep each tab focused on one file's story; the diff length is whatever git produced.

## Grounding

Prose explains *intent and risk*. Structured content (diff lines, file tree, stats)
is already true by construction. Do not restate diff lines in prose, and never edit
them — if a hunk looks wrong, that is the real code, report it in the summary.
