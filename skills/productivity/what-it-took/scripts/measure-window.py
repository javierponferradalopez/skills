#!/usr/bin/env python3
"""Aggregate one Claude Code session transcript into a compact window-footprint report.

Deliberately dumb: it sums, groups, sorts and counts. Every judgement about *why*
a number is what it is belongs to the agent reading this output.

Usage:
    measure-window.py <session-id | path-to-transcript.jsonl> [--zoom N] [--top N]
    measure-window.py <transcript.jsonl> --stretch N     # read the Nth costliest stretch
"""

import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

CHARS_PER_TOKEN = 4  # declared approximation; the only one in this script
EXCERPT = 600        # chars kept per block when rendering a stretch

LOCATE_TOOLS = {"Grep", "Glob", "LS", "NotebookRead"}
COMPREHEND_TOOLS = {"Read", "WebFetch", "WebSearch"}
WORK_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit", "TodoWrite",
              "TaskCreate", "TaskUpdate", "Artifact"}
DELEGATE_TOOLS = {"Task", "Agent", "Skill", "Workflow"}

LOCATE_CMD = re.compile(r"\b(grep|rg|ag|find|fd|ls|tree|glob|locate|which)\b")
COMPREHEND_CMD = re.compile(
    r"\b(cat|sed|head|tail|less|more|jq|wc|nl|"
    r"git\s+(show|log|diff|blame)|gh\s+\w+\s+view|gh\s+api|glab\s+\w+\s+view)\b")
WORK_CMD = re.compile(
    r"\b(git\s+(add|commit|push|checkout|branch|stash|rebase|merge)|"
    r"npm|pnpm|yarn|bun|make|cargo|go\s+test|pytest|jest|vitest|tsc|"
    r"mkdir|touch|mv|cp|rm|chmod|tee)\b")

# An interpreter is not work; writing a file is. A heredoc that only prints stays a read.
WRITES = re.compile(
    r"(?<![0-9&])>>?\s*(?!&)(?!/dev/null)[\w.~/-]*[/.][\w.~/-]+"  # > path/file, >> file.ext
    r"|\.write\w*\("                                             # .write(, .writeFileSync(
    r"|\bopen\([^)]*['\"][wa]\+?['\"]")                          # open(p, "w")




def die(msg):
    print(f"measure-window: {msg}", file=sys.stderr)
    sys.exit(1)


def resolve_transcript(arg):
    if os.path.sep in arg or arg.endswith(".jsonl"):
        if not os.path.isfile(arg):
            die(f"no transcript at {arg}")
        return arg
    root = os.path.expanduser("~/.claude/projects")
    if not os.path.isdir(root):
        die(f"no transcript store at {root} — cannot measure this session")
    hits = []
    for project in os.listdir(root):
        candidate = os.path.join(root, project, f"{arg}.jsonl")
        if os.path.isfile(candidate):
            hits.append(candidate)
    if not hits:
        die(f"no transcript found for session id {arg} under {root}")
    return max(hits, key=os.path.getmtime)


def tokens_of(text):
    return math.ceil(len(text) / CHARS_PER_TOKEN)


def flatten(content):
    """Every block shape a transcript uses, reduced to the text that reached the model."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        return flatten(content.get("content") or content.get("text") or "")
    if isinstance(content, list):
        return "\n".join(flatten(b) for b in content)
    return str(content)


HEADING = re.compile(r"#{1,6}\s+\S")


def outline(text):
    """A document's headings with the size of each section — its branches, priced."""
    lines = (text or "").splitlines()
    marks = [i for i, l in enumerate(lines) if HEADING.match(l.strip())]
    if not marks:
        return []
    sections = []
    if marks[0] > 0:
        sections.append(("(before the first heading)", tokens_of("\n".join(lines[:marks[0]]))))
    for n, i in enumerate(marks):
        end = marks[n + 1] if n + 1 < len(marks) else len(lines)
        sections.append((" ".join(lines[i].split())[:90], tokens_of("\n".join(lines[i:end]))))
    return sections


