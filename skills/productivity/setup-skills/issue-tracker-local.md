# Issue tracker: Local Markdown

Issues and PRDs for this repo live as markdown files in `.kanban/`.

## Conventions

- One feature per directory: `.kanban/<feature-slug>/`
- The PRD is `.kanban/<feature-slug>/PRD.md`
- Implementation issues are `.kanban/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`
- Status is recorded as a `Status:` line near the top of each issue file
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## When a skill says "publish to the issue tracker"

Create a new file under `.kanban/<feature-slug>/` (creating the directory if needed).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.
