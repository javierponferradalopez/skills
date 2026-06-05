#!/usr/bin/env bash
#
# rank-contributors.sh — rank likely PR reviewers from the branch diff.
#
# All heavy git history processing happens here, in the shell. The script
# emits ONLY a compact top-N table so the calling agent never ingests raw
# `git log`/`git blame` output into its context.
#
# Usage:
#   rank-contributors.sh [--base <ref>] [--months <N>] [--recent-days <N>] [--top <N>]
#
# Defaults: base = origin's default branch (fallback main → master),
#           months = 12, recent-days = 90, top = 10.
#
# Output (tab-separated, one row per candidate, best first):
#   login \t score \t commits \t recent_commits \t files_touched \t display
# Plus two metadata lines on stderr-free stdout, prefixed with "#":
#   # base=<ref> merge_base=<sha> changed_files=<count>
#   # changed_files_list follows (one per line, prefixed "  ")
#
set -euo pipefail

BASE=""
MONTHS=12
RECENT_DAYS=90
TOP=10

while [ $# -gt 0 ]; do
  case "$1" in
    --base)        BASE="$2"; shift 2 ;;
    --months)      MONTHS="$2"; shift 2 ;;
    --recent-days) RECENT_DAYS="$2"; shift 2 ;;
    --top)         TOP="$2"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "ERROR: not a git repository" >&2; exit 1; }

# --- Resolve base branch -----------------------------------------------------
if [ -z "$BASE" ]; then
  BASE="$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || true)"
  [ -z "$BASE" ] && git show-ref --verify --quiet refs/remotes/origin/main && BASE="origin/main"
  [ -z "$BASE" ] && git show-ref --verify --quiet refs/remotes/origin/master && BASE="origin/master"
  [ -z "$BASE" ] && BASE="master"
fi
# Normalize to a comparable ref (prefer origin/<base> when it exists).
if git show-ref --verify --quiet "refs/remotes/origin/$BASE"; then
  BASE_REF="origin/$BASE"
else
  BASE_REF="$BASE"
fi

MB="$(git merge-base "$BASE_REF" HEAD 2>/dev/null || true)"
[ -z "$MB" ] && { echo "ERROR: cannot compute merge-base against $BASE_REF (fetch origin?)" >&2; exit 1; }

# --- Changed files -----------------------------------------------------------
CHANGED="$(git diff --name-only "$MB"..HEAD)"
N_CHANGED="$(printf '%s\n' "$CHANGED" | sed '/^$/d' | wc -l | tr -d ' ')"
[ "$N_CHANGED" -eq 0 ] && { echo "ERROR: no changed files vs $BASE_REF" >&2; exit 1; }

echo "# base=$BASE_REF merge_base=$MB changed_files=$N_CHANGED"
echo "# changed_files_list:"
printf '%s\n' "$CHANGED" | sed '/^$/d' | sed 's/^/  /'

# --- Recency cutoff (ISO date, compared lexically — portable, no mktime) -----
SINCE_DATE="$(date -v-"${MONTHS}"m +%Y-%m-%d 2>/dev/null || date -d "-${MONTHS} months" +%Y-%m-%d)"
RECENT_CUTOFF="$(date -v-"${RECENT_DAYS}"d +%Y-%m-%d 2>/dev/null || date -d "-${RECENT_DAYS} days" +%Y-%m-%d)"

# --- Stream commit-touches into awk and aggregate ----------------------------
# Per changed file, list authors of commits touching it within the window.
# Emit: email \t name \t commitDateISO \t file   (one line per commit-touch)
# awk aggregates; only the ranked summary leaves this pipeline.
RANKED="$(
  printf '%s\n' "$CHANGED" | sed '/^$/d' | while IFS= read -r f; do
    git log --since="$SINCE_DATE" --no-merges \
      --format="%aE	%aN	%cI" -- "$f" 2>/dev/null \
      | awk -v file="$f" -F'\t' 'NF>=3 {print $1"\t"$2"\t"substr($3,1,10)"\t"file}'
  done | awk -F'\t' -v rc="$RECENT_CUTOFF" '
    {
      email=$1; name=$2; d=$3; file=$4;
      if (email=="") next;
      commits[email]++;
      names[email]=name;
      if (d >= rc) recent[email]++;
      key=email SUBSEP file;
      if (!(key in seenfile)) { seenfile[key]=1; nfiles[email]++; }
    }
    END {
      for (e in commits) {
        score = commits[e] + 2*recent[e];
        printf "%d\t%d\t%d\t%d\t%s\t%s\n", score, commits[e], recent[e]+0, nfiles[e], e, names[e];
      }
    }
  ' | sort -t$'\t' -k1,1nr | head -n "$TOP"
)"

[ -z "$RANKED" ] && { echo "ERROR: no commit history in the last $MONTHS months for the changed files" >&2; exit 1; }

# --- Map author email -> GitHub login (GitHub's own resolution) --------------
REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"

echo "# candidates (login	score	commits	recent	files	display):"
printf '%s\n' "$RANKED" | while IFS=$'\t' read -r score commits recent nfiles email name; do
  login=""
  if [ -n "$REPO" ]; then
    login="$(gh api "repos/$REPO/commits" -X GET -f author="$email" -f per_page=1 \
      --jq '.[0].author.login // empty' 2>/dev/null || true)"
  fi
  [ -z "$login" ] && login="-"
  printf '%s\t%s\t%s\t%s\t%s\t%s <%s>\n' "$login" "$score" "$commits" "$recent" "$nfiles" "$name" "$email"
done
