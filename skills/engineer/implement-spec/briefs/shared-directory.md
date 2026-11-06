You share this working directory with agents building other tickets. Make file edits only, and before your first edit to a file run `git status --porcelain --untracked-files=all -- <path>`: a file it lists belongs to another agent, so leave it as it is and escalate the overlap, naming the path.

Scope each typecheck, lint and test run to the apps and packages you touch. A failure in a path you did not change belongs to another agent: name it in your report, and go on.

The orchestrator owns the environment: dependencies, builds and the running apps. Use it as you find it and leave installing, building, starting and stopping to the orchestrator; when your work needs one of those, escalate it, naming what you need.
