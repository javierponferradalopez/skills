# Comments on a Pull Request

The Pull Request branch of [`grill-me-comments`](SKILL.md): where the comments come from, and — once the user asks for it — how a thread gets answered. The rest of the flow, sorting through the OK to the grilling, is the same.

This feedback comes from other people, so the tree the batch is agreed against has to be the one that was reviewed.

## Check the ground

The current branch must be the PR's head branch, with no divergence from its remote:

```bash
gh pr view --json number,headRefName,url,state
git fetch && git status -sb
```

Anything off — a different branch, unpushed commits, behind the remote — stop and name it. A review applied to a tree that is not the reviewed one produces changes nobody asked for.

## Collect the threads

The script lives next to this file; run it by its path relative to this skill's directory:

```bash
scripts/pr-threads.sh          # the current branch's PR
scripts/pr-threads.sh 1234     # a number, URL or branch for another PR
```

It returns the unresolved threads and the review bodies, keeping every author — the user comments on their own PRs too. If it exits non-zero, surface the exact error and stop.

Each thread is one comment for the batch, `path:line` as its ref; a review body covers the PR as a whole and has no anchor.

Read each thread against the working tree **as it is today**, not against the diff that was reviewed. A thread flagged `outdated` whose code is already gone settles as _no longer applies_ and goes on the agreed batch like any other, with where the code went as its line — the PR is written to once, when the user says so, or not at all.

A GitHub `suggested change` is AFK by construction — the reviewer wrote the only implementation there is — and goes on the AFK list like any other: the reviewer settled the how, not the whether.

## Answering the threads

Reference for the moment the user asks for the threads to be answered — after the changes are in, never during the batch. An answered thread is a claim about code that exists.

Draft one reply per thread and **show the user every reply before posting it**: another person reads them, with the user's name on top.

| Outcome           | Reply               | Thread                                        |
| ----------------- | ------------------- | --------------------------------------------- |
| Change applied    | what was done       | resolve                                        |
| Left as it is     | the reason          | leave open — the reviewer keeps the last word  |
| No longer applies | where the code went | resolve                                        |

`repo`, `pr`, `reply_to` and `thread_id` all come from the script's output:

```bash
gh api "repos/$repo/pulls/$pr/comments" -f body='…' -F in_reply_to=$reply_to
gh api graphql -f id="$thread_id" \
  -f query='mutation($id:ID!){ resolveReviewThread(input:{threadId:$id}){ thread { id } } }'
```

A review body has no thread to reply to and nothing to resolve: answer it once, as a comment on the PR.

```bash
gh pr comment "$pr" --body '…'
```

Close by listing the threads still open: they are the live disagreements, waiting on the reviewer.
