---
name: grill
description: Interrogate the user until every ambiguity about the task or idea is resolved — corner cases, implicit assumptions, conflicts with what already exists. On close, emit a GRILL RESULT block and explicitly ask the user where to deposit the conclusions (ClickUp, markdown, conversation, etc.).
---

# Grill

Interrogate the user until every ambiguity is resolved. Surface corner cases, implicit assumptions, and conflicts with existing code. The output lives in the conversation, not on disk.

## Procedure

1. Read the project's `AGENTS.md` if it exists. Skim the related code so you don't ask what the repo already answers.
2. Mentally list: acceptance criteria, assumptions, obvious corner cases.
3. Ask **one thing at a time**. For each question:
   - If the codebase can answer it, **explore instead of asking**.
   - Otherwise, propose your recommended answer alongside the question so the user can confirm or correct rather than write it from scratch.
4. Walk the dimensions the task actually touches (not a fixed checklist, follow the thread):
   - **Inputs**: formats, validations, what happens with empty/invalid input.
   - **Outputs**: success, error, HTTP codes if applicable.
   - **State**: persistent data, migrations, backward compatibility.
   - **Permissions**: who can execute this, what happens without permission.
   - **Concurrency**: two users triggering this at once.
   - **Failures**: external dependency down, retries, idempotency.
   - **Observability**: logs, metrics, alerts.
   - **Tests**: test types, test data.
5. When an answer opens new doubts, dig deeper before moving to the next dimension.
6. When you believe you've covered what matters, ask: "Anything important I haven't asked?"

## Close

When the user gives the grill for closed, the final message ALWAYS takes this shape:

```
<!-- GRILL RESULT -->
- Confirmed assumptions: …
- Corner cases detected and their expected behavior: …
- Closed decisions: …
- Open decisions (if any remain): …
<!-- /GRILL RESULT -->

---

**Where do you want to deposit this result?**

Options I suggest based on your setup (read `~/harness/<slug>/config.json` if it exists):
- ClickUp (as a comment or ticket description) — paste URL/ID
- Markdown in local — tell me the path
- In the original ticket where the task came from
- Only in the conversation, no persistence

Or tell me another destination.
```

The `<!-- GRILL RESULT -->` block is the grill's contract: anything that comes after must respect it. The destination question is mandatory — do not close the skill without asking it. If the user picks a destination you can execute (write markdown, dictate the comment for ClickUp/Linear), do it; otherwise, leave the content ready for copy-paste.

## Anti-patterns

- Asking 5 questions in a single message. One at a time.
- Asking things the code already answers.
- Asking about stack or architecture that's already in `AGENTS.md`.
- Writing files without the user asking for it. The skill is ephemeral by default.
- Closing the grill without emitting the `<!-- GRILL RESULT -->` block or the destination question.
