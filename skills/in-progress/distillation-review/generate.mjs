#!/usr/bin/env node
//
// generate.mjs — extract the deterministic half of a distillation review.
//
// Parses a branch diff and writes a fresh review folder to the OS temp dir:
//   - review-data.js   window.REVIEW_DATA = {…}  (hunks, file tree, PROJECT grouping,
//                       and per-file LINKS are TRUE BY CONSTRUCTION; prose fields are
//                       null for the agent to fill)
//   - index.html       the renderer, copied verbatim from template/
//
// Three sources (the agent picks one from conversation context; see SKILL.md):
//   node generate.mjs                 local: merge-base(base, HEAD) → working tree
//   node generate.mjs --pr <n|url>    a GitHub PR, via `gh pr diff` (no checkout)
//   node generate.mjs --branch <name> a remote branch, via GitHub compare API
//
// The diff, the project grouping, and the per-file links are all copied/derived VERBATIM
// from an authoritative source (git or GitHub); the script NEVER writes prose and NEVER
// opens the browser — those are the agent's job.
// Uses only Node built-ins plus the `git`/`gh` CLIs: no npm install, no node_modules.
//
// Usage: node generate.mjs [--base <ref>] [--pr <n|url>] [--branch <name>]

import { execFileSync } from "node:child_process";
import { mkdirSync, writeFileSync, copyFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));

