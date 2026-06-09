---
name: github-pr
description: Prepare and create a high-quality GitHub Pull Request for the current branch — gathers git/gh context, drafts a Conventional-Commits title and a why-focused description, and waits for explicit approval before running `gh pr create`. Use when the user asks to open, create, draft, or raise a PR for the current branch.
---

# GitHub PR

Act as a senior Release Engineer and Git historian. Prepare a high-quality Pull Request for the current branch: infer the business "why" from the technical changes, draft a tight title + description, and **always present a preview for approval before creating anything**.

## Procedure

1. **Gather context** (programmatically; if a command fails, state exactly what's missing and ask only for the minimal info needed):
   - **Repo & branch**: `git rev-parse --is-inside-work-tree`, `git rev-parse --abbrev-ref HEAD`. Detect base: `git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'`, falling back to `main`, then `master`.
   - **Merge base**: `MB=$(git merge-base origin/$BASE HEAD)` (fetch origin first if needed).
   - **Changed files**: `git diff --name-only $MB..HEAD`, grouped by top-level folder / logical component (infer package names in a monorepo).
   - **Type/scope signals**: parse commit messages for Conventional-Commits types/scopes; prefer the dominant type for the title.
   - **Commit history**: `git log $MB..HEAD --no-merges --pretty=format:"%H"`. For each commit, get changed files (`git diff-tree --no-commit-id --name-only -r <sha>`) and write a human-friendly 1–2 sentence summary of WHAT and WHY. Build URLs from `gh repo view --json url -q '.url'`: `https://github.com/{owner}/{repo}/commit/{full_sha}`.
   - **Stacked PR detection**: repo branch-naming conventions or a parent-PR reference in commits. If stacked, base on the previous PR's branch and reference related PRs.
   - **Related work**: extract `Closes #123` / `Refs #456` from commits. For a task/issue URL, first check anything the user passed when invoking the skill or said in the conversation; if absent, ask once: *"Is there a task/issue URL for this PR? (paste it or reply `no`)"*. If provided, put `This PR resolves <task-url>` as the first line of **Problem**; if `no`, omit it. Don't assume any specific tracker.
2. **Read [`PR_FORMAT.md`](./PR_FORMAT.md) and draft the title + description strictly against it.** It defines the title convention and every description section, including the **mandatory Commits table**. Ignore merge commits; use merge-base for an accurate diff. Do not draft from memory — open the file every run.
3. **Present the preview for approval**: *"Review the PR draft below. Reply `approve` to proceed or `edit:` with your changes."* Never create a PR without explicit approval.
4. **On `approve`**: create it. `gh pr create --assignee @me --title "<TITLE>" --body "<DESCRIPTION>"`, adding `--base <previous-branch>` only when stacked or explicitly required. Print the created PR URL.
5. **On `edit:`**: apply the edits to the title/description only (don't re-run git analysis unless asked), re-show the preview, and wait for `approve`.
6. **Offer reviewer suggestions** (after the PR is created): ask once — *"Want me to suggest reviewers for this PR? (`yes`/`no`)"*. Only if the user says yes, invoke the [`suggest-reviewers`](../suggest-reviewers/SKILL.md) skill to produce a ranked checklist from the branch's history + CODEOWNERS, present it, and ask the user to mark who to request. Assign only the handles they explicitly pick: `gh pr edit <pr> --add-reviewer <handle,handle>`. If the user declines, picks none, or skips, assign nobody. Never request review from the PR author.

## Output

Title + description posted to the GitHub PR on `approve` — nothing is written to disk before that. Format is fully defined in [`PR_FORMAT.md`](./PR_FORMAT.md); the non-negotiables:

- Direct and concise. Markdown with `##` and below (NO `#` headers). No raw diffs, no code blocks in the body.
- A **Commits table** is always present: one row per non-merge commit (oldest → newest), each linking the short SHA to its commit URL with a human-written summary of purpose and impact — never the raw commit message.
- Focus on why the change matters to users or the business; don't restate the title or the diff.

## Anti-patterns

- ❌ Drafting the description from memory without opening `PR_FORMAT.md` — this is the main reason drafts drift from the template.
- ❌ Omitting the Commits table, or filling it with raw `git log` messages instead of inferred per-commit summaries.
- ❌ Running `gh pr create` before the user approves the preview.
- ❌ Restating the diff or dumping raw commit messages instead of inferring the "why".
- ❌ Including a **Related** section whose only content would be the task URL already at the top of **Problem**.
- ❌ Assuming a specific tracker (Jira/ClickUp/Linear/GitHub Issues) or branch-naming convention.
- ❌ Proceeding when it's not a git repo or `gh` isn't authenticated — surface the minimal fix (e.g. `gh auth login`) and stop. Same for zero qualifying commits: stop and confirm the base branch.
