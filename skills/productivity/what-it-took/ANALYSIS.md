# The analysis

You are diagnosing **one session's context window** from its transcript. You did
not live that session: the transcript is the only evidence, which is exactly what
makes the reading honest. Everything you learn stays in your window — the caller
gets one line.

The unit is **footprint** (what is resident) rather than tokens billed. The
question on every finding is **"was there a cheaper way to know this?"**, never
"should this call have happened" — a search that led nowhere still bought
understanding, and the repo is what made it expensive.

## 1. Measure

Run the aggregator from this skill's directory, passing the transcript path:

```bash
scripts/measure-window.py <transcript.jsonl>
```

It sums, groups and counts — nothing more. Every judgement below is yours.

Take its warnings seriously and carry them into the report: a low reconciliation
percentage, a detected compaction, or missing usage figures all bound what you
are entitled to claim. When it exits non-zero, report that verbatim and stop.

The buckets come from a classifier reading command lines, so a few calls land in
the wrong one. Check what a call actually did before you build a finding on its
bucket — the zoom in step 4 shows you.

## 2. Read the shape

The split across buckets *is* the diagnosis, and each shape points somewhere
different. Read it before you read any detail:

- **Toll heavy** — the first-turn figure is a large slice of what is resident,
  or `growth no payload accounts for` shows thousands arriving on turns that
  received nothing. Something is loading whether or not it gets used: skill
  descriptions, tool schemas, an always-loaded `CLAUDE.md`, a skill body pulled
  in mid-session. This one is multiplied by every turn that follows it.
- **Locate heavy** — the session paid to find *where things live*. The repo's
  vocabulary and its layout disagree.
- **Comprehend heavy** — the session paid to find out *what things do*. The code
  does not say what it is for, so it had to be read whole.
- **Own output heavy** — the biggest resident block is the agent's own text and
  thinking. The repo is not the problem; session length is.
- **Work heavy with a low first-work milestone** — the session got to work early
  and spent its window doing the job. This is a healthy session, and saying so
  plainly is a real finding.

The **first work** milestone is the headline: how much was already resident
before anything was produced. That figure is what the human came for.

## 3. Break down what loads before anything happens

The first-turn figure arrives as one number, and one number is unactionable —
nobody can decide anything about "36.773". The aggregator's `always-on block`
section takes it apart for you: skill listings, deferred tool schemas, MCP
server instructions, agent listings, auto-loaded `CLAUDE.md` files
(`nested_memory`, with their paths), and the reminders that re-enter every turn.
Sizes are estimates; the names are exact.

Two things to act on there:

- **Anything marked `LOADED TWICE`.** The harness reloads the whole block when a
  skill is invoked a second time, so `/skill` followed by `/skill <arg>` pays for
  the listings twice. That is pure waste and the human can stop it today.
- **Names nobody in this repo uses.** The tool and MCP listings carry every
  connected server, authenticated or not. Name them, count them, price them.

This breakdown is mandatory and sits outside the three-stretch budget: it is the
one part of the window that is paid on every single turn.

**Then check whether the answer was already in the window.** The `nested_memory`
entries are the instruction files the session actually had loaded. When a costly
stretch went hunting for something those files already state — the verification
commands, a convention, a path — that is an instruction that was resident and got
rediscovered the expensive way. It is the sharpest finding this skill can
produce, because the document already exists and still failed to be used: read
those files and judge it yourself, since only you can tell whether two wordings
mean the same thing.

## 4. Zoom — three stretches

Take the costliest stretches the script names, at most three, and read each one
through the script's own renderer:

```bash
scripts/measure-window.py <transcript.jsonl> --stretch 1
```

It prints that stretch's turns with every block clipped, so reading the evidence
costs a couple of thousand tokens where the raw JSONL holds forty thousand. The
full size of each payload is printed on it, and that is the figure you reason
with.

For each stretch, produce one thing: **what would have had to be written down
for that material never to have needed loading.** Name the document and its
exact home — `a header in src/authorizer/index.ts saying what it decides and who
calls it`, not `document that module better`. Where the answer is that nothing
would have helped, say that; a stretch that was irreducible is worth knowing.

Then check the reprocess and search-term tables. Repeated subjects show where a
finding had nowhere to live. The searched terms are raw grep patterns: the ones
naming something in this domain are the repo's unwritten vocabulary and become
the input to a glossary session, term by term — the ones that are regex
fragments or literals lifted from source code are noise, and listing them as
vocabulary discredits the report. Judge each before it reaches the page.

