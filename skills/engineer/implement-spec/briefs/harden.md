# Harden brief

Append [`shared-directory.md`](shared-directory.md) verbatim to the message.

## Message

Invoke `/harden <ticket reference>`. You run under an orchestrator. The change is committed as a WIP on GitButler branch `<branch>`: wherever the skill reads `git diff HEAD` or `git status`, read `but diff <branch>`.

End your report with a `Files:` section: every path you created, modified or deleted, relative to the repo root. An empty list is valid.
