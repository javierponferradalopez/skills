# PR title & description format

## Title — Conventional Commits

- Format: `type(scope): concise, user-facing summary`
- Examples: `feat(api): add rate-limited search endpoint`, `fix(web): resolve 500 on profile save`
- Pick the dominant commit type; if mixed, choose the most impactful user-visible change (priority: feat, fix, perf, refactor, others).

## Description — Markdown, English, no fluff

Rules: use `##` and below (NO `#`). No raw diffs. No code blocks in the body. Each bullet short. Infer the business "why" from the technical changes.

```markdown
## Problem

If a task/issue URL was provided, include it as the first line: `This PR resolves <task-url>`. Otherwise omit this line.

[Infer the problem being solved from the commits and changes — the business need or technical requirement that motivated them.]

## Solution

[Explain the changes useful to the reviewer, without redundant technical detail already visible in the diff.]

- **[Category of changes]**
    - [Specific implementation detail]
    - [Another relevant detail]

### Commits
> Review each commit individually for easier navigation:

| Commit | Summary |
|--------|---------|
| [`abc1234`](https://github.com/owner/repo/commit/full_sha) | Adds input validation for email and password to prevent malformed data reaching the API |
| [`def5678`](https://github.com/owner/repo/commit/full_sha) | Refactors the auth service to use dependency injection, improving testability |

*(List all commits oldest → newest. Write a human-friendly summary of what each does based on the actual changes, NOT just the commit message — focus on purpose and impact.)*

### Technical Implementation (if not covered above)
- 3–6 crisp bullets on key design/architecture decisions, tradeoffs, or constraints.

### Testing
- ✅ What was tested (unit, integration, e2e).
- ✅ Relevant QA steps or manual verification.
- ❌ What was not tested, if applicable.
- ❌ Known limitations or risks.

### Next Steps (only if applicable)
- Short bullets for follow-ups or stacked PRs.

### Related (ONLY if there are PR/issue references or stacked PR links — if the only reference would be the task URL already at the top of Problem, OMIT this entire section)
- PR/issue references discovered (e.g. `#123`, `#456`) and links to dependent/parent PRs if stacked.
```

Do NOT add the current branch name or repeat the task URL in **Related** — it's redundant.
