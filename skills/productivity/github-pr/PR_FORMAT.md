# PR title & description format

## Title — Conventional Commits

- Format: `type(scope): concise, user-facing summary` — e.g. `feat(api): add rate-limited search endpoint`.
- Pick the dominant commit type; if mixed, choose the most impactful user-visible change (priority: feat, fix, perf, refactor, others).

## Description — Markdown, skimmable

Use `##` and below (NO `#`). Never paste diffs or code snippets from the PR — the reviewer already has the diff. Mermaid and file-tree blocks ARE allowed and encouraged where they help. The goal: a reviewer who grasps problem and solution at a glance and can skip the parts of the diff a diagram already explained.

```markdown
## Problem

First line, only if a tracker reference exists: `This PR resolves <ref>`.

[The business need or technical requirement behind the change.]

## Solution

[Compose freely — prose, diagrams, or both, in whatever order communicates fastest. Give the reviewer what they need to navigate the change and the key decisions behind it, without restating detail visible in the diff.]

### Testing
- ✅ What was tested (unit, integration, e2e) and any manual QA.
- ❌ What was not tested, known limitations, or risks.

### Next Steps (only if applicable)
- Follow-ups or stacked PRs.

### Related (only if there are PR/issue cross-references or stacked-PR links beyond the tracker reference already in Problem)
- Discovered references (e.g. `#123`) and links to dependent/parent PRs.
```

## Graphics in the Solution

Use a graphic only when it communicates faster than the prose it replaces — otherwise it's noise. Typical cases (illustrative, not a checklist):

- **File-tree block** — directories created, moved, or renamed:

  ```
  src/
  ├── auth/           # new: extracted from user/
  │   ├── login.ts
  │   └── session.ts
  └── user/
      └── profile.ts
  ```

- **Mermaid flowchart** — a control flow or decision path changed:

  ```mermaid
  flowchart LR
    Request --> Auth{Authenticated?}
    Auth -->|no| Reject
    Auth -->|yes| Handler
  ```

- **Mermaid sequence / state diagram** — the interaction between services or a lifecycle changed.

GitHub renders ` ```mermaid ` blocks natively, so they show as images, not code.