def clip(text, n=EXCERPT):
    text = " ".join((text or "").split())
    if len(text) <= n:
        return text
    return f"{text[:n]} …[{len(text) - n:,} more chars]… {text[-120:]}"


def render_stretch(path, lo, hi):
    """The stretch as the model saw it, every block clipped — the cheap way to read evidence."""
    with open(path, encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            if lineno < lo:
                continue
            if lineno > hi:
                return
            raw = raw.strip()
            if not raw:
                continue
            try:
                d = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if d.get("isSidechain"):
                continue
            kind = d.get("type")
            if kind == "assistant":
                for b in (d.get("message") or {}).get("content") or []:
                    if not isinstance(b, dict):
                        continue
                    if b.get("type") in ("text", "thinking"):
                        body = clip(flatten(b.get("text") or b.get("thinking") or ""))
                        if body:
                            print(f"[{lineno}] {b['type']}: {body}")
                    elif b.get("type") == "tool_use":
                        arg = json.dumps(b.get("input"), ensure_ascii=False)
                        print(f"[{lineno}] -> {b.get('name')} {clip(arg)}")
            elif kind == "user":
                content = (d.get("message") or {}).get("content")
                blocks = content if isinstance(content, list) else [{"type": "text", "text": flatten(content)}]
                for b in blocks:
                    if not isinstance(b, dict):
                        continue
                    if b.get("type") == "tool_result":
                        text = flatten(b.get("content"))
                        print(f"[{lineno}] <- {tokens_of(text):,} tokens: {clip(text)}")
                    else:
                        text = flatten(b.get("text") or b)
                        print(f"[{lineno}] {'reminder' if d.get('isMeta') else 'HUMAN'}: {clip(text)}")
            elif kind == "attachment":
                a = d.get("attachment") or {}
                print(f"[{lineno}] attachment {a.get('type', '?')} ({tokens_of(flatten(a) or json.dumps(a, ensure_ascii=False)):,} tokens)")


def classify(name, tool_input):
    if name in LOCATE_TOOLS:
        return "locate"
    if name in COMPREHEND_TOOLS:
        return "comprehend"
    if name in WORK_TOOLS:
        return "work"
    if name in DELEGATE_TOOLS:
        return "delegate"
    if name == "Bash":
        cmd = (tool_input or {}).get("command", "")
        if WORK_CMD.search(cmd) or WRITES.search(cmd):
            return "work"
        if LOCATE_CMD.search(cmd):
            return "locate"
        if COMPREHEND_CMD.search(cmd):
            return "comprehend"
        return "other"
    if name.startswith("mcp__"):
        return "comprehend"
    return "other"


def path_in(cmd):
    """The first file a command names — so `cat X` and `sed -n '1,5p' X` share a subject."""
    for raw in re.split(r"[\s'\"|;&()<>]+", cmd or ""):
        tok = raw.strip(",").lstrip("./") if raw.startswith("./") else raw.strip(",")
        if not tok or tok.startswith("-") or tok.startswith("/dev/") or tok.endswith("*"):
            continue
        if "/" in tok or re.search(r"\.[A-Za-z]\w{0,7}$", tok):
            return tok.rstrip("/") or None
    return None


def same_file(a, b):
    """Two subjects naming the same file, whichever way each was reached."""
    if a == b:
        return True
    if a.startswith("cmd:") or b.startswith("cmd:"):
        return False
    return os.path.basename(a) == os.path.basename(b)


def subject_of(name, tool_input):
    """The thing a call was about — a path, a pattern, a command — for reprocess detection."""
    i = tool_input or {}
    for key in ("file_path", "path", "notebook_path", "url"):
        if i.get(key):
            return str(i[key])
    if i.get("pattern"):
        return f"pattern:{i['pattern']}"
    if i.get("command"):
        named = path_in(str(i["command"]))
        if named:
            return named
        return f"cmd:{' '.join(str(i['command']).split())[:120]}"
    if i.get("query"):
        return f"query:{i['query']}"
    return f"{name}:?"


SEARCH_TERM = re.compile(r"(?:grep|rg)\b[^|]*?['\"]([^'\"]{2,60})['\"]")


def search_terms(name, tool_input):
    i = tool_input or {}
    if name in ("Grep", "Glob") and i.get("pattern"):
        return [str(i["pattern"])]
    if name == "Bash":
        return SEARCH_TERM.findall(i.get("command", ""))
    return []


def main():
    args = [a for a in sys.argv[1:]]
    zoom = 3
    top = 12
    stretch_n = 0
    positional = []
    while args:
        a = args.pop(0)
        if a == "--zoom":
            zoom = int(args.pop(0))
        elif a == "--top":
            top = int(args.pop(0))
        elif a == "--stretch":
            stretch_n = int(args.pop(0))
        else:
            positional.append(a)
    if not positional:
        die("usage: measure-window.py <session-id | transcript.jsonl> [--zoom N] [--top N]")

    path = resolve_transcript(positional[0])

    turns = []            # main-thread requests, in order (one per requestId)
    seen_requests = set()
    calls = []            # every tool_use with its result size
    pending = {}          # tool_use_id -> call record awaiting its result
    prompt_tokens = 0     # what the human typed
    output_tokens = 0     # the agent's own text and thinking
    injected_tokens = 0   # attachments and reminders arriving after turn 1
    pre_injected = 0      # the same, before turn 1 — already inside `toll`
    pre_prompt = 0        # the opening prompt — likewise inside `toll`
    sidechain_calls = 0
    first_prompt = None
    attachments = defaultdict(lambda: {"n": 0, "tokens": 0, "detail": Counter(),
                                       "lines": [], "files": Counter(), "outlines": {},
                                       "first_turn": None})
    cwd = None
    warnings = []

    with open(path, encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                d = json.loads(raw)
            except json.JSONDecodeError:
                warnings.append(f"line {lineno} is not valid JSON — skipped")
                continue
            kind = d.get("type")
            sidechain = bool(d.get("isSidechain"))
            if cwd is None and d.get("cwd"):
                cwd = d["cwd"]

            if kind == "assistant":
                msg = d.get("message") or {}
                usage = msg.get("usage") or {}
                content = msg.get("content")
                request = d.get("requestId") or msg.get("id") or f"line-{lineno}"
                if not sidechain and request not in seen_requests:
                    seen_requests.add(request)
                    window = (usage.get("input_tokens", 0)
                              + usage.get("cache_creation_input_tokens", 0)
                              + usage.get("cache_read_input_tokens", 0))
                    if window:
                        turns.append({"line": lineno, "window": window,
                                      "output": usage.get("output_tokens", 0)})
                    output_tokens += usage.get("output_tokens", 0)
                if isinstance(content, list):
                    for b in content:
                        if b.get("type") != "tool_use":
                            continue
                        if sidechain:
                            sidechain_calls += 1
                            continue
                        rec = {
                            "line": lineno,
                            "turn": len(turns),
                            "name": b.get("name", "?"),
                            "bucket": classify(b.get("name", "?"), b.get("input")),
                            "subject": subject_of(b.get("name", "?"), b.get("input")),
                            "terms": search_terms(b.get("name", "?"), b.get("input")),
                            "tokens": 0,
                            "result_line": None,
                        }
                        calls.append(rec)
                        if b.get("id"):
                            pending[b["id"]] = rec

            elif kind == "user" and not sidechain:
                msg = d.get("message") or {}
                content = msg.get("content")
                blocks = content if isinstance(content, list) else [{"type": "text", "text": flatten(content)}]
                for b in blocks:
                    if not isinstance(b, dict):
                        continue
                    if b.get("type") == "tool_result":
                        text = flatten(b.get("content"))
                        rec = pending.pop(b.get("tool_use_id"), None)
                        if rec is not None:
                            rec["tokens"] = tokens_of(text)
                            rec["result_line"] = lineno
                        elif turns:
                            injected_tokens += tokens_of(text)
                        else:
                            pre_injected += tokens_of(text)
                    else:
                        text = flatten(b.get("text") or b)
                        if d.get("isMeta"):
                            if turns:
                                injected_tokens += tokens_of(text)
                            else:
                                pre_injected += tokens_of(text)
                        else:
                            if turns:
                                prompt_tokens += tokens_of(text)
                            else:
                                pre_prompt += tokens_of(text)
                            if first_prompt is None:
                                first_prompt = text[:400]

            elif kind == "attachment" and not sidechain:
                a = d.get("attachment") or {}
                text = flatten(a) or json.dumps(a, ensure_ascii=False)
                tok = tokens_of(text)
                if turns:
                    injected_tokens += tok
                else:
                    pre_injected += tok
                rec = attachments[a.get("type", "?")]
                rec["n"] += 1
                rec["tokens"] += tok
                rec["lines"].append(lineno)
                if rec["first_turn"] is None:
                    rec["first_turn"] = len(turns)
                for key in ("addedNames", "names", "addedTypes", "pendingMcpServers"):
                    for v in (a.get(key) or []):
                        rec["detail"][str(v)] += 1
                if a.get("path"):
                    rec["files"][str(a["path"])] += tok
                    rec["outlines"][str(a["path"])] = outline(flatten(a))

    if not turns:
        die(f"{path} holds no assistant turns with usage — nothing to measure")
    if not any(c["tokens"] for c in calls):
        warnings.append("no tool results carried measurable text — bucket sizes are unreliable")

    windows = [t["window"] for t in turns]
    now = windows[-1]
    peak = max(windows)
    toll = windows[0]

    # A compaction is the turn where the window *drops*, not every turn that follows it low.
    compactions = []
    for i in range(1, len(windows)):
        if windows[i] < windows[i - 1] * 0.7 and windows[i - 1] > 20000:
            compactions.append({"turn": i + 1, "line": turns[i]["line"],
                                "from": windows[i - 1], "to": windows[i]})
    compaction = compactions[-1] if compactions else None

    first_work = next((c for c in calls if c["bucket"] == "work"), None)

    by_bucket = Counter()
    for c in calls:
        by_bucket[c["bucket"]] += c["tokens"]
    tool_total = sum(by_bucket.values())

    # Reprocess: the same subject entering the window more than once.
    repeats = defaultdict(list)
    for c in calls:
        if c["bucket"] in ("locate", "comprehend"):
            repeats[c["subject"]].append(c)
    reprocess = [(s, cs) for s, cs in repeats.items() if len(cs) > 1]
    reprocess.sort(key=lambda p: sum(c["tokens"] for c in p[1]), reverse=True)
    reprocess_tokens = sum(sum(c["tokens"] for c in cs) - max(c["tokens"] for c in cs)
                           for _, cs in reprocess)

    # Grep patterns double as regex and as source-code literals; only name-shaped ones are vocabulary.
    term_ok = re.compile(r"^[\w][\w .:@/-]{1,58}$")
    terms = Counter()
    for c in calls:
        for raw_term in c["terms"]:
            for t in re.split(r"\\?\|", raw_term):
                t = t.strip(" .*\\^$()[]?+")
                if len(t) > 2 and term_ok.match(t):
                    terms[t] += 1

    # Costly stretches: consecutive turns ranked by the tool payload they let in.
    per_turn = defaultdict(list)
    for c in calls:
        per_turn[c["turn"]].append(c)
    span = max(2, len(turns) // 8)
    stretches = []
    for start in range(1, len(turns) + 1):
        window_calls = [c for t in range(start, start + span) for c in per_turn.get(t, [])]
        if not window_calls:
            continue
        stretches.append({
            "turns": (start, min(start + span - 1, len(turns))),
            "lines": (min(c["line"] for c in window_calls), max(c["result_line"] or c["line"] for c in window_calls)),
            "tokens": sum(c["tokens"] for c in window_calls),
            "calls": window_calls,
        })
    stretches.sort(key=lambda s: s["tokens"], reverse=True)
    chosen, claimed = [], set()
    for s in stretches:
        if any(t in claimed for t in range(s["turns"][0], s["turns"][1] + 1)):
            continue
        chosen.append(s)
        claimed.update(range(s["turns"][0], s["turns"][1] + 1))
        if len(chosen) == zoom:
            break

    if stretch_n:
        if not 1 <= stretch_n <= len(chosen):
            die(f"no stretch {stretch_n} — this transcript has {len(chosen)}")
        s = chosen[stretch_n - 1]
        print(f"# stretch {stretch_n}: turns {s['turns'][0]}-{s['turns'][1]}, "
              f"{s['tokens']:,} tokens of payload, jsonl lines {s['lines'][0]}-{s['lines'][1]}")
        print(f"Every block below is clipped to {EXCERPT} chars; the size printed on each "
              f"tool result is the full figure.")
        print()
        render_stretch(path, s["lines"][0], s["lines"][1])
        return

    out = print
    out(f"# window footprint — {os.path.basename(path)}")
    out(f"transcript: {path}")
    out(f"turns: {len(turns)}   tool calls: {len(calls)}   delegated calls (sidechain, off this window): {sidechain_calls}")
    out(f"token estimates from characters/{CHARS_PER_TOKEN}; usage figures are exact")
    for w in warnings:
        out(f"WARNING: {w}")
    out("")

    out("## resident")
    out(f"now: {now:,}   peak: {peak:,}   toll (first turn, before any work): {toll:,}")
    for c in compactions:
        out(f"COMPACTED at turn {c['turn']} (line {c['line']}): "
            f"{c['from']:,} -> {c['to']:,}. "
            f"Everything before that line left the window; totals below do not reconcile with 'now'.")
    if first_work:
        w = turns[first_work['turn'] - 1]['window'] if 0 < first_work['turn'] <= len(turns) else 0
        out(f"first work: turn {first_work['turn']} of {len(turns)} (line {first_work['line']}) — "
            f"{w:,} resident by then ({w / now * 100:.0f}% of what is resident now), "
            f"{first_work['name']} on {first_work['subject'][:80]}")
    else:
        out("first work: none — this session has only read, searched and talked so far")
    out("")

    out("## where it came from")
    out(f"{'bucket':<12} {'tokens':>10}  share of tool payload")
    for bucket in ("locate", "comprehend", "work", "delegate", "other"):
        t = by_bucket.get(bucket, 0)
        share = (t / tool_total * 100) if tool_total else 0
        out(f"{bucket:<12} {t:>10,}  {share:5.1f}%")
    out(f"{'--':<12} {tool_total:>10,}  tool payload total")
    out(f"{'prompts':<12} {prompt_tokens:>10,}  what the human typed")
    out(f"{'own output':<12} {output_tokens:>10,}  the agent's text and thinking")
    out(f"{'injected':<12} {injected_tokens:>10,}  attachments, reminders, auto-loaded files")
    accounted = toll + tool_total + prompt_tokens + output_tokens + injected_tokens
    out(f"{'toll':<12} {toll:>10,}  system prompt, skill descriptions, tool definitions, CLAUDE.md "
        f"(includes {pre_injected:,} of attachments and {pre_prompt:,} of opening prompt, counted here only)")
    out(f"reconciles to {accounted:,} against {now:,} resident "
        f"({accounted / now * 100:.0f}% — the gap is the chars/{CHARS_PER_TOKEN} estimate"
        f"{' and the compaction above' if compaction else ''})")
    out("")

    out("## growth no payload accounts for")
    out("A turn whose window grew far beyond the payload it received loaded something else —")
    out("a skill body, a tool schema, an auto-attached file. This is toll arriving mid-session.")
    payload_by_turn = defaultdict(int)
    for c in calls:
        payload_by_turn[c["turn"]] += c["tokens"]
    unexplained = []
    for i in range(1, len(turns)):
        delta = turns[i]["window"] - turns[i - 1]["window"]
        own = turns[i - 1]["output"]
        payload = payload_by_turn.get(i, 0)
        gap = delta - payload - own
        if gap > 2000:
            unexplained.append((gap, i + 1, turns[i]["line"], delta, payload, own))
    unexplained.sort(reverse=True)
    for gap, turn, line, delta, payload, own in unexplained[:top]:
        out(f"{gap:>8,} unaccounted  turn {turn:<4} line {line:<6} "
            f"window grew {delta:,} on {payload:,} payload + {own:,} own output")
    if not unexplained:
        out("none above 2,000 tokens")
    out("")

    out(f"## costliest stretches (zoom budget: {zoom})")
    for s in chosen:
        out(f"turns {s['turns'][0]}-{s['turns'][1]}  {s['tokens']:,} tokens  "
            f"jsonl lines {s['lines'][0]}-{s['lines'][1]}   (sed -n '{s['lines'][0]},{s['lines'][1]}p' <transcript>)")
        for c in sorted(s["calls"], key=lambda c: c["tokens"], reverse=True)[:6]:
            out(f"    {c['tokens']:>8,}  {c['bucket']:<10} {c['name']:<10} {c['subject'][:90]}")
    zoomed_turns = {t for s in chosen for t in range(s["turns"][0], s["turns"][1] + 1)}
    left = sum(c["tokens"] for c in calls if c["turn"] not in zoomed_turns)
    if left:
        out(f"not zoomed: {left:,} tokens of tool payload outside these stretches")
    out("")

    out(f"## heaviest single calls (top {top})")
    for c in sorted(calls, key=lambda c: c["tokens"], reverse=True)[:top]:
        out(f"{c['tokens']:>8,}  turn {c['turn']:<4} line {c['line']:<6} {c['bucket']:<10} {c['name']:<10} {c['subject'][:90]}")
    out("")

    out(f"## reprocess — same material entering twice ({reprocess_tokens:,} tokens beyond the first entry)")
    for subject, cs in reprocess[:top]:
        out(f"{len(cs)}x  {sum(c['tokens'] for c in cs):>8,}  {cs[0]['bucket']:<10} "
            f"turns {','.join(str(c['turn']) for c in cs[:8])}  {subject[:90]}")
    if not reprocess:
        out("none")
    out("")

    out("## buried material — lost in the middle")
    out("Material sitting far from the end of the window, where attention thins.")
    win_of = lambda turn: turns[turn - 1]["window"] if 0 < turn <= len(turns) else 0

    # A subject re-entering the window after a long gap: proof it stopped being reachable.
    reread = []
    for subject, cs in repeats.items():
        for earlier, later in zip(cs, cs[1:]):
            gap = win_of(later["turn"]) - win_of(earlier["turn"])
            if gap > 0:
                reread.append((gap, subject, earlier["turn"], later["turn"], later["tokens"]))
    reread.sort(reverse=True)
    out("re-read after a gap (window tokens between the two entries):")
    for gap, subject, t1, t2, tok in reread[:top]:
        out(f"{gap:>8,} apart  turns {t1}->{t2}  {tok:>7,} to bring it back  {subject[:80]}")
    if not reread:
        out("  none — nothing had to be brought back")

    # Distance between reading a file and acting on it: the edit works from a faded memory.
    last_seen = {}
    acted = []
    for c in calls:
        if c["bucket"] in ("locate", "comprehend"):
            last_seen[c["subject"]] = c
        elif c["bucket"] == "work":
            touched = [seen for seen in last_seen if same_file(seen, c["subject"])]
            for subject in touched:
                src = last_seen[subject]
                gap = win_of(c["turn"]) - win_of(src["turn"])
                if gap > 0:
                    acted.append((gap, subject, src["turn"], c["turn"]))
    acted.sort(reverse=True)
    widest = {}
    for gap, subject, t1, t2 in acted:
        if subject not in widest:
            widest[subject] = (gap, subject, t1, t2)
    acted = list(widest.values())
    out("acted on long after it was read (window tokens between reading and working on it):")
    for gap, subject, t1, t2 in acted[:top]:
        out(f"{gap:>8,} apart  read turn {t1}, worked turn {t2}  {subject[:80]}")
    if not acted:
        out("  none — everything was acted on close to when it was read")

    # Where the payload physically sits, and how much of it was ever needed again.
    thirds = [("first", 0, now / 3), ("middle", now / 3, now * 2 / 3), ("last", now * 2 / 3, now + 1)]
    later_subjects = defaultdict(list)
    for c in calls:
        later_subjects[c["subject"]].append(c["turn"])
    out("distance from the end of the window to the heaviest evidence:")
    for c in sorted(calls, key=lambda c: c["tokens"], reverse=True)[:6]:
        behind = now - win_of(c["turn"])
        out(f"{behind:>8,} behind the end  ({behind / now * 100:2.0f}% of the window ago)  "
            f"{c['tokens']:>7,} {c['bucket']:<10} {c['subject'][:70]}")
    out("where the payload sits, by window position:")
    for label, lo, hi in thirds:
        zone = [c for c in calls if lo <= win_of(c["turn"]) < hi]
        tok = sum(c["tokens"] for c in zone)
        revisited = sum(c["tokens"] for c in zone
                        if max(later_subjects[c["subject"]]) > c["turn"])
        share = (revisited / tok * 100) if tok else 0
        out(f"  {label:<7} third: {tok:>8,} tokens, {share:4.0f}% of it needed again later")
    out("")

    out("## terms searched for (candidates for a glossary)")
    for term, n in terms.most_common(top):
        out(f"{n}x  {term[:90]}")
    if not terms:
        out("none")
    out("")

    out("## the injected block, itemised")
    out("What the harness loads whether or not it gets used. Sizes are estimates;")
    out("the names are exact, and a type listed twice was loaded twice.")
    out("A block arriving at turn 1 sits inside `toll`; one arriving later is paid by every")
    out("turn after it, and shows up above as growth no payload accounts for.")
    for kind, rec in sorted(attachments.items(), key=lambda kv: kv[1]["tokens"], reverse=True):
        repeated = " LOADED TWICE" if kind in ("skill_listing", "deferred_tools_delta",
                                               "mcp_instructions_delta", "agent_listing_delta") \
                   and rec["n"] > 1 else ""
        ft = rec["first_turn"] or 0
        when = ("at turn 1, inside toll" if ft == 0 else
                f"from turn {ft} on — paid by the {len(turns) - ft} turns after it")
        out(f"{rec['tokens']:>8,}  {kind:<24} x{rec['n']:<4} {when}  lines {rec['lines'][:4]}{repeated}")
        for fp, tok in rec["files"].most_common(15):
            out(f"          {tok:>7,}  {fp.replace(cwd + '/', '') if cwd else fp}")
        if len(rec["files"]) > 15:
            out(f"          ...and {len(rec['files']) - 15} more files")
        if rec["detail"]:
            names = ", ".join(n for n, _ in rec["detail"].most_common(10))
            out(f"          {names[:200]}")
            if len(rec["detail"]) > 10:
                out(f"          ...and {len(rec['detail']) - 10} more")
    if not attachments:
        out("none recorded in this transcript")
    out("")

    priced = [(fp, rec["files"][fp], o) for rec in attachments.values()
              for fp, o in rec["outlines"].items() if o]
    if priced:
        out("## what the auto-loaded instructions contain")
        out("Each instruction file broken into its sections, largest first. The document was")
        out("paid for whole; judge section by section which of it this session actually needed.")
        for fp, size, sections in sorted(priced, key=lambda t: t[1], reverse=True):
            out(f"{size:>8,}  {fp.replace(cwd + '/', '') if cwd else fp}")
            for head, tok in sorted(sections, key=lambda t: t[1], reverse=True)[:12]:
                out(f"          {tok:>7,}  {head}")
            if len(sections) > 12:
                out(f"          ...and {len(sections) - 12} more sections")
        out("")

    out("## how far the opening instructions got diluted")
    at_work = turns[first_work["turn"] - 1]["window"] if first_work else toll
    out(f"they were 100% of the window at turn 1, "
        f"{toll / at_work * 100:.0f}% by the first work, "
        f"{toll / now * 100:.0f}% now — competing with {now - toll:,} tokens loaded since")
    out("")

    if first_prompt:
        out("## the task, as the human first stated it")
        out(first_prompt.replace("\n", " ")[:400])


if __name__ == "__main__":
    main()
