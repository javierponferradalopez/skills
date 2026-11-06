# Gaps brief

The gaps sub-agent is read-only. The orchestrator launches it with the review message, then resumes the same sub-agent with the plan message and the PR message: it already holds the ticket, its spec and the diff.

## Review message

Invoke `/gaps <ticket reference>`. You run under an orchestrator. The change is committed as a WIP on GitButler branch `<branch>`: wherever the skill reads `git diff HEAD` or `git status`, read `but diff <branch>`.

## Plan message

Invoke `/commit` to plan this ticket's atomic commits, reading `but diff <branch>` wherever the skill reads `git status` or `git diff HEAD`. Run only its planning steps and answer with the plan: the orchestrator creates the commits with `but`, so leave the branches and the working tree as they are. When one file goes into more than one commit, name the hunks of each commit.

## PR message

Invoke `/github-pr`: the changes are `but diff <branch>` and the commits of this branch in `but status -fv`. The PR is stacked on `<base branch>`. Stop at its approval gate and answer with the title and the description: the orchestrator publishes them.
