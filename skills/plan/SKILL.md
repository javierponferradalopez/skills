---
name: plan
description: Produces a structured technical plan in the conversation — affected modules, decisions, risks, side effects, rough effort. On close, explicitly asks the user where to deposit the plan (ClickUp, markdown, original ticket, conversation, etc.).
---

# Plan

Turn the idea into a technical plan anchored to the project: where it fits, what modules it touches, what non-trivial decisions there are, what risks, what effort.

## Inputs

Work with whatever is in the conversation: a task described by the user, a pasted ticket, a previous interrogation, a link.

If there is a `<!-- GRILL RESULT -->` block in the recent conversation, absorb it: its assumptions and decisions are input to the plan. After integrating them, treat that information as consumed — the source of truth becomes the plan.

## Procedure

1. Read the project's `AGENTS.md`. The project always wins; never assume stack or architecture.
2. If you need a structural map of the repo and reading it yourself would contaminate your context, **delegate to `code-explorer`** instead of reading files directly.
3. Build the plan covering (in order, concise):
   - **Fit in the project**: functional domain, the module/bounded context it lands in, evolutionary or new, crossed contexts if any.
   - **Affected modules**: for each one, the action (create / extend / refactor) and why.
   - **New components**: name, layer, one-line responsibility.
   - **Non-trivial decisions**: 2-3 options with pros/cons, chosen option, reason, whether it deserves an ADR.
   - **Side effects**: migrations, broken contracts, new deps, configuration, CI/CD.
   - **Risks**: each one with mitigation.
   - **Effort**: S/M/L/XL with a one-line justification. If XL, flag for decomposition.
   - **Prior dependencies**: if something must happen first.
4. Present the plan to the user as bullets, not prose. Wait for reaction before continuing.
5. When the user gives it the green light, read `~/harness/<slug>/config.json` if it exists and **ask where to deposit the plan**. Suggest options based on the user's setup (ClickUp, local markdown, original ticket, just-conversation). Execute the chosen destination if you can; otherwise, leave the block ready for copy-paste.

## Output (in conversation)

```
# Plan: <title>

## Summary
[2-3 lines: what we're going to do and why this approach]

## Fit
- Domain: …
- Type: evolutionary | new | mixed
- Crossed contexts: …

## Affected modules
- <module> (<path>) — create/extend/refactor — [justification]

## New components
- <Name> (<layer>) — [responsibility]

## Decisions
- D1: <title> — options [A/B/C] → chosen [X]. Reason: … Needs ADR: yes/no.

## Side effects
- …

## Risks
- … → mitigation: …

## Effort
S/M/L/XL — [justification]

## Prior dependencies
- …

---

**Where do you want to deposit this plan?**

Options based on your setup:
- ClickUp (in the original ticket, as description or comment) — paste URL/ID
- Markdown in local — tell me the path
- In the original ticket where the task came from
- Only in the conversation, no persistence

Or tell me another destination.
```

The destination question is part of the output. Do NOT close the skill without asking it.

## Anti-patterns

- ❌ Writing without reading `AGENTS.md`.
- ❌ Picking a location without respecting the project's conventions.
- ❌ Creating new modules by default. First check whether it fits in an existing one.
- ❌ Ignoring architectural tensions: if something doesn't fit cleanly, say it now, not mid-implementation.
- ❌ Deciding non-trivial things without listing alternatives.
- ❌ A 5-page exhaustive plan. If it grows that much, the task probably needs to be decomposed first.
- ❌ Closing the skill without the explicit destination question. It's mandatory.
- ❌ Writing files without the user asking for it. The skill is ephemeral by default.
