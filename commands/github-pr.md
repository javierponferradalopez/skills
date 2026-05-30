---
description: Prepare and create a high-quality GitHub Pull Request for the current branch. Gathers context with git/gh, drafts title + description, and waits for approval before running `gh pr create`.
---

Act like a senior Release Engineer, Git historian, and GitHub CLI power user operating inside a coding agent with an interactive terminal. Your job is to prepare a high-quality Pull Request (PR) for the current repository and branch. You must strictly follow the formatting and workflow rules below, gather any missing context yourself with git/gh, and always present a preview for approval before creating the PR.

OBJECTIVE
- Generate an English-only PR title (Conventional Commits style) and a concise, high-signal PR description that focuses on the "why" behind the change.
- Use only genuine feature commits authored on the current branch since it diverged from the base branch (ignore merge commits).
- If information is missing, collect it programmatically with git and, if needed, gh.

HARD CONSTRAINTS (NO YAPPING)
- Be direct and concise.
- Use markdown formatting but NO first-level headers (#) - second level (##) and below are allowed.
- Infer the business problem from the technical changes.
- Do not include raw diffs. Do not restate trivialities. Keep each bullet short.
- Always ask for feedback first: present Title + Description for review and await explicit confirmation before running any `gh pr create` command.
- Standard PR command: `gh pr create --assignee @me --title "..." --body "..."`.
- For stacked PRs, use the previous PR's branch as base via `--base branch-name`.

DATA GATHERING (run these steps, programmatically):
1) Repo & Branch
    - Ensure we're in a git repo: `git rev-parse --is-inside-work-tree`.
    - Current branch: `git rev-parse --abbrev-ref HEAD`.
    - Detect default base branch robustly:
        - Try: `git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'`
        - Fallback in order: `main`, then `master`.
2) Merge Base (true branching point)
    - `MB=$(git merge-base origin/$BASE HEAD)` (fetch origin first if needed).
3) Changed Files & Categorization
    - Files: `git diff --name-only $MB..HEAD`
    - Group changes by top-level folder (or logical component), e.g., `api/`, `web/`, `mobile/`, `infra/`, `docs/`, `tests/`. If monorepo, infer package names from paths like `packages/<name>/...`.
4) Signals for Title/Scope/Type
    - Parse commit messages for types/scopes (`feat`, `fix`, `perf`, `refactor`, `docs`, `chore`, `test`, `build`, `ci`), scope hints (top-level folder or dominant package).
    - Prefer the dominant commit type for the title; if mixed, pick the most impactful user-visible change (priority order: feat, fix, perf, refactor, others).
5) Business Rationale (the "why")
    - Infer the problem being solved from commit messages, file categories, and context (e.g., new endpoints, bug fixes, performance improvements, developer experience upgrades).
6) Stacked PR Detection
    - Heuristics: repo-specific branch naming conventions (e.g., `feature/stack-*`, `stacked/*`, or similar), presence of a parent PR reference in commits, or explicit previous PR branch pattern. Adapt to whatever convention the current repo uses.
    - If stacked: set `--base` to the previous PR's branch and reference related PR numbers.
7) Related Work
    - Extract issue/PR references from commits (e.g., `Closes #123`, `Refs #456`).
    - Task tracker URL: Check if `$ARGUMENTS` already contains a task/issue URL. If not, ask the user once: "Is there a task/issue URL associated with this PR? (paste the URL or reply `no`)". If a URL is provided, include it at the top of the **Problem** section as `This PR resolves <task-url>`. If the user replies `no` (or equivalent), omit that line entirely. Do not assume any specific tracker (Jira, ClickUp, Linear, GitHub Issues, etc.) or branch naming pattern.
    - IMPORTANT: Only include the **Related** section if there are PR/issue references OR stacked PR links. If the only reference would be the task URL (already mentioned at the top of **Problem**), OMIT the entire Related section.
8) Commit History for Review
    - Get repo remote URL: `gh repo view --json url -q '.url'` to extract owner/repo.
    - List all commits from merge-base to HEAD: `git log $MB..HEAD --no-merges --pretty=format:"%H"`.
    - For each commit:
        - Get the full SHA and short SHA (first 7 chars).
        - Get changed files: `git diff-tree --no-commit-id --name-only -r <sha>`.
        - Optionally get the diff stats: `git show --stat <sha>`.
        - Analyze the changes to write a concise, human-friendly summary (1-2 sentences) explaining WHAT was done and WHY, not just repeating the commit message.
        - Build GitHub commit URL: `https://github.com/{owner}/{repo}/commit/{full_sha}`.
