# Issue tracker: ClickUp

Issues and PRDs for this repo live as ClickUp tasks, used as a three-level hierarchy.

Operations go through the **ClickUp MCP server** (`mcp__claude_ai_ClickUp__*`). The exact tool set is discovered on demand: run `ToolSearch` with a query like `clickup task` to load the schemas, authenticate first if prompted, then call the tools. For headless/cron runs where the MCP server is unavailable, fall back to the ClickUp REST API with a `CLICKUP_API_TOKEN`.

## Hierarchy

Three levels, relying on ClickUp **nested subtasks**:

```
Product epic (Task)          ← created by product. Requirements + acceptance criteria. We only READ it.
└─ Tech task (subtask)       ← the PRD. Created/filled by `to-prd`.
   └─ Issues (nested subtasks) ← tracer-bullet slices. Created by `to-issues`.
```

The skills **never create top-level tasks** — the tech task always hangs off a product epic, and issues always hang off the tech task. Everything inherits the parent's List, so no List/Space/Folder needs configuring here.

## Referencing a ticket

The user passes either a full task **URL** (`app.clickup.com/t/<id>`) or a **custom ID** (`GEN-142`). Normalise it:

- URL → extract the `<id>` segment.
- `LETTERS-number` → resolve the custom ID to the internal task ID via the API/MCP.
- Otherwise → treat it as an internal task ID.

## When a skill says "publish to the issue tracker"

- **`to-prd`** — the PRD lives in the **description** of the tech task.
  - If the reference is a **product epic**, create a new subtask (the tech task) under it and write the PRD into its description.
  - If the reference is already a **tech task**, write the PRD into its description (create nothing).
  - Content convention: start with a link to the parent product epic plus 1–2 sentences of context. **Do not recopy** requirements or acceptance criteria — the product epic is their source of truth and they must not diverge. The bulk of the tech PRD is implementation/testing decisions and technical references for the nested issues.
  - Adapting `to-prd`'s template here: `Problem Statement`, `Solution` and `User Stories` are owned by the product epic — **replace them with the link + 1–2 sentence summary** rather than reproducing them. Keep `Implementation Decisions`, `Testing Decisions`, `Out of Scope` and `Further Notes` in full; that is the value the tech task adds on top of the epic.
- **`to-issues`** — create the slices as **nested subtasks** under the tech task, in dependency order. For each "Blocked by" relationship, also create the **native ClickUp dependency** (blocking / waiting on) using the real task IDs, in addition to mentioning it in the issue text.

Record decisions and conversation history as **native task comments**, not by editing the description (the description is reserved for the PRD / issue body).

Do not set status, tags, custom fields, assignees or priority — leave the List defaults. (If a workspace needs specific metadata, add those rules here.)

## When a skill says "fetch the relevant ticket"

Resolve the reference, then read **one level up + one level down**:

- Reference is a **tech task** → read its description + comments, read its parent **product epic** (requirements + acceptance criteria) for context, and list its existing issue subtasks.
- Reference is a **product epic** → read its requirements + acceptance criteria and list the tech tasks under it.
- Reference is an **issue** (subtask) → read its body + comments and read its parent **tech task** for context.

Do not pull the whole branch recursively — one level up and one level down is enough.
