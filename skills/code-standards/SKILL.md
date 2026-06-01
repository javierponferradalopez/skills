---
name: code-standards-review
description: Reviews JavaScript and TypeScript code against a set of quality standards distilled from the classics of software engineering (Clean Code, The Pragmatic Programmer, A Philosophy of Software Design, Refactoring, The Design of Design, and more) and produces a findings report with severity levels. Use this skill WHENEVER the user asks to review, audit, or evaluate JS/TS code, asks whether their code meets the standards, is clean, is maintainable, or follows best practices, shares a .js/.ts/.jsx/.tsx file or a snippet for critique, or asks for a code review. This is a READ-ONLY skill that reports problems and proposes how to fix them, but does not modify the code unless the user explicitly asks afterward.
---

# Code Standards Review (JS/TS)

This skill applies a concrete, actionable set of standards to review JavaScript/TypeScript
code. The standards are distilled from the canon of software engineering (see
`references/sources.md`) and written as verifiable rules.

The goal is not to show off theory: it is to produce a **useful report** that says what is
wrong, **why it matters** (citing the source of the principle), and **how to fix it**.

## Guiding principle

Don't report noise. Every finding must earn its place: it must genuinely affect correctness,
readability, maintainability, or design. A report with 40 nitpicks is worse than one with the
6 problems that truly matter. Prioritize signal over volume.

## Workflow

1. **Identify what to review.** It may be an uploaded file, a snippet pasted in the chat, or
   several files from a repo. If the scope of the review is unclear, ask in a single sentence
   before starting.

2. **Load the standards.** Read `references/standards.md` in full before evaluating. It holds
   the rules grouped by category, each with its default severity and the source of the
   principle. If you need to recall what each book contributes, consult `references/sources.md`.

3. **Read the code carefully.** Don't stay on the surface. Understand what it does, what
   responsibilities each function/module has, where the boundaries and dependencies are. Many
   of the serious problems (coupling, wrong abstractions, accidental complexity) only become
   visible by reading it properly.

4. **Evaluate category by category.** Walk through the categories in `standards.md`. For each
   potential finding, ask: does this genuinely affect quality, or is it just my preference?
   Only report the former.

5. **Assign a severity** to each finding (see scale below). Adjust the rule's default severity
   to the real impact in *this* context.

6. **Produce the report** in the format defined below. Do not edit the code: this skill only
   reports.

## Severity scale

- 🔴 **Blocker** — Seriously compromises correctness, security, or maintainability. Examples:
  silently swallowed errors, massive duplication of logic, `any` that voids the type contract
  at a critical boundary, a giant function that's impossible to test.
- 🟠 **Major** — A clear smell that should be fixed soon. Examples: a function that does too
  many things, misleading names, high coupling, a leaky abstraction.
- 🟡 **Minor** — A readability or consistency improvement, low risk. Examples: an improvable
  name, a redundant comment, avoidable nesting.
- 🔵 **Suggestion** — An optional improvement or refactor the author can take or leave.

## Report format

Write the report in **English by default**. If the user asks for it in another language (for
example Spanish), write it in that language instead — follow the user's request.

Deliver the report **inline in the conversation** as your response. Do **not** create a file.
After presenting the report, you may offer to export it to a file (e.g. Markdown) if the user
wants to keep it.

Always use this structure:

\`\`\`markdown
# Code Standards Review

**Scope:** <files or snippet reviewed>
**Verdict:** ✅ Pass · ⚠️ Pass with observations · ❌ Fail

## Summary
<1–3 sentences: overall state and the 1–2 dominant themes>

## Findings

### 🔴 Blockers
- **[Category] Short title** — \`file:line\`
  - **What's happening:** <concrete description, pointing at the code>
  - **Why it matters:** <real impact> *(Source: <book / principle>)*
  - **How to fix it:** <specific action, not generic advice>

### 🟠 Major
<same format>

### 🟡 Minor
<same format; you may condense simple ones into single bullets>

### 🔵 Suggestions
<same format>

## What's good
<2–4 bullets of concrete positive reinforcement — what's well solved and why>
\`\`\`

Report rules:
- If a severity section is empty, **omit it** (don't write "None").
- Always cite the source of the principle in parentheses at the end of "Why it matters".
- "How to fix it" must be specific to this code, not generic book advice.
- The "What's good" section is not optional: a good review also recognizes what's done well
  (it reinforces good habits and makes the report more credible and actionable).

## Verdict

- ✅ **Pass** — No blockers and no major issues. At most minor ones/suggestions.
- ⚠️ **Pass with observations** — No blockers, but one or more major issues.
- ❌ **Fail** — At least one blocker.

## Extending the standards

The standards live in `references/standards.md`. There is a final section marked
**"Team-specific standards"** meant for the user to add their own rules over time. When the
user asks to add a rule:
- Add it to that section using the same format (rule, what to flag, default severity).
- Team-specific rules **take priority** over the canon if they conflict: they are deliberate
  team decisions.
- If the user describes a vague rule, help them turn it into something verifiable before
  saving it (a rule you can't check is useless for reviewing).
