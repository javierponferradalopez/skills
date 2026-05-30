---
name: diagnose
description: Disciplined loop for hard bugs, unexpected regressions, or performance problems. Reproduce → minimize → hypothesis → instrument → fix → regression test. Use it when a bug is not obvious in 5 minutes of looking at the code, when there are regressions whose cause is not clear, or when something works locally but not in CI/production. Do NOT use this skill for typos or trivial bugs.
---

# Diagnose

Disciplined loop for non-obvious bugs.

## Procedure

### 1. Reproduce
- Find the minimum set of steps that reproduces the bug reliably.
- If it doesn't reproduce reliably, first goal: make it reliable.

### 2. Minimize
- Reduce the case to its minimal expression.
- Remove unnecessary dependencies.
- Isolate the culprit module.

### 3. Hypothesize
- List 2-3 concrete, FALSIFIABLE hypotheses about the cause.
- For each: what experiment would confirm or rule it out.

### 4. Instrument
- Add logs/breakpoints/traces aimed at falsifying the hypothesis,
  not at "seeing what happens".

### 5. Fix
- Only when the root cause is identified with certainty, not before.
- The fix targets the cause, not the symptom.

### 6. Regression test
- Before closing, a test that fails with the old code and passes with
  the new one. Without this, the bug will come back.

## Anti-patterns

- ❌ "I'll try changing X to see if it works." That's not diagnosis.
- ❌ Fixing without understanding the cause.
- ❌ Closing without a regression test.
