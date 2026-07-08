---
name: github-pr
description: Prepare and create a high-quality GitHub Pull Request for the current branch
---

# GitHub PR

Prepare a Pull Request for the current branch: infer the business *why* from the changes, and always present a preview for approval before creating anything.

## Procedure

1. **Gather context.** Run the commands; if one fails, say what's missing and ask only for that. Stop if it's not a git repo, `gh` isn't authenticated (surface the fix, e.g. `gh auth login`), or there are zero commits over the base (confirm the base).
   - **Repo & branch**: `git rev-parse --abbrev-ref HEAD`. Detect base: `git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'`, falling back to `main`, then `master`.
   - **Merge base**: `MB=$(git merge-base origin/$BASE HEAD)` (fetch origin first if needed).
   - **Changed files**: `git diff --name-only $MB..HEAD`, grouped by logical component.
   - **Commits**: `git log $MB..HEAD --no-merges` — take the dominant Conventional-Commits type/scope for the title, and infer problem + solution from the changes. Never list the commits one by one.
   - **Stacked PR**: a parent-PR reference in commits or branch-naming convention. If stacked, base on the previous branch and reference the related PRs.
   - **Linked issue**: if `docs/agents/issue-tracker.md` exists, it defines the project's tracker and how a ticket is referenced and fetched. Look for a reference in the user's input, the commit messages, and the branch name; if found, fetch the ticket and infer **Problem** from its stated need. Otherwise infer **Problem** from the commits and diff.
2. **Draft the title + description strictly against [`PR_FORMAT.md`](./PR_FORMAT.md)** — open it every run, don't draft from memory.
3. **Present the preview**: *"Review the PR draft. Reply `approve` to proceed or `edit:` with changes."* Never create the PR without explicit approval.
4. **On `approve`**: `gh pr create --assignee @me --title "<TITLE>" --body "<DESCRIPTION>"`, adding `--base <previous-branch>` only when stacked. Print the PR URL.
5. **On `edit:`**: apply the edits to the title/description only, re-show the preview, wait for `approve`.
