# Issue tracker: ClickUp

Issues and specs for this repo live as ClickUp tasks, used as a three-level hierarchy.

Operations go through the **ClickUp MCP server** (`mcp__claude_ai_ClickUp__*`). The exact tool set is discovered on demand: run `ToolSearch` with a query like `clickup task` to load the schemas, authenticate first if prompted, then call the tools. For headless/cron runs where the MCP server is unavailable, fall back to the ClickUp REST API with a `CLICKUP_API_TOKEN`.

## Hierarchy

Three levels, relying on ClickUp **nested subtasks**:

```
Product epic (Task)          ← created by product. Requirements + acceptance criteria. We only READ it.
└─ Tech task (subtask)       ← the spec. Created/filled by `to-spec`.
   └─ Issues (nested subtasks) ← tracer-bullet slices. Created by `to-tickets`.
```

The skills **never create top-level tasks** — the tech task always hangs off a product epic, and issues always hang off the tech task. Everything inherits the parent's List, so no List/Space/Folder needs configuring here.

## Referencing a ticket

The user passes either a full task **URL** (`app.clickup.com/t/<id>`) or a **custom ID** (`GEN-142`). Normalise it:

- URL → extract the `<id>` segment.
- `LETTERS-number` → resolve the custom ID to the internal task ID via the API/MCP.
- Otherwise → treat it as an internal task ID.

## When a skill says "publish to the issue tracker"

- **`to-spec`** — the spec lives in the **description** of the tech task.
  - If the reference is a **product epic**, create a new subtask (the tech task) under it and write the spec into its description.
  - If the reference is already a **tech task**, write the spec into its description (create nothing).
  - Content convention: start with a link to the parent product epic plus 1–2 sentences of context. **Do not recopy** requirements or acceptance criteria — the product epic is their source of truth and they must not diverge. The bulk of the tech spec is implementation/testing decisions and technical references for the nested issues.
  - Adapting `to-spec`'s template here: `Problem Statement`, `Solution` and `User Stories` are owned by the product epic — **replace them with the link + 1–2 sentence summary** rather than reproducing them. Keep `Implementation Decisions`, `Testing Decisions`, `Out of Scope` and `Further Notes` in full; that is the value the tech task adds on top of the epic.
- **`to-tickets`** — create the slices as **nested subtasks** under the tech task, in dependency order. For each "Blocked by" relationship, also create the **native ClickUp dependency** (blocking / waiting on) using the real task IDs, in addition to mentioning it in the issue text.

Record decisions and conversation history as **native task comments**, not by editing the description (the description is reserved for the spec / issue body).

Do not set status, tags, custom fields, assignees or priority — leave the List defaults. (If a workspace needs specific metadata, add those rules here.)

## When a skill says "fetch the relevant ticket"

Resolve the reference, then read **one level up + one level down**:

- Reference is a **tech task** → read its description + comments, read its parent **product epic** (requirements + acceptance criteria) for context, and list its existing issue subtasks.
- Reference is a **product epic** → read its requirements + acceptance criteria and list the tech tasks under it.
- Reference is an **issue** (subtask) → read its body + comments and read its parent **tech task** for context.

Do not pull the whole branch recursively — one level up and one level down is enough.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single task with **child** subtasks as tickets.

- **Map**: a task tagged `wayfinder:map` (`clickup_add_tag_to_task`), holding the Destination / Notes / Decisions-so-far / Not-yet-specified / Out-of-scope body in its description. Wayfinding is the exception to the "never create top-level tasks" rule — the map may be a top-level task, or hang under a product epic when there is one.
- **Child ticket**: a subtask of the map task, carrying its `## Question` in the description and tagged `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`). Once claimed, the ticket is assigned to the driving dev.
- **Blocking**: ClickUp's **native task dependencies** (`clickup_add_task_dependency`, blocking / waiting on) using the real task IDs — the canonical, UI-visible representation. A ticket is unblocked when every blocker is closed.
- **Frontier query**: `clickup_filter_tasks` scoped to the map's subtasks, drop any with an open blocker (a waiting-on dependency to an unclosed task) or an assignee; first in map order wins.
- **Claim**: assign the subtask to yourself (`clickup_update_task`) — the session's first write.
- **Resolve**: post the answer as a task comment (`clickup_create_comment`), set the subtask's status to a closed/done state, then append a context pointer (asset + link) to the map's Decisions-so-far.
