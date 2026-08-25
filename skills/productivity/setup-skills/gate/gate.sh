#!/bin/bash
# The quality gate. No arguments: everything it judges it derives from the diff.
#
#   GATE_BASE   the revision to diff against. Default HEAD — the dirty,
#               pre-commit tree that `validate` has in front of it. Ask for the
#               whole branch explicitly:
#                   GATE_BASE=$(git merge-base origin/main HEAD) .agents/gate/gate.sh
#
# Verdicts: PASS / FAIL / SKIPPED judge the code; BROKEN judges the gate —
# "I could not judge", never "your code is wrong". Exit 0 = PASS or SKIPPED,
# exit 1 = anything else.
#
# Detail for failures goes to stdout as TSV grouped by file. Stages that pass
# save nothing at all — that is where the token saving lives. The full reports
# stay in last-run/ as an escape hatch.
set -u

GATE_HOME="$(cd "$(dirname "$0")" && pwd)"
PROJECT="$(cd "$GATE_HOME/../.." && pwd)"
GATE_BASE="${GATE_BASE:-HEAD}"
GATE=".agents/gate"

command -v jq > /dev/null || { echo "gate: BROKEN — falta jq"; exit 1; }

# The only location lever there is: neither ESLint nor Stryker takes a project
# root flag, both resolve against cwd.
cd "$PROJECT" || { echo "gate: BROKEN — no se pudo entrar en $PROJECT"; exit 1; }

# Full form mutates; short form only measures complexity. The pair of files a
# form installs is what tells them apart.
if [ -f "$GATE/stryker.config.json" ]; then FORM=full; else FORM=short; fi

[ -x "$GATE/node_modules/.bin/eslint" ] || {
  echo "gate: BROKEN — el gate no está montado (falta $GATE/node_modules); corre $GATE/ensure.sh"; exit 1; }
if [ "$FORM" = full ] && [ ! -x "$GATE/node_modules/.bin/stryker" ]; then
  echo "gate: BROKEN — el gate no está montado (falta stryker); corre $GATE/ensure.sh"; exit 1
fi

RUN="$GATE/last-run"
PREVIOUS="$GATE/.previous.json"   # sibling of last-run/, so the wipe below cannot take it
rm -rf "$RUN"
mkdir -p "$RUN"

# --- what the gate judges -----------------------------------------------------

judgeable() {
  grep -E '\.(cjs|mjs|js|ts|mts|cts|jsx|tsx)$' \
    | grep -vE '\.(test|spec)\.' \
    | grep -vE '(^|/)(eslint|vitest|stryker|vite|rollup|webpack|tailwind|next|astro)\.config\.' \
    | grep -vE '^\.agents/'
}

# A file `implement` just wrote is untracked, so `git diff` alone cannot see it —
# and that is the commonest thing the gate has to judge.
UNTRACKED="$(git ls-files --others --exclude-standard | judgeable)"
GATE_FILES="$(
  { git diff --name-only --diff-filter=ACMR "$GATE_BASE" -- | judgeable
    printf '%s\n' "$UNTRACKED"; } | grep -v '^$' | sort -u
)"

echo "gate: base $GATE_BASE · forma $FORM"

if [ -z "$GATE_FILES" ]; then
  echo "gate: SKIPPED — el diff contra $GATE_BASE no toca código fuente"
  exit 0
fi

GATE_RANGES="$(
  echo "$GATE_FILES" \
    | while IFS= read -r f; do
        if printf '%s\n' "$UNTRACKED" | grep -qxF "$f"; then
          awk -v f="$f" 'END { print f ":1-" (NR > 0 ? NR : 1) }' "$f"
        else
          git diff -U0 "$GATE_BASE" -- "$f" \
            | grep -E '^@@' \
            | sed -E 's/^@@ -[^ ]+ \+([0-9]+)(,([0-9]+))? @@.*/\1 \3/' \
            | awk -v f="$f" '{ s = $1; n = ($2 == "" ? 1 : $2); if (n > 0) print f ":" s "-" (s + n - 1) }'
        fi
      done \
    | paste -sd, -
)"

# Group a TSV stream by its first column, capping each file so one untested file
# cannot bury the rest. The cap is per file, never global: this is a list of
# findings, not a chronological log — cutting at line 100 erases whole files.
CAP=20
plural() {  # <n> <singular> <plural>
  if [ "$1" -eq 1 ]; then printf '%s %s' "$1" "$2"; else printf '%s %s' "$1" "$3"; fi
}

group_by_file() {
  awk -F'\t' -v cap="$CAP" '
    {
      if (!($1 in n)) order[++k] = $1
      n[$1]++
      if (n[$1] <= cap) lines[$1] = lines[$1] $0 "\n"; else over[$1]++
    }
    END {
      for (i = 1; i <= k; i++) {
        f = order[i]
        printf "%s", lines[f]
        if (over[f] > 0) printf "… y %d hallazgos más en %s\n", over[f], f
      }
    }'
}

VERDICT_COMPLEXITY=
VERDICT_MUTATION=

# --- complexity ---------------------------------------------------------------
# It runs first, and a failure here skips mutation: fixing complexity refactors
# code, which makes a mutation report that cost minutes to produce a lie.

OLD_IFS="$IFS"; IFS=$'\n'; set -- $GATE_FILES; IFS="$OLD_IFS"

"$GATE/node_modules/.bin/eslint" \
  --config "$GATE/eslint.complexity.config.mjs" \
  --no-config-lookup --max-warnings 0 -f json \
  "$@" > "$RUN/complexity.json" 2> "$RUN/complexity.err"
ESLINT_EXIT=$?

if [ "$ESLINT_EXIT" -ge 2 ]; then
  VERDICT_COMPLEXITY=BROKEN
  echo "complexity: BROKEN — eslint salió $ESLINT_EXIT"
  sed -n '1,20p' "$RUN/complexity.err"
