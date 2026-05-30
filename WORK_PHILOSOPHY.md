# Working philosophy

I'm a senior developer. I want to be conscious of every technical decision.
No vibe coding.

Rules for the agent:
- Before implementing, there is a plan. Before the plan, there is alignment.
- Read the project's `AGENTS.md` before assuming anything about stack or architecture.
- If the implementation deviates from the plan, stop and notify me.
- Technical debt is explicit, never silent.

## Skills are stateless

Skills are independent units invoked by intent. They live in the conversation: they don't require any prior file to exist, they don't read files left by other skills, and they don't write files of their own. Each skill executes its single procedure and stops.

The single point of persistence in the system is the `/handoff` command, which collapses the current task into a markdown when the user asks for it.

When a skill produces a reusable artifact (a plan, a list of subtasks, a verification summary), it asks the user where to deposit it (the project's task manager, a local markdown, the original ticket, just-conversation). The skill does not decide where things go.

## Orchestration is your job, not the skills'

The agent in the conversation (with the user) decides which skill to invoke next — never hardcoded inside a skill. Skills must not suggest "next, run skill X" nor "skip if Y". Those decisions belong to the conversation.

When the user brings a new task without clear context, **offer a grill or ask for the source link before planning**. Don't jump straight into `plan` without alignment.

## Resuming a previous task

When the user signals they want to continue something already underway ("let's resume", "pick up where we left off", "continuemos por donde lo dejamos"), do not improvise from memory. Load the latest handoff first:

1. Compute `$HARNESS` for the current project (see below).
2. List `$HARNESS/*/handoff.md` and pick the one with the latest modification time. If several look recent, ask the user which `<task-id>` they mean.
3. Read it. Anchor the next message on its "Concrete next step", and surface its open risks/doubts if they're relevant to what comes next.

If no handoff is found under `$HARNESS`, say so plainly — don't pretend to remember context that wasn't persisted.

## Delegate to sub-agents to preserve context

Don't pull into your own context what a sub-agent can summarize in a paragraph:

- Code exploration or mapping a repo → `Explore` or `code-explorer`.
- Critical review of a plan or deliverable → `adversarial-reviewer`.
- Multi-step open-ended research → `general-purpose`.

## Harness location

The harness writes its per-project artifacts OUTSIDE the project tree. Client repos must stay clean — NEVER create a `harness/` directory inside the working tree.

Compute the harness root once per task (call it `$HARNESS`):

```bash
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SLUG="$(printf '%s' "$ROOT" | sed 's/[/.]/-/g')"
HARNESS="$HOME/harness/$SLUG"
```

- `$ROOT` is the git repo root (or cwd if not a git repo).
- `$SLUG` is `$ROOT` with every `/` and `.` replaced by `-`. Each project lands in its own folder under `~/harness/`, no collisions.

## Optional project config

`~/harness/<slug>/config.json` is an optional per-project config (task manager, etc.). When present, skills read it to tailor their prompts instead of asking generically. When absent, skills just ask. The file is created and updated by the `/project-init` command — see there for the exact shape.