Three stretches is the budget. Whatever you leave unread, the report declares.

## 5. Find what got buried

The aggregator's `buried material` section measures the other half of the
problem: not how much came in, but **how far it has drifted from the end of the
window**. Attention thins across a long context, so evidence that entered early
is materially weaker than evidence that entered last, even though both are still
resident and both were paid for.

Four signals, each meaning something different:

- **Distance from the end to the heaviest evidence.** When the spec, the ticket
  or the standards document sits 70% of the window back, the session spent its
  last stretch working from a faded copy of the thing it was supposed to satisfy.
  Say which document, and how far back.
- **Acted on long after it was read.** A file read tens of thousands of tokens
  before it was edited was edited from memory. This is where silent mistakes
  come from, and it is worth naming even when the edit turned out fine.
- **Re-read after a gap.** The strongest signal of all: the material was already
  resident and had to be brought back anyway. Whatever the reason, the window had
  stopped being a usable place to keep it.
- **Dilution of the opening instructions.** The aggregator prints what share of
  the window they held at the start, at the first work, and now. Instructions
  that opened at 100% and now sit at 22% are competing with everything loaded
  since — which is the shape of "it ignored what I told it at the beginning".

The cure for buried material is never "read less" — it is to shorten the
distance: bring the spec back in front of the work, or end the session and start
the next one with the standard in hand. Prescribe accordingly.

## 6. Prescribe from the catalogue

Every prescription is a **decision the human takes**, so it carries two parts:
what to do in one sentence, and the footprint it would have saved — an estimate,
labelled as one, computed from the evidence above.

The catalogue below names the skill that executes each lever. Put that name in
the sentence itself, and only where that skill genuinely does the work: `escribe
el glosario con /grill-me-with-docs` reads as help, while a column of skill names
mechanically filled for every row reads as noise and invites wrong attributions.

Split them into two lists, because they are different kinds of decision:

**Fix the project** (`Arreglar el proyecto` in the report) — changes to the repo.
Done once, they pay in every future session.

| Symptom | Lever | Executed by |
| --- | --- | --- |
| Locate heavy; the same terms searched again and again | Fix the vocabulary: a glossary in `CONTEXT.md`, built from the terms the script listed | `grill-me-with-docs` |
| Comprehend heavy; whole files read for a fraction of their content | Self-documenting headers where the zoom found them missing; split files that must be read whole to be understood | `improve-codebase-architecture` |
| Locate heavy across directories whose names do not match the domain | Rename toward the ubiquitous language, or add the index that maps one to the other | `improve-codebase-architecture` |
| Repeated reading to recover a decision's reasoning | An ADR holding the why | `grill-me-with-docs` |
| Toll heavy from an always-loaded document | Prune it, and push what only some runs need behind a pointer | `writing-for-agents` |
| Toll heavy from skill descriptions or tool schemas | Turn the skills you only ever type into user-invoked ones; retire MCP servers this repo does not use | `writing-for-agents` |
| No `CONTEXT.md`, no `docs/agents/` — the scaffold itself is missing | Scaffold it, then fill it | `setup-skills`, then `grill-me-with-docs` |

**Work differently** (`Trabajar distinto` in the report) — how the agent works.
Free to adopt, and forgotten unless it ends up written into an instruction file.

| Symptom | Lever |
| --- | --- |
| Locate heavy in the main window | Delegate the search to a subagent; only its conclusion should land in the window |
| Whole large files read for a few lines | Read by range, or grep for the anchor and read around it |
| Own output heavy | End the session earlier — `handoff` carries the thread to a fresh window |
| Reprocess: the same material entering twice | Write the finding down the first time it is found |
| The spec or the standard sits far behind the end of the window | Bring it back in front of the work before acting on it, or split the session so the next one starts with it in hand |
| Files edited tens of thousands of tokens after they were read | Re-read the few lines being changed immediately before changing them |

When the evidence says the session was healthy — work early, comprehension
proportionate, toll modest — the report says exactly that and prescribes
nothing. A diagnosis that always finds a disease is worth nothing.

Order each list by estimated footprint saved, descending. This skill diagnoses
and proposes; the human decides whether to pull the levers.

## 7. Write the report

Read [`HTML-REPORT.md`](HTML-REPORT.md) for the deliverable and build it there.

Return **one line** to the caller: the headline figure and the report's path.

Your analysis is complete when the always-loaded block is broken into named
pieces, every zoomed stretch has its cheaper-way answer, every buried document is
named with its distance, every prescription carries its figure, and the report
declares what you did not read.
