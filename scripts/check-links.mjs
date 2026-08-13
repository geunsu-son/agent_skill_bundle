#!/usr/bin/env node
// Offline internal link checker for the Markdown docs in this repository.
// Scans every tracked .md/.mdc file, extracts relative Markdown links, and
// verifies that each target file exists. External links (http/https/mailto)
// and pure in-page anchors (#...) are skipped on purpose: this repo is offline
// documentation and only its internal cross-references need to stay valid.

import { readFileSync, statSync } from "node:fs";
import { join, dirname, resolve, relative } from "node:path";
import { execSync } from "node:child_process";

const repoRoot = resolve(process.cwd());

function listDocs() {
  const out = execSync("git ls-files '*.md' '*.mdc'", {
    cwd: repoRoot,
    encoding: "utf8",
  });
  return out.split("\n").map((l) => l.trim()).filter(Boolean);
}

// Inline links: [text](target)  and  reference definitions: [id]: target
const inlineLink = /\[[^\]]*\]\(([^)]+)\)/g;
const refDef = /^\s*\[[^\]]+\]:\s+(\S+)/gm;

function extractTargets(content) {
  const targets = [];
  for (const m of content.matchAll(inlineLink)) targets.push(m[1]);
  for (const m of content.matchAll(refDef)) targets.push(m[1]);
  return targets;
}

function isExternalOrAnchor(target) {
  if (!target) return true;
  if (target.startsWith("#")) return true;
  return /^(https?:|mailto:|tel:|data:)/i.test(target);
}

const docs = listDocs();
let checked = 0;
const problems = [];

for (const doc of docs) {
  const abs = join(repoRoot, doc);
  const content = readFileSync(abs, "utf8");
  for (let target of extractTargets(content)) {
    target = target.trim().replace(/^<|>$/g, "");
    if (isExternalOrAnchor(target)) continue;
    // Strip title text: [text](path "title")
    target = target.split(/\s+/)[0];
    // Drop any anchor fragment on a relative file link.
    const filePart = target.split("#")[0];
    if (!filePart) continue;
    checked++;
    const resolved = resolve(dirname(abs), filePart);
    let ok = false;
    try {
      statSync(resolved);
      ok = true;
    } catch {
      ok = false;
    }
    if (!ok) {
      problems.push({
        source: doc,
        target,
        resolved: relative(repoRoot, resolved),
      });
    }
  }
}

console.log(
  `Checked ${checked} internal link(s) across ${docs.length} Markdown file(s).`
);

if (problems.length > 0) {
  console.error(`\nFound ${problems.length} broken internal link(s):`);
  for (const p of problems) {
    console.error(`  - ${p.source} -> ${p.target}  (missing: ${p.resolved})`);
  }
  process.exit(1);
}

console.log("All internal links resolve.");
