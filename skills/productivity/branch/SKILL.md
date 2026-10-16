---
name: branch
description: Create a git branch off the current one, named `<task-code>-<type>-<description>`. Use when the user wants a new branch.
---

# Branch

Create a branch off the current branch. Hyphens join the three segments of the name; underscores join the words of the description:

`<task-code>-<type>-<description>`, for example `PD-1234-feature-creation_resource_endpoint`.

## 1. Find the segments

- **Task code**: find the task in the session. Write its reference as `docs/agents/issue-tracker.md` defines it, without `#`: the ClickUp custom ID `PD-1234` stays `PD-1234`, the issue `#42` becomes `42`. If the session has no task, ask the user for its code.
- **Type**: one of `feature`, `fix`, `hotfix`, `chore`, `refactor`, `docs`, `test`, inferred from the session. If more than one type fits, ask the user.
- **Description**: the work of the session in five words or fewer. If the session does not tell enough, fetch the relevant ticket and use its title. Write lowercase ASCII words.

The step is done when you know all three segments.

## 2. Propose the name

Show the full name. Go to step 3 only on an explicit OK from the user.

## 3. Create the branch

```bash
git switch -c <name>
```

If git says that the branch exists, tell the user and stop.
