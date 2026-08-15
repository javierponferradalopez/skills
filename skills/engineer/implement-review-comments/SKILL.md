---
name: implement-review-comments
description: Work through review comments — your notes on the code, a Pull Request's threads, or feedback you paste — applying the obvious ones on a single OK and grilling the rest one at a time.
disable-model-invocation: true
---

# Implement review comments

Some comments are one instruction with one obvious implementation; others hide a decision that belongs to the user. Applying everything silently gets the second kind wrong, and discussing everything wastes the user on the first — so sort them, then treat each kind on its own terms.

## 1. Find them

Start from the source the user's message already names. Invoked with nothing, ask — closed, so one word answers it: **their notes on the code, a Pull Request, or something they paste?**

- **Their notes** — the comments they left for you on the code, in the format their `CLAUDE.md` defines. Read each one whole: a note can run past its first line.
- **A Pull Request** — [`PR.md`](PR.md) has the ground check, the collection script and the reply mechanics.
- **Pasted** — take them as given.

## 2. Sort — the uniqueness test

For each comment ask: **is there more than one reasonable way to satisfy this?**

- No → **clear**.
- Yes → **open**. It needs the user.

A comment is open when it reaches code outside its own file, changes a signature or any other public contract, names a new concept, or asks a question instead of giving an instruction. Borderline counts as open: a question costs one turn, a wrong guess costs the user's trust in the whole batch.

## 3. Post the map, then get an OK on the clear ones

Lead with the shape of the batch — _"12 comments: 7 clear, 5 to talk through."_

List the clear ones, one line each: what the comment asks, and what you will do about it. End with how you will close them (step 5). Then wait.

Clear says the implementation is obvious, never that the change is wanted — and the comment may be someone else's, so the user decides whether it lands at all.

One OK covers the whole list and the closing. Anything the user pulls out of it — _"all but the third"_ — turns open and gets grilled with the rest. Apply the approved ones together.

## 4. Grill the open ones

Run a `/grill-me` session over the open comments. Three things are specific to this one:

- **The shared understanding is per comment, not per batch.** Settle one and apply it (step 5) before opening the next, rather than holding every change until the end.
- **Two comments that are the same decision** in two places: merge them and say so.
- **A comment that runs past one exchange**: park it and keep going with the rest, so one long argument holds nothing else hostage.

## 5. Close on the spot

The moment a comment is settled, apply its change and close it **in the same edit**:

| Source          | Closing it means                                  |
| --------------- | ------------------------------------------------- |
| Their notes     | Delete the note, whether the code changed or not  |
| A Pull Request  | Answer the thread, per [`PR.md`](PR.md)           |
| Pasted          | Nothing to close                                  |

Open comments are the state of the batch — what is still open is what is left to do, so an interrupted run loses nothing and resuming is just running again.

A comment settled as **leave the code as it is** closes too. If the discussion produced a reason that is invisible from the code — a constraint, a trade-off already tried — offer to leave it as a comment there. The user decides; a codebase padded with defensive comments is worse than the debate repeating.

## 6. Hand back

The batch ends with every comment closed and the working tree dirty. Committing is a separate step: `/commit` groups the diff by cohesion, which the order of the comments does not.
