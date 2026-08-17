#!/usr/bin/env bash
#
# Unresolved review threads and review bodies of a Pull Request, as compact JSON.
#
#   pr-threads.sh              # the current branch's PR
#   pr-threads.sh 1234         # a PR number, URL or branch
#
# Resolved threads are dropped: someone already closed them. Every author is
# kept, the current user included — people comment on their own PRs.
#
# Each thread carries `reply_to`, the REST id its replies hang from:
#   gh api "repos/$repo/pulls/$pr/comments" -f body=… -F in_reply_to=$reply_to
set -euo pipefail

pr="${1:-}"

repo=$(gh repo view --json nameWithOwner -q .nameWithOwner)
owner=${repo%%/*}
name=${repo##*/}
number=$(gh pr view ${pr:+"$pr"} --json number -q .number)

gh api graphql \
  -f owner="$owner" -f name="$name" -F number="$number" \
  -f query='
    query($owner:String!, $name:String!, $number:Int!) {
      repository(owner:$owner, name:$name) {
        pullRequest(number:$number) {
          reviewThreads(first:100) {
            nodes {
              id isResolved isOutdated path line originalLine
              comments(first:50) { nodes { databaseId author { login } body } }
            }
          }
          reviews(first:50) { nodes { author { login } state body } }
        }
      }
    }' |
  jq --arg repo "$repo" --argjson pr "$number" '
    .data.repository.pullRequest as $pr_data | {
      repo: $repo,
      pr: $pr,
      threads: [
        $pr_data.reviewThreads.nodes[]
        | select(.isResolved | not)
        | {
            thread_id: .id,
            reply_to: .comments.nodes[0].databaseId,
            ref: "\(.path):\(.line // .originalLine)",
            outdated: .isOutdated,
            comments: [.comments.nodes[] | { author: .author.login, body }]
          }
      ],
      reviews: [
        $pr_data.reviews.nodes[]
        | select(.body != "")
        | { author: .author.login, state, body }
      ]
    }'
