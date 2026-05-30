---
name: subtasks
description: Decomposes a plan into vertical, independently-closable subtasks. On close, explicitly asks the user where to deposit them (ClickUp, markdown, original ticket, conversation, etc.).
---

# Subtasks

Turn a technical plan into a list of vertical subtasks that can be tackled and closed independently, and **explicitly ask the user where to deposit them**.

## Principles

- **Vertical, not horizontal**: each subtask crosses all the layers needed to deliver a fragment of value. NOT "first all the models, then all the services".
- **Closable**: each subtask ends with green tests and, if applicable, its own PR.
- **Independent**: if subtask 2 depends heavily on 1, reconsider the cut.
- **Granularity**: each subtask should be closable in a reasonable sitting. If one feels "too big to tackle in one piece", cut it finer.

## Inputs

Work with the plan that's in the conversation (described by the user or produced during the session). No prior file required.

## Procedure

1. **Ask the user whether they want to break the task into subtasks.** Summarize the plan in one line and ask: "Do you want me to split this into vertical subtasks, or would you rather tackle it in one go?" If they say no, end the skill.
2. If they confirm, collect the plan from the conversation.
3. Identify natural vertical cuts (by feature, by endpoint, by domain use case).
4. For each cut, define:
   - Its own acceptance criteria (subset of the global ones).
   - Layers it touches.
   - Dependencies on other subtasks (ideally zero).
5. Order by dependencies and by risk (riskiest first, to discover earlier).
6. Present the list to the user using the Output format (next section). The last paragraph of the message is **always** the destination question.
7. Read `~/harness/<slug>/config.json` if it exists and use it to suggest destination options matching the declared task manager.
8. When the user picks, execute the chosen destination if you can (write markdown, dictate the format to paste into ClickUp/Linear, etc.). If you can't execute it, leave the block ready for copy-paste.

## Output (in conversation)

The message to the user ALWAYS takes this shape:

```
# Subtasks

## Summary
- Total: N subtasks
- Recommended order: [01, 02, 03, …]

## 01-<slug>
- What: [one sentence]
- Why first: …
- Acceptance: …
- Layers touched: …
- Depends on: none | <other-subtask>

## 02-<slug>
…

---

**Where do you want to deposit these subtasks?**

Options I suggest based on your setup:
- ClickUp (in the original ticket, as checklist or subtasks) — paste URL/ID
- Markdown in local — tell me the path
- In the original ticket where the task came from
- Only in the conversation, no persistence

Or tell me another destination.
```

The destination question is part of the output. Do NOT close the skill without asking it.

## Anti-patterns

- ❌ Horizontal cuts by layer.
- ❌ Subtasks that cannot close without first finishing another one.
- ❌ Too many subtasks to the point the list is unmanageable. If it grows that much, group them or question the scope.
- ❌ Subtasks so small they are noise; better group them with the neighbor.
- ❌ Deciding yourself whether the task "deserves" splitting or where to save the result. Those decisions are the user's; ask them.
- ❌ Closing the skill without the explicit destination question. It's mandatory.
- ❌ Writing files without the user asking for it. The skill is ephemeral by default.
