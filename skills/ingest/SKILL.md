---
name: ingest
description: Normalizes a task from any source (ClickUp/Linear/Jira ticket, email, free-form description, voice notes) into a structured block in the conversation. On close, asks the user where to deposit the normalized version.
---

# Ingest

Turn any task description into a normalized, traceable version ready to work on.

## Inputs

Whatever the user gives you: a pasted text, a URL, a transcribed voice note, a Slack conversation. No prior file required.

If `~/harness/<slug>/config.json` exists and declares a `task_manager` (clickup, linear, jira, markdown…), use it: instead of asking generically "where does the task come from?", ask directly for the URL/ID of the declared manager.

## Procedure

1. Collect the raw input from the user.
2. Read `~/harness/<slug>/config.json` if it exists. If it declares `task_manager`, ask for the concrete URL/ID; otherwise, ask the source (ticket / email / voice / free-form).
3. Ask for a short slug to identify the task during the session (useful for naming files if the user later decides to persist it).
4. Build the normalized block following the Output format.
5. Mark with ❓ any inference of yours that is not explicit in the source. The ❓ remain open to be resolved later in the conversation.
6. Present the block to the user and ask them to confirm or correct. The last paragraph is **always** the destination question.
7. Suggest destination options matching `config.json`. Execute the chosen destination if you can; otherwise, leave the block ready for copy-paste.

## Output (in conversation)

```
# Normalized task: <clear, actionable title>

**Slug**: <short-slug>
**Source**: <ClickUp #X | Linear ABC-123 | PM email | voice note | conversation>
**Ingestion date**: <YYYY-MM-DD>

## Context
[Why the task exists. If not clear, mark "❓ context to clarify".]

## Acceptance criteria
- [ ] [explicit criterion 1]
- [ ] [explicit criterion 2]
- ❓ [criterion that is your inference, not in the statement]

## Constraints / non-goals
- [if the source says "don't touch X"]

## Links
- [original]
- [designs if applicable]
- [related issues]

## Raw material
[Paste the source verbatim for traceability]

---

**Where do you want to deposit this normalized task?**

Options based on your setup:
- In the ClickUp ticket itself (as a comment or enriched description) — paste URL/ID
- Markdown in local — tell me the path
- Only in the conversation (keep working here without persisting)

Or tell me another destination.
```

The destination question is part of the output. Do NOT close the skill without asking it.

## Anti-patterns

- ❌ Inventing context the source does not give. Mark with ❓.
- ❌ Rewriting criteria "to improve them". Copy them verbatim; if they need reformulation, leave it for a later interrogation session.
- ❌ Skipping the "raw material": it's your only source of truth when in doubt.
- ❌ Assuming the task manager without reading `config.json`.
- ❌ Closing the skill without the explicit destination question. It's mandatory.
- ❌ Writing files without the user asking for it. The skill is ephemeral by default.
