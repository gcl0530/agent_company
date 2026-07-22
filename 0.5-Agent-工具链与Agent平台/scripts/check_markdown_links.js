#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const target = process.argv[2] || '.';
const root = path.resolve(target);
const ignored = new Set(['.git', 'Temp', 'node_modules']);
const markdownFiles = [];

function collect(current) {
  const stat = fs.statSync(current);
  if (stat.isFile()) {
    if (current.endsWith('.md')) markdownFiles.push(current);
    return;
  }
  for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
    if (entry.isDirectory() && ignored.has(entry.name)) continue;
    collect(path.join(current, entry.name));
  }
}

collect(root);
const errors = [];
for (const file of markdownFiles) {
  const content = fs.readFileSync(file, 'utf8');
  for (const match of content.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
    let link = match[1].trim();
    if (/^(https?:|mailto:|#)/.test(link)) continue;
    link = link.split('#')[0].replace(/^<|>$/g, '');
    if (!link) continue;
    if (!fs.existsSync(path.resolve(path.dirname(file), link))) {
      errors.push(`${path.relative(root, file)} -> ${link}`);
    }
  }
}

if (errors.length) {
  console.error(errors.join('\n'));
  process.exit(1);
}

console.log(`Markdown links passed: ${markdownFiles.length} files checked`);
