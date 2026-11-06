# Build brief

Append [`shared-directory.md`](shared-directory.md) verbatim to the message.

## Message

Invoke `/build <ticket reference>`. You run under an orchestrator, on GitButler branch `<branch>`, in a working tree that you share with other agents:

- Skip the start-state check of step 2: the orchestrator checked the base, and the tree is dirty with the work of the other agents.
- Wherever the skill reads `git diff HEAD` or `git status`, read them only for the paths you changed: `git diff HEAD -- <paths>`.

End your report with a `Files:` section: every path you created, modified or deleted, relative to the repo root.

## Resume line

Add it to the message when the ticket has earlier work from a previous run:

Earlier work on this ticket is committed as WIP on `<branch>`. Read it with `but diff <branch>`, and complete it.