// --- shell helpers -----------------------------------------------------------
function run(cmd, args) {
  return execFileSync(cmd, args, { encoding: "utf8", maxBuffer: 256 * 1024 * 1024 });
}
function git(args) { return run("git", args); }
function gitSafe(args) { try { return git(args).trim(); } catch { return ""; } }
// gh() THROWS on failure with the CLI's own stderr — so callers can try/catch and
// degrade (e.g. a best-effort merge-base). Use ghOrDie() when failure is terminal.
function gh(args) {
  try { return run("gh", args); }
  catch (e) {
    const msg = ((e.stderr || e.stdout || e.message || "") + "").trim();
    const err = new Error(msg || "unknown error");
    err.ghStderr = msg;
    throw err;
  }
}
function ghSafe(args) { try { return gh(args); } catch { return ""; } }
function ghOrDie(args) {
  try { return gh(args); }
  catch (e) {
    die(`gh command failed — ${e.ghStderr || e.message || "unknown error"}\n` +
        `(the --pr / --branch modes need the GitHub CLI; check 'gh auth status')`);
  }
}
function refExists(ref) { try { git(["show-ref", "--verify", "--quiet", ref]); return true; } catch { return false; } }
function die(msg) { console.error(`distillation-review: ${msg}`); process.exit(1); }
const short = (s) => (s || "").slice(0, 9);
const strip = (p) => p.replace(/^[ab]\//, "");
const sanitize = (s) => (s || "HEAD").replace(/[^\w.-]+/g, "-");
const sha256hex = (s) => createHash("sha256").update(s, "utf8").digest("hex");

// --- args --------------------------------------------------------------------
let argBase = "", argPr = "", argBranch = "";
for (let i = 2; i < process.argv.length; i++) {
  const a = process.argv[i];
  if (a === "--base") argBase = process.argv[++i] || "";
  else if (a === "--pr") argPr = process.argv[++i] || "";
  else if (a === "--branch") argBranch = process.argv[++i] || "";
  else die(`unknown argument: ${a}`);
}
if (argPr && argBranch) die("--pr and --branch are mutually exclusive; pick one source");

// Every source resolves the repo from the current directory (gh reads the cwd's git
// remote), so the script MUST run from inside the target repo — never `cd` elsewhere.
if (!gitSafe(["rev-parse", "--is-inside-work-tree"])) die("not inside a git repository");

// --- path-based classification hint (non-binding; the agent decides block type) --
function hintFor(path) {
  const p = path.toLowerCase();
  if (/(^|\/)migrations?\//.test(p) || /\.(sql|prisma)$/.test(p) || /schema\.(rb|sql)$/.test(p)) return "data-model";
  if (/\.(graphql|gql)$/.test(p) || /(openapi|swagger)/.test(p) || /(^|\/)(routes?|controllers?|endpoints?|api)\//.test(p)) return "api-endpoint";
  if (/\.(tsx|jsx|vue|svelte)$/.test(p) || /\.(css|scss|less)$/.test(p) || /(^|\/)components?\//.test(p)) return "wireframe";
  return null;
}

// --- monorepo project detection (deterministic; the agent may refine) --------
// A "project" is the directory of the nearest package manifest above a file. We
// discover manifest directories from the repo tree (per source), then assign each
// touched file to the DEEPEST manifest dir that is its ancestor. Files with no
// manifest ancestor fall back to their top-level path segment. This is the
// projectHint; the agent may reassign in unusual architectures (see blocks.md).
const MANIFESTS = new Set([
  "package.json", "pyproject.toml", "setup.py", "setup.cfg", "go.mod",
  "Cargo.toml", "pom.xml", "build.gradle", "build.gradle.kts", "composer.json",
  "Gemfile", "turbo.json", "pnpm-workspace.yaml", "deno.json", "mix.exs",
]);
const baseName = (p) => p.slice(p.lastIndexOf("/") + 1);
const isManifest = (p) => MANIFESTS.has(baseName(p)) || /\.csproj$/i.test(p);
const dirOf = (p) => { const i = p.lastIndexOf("/"); return i === -1 ? "." : p.slice(0, i); };
const topSegment = (p) => { const i = p.indexOf("/"); return i === -1 ? "(root)" : p.slice(0, i); };

function manifestDirsFrom(paths) {
  const dirs = new Set();
  for (const p of paths) if (p && isManifest(p)) dirs.add(dirOf(p));
  return dirs;
}
// deepest manifest dir that is an ancestor of `path`, or null if none applies
function projectHintFor(path, dirs) {
  let bestDir = null, bestLen = -1;
  for (const d of dirs) {
    const isAncestor = d === "." || path === d || path.startsWith(d + "/");
    if (!isAncestor) continue;
    const len = d === "." ? 0 : d.length;
    if (len > bestLen) { bestLen = len; bestDir = d; }
  }
  return bestDir;
}
// group files into projects[] (TRUE BY CONSTRUCTION: name/path/counts; role is prose)
function buildProjects(files) {
  const map = new Map();
  for (const f of files) {
    const key = f.project;
    let pr = map.get(key);
    if (!pr) { pr = { name: key === "." ? "(root)" : key, path: key, fileCount: 0, added: 0, removed: 0 }; map.set(key, pr); }
    pr.fileCount++; pr.added += f.added; pr.removed += f.removed;
  }
  return [...map.values()].sort((a, b) => (b.added + b.removed) - (a.added + a.removed));
}

// --- unified-diff parser (shared by every source) ---------------------------
// Input is a git-style unified diff string; output is files[] with hunks. Status
// is inferred from the diff headers here and may be refined later via a statusMap.
function parseDiff(fullDiff) {
  const files = [];
  let cur = null;
  let hunk = null;

  for (const line of fullDiff.split("\n")) {
    if (line.startsWith("diff --git ")) {
      if (cur) files.push(cur);
      cur = { path: null, oldPath: null, status: "M", added: 0, removed: 0, binary: false, hunks: [] };
      hunk = null;
      continue;
    }
    if (!cur) continue;

    if (!hunk && line.startsWith("--- ")) {
      const p = line.slice(4);
      cur.oldPath = p === "/dev/null" ? null : strip(p);
      if (p === "/dev/null") cur.status = "A";
      continue;
    }
    if (!hunk && line.startsWith("+++ ")) {
      const p = line.slice(4);
      if (p === "/dev/null") { cur.status = "D"; cur.path = cur.oldPath; }
      else cur.path = strip(p);
      continue;
    }
    if (!hunk && line.startsWith("rename from ")) { cur.oldPath = line.slice(12); continue; }
    if (!hunk && line.startsWith("rename to ")) { cur.path = line.slice(10); cur.status = "R"; continue; }
    if (line.startsWith("Binary files")) { cur.binary = true; continue; }

    if (line.startsWith("@@")) {
      hunk = { header: line, lines: [] };
      cur.hunks.push(hunk);
      continue;
    }
    if (hunk && (line[0] === "+" || line[0] === "-" || line[0] === " ")) {
      const t = line[0] === "+" ? "add" : line[0] === "-" ? "del" : "ctx";
      if (t === "add") cur.added++;
      else if (t === "del") cur.removed++;
      hunk.lines.push({ t, text: line.slice(1) });
    }
    // "\ No newline at end of file" and blank separators are ignored
  }
  if (cur) files.push(cur);
  return files;
}

// map a GitHub compare `files[].status` to the single-letter code the tree uses
function ghStatusToCode(s) {
  return { added: "A", removed: "D", modified: "M", renamed: "R", copied: "C", changed: "T" }[s] || "M";
}

// --- resolve the source -----------------------------------------------------
// Each branch sets: fullDiff, meta, statusMap, dirKey, plus the link context
// (repoWebUrl / headRef / repoRoot) and manifestDirs used to build per-file links
// and the project grouping.
let fullDiff = "", statusMap = null, dirKey = "", meta = {};
let repoWebUrl = "", headRef = "", repoRoot = "", manifestDirs = new Set();
const source = argPr ? "pr" : argBranch ? "branch" : "local";

if (argPr) {
  // ---- PR mode: gh pr diff (verbatim) + gh pr view (metadata) --------------
  let view;
  try {
    view = JSON.parse(gh(["pr", "view", argPr, "--json",
      "number,title,headRefName,headRefOid,baseRefName,baseRefOid,isCrossRepository,url"]));
  } catch (e) { die(`could not read PR '${argPr}' — ${(e.ghStderr || e.message || e).toString().trim()}`); }

  fullDiff = ghOrDie(["pr", "diff", argPr]);
  if (!fullDiff.trim()) die(`PR #${view.number} has no textual diff — nothing to review`);

  // best-effort true merge-base; falls back to the base tip if compare fails
  let mb = "";
  try {
    const cmp = JSON.parse(gh(["api", `repos/{owner}/{repo}/compare/${view.baseRefName}...${view.headRefOid}`]));
    mb = cmp.merge_base_commit?.sha || "";
  } catch { /* non-fatal: header degrades to base tip */ }

  meta = {
    branch: view.headRefName,
    base: view.baseRefName,
    mergeBase: short(mb || view.baseRefOid),
    headSha: short(view.headRefOid),
    prNumber: view.number,
    prUrl: view.url,
    note: `Diff = base(${view.baseRefName}) → PR #${view.number} head, copied verbatim from GitHub (gh pr diff). No local checkout.`,
  };
  dirKey = `pr-${view.number}-${short(view.headRefOid)}`;

  // link context: anchored diff URLs on github.com; repo web url = PR url minus /pull/N
  repoWebUrl = (view.url || "").replace(/\/pull\/\d+.*$/, "");
  headRef = view.headRefName;
  // manifests from the PR head tree (best-effort; degrades to topSegment fallback)
  const tree = ghSafe(["api", `repos/{owner}/{repo}/git/trees/${view.headRefOid}?recursive=1`, "--jq", ".tree[].path"]);
  manifestDirs = manifestDirsFrom(tree.split("\n"));

} else if (argBranch) {
  // ---- branch mode: GitHub compare API (works even without an open PR) -----
  // base is auto-detected the same way as local mode (never hardcode main).
  let base = argBase;
  if (!base) {
    base = gitSafe(["symbolic-ref", "refs/remotes/origin/HEAD"]).replace(/^refs\/remotes\/origin\//, "");
    if (!base && refExists("refs/remotes/origin/main")) base = "main";
    if (!base && refExists("refs/remotes/origin/master")) base = "master";
    if (!base) base = "main";
  }

  let cmp;
  try {
    cmp = JSON.parse(gh(["api", `repos/{owner}/{repo}/compare/${base}...${argBranch}`]));
  } catch (e) { die(`could not compare ${base}...${argBranch} on origin — does the branch exist remotely? (${(e.ghStderr || e.message || e).toString().trim()})`); }

  fullDiff = ghOrDie(["api", `repos/{owner}/{repo}/compare/${base}...${argBranch}`,
    "-H", "Accept: application/vnd.github.diff"]);
  if (!fullDiff.trim()) die(`no changes on ${argBranch} vs ${base} — nothing to review`);

  statusMap = new Map();
  for (const f of cmp.files || []) statusMap.set(f.filename, ghStatusToCode(f.status));

  const headSha = cmp.commits?.length ? cmp.commits[cmp.commits.length - 1].sha : "";
  meta = {
    branch: argBranch,
    base,
    mergeBase: short(cmp.merge_base_commit?.sha),
    headSha: short(headSha),
    note: `Diff = compare ${base}...${argBranch} (merge-base → branch tip) via the GitHub API. No local checkout.`,
  };
  dirKey = `${sanitize(argBranch)}-${short(headSha)}`;

  // link context: blob URLs on github.com at the branch ref
  repoWebUrl = ghSafe(["api", "repos/{owner}/{repo}", "--jq", ".html_url"]).trim();
  headRef = argBranch;
  const tree = ghSafe(["api", `repos/{owner}/{repo}/git/trees/${headSha || argBranch}?recursive=1`, "--jq", ".tree[].path"]);
  manifestDirs = manifestDirsFrom(tree.split("\n"));

} else {
  // ---- local mode: merge-base(base, HEAD) → working tree (unchanged) -------
  let base = argBase;
  if (!base) {
    base = gitSafe(["symbolic-ref", "refs/remotes/origin/HEAD"]).replace(/^refs\/remotes\/origin\//, "");
    if (!base && refExists("refs/remotes/origin/main")) base = "main";
    if (!base && refExists("refs/remotes/origin/master")) base = "master";
    if (!base) base = refExists("refs/heads/main") ? "main" : "master";
  }
  const baseRef = refExists(`refs/remotes/origin/${base}`) ? `origin/${base}` : base;

  const mergeBase = gitSafe(["merge-base", baseRef, "HEAD"]);
  if (!mergeBase) die(`cannot compute merge-base against ${baseRef} — try 'git fetch origin'`);

  const branch = gitSafe(["rev-parse", "--abbrev-ref", "HEAD"]) || "HEAD";
  const headSha = gitSafe(["rev-parse", "--short", "HEAD"]);

  const nameStatus = gitSafe(["diff", "--name-status", mergeBase]);
  fullDiff = gitSafe(["diff", mergeBase]);
  if (!fullDiff) {
    if (branch === base || `origin/${branch}` === baseRef) die(`you are on the base branch (${branch}); nothing to review`);
    die(`no changes vs ${baseRef} — nothing to review`);
  }

  statusMap = new Map();
  for (const line of nameStatus.split("\n")) {
    if (!line) continue;
    const parts = line.split("\t");
    statusMap.set(parts[parts.length - 1], parts[0][0]); // key by new path
  }

  meta = {
    branch,
    base: baseRef,
    mergeBase: short(mergeBase),
    headSha,
    note: "Diff = merge-base(base, HEAD) → working tree, including uncommitted tracked changes. Untracked files are not shown.",
  };
  dirKey = `${sanitize(branch)}-${headSha}`;

  // link context: no URL — the affordance copies the absolute path to the clipboard
  repoRoot = gitSafe(["rev-parse", "--show-toplevel"]);
  // manifests from the tracked working tree
  manifestDirs = manifestDirsFrom(gitSafe(["ls-files"]).split("\n"));
}

// --- per-file link (TRUE BY CONSTRUCTION) ------------------------------------
// PR    → anchored diff URL so the reviewer can jump straight to the file and comment.
// branch→ read-only blob URL on origin at the branch ref.
// local → { mode:"copy" } with the absolute path (no URL exists).
function linkFor(path) {
  if (source === "pr" && repoWebUrl && meta.prNumber != null)
    return { mode: "href", href: `${repoWebUrl}/pull/${meta.prNumber}/files#diff-${sha256hex(path)}` };
  if (source === "branch" && repoWebUrl)
    return { mode: "href", href: `${repoWebUrl}/blob/${headRef}/${path}` };
  if (source === "local" && repoRoot)
    return { mode: "copy", path: join(repoRoot, path) };
  return null;
}

// --- parse + finalize per-file metadata -------------------------------------
const files = parseDiff(fullDiff);
for (const f of files) {
  if (!f.path) f.path = f.oldPath || "(unknown)";
  if (statusMap && statusMap.get(f.path)) f.status = statusMap.get(f.path);
  f.hint = hintFor(f.path);
  f.projectHint = projectHintFor(f.path, manifestDirs);   // deepest manifest dir, or null
  f.project = f.projectHint || topSegment(f.path);         // resolved grouping key
  f.link = linkFor(f.path);
}

const projects = buildProjects(files);
const totalAdded = files.reduce((n, f) => n + f.added, 0);
const totalRemoved = files.reduce((n, f) => n + f.removed, 0);

// --- assemble review-data ----------------------------------------------------
const data = {
  meta: { ...meta, source, fileCount: files.length, totalAdded, totalRemoved },
  // TRUE BY CONSTRUCTION — do not edit. Diff lines, project grouping, and links
  // are derived verbatim from git/GitHub.
  files,
  projects,          // [ { name, path, fileCount, added, removed } ] — add `role` (prose) per project
  // PROSE — the agent fills these nulls in place. See references/blocks.md.
  mentalMap: null,   // { problem: string, approach: string, impact: string } — the problem solved
  diagrams: null,    // [ { kind, title, mermaid } ]  1-4 typed diagrams, or []  (kind: inheritance|relationship|types|flow|state)
  keyChanges: null,  // [ { path, project, blockType, impact, impactWhy, title, summary, wireframeHtml? } ] — ordered by disruption
};

// --- write the review folder -------------------------------------------------
const dir = join(tmpdir(), `distillation-review-${dirKey}`);
mkdirSync(dir, { recursive: true });
writeFileSync(join(dir, "review-data.js"), `window.REVIEW_DATA = ${JSON.stringify(data, null, 2)};\n`);
copyFileSync(join(HERE, "template", "index.html"), join(dir, "index.html"));

// --- report paths for the agent ---------------------------------------------
console.log(JSON.stringify({
  reviewDir: dir,
  dataFile: join(dir, "review-data.js"),
  htmlFile: join(dir, "index.html"),
  source,
  branch: meta.branch, base: meta.base,
  fileCount: files.length, totalAdded, totalRemoved,
  projects: projects.map((p) => p.name),
}, null, 2));
