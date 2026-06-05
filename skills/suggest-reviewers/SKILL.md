---
name: suggest-reviewers
description: Suggest GitHub reviewers for the current branch's Pull Request by ranking the people who actually own and recently touched the changed files (git history + CODEOWNERS). Use when the user asks who should review this PR/branch or wants reviewer suggestions. Also invoked as the final step of the github-pr skill.
---

# Suggest Reviewers

Act as a senior maintainer who knows the codebase's social graph. Given the current branch's diff, produce a ranked, justified shortlist of GitHub users to request review from — grounded in who recently authored the changed files and who owns them via CODEOWNERS.

**Core principle — keep the heavy history out of context.** The `git log`/`git blame` over every changed file can be megabytes. Never read that raw. The bundled script aggregates it in the shell and returns only a compact top-N table (~10 rows). You reason over that table, not over commit history.

## Procedure

1. **Run the ranking script** (it resolves base branch, merge-base, changed files, recency-weighted contributor scores, and email→GitHub-login mapping — all in the shell). The script lives next to this file, in `scripts/` — run it by its path relative to this skill's directory:

   ```bash
   scripts/rank-contributors.sh --top 10
   ```

   Pass `--base <ref>` only if the user names a non-default base; `--months`/`--recent-days`/`--top` are tunable but the defaults (12mo window, 90-day recency boost, top 10) are good. The script operates on the repo via `git`, so it works regardless of the directory it's invoked from.
   - If it exits non-zero, surface the exact error (not a git repo, no merge-base → suggest `git fetch origin`, no history) and stop. Don't fabricate names.

2. **Read CODEOWNERS if present** (`.github/CODEOWNERS`, `CODEOWNERS`, or `docs/CODEOWNERS`). These files are small — reading them into context is fine and expected. Match each changed file (listed in the script's `# changed_files_list:` block) against the ownership patterns and collect the owning `@user`/`@org/team` handles. If no CODEOWNERS file exists, skip this silently.

3. **Merge and clean the candidate set:**
   - **Dedupe linked rows by GitHub login** — the same person may appear under multiple commit emails (e.g. work + personal). Sum their scores into one row. **Do NOT merge unresolved rows together**: every row whose login is `-` is a *distinct* person; dedupe those by name/email, never by the shared `-` placeholder.
   - **Exclude the PR author / current user**: `gh api user -q .login`. Never suggest the author as their own reviewer.
   - **Drop bots only**: skip logins ending in `[bot]`.
   - **Keep contributors with no linked GitHub account** — they rank by the exact same score as everyone else. A `-` login means GitHub couldn't map their commit email to an account, not that their review is worth less. List them by name `<email>` (you cannot `@`-mention them) with a short `(no linked GitHub account — ping manually)` note so the user knows to reach them outside the reviewer field.
   - **CODEOWNERS owners always make the shortlist**, even if their commit score is low — ownership is an explicit signal. Flag them as owners.

4. **Present the checklist** in the conversation. One line per candidate, ranked (owners and high-score contributors first), each with a one-phrase justification grounded in the data:

   ```
   Suggested reviewers for this PR (base: <base>, <N> files changed):

   - [ ] @ana — CODEOWNER of `commons/permissions/**` · 22 recent commits across 5 changed files
   - [ ] @luis — top contributor: 31 commits, 4/17 changed files
   - [ ] @marta — recently active in `apps/panel/**` (10 commits, last 90 days)
   - [ ] Diego Ruiz <diego@example.com> — top contributor: 18 commits, 6/17 changed files · no linked GitHub account, ping manually
   ```

   Justifications come from the script columns (score / commits / recent / files) and CODEOWNERS matches — never invented. Contributors without a linked GitHub account appear in the same ranking by score; show them by name `<email>` instead of an `@handle`.

## Modes

- **Standalone** (user invoked `/suggest-reviewers` directly): output the checklist in the conversation and **stop**. No writes, no `gh pr edit`. The user adds whoever they want themselves.
- **Called by `github-pr`**: same ranking, but after the user marks their picks the calling skill assigns them to the existing PR with `gh pr edit <pr> --add-reviewer <handle,handle>`. Only assign the handles the user explicitly checked. Contributors with no linked GitHub account can't be added this way — if the user picks one, skip the `--add-reviewer` call for them and tell the user to ping that person manually (they have no handle to assign).

## Output

A ranked markdown checklist of GitHub `@handles` with data-backed justifications. Nothing is written to disk or to GitHub in standalone mode.

## Anti-patterns

- ❌ Reading raw `git log`/`git blame` into context instead of using the script's aggregated table — defeats the entire design.
- ❌ Listing the same person twice because they commit under two emails — dedupe by login.
- ❌ Dropping a strong contributor just because their commit email isn't linked to a GitHub account — they rank by the same score; list them by name `<email>` with a "ping manually" note.
- ❌ Collapsing several unlinked contributors into one row because they all show login `-` — they're different people; dedupe by name/email.
- ❌ Suggesting the PR author as a reviewer of their own PR.
- ❌ Inventing a justification ("expert in this area") not backed by the script columns or CODEOWNERS.
- ❌ Running `gh pr edit --add-reviewer` in standalone mode, or assigning anyone the user didn't explicitly pick.
- ❌ Failing when CODEOWNERS is absent — it's optional; fall back to history-only ranking.
