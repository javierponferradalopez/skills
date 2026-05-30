---
name: verify
description: Compares the delivered work against the original acceptance criteria and leaves technical debt explicit. On close, asks the user where to deposit the summary (PR description, ClickUp, markdown, original ticket, etc.).
---

# Verify

Formal closure of a task: compare delivered vs expected, leave technical debt visible, and produce a summary reusable as a PR description.

## Inputs

Acceptance criteria can come from several places; take the first one available and don't abort if one is missing:

- A recent `<!-- GRILL RESULT -->` block in the conversation.
- A structured plan in the conversation.
- The original ticket (if the user pastes it).
- If none of the above are present, **ask the user for the criteria** before continuing.

No prior file on disk is required.

## Procedure

1. Collect the acceptance criteria from the closest source in the conversation. If they don't appear, explicitly ask the user.
2. Collect the delivered state: current diff, test output, observed behavior. If needed, run the tests or ask the user for them.
3. For each criterion:
   - ✅ if met.
   - ⚠️ if partially met (explain what's missing).
   - ❌ if NOT met (justify why it's being closed like this).
4. List the technical debt generated during the implementation. For each item, check it has its tracking (issue, TODO with reference, ADR). If any is loose, propose creating it.
5. List contract changes (APIs, schemas, configs) so they're easy to include in the PR.
6. Present the summary to the user using the Output format. The last paragraph of the message is **always** the destination question.
7. Read `~/harness/<slug>/config.json` if it exists and suggest destination options matching it (PR description, ClickUp, original ticket, markdown).
8. Execute the chosen destination if you can; otherwise, leave the block ready for copy-paste.

## Output (in conversation)

```
# Closure verification

## Acceptance criteria
- ✅ <criterion 1>
- ⚠️ <criterion 2> — partial because …
- ❌ <criterion 3> — not covered because … — tracking: <issue>

## Technical debt generated
- <item> — origin: <context> — tracking: <issue/TODO>

## Contract changes
- [endpoint / schema / config] — [breaking? yes/no]

## Executive summary
[2-3 sentences ready for the PR description]

---

**Where do you want to deposit this summary?**

Options based on your setup:
- PR description (I'll dictate the body in the format you use)
- ClickUp (in the original ticket as a closure comment) — paste URL/ID
- Markdown in local — tell me the path
- In the original ticket where the task came from
- Only in the conversation, no persistence

Or tell me another destination.
```

The destination question is part of the output. Do NOT close the skill without asking it.

## Anti-patterns

- ❌ Marking ✅ something that isn't fully done.
- ❌ Closing the task with untracked debt.
- ❌ Forgetting implicit criteria that came up during the conversation but weren't in the statement.
- ❌ Deciding yourself where to save the summary. That decision is the user's; ask them.
- ❌ Closing the skill without the explicit destination question. It's mandatory.
- ❌ Writing files without the user asking for it. The skill is ephemeral by default.
