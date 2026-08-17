---
name: grill-me-comments
description: Work through review comments — the ones in the code, a Pull Request's threads, or feedback you paste — settling the obvious ones on a single OK, grilling the rest one at a time, and handing back the agreed batch for the user to say what becomes of it.
disable-model-invocation: true
---

# Grill me on the review comments

Some comments are one instruction with one obvious implementation; others hide a decision that belongs to the user. Applying everything silently gets the second kind wrong, and discussing everything wastes the user on the first — so sort them, then treat each kind on its own terms.

The whole run is agreement, not work: nothing is written until the user has said what becomes of the batch — not a line of code, not a reply on GitHub, not a comment deleted. A comment is closed by the change that satisfies it actually landing, so a comment nobody implemented stays exactly where it is.

## 1. Find them

Start from the source the user's message already names. Invoked with nothing, ask — closed, so one word answers it: **in the code, on a Pull Request, or pasted here?**

- **In the code** — the comments they left for you there, in the format their `CLAUDE.md` defines. Read each one whole: a comment can run past its first line.
- **On a Pull Request** — [`PR.md`](PR.md) has the ground check, the collection script and the reply mechanics.
- **Pasted here** — take them as given.

## 2. Sort — the uniqueness test

For each comment ask: **is there more than one reasonable way to satisfy this?**

- No → **AFK**. It resolves with the agent alone.
- Yes → **HITL** — human in the loop. It only resolves through a live exchange with the user, who speaks for themselves; an agent that answers for them has broken this.

A comment is HITL when it reaches code outside its own file, changes a signature or any other public contract, names a new concept, or asks a question instead of giving an instruction. Borderline counts as HITL: a question costs one turn, a wrong guess costs the user's trust in the whole batch.

## 3. Post the map, then get an OK on the AFK ones

Lead with the shape of the batch — _"12 comments: 7 AFK, 5 HITL."_

List the AFK ones, one line each: what the comment asks, and what you will do about it. Then wait.

AFK says the implementation is obvious, never that the change is wanted — and the comment may be someone else's, so the user decides whether it lands at all.

One OK settles the whole list; it applies nothing. Anything the user pulls out of it — _"all but the third"_ — turns HITL and gets grilled with the rest, so the OK is worth waiting for even though no code moves.

## 4. Grill the HITL ones

Run a `/grill-me` session over the HITL comments. Three things are specific to this one:

- **The shared understanding is per comment, not per batch.** Settle one and record what was agreed before opening the next.
- **Two comments that are the same decision** in two places: merge them and say so.
- **A comment that runs past one exchange**: park it and keep going with the rest, so one long argument holds nothing else hostage.

A comment can settle as **leave the code as it is**. If the discussion produced a reason that is invisible from the code — a constraint, a trade-off already tried — offer to leave it as a code comment there, and it joins the batch like any other change. The user decides; a codebase padded with defensive comments is worse than the debate repeating.

## 5. Hand back the agreed batch

With every comment settled, write the batch out: one line per comment — AFK and grilled alike, the ones settled as leave-it-alone included — in the same shape as the map in step 3. This is the only place the agreed work exists in writing, and it is what the user reads to decide.

Then ask, proposing nothing: **what happens to this now?**

## 6. Wait

Their answer is the whole of what happens next — implementing it here, writing it up, dropping it. Nothing moves before it arrives.
