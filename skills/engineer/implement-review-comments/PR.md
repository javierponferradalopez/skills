# Comments on a Pull Request

The Pull Request branch of [`implement-review-comments`](SKILL.md): where the comments come from, and what closing one means. The rest of the flow — sorting, the OK, the grilling — is the same.

This feedback comes from other people, and closing it writes back to GitHub under the user's name. Two things follow: the tree you edit has to be the one that was reviewed, and every reply is shown to the user before it is posted.

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

Read each thread against the working tree **as it is today**, not against the diff that was reviewed. A thread flagged `outdated` whose code is already gone is settled on the spot: reply with where it went, and resolve it.

A GitHub `suggested change` is clear by construction — the reviewer wrote the only implementation there is — and goes on the approved list like any other: the reviewer settled the how, not the whether.

## Reply

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
