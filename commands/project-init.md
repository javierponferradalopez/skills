---
description: Configure this project for Claude — for now only the task manager. Writes ~/harness/<slug>/config.json. Idempotent: if it exists, reads it and lets you edit.
---

# /project-init

Initialize or update the minimal configuration of the current project so skills know what setup you're working with.

## Where the config lives

Outside the repo, at `~/harness/<slug>/config.json`, where `<slug>` is computed like this (see `WORK_PHILOSOPHY.md`):

```bash
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SLUG="$(printf '%s' "$ROOT" | sed 's/[/.]/-/g')"
CONFIG="$HOME/harness/$SLUG/config.json"
```

The file is optional. If it doesn't exist, skills still work (they ask the user what they need). This command only creates it when you want to skip those questions in every session.

## Procedure

1. Compute `$CONFIG`. Create `~/harness/<slug>/` if it doesn't exist.
2. If `$CONFIG` exists, read it and show it to the user:
   > "You already have this config:
   > ```
   > <contents>
   > ```
   > Do you want to edit it, leave it as is, or reset it?"
   - If they say "leave it", end.
   - If they say "edit", ask only about the fields they want to change.
   - If they say "reset", proceed as if it didn't exist.
3. If `$CONFIG` doesn't exist (or is being reset), ask:
   - **Task manager**: `clickup` | `linear` | `jira` | `markdown` | `none`. (Metadata only — skills will use the value to suggest destinations. It does NOT connect to any API.)
4. Write `$CONFIG` with this exact format:

   ```json
   {
     "task_manager": "<clickup|linear|jira|markdown|none>"
   }
   ```

5. Show the user the absolute path of the created file and a reminder: "Skills (`ingest`, `subtasks`, `plan`, `verify`) will read this config when they need it."

## Rules

- The file is **personal and per-project**, outside the repo. Not versioned.
- **No secrets**: no API keys, no tokens, no passwords.
- **No API integrations**: declaring `task_manager: "clickup"` does NOT call ClickUp. It only tells skills "the manager of this project is ClickUp, ask the user for ClickUp URLs/IDs directly".
- **Minimal scope**: for now only `task_manager`. Don't add fields without a skill that reads them.

## Anti-patterns

- ❌ Creating the file inside the repo instead of `~/harness/<slug>/`.
- ❌ Saving secrets.
- ❌ Assuming the user wants reset when they say "edit". Ask the scope before overwriting.
- ❌ Adding speculative fields (`commit_style`, `test_command`, etc.) without a skill that consumes them.