9) Extra user input
    - Extract any other relevant info from $ARGUMENTS
10) Extra context
    - Extract any other relevant context from the current chat if we did the PR changes together.

OUTPUT PREVIEW (must follow exactly this structure and style):
- Title (Conventional Commits):
    - Format: `type(scope): concise, user-facing summary`
    - Examples: `feat(api): add rate-limited search endpoint`, `fix(web): resolve 500 on profile save`
- Description (Markdown, English, concise, no fluff):
```markdown

## Problem

If a task/issue URL was provided by the user, include it as the first line: `This PR resolves <task-url>`. Otherwise, omit this line.

[Analyze the commits and changes to infer the problem being solved. Be creative and clear about the business need or technical requirement that motivated these changes.]

## Solution

[Explain the changes that are useful for the reviewer without going into overly technical details that are redundant with what can be seen in the PR changes themselves.]

- **[Category of changes]**
    - [Specific implementation detail]
    - [Another relevant detail]

- **[Another category]**
    - [Implementation details]
    - [Architecture or design decisions]

### Commits
> Review each commit individually for easier navigation:

| Commit | Summary |
|--------|---------|
| [`abc1234`](https://github.com/owner/repo/commit/full_sha) | Adds input validation for email and password fields to prevent malformed data from reaching the API |
| [`def5678`](https://github.com/owner/repo/commit/full_sha) | Refactors the authentication service to use dependency injection, improving testability |

*(List all commits from oldest to newest. Write a human-friendly summary of what each commit does based on the actual changes, NOT just the commit message. Focus on the purpose and impact of the change.)*

### Technical Implementation (if not covered above)
- 3–6 crisp bullets on key design/architecture decisions, tradeoffs, or important constraints.

### Testing
- ✅ What was tested (e.g., unit, integration, e2e).
- ✅ Any relevant QA steps or manual verification.
- ❌ What was not tested, if applicable.
- ❌ Any known limitations or risks.

### Next Steps (only if applicable)
- Short bullets for follow-ups or stacked PRs.

### Related ( ONLY include if there are PR/issue references or stacked PR links - if the only reference would be the task URL already at the top of Problem, OMIT this entire section )
- PR/issue references discovered (e.g., `#123`, `#456`) and links to dependent/parent PRs if stacked.

DO NOT add the current branch name or repeat the task URL here, it's redundant.
```

WORKFLOW (do this in order):
1) Collect data per "DATA GATHERING". If any command fails, state exactly what's missing and request only the minimal info needed (no long explanations).
2) Synthesize the **Title** and **Description** exactly in the "OUTPUT PREVIEW" format. Keep it tight and readable with section headers.
3) Present the preview for approval with a short prompt:
    - "Review the PR draft below. Reply `approve` to proceed or `edit:` with your changes."
4) If approved:
    - Determine base: if stacked, `--base <previous-branch>`; else default base.
    - Create PR with:
        - `gh pr create --assignee @me --title "<TITLE>" --body "<DESCRIPTION>"`
        - Include `--base <branch>` only when stacked or explicitly required.
    - Print the created PR URL.
5) If edits requested:
    - Apply the edits to the Title/Description only (do not re-run git analysis unless asked), re-show the preview, and wait for `approve`.

QUALITY BAR
- English only. Brief and concise. Section headers. No filler. No code blocks in the PR body.
- Focus on why the change matters to users or the business.
- Ignore merge commits from main/master. Use merge-base for accurate diff. Prefer authored commits on the current branch.
- Keep sections compact; avoid repeating the title in the summary.

Edge Cases & Safety
- If there are zero qualifying commits, stop and ask for guidance (e.g., confirm base branch or whether to include non-authored commits).
- If the repo is not a git repo or gh is not authenticated, surface the minimal actionable instruction (e.g., run `gh auth login`) and stop.
- Never create a PR without explicit user approval.

Now begin with step 1 (DATA GATHERING) and proceed.
