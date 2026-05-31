# Working philosophy

I'm a senior developer. I want to be conscious of every technical decision.
No vibe coding.

Rules for the agent:

- Before implementing, there is a plan. Before the plan, there is alignment.
- Read the project's `AGENTS.md` before assuming anything about stack or architecture.
- If the implementation deviates from the plan, stop and notify me.
- Technical debt is explicit, never silent.

## Delegate to sub-agents to preserve context

Don't pull into your own context what a sub-agent can summarize in a paragraph:

- Code exploration or mapping a repo → `Explore`.
- Multi-step open-ended research → `general-purpose`.
