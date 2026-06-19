# Issue tracker: ClickUp

This repo's PRDs and issues live as ClickUp tasks. Every operation goes through
the **ClickUp MCP server**, discovering the tools on-demand with ToolSearch.

## Hierarchy

```
(Epic task — optional)
└── PRD (task)
    └── Issues (subtasks of the PRD)
```

- The fixed relationship is **PRD → Issues**: issues always hang as subtasks of
  the PRD.
- Above the PRD there may optionally be an epic task. It is not required.
- **Every creation starts from a reference the user gives you.** Never create a
  top-level task on your own.
- Since everything hangs off an existing task, its location (List / Space /
  Folder) is inherited. There is nothing to configure for that.

## Task references

The user may reference tasks in three formats:

- **URL** (`app.clickup.com/t/<id>`) → extract the `<id>`.
- **Custom ID** (e.g. `PD-615`) → use it as-is.
- **Internal ID** → use it as-is.

## When a skill says "publish to the issue tracker"

Create a ClickUp task **following the reference the user gives you**:

- If the reference is an **existing epic task** → create the PRD as a subtask of
  it.
- If the reference is a **placeholder task that is already the epic** → write
  the PRD directly into that task's description (don't create anything new) and
  **also update the title** of that task.

The PRD body and the issue bodies go in the task **description**.

## When a skill says "fetch the relevant ticket"

Always fetch the task's **description + comments**.

Context scope:
- **One level up** (only if a parent exists).
- **One level down**, listing the child tasks.
- No recursion.

## Creating issues

- Create them **in dependency order**.
- For each blocking relationship, also create the **native ClickUp dependency**
  (blocking / waiting on) with the real IDs — not just by mentioning it in the
  issue text.

## Metadata

Don't set status, tags, priority, assignees, or custom fields. Leave the List's
default values when creating/editing tasks.
