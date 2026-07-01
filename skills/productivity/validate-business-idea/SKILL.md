---
name: validate-business-idea
description: Validate a business idea — does it already exist, and if so how to differentiate — ending in a shareable HTML report.
disable-model-invocation: true
---

Validate a business idea: **does it already exist, and if so how do you differentiate?** The run ends in a self-contained HTML report.

Two hard rules across every step:

- **Write all returned content in the user's configured language**, not this skill's English. The idea and the report are theirs.
- **The existence verdict rests on live web search, never memory.** Your training has a cutoff and does not know recent products. A confident-looking report built from recall is the failure this skill exists to prevent.

## 1. Scope the idea (bounded grill)

Invoke the `grill-me` skill with this brief so it arrives constrained: interrogate **only** to capture the four data points below, one question at a time with a recommended answer, reask if an answer is unclear — and **stop the moment all four are clear**. Objective governs, not question count.

1. **What it is**, in one sentence.
2. **Problem + target customer** — what it solves and for whom.
3. **Differentiation hypothesis** — how the user believes it differs from what exists.
4. **Market / geography** — global, a country, a niche. Sharpens the search.

Completion: all four captured.

## 2. Pick research depth

Ask the user to choose — the right effort depends on the person and the moment, so don't guess:

- **Quick** — 1–2 searches, preliminary verdict.
- **Standard** — 4–6 multi-angle searches, verify 3–5 top competitors.
- **Deep** — more angles, more competitors verified.

Completion: user has chosen a level.

## 3. Research (mandatory web)

Search from several angles — by product name, by the problem it solves, by category, "alternatives to X", "competitors of Y". Then open the most relevant hits with `WebFetch` to confirm what each actually does. Scale counts to the chosen depth; stop when searches stop surfacing new names.

- **Every competitor cited carries its link.**
- **If nothing is found, say so explicitly.** Never fill the gap from memory.

Completion: top competitors for the depth level verified via `WebFetch`, each with a link.

## 4. Analyze

Produce four pieces, then a verdict:

1. **Existence verdict** — one clear label: *saturated* / *fragmented (weak, scattered players)* / *white space (suspicious — why does nobody do this?)*.
2. **Competitor table** — who, what they do, for whom, price/model if found, link.
3. **Differentiation axes** — compare the user's hypothesis (step 1.3) against what competitors already offer. Which axis is defensible, which isn't.
4. **Risks / red flags** — is the white space a graveyard (players who tried and folded)? Is the leader unbeatable on the chosen axis?

Close with a **final recommendation**: *pursue* / *pivot the angle* / *abandon*, with the why.

## 5. Checkpoint — stop before the report

Present a brief chat summary — verdict, key competitors, differentiation axes, recommendation — and **stop**. Build the HTML only on the user's explicit OK; if they ask for fixes, apply them first, then re-confirm.

## 6. Generate the report

Read [`report-template.html`](report-template.html) and fill its placeholders. It carries the shadcn/ui styling, the Mermaid CDN wiring, and a `quadrantChart` positioning map — keep them; render section labels in the user's language.

- Always include the competitor table; add diagrams the analysis calls for.
- Save to a temp file by default (e.g. `$TMPDIR/validate-business-idea-<slug>-<date>.html`); accept a custom path if the user gives one.
- Open it in the browser (`open` on macOS) and print the path.
