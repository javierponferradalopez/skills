# Briefing format

The briefing is **one self-contained HTML file** — inline CSS, no external scripts, fonts, or CDNs — so it opens instantly in a browser, offline, from the temp dir. It reads top to bottom as a single scroll: the story of what the team did since the anchor, then where each thread rests now.

Design bar: **calm and readable**. Generous whitespace, one restrained palette, type sized for comfortable reading. The user should want to read it. But presentation never outranks truth — see the timeline rule.

## Sections, in scroll order

### 1. Hero

The overall state of the epic in one or two sentences — the headline you'd say out loud. Beneath it, the anchor and mode (_delta since `<date>`_ / _full_) and a one-line legend for the rung colours.

### 2. Timeline — the spine

The chronological story of what changed since the anchor, oldest-first so it reads as a story (in full mode, the whole history). Each beat is one real event: a commit cluster, a PR opened, a PR merged, a decision in a comment, a blocker raised. Every beat carries its date, a one-line prose description, and a link to its source.

**The timeline is storytelling that is true.** Every beat is an event that happened, linked to its proof. Never add connective tissue you can't source — no "the team decided to pivot" unless a comment says so. The chronology supplies the narrative; you supply only sourced facts. An inference you can't link belongs in blind spots, not on the timeline.

### 3. Current state — the ladder

Each subtask on its rung, coloured by rung. For an epic with several subtasks, render a visual tree in pure HTML/CSS coloured by rung. For a single ticket or a handful, a coloured list reads clearer — skip the tree. Each node links its PRs, branches, and ticket.

Rungs, cool→warm→done: _nothing_ (grey) → _branch, no PR_ (amber) → _open PR_ (blue) → _merged_ (green).

### 4. Blind spots

Sources not reached, tasks with no cited identifier, anything the briefing can't vouch for. **Never dropped or shrunk to grey fine-print for the sake of a clean look** — a briefing that hides its own gaps is worse than an ugly one. Give it real visual weight.

## Links

Every PR, commit, branch, and ticket renders as a clickable link to its URL (`[PD-123](…)`, `[#482](…)`, `[a1b2c3d](…)` → `<a href>`). A reference whose URL the finding didn't carry stays plain text and is named in blind spots.
