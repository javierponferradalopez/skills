# Observability: Sentry

Sentry is this repo's source for **errors and exceptions** in production — stack traces, breadcrumbs, affected releases, and how often an issue fires.

## Scope

- **Org**: `<sentry-org-slug>`
- **Project(s)**: `<sentry-project-slug>`

Queries target this org/project unless the user points at a different one.

## Connection

Operations go through the **Sentry MCP server** (`mcp__claude_ai_Sentry__*`), discovered on demand: run `ToolSearch` with a query like `sentry issues` to load the schemas, authenticate first if prompted, then call the tools.

## Conventions

- **Fetch an issue by reference**: resolve a Sentry issue link or short id to the issue, then read its latest event — stack trace, breadcrumbs, tags, and the event count / frequency.
- **Search issues**: query the configured project by message, culprit, release, or environment to find the issue behind a described symptom.
- **List recent issues**: the project's unresolved issues, most-frequent or most-recent first, to surface what is currently on fire.

## Referencing a Sentry issue

The user may pass a full **URL** (`<org>.sentry.io/issues/<id>` or `sentry.io/organizations/<org>/issues/<id>`) or a **short id** (`PROJECT-1A2B`). Normalise it:

- URL → extract the issue `<id>` segment.
- `PROJECT-XXXX` → resolve the short id to the issue.

## When a skill needs error context

Fetch the referenced issue's latest event and hand back the stack trace, breadcrumbs, affected release, and frequency. If only a symptom is described (no reference), search the project for the matching issue first.