elif [ "$ESLINT_EXIT" -eq 1 ]; then
  VERDICT_COMPLEXITY=FAIL
  jq -r --arg root "$PROJECT/" \
    '.[] | (.filePath | ltrimstr($root)) as $f | .messages[] | [$f, .line, .message] | @tsv' \
    "$RUN/complexity.json" > "$RUN/complexity.tsv"
  N="$(wc -l < "$RUN/complexity.tsv" | tr -d ' ')"
  M="$(cut -f1 "$RUN/complexity.tsv" | sort -u | wc -l | tr -d ' ')"
  echo "complexity: FAIL — $(plural "$N" "función" "funciones") sobre el límite en $(plural "$M" fichero ficheros)"
  sort "$RUN/complexity.tsv" | group_by_file
else
  VERDICT_COMPLEXITY=PASS
  echo "complexity: PASS"
  rm -f "$RUN/complexity.json" "$RUN/complexity.err"
fi

# --- mutation -----------------------------------------------------------------

PREV_SURVIVORS="$(jq -r '.survivors // empty' "$PREVIOUS" 2> /dev/null)"

if [ "$FORM" = short ]; then
  VERDICT_MUTATION=SKIPPED
  echo "mutation: SKIPPED — este gate es de forma corta (sin mutación)"
elif [ "$VERDICT_COMPLEXITY" != PASS ]; then
  VERDICT_MUTATION=SKIPPED
  echo "mutation: SKIPPED — complexity $VERDICT_COMPLEXITY"
elif [ -z "$GATE_RANGES" ]; then
  VERDICT_MUTATION=SKIPPED
  echo "mutation: SKIPPED — GATE_RANGES vacío"
else
  rm -f "$RUN/mutation.json"   # Stryker leaves the previous report in place when it aborts
  "$GATE/node_modules/.bin/stryker" run "$GATE/stryker.config.json" \
    --mutate "$GATE_RANGES" > "$RUN/mutation.log" 2>&1
  STRYKER_EXIT=$?
  rm -rf "$GATE/.stryker-tmp"  # always, above all when it failed: the only measured
                               # producer of contamination back into the project

  if grep -q 'There were failed tests in the initial test run' "$RUN/mutation.log"; then
    VERDICT_MUTATION=BROKEN
    echo "mutation: BROKEN — la suite del proyecto está roja; el informe viene vacío"
  elif [ ! -f "$RUN/mutation.json" ]; then
    VERDICT_MUTATION=BROKEN
    echo "mutation: BROKEN — stryker abortó sin informe (salió $STRYKER_EXIT)"
    grep -E 'ERROR|WARN' "$RUN/mutation.log" | sed -n '1,10p'
  elif [ "$STRYKER_EXIT" -eq 0 ]; then
    VERDICT_MUTATION=PASS
    echo "mutation: PASS"
    printf '{ "survivors": 0 }\n' > "$PREVIOUS"
    rm -f "$RUN/mutation.json" "$RUN/mutation.log"
  else
    jq -r '.files | to_entries[] | .key as $f | .value.mutants[]
           | select(.status == "Survived" or .status == "NoCoverage")
           | [$f, .location.start.line, .status, .mutatorName, .replacement] | @tsv' \
      "$RUN/mutation.json" > "$RUN/mutation.tsv"
    N="$(wc -l < "$RUN/mutation.tsv" | tr -d ' ')"
    M="$(cut -f1 "$RUN/mutation.tsv" | sort -u | wc -l | tr -d ' ')"
    if [ "$N" -eq 0 ]; then
      VERDICT_MUTATION=BROKEN
      echo "mutation: BROKEN — stryker salió $STRYKER_EXIT y el informe no trae supervivientes"
      grep -E 'ERROR' "$RUN/mutation.log" | sed -n '1,10p'
    else
      VERDICT_MUTATION=FAIL
      # The previous count turns "I am stuck" into a fact on screen instead of a
      # tally the agent has to remember. No count yet means this is the first
      # pass, and that absence is itself the signal.
      if [ -z "$PREV_SURVIVORS" ]; then
        SINCE=""
      elif [ "$N" -lt "$PREV_SURVIVORS" ]; then
        SINCE=" (antes $PREV_SURVIVORS)"
      else
        SINCE=" (antes $PREV_SURVIVORS, sin progreso)"
      fi
      echo "mutation: FAIL — $(plural "$N" superviviente supervivientes) en $(plural "$M" fichero ficheros)$SINCE"
      sort "$RUN/mutation.tsv" | group_by_file
      printf '{ "survivors": %s }\n' "$N" > "$PREVIOUS"
    fi
  fi
fi

# --- verdict ------------------------------------------------------------------

case "$VERDICT_COMPLEXITY $VERDICT_MUTATION" in
  *BROKEN*) VERDICT=BROKEN ;;
  *FAIL*)   VERDICT=FAIL ;;
  *)        VERDICT=PASS ;;
esac

jq -n \
  --arg base "$GATE_BASE" --arg form "$FORM" --arg verdict "$VERDICT" \
  --arg ranges "$GATE_RANGES" \
  --arg complexity "$VERDICT_COMPLEXITY" --arg mutation "$VERDICT_MUTATION" \
  '{ base: $base, form: $form, verdict: $verdict, ranges: $ranges,
     stages: [ { capability: "complexity", verdict: $complexity },
               { capability: "mutation",   verdict: $mutation } ] }' \
  > "$RUN/last-run.json"

if [ "$VERDICT" = PASS ]; then
  echo "gate: PASS"
  exit 0
fi

echo "gate: $VERDICT — informe completo en $GATE/last-run/"
exit 1
