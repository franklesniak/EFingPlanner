#!/usr/bin/env node

/**
 * Render Markdown for the Last Updated check
 *
 * check-last-updated.py uses this helper so that its decisions follow a real
 * CommonMark parser instead of hand-written rules. It reads one JSON string per
 * line on stdin, a Markdown document, and writes one JSON object per line on
 * stdout:
 *
 *   html         the document rendered with markdown-it in CommonMark mode, with
 *                trailing spaces and tabs removed from each output line and
 *                trailing blank lines removed. Two versions of a document whose
 *                html is equal differ only in ways that do not render, which is
 *                what the documentation style guide calls mechanical.
 *   lastUpdated  YYYY-MM-DD from the `- **Last Updated:** YYYY-MM-DD` item of the
 *                metadata header block, or null.
 *   version      the whole `**Version:** <major>.<minor>.<YYYYMMDD>.<revision>`
 *                value from the line directly after the H1, or null.
 *
 * The metadata header block is found where the documentation style guide's
 * "Placement Rules for the Tier 1 Metadata Header Block" put it, after any YAML
 * front matter: directly after an H1 that starts in the first 30 lines of the
 * body (past one optional `**Version:**` line and an optional `## Metadata`
 * heading), or else at the top of the body. HTML comment blocks, such as the
 * `<!-- markdownlint-disable MD013 -->` directive, are skipped at those places,
 * because they render nothing. A metadata-like list anywhere else, such as an
 * example later in the body, is never read.
 *
 * Trailing whitespace is trimmed from the output because the guide exempts
 * trailing-whitespace fixes; a real hard line break still renders as <br />.
 *
 * Usage:
 *   node .github/scripts/render-markdown.js < requests.jsonl
 */

const readline = require('readline');
const MarkdownIt = require('markdown-it');

const md = new MarkdownIt('commonmark');
const LAST_UPDATED = /^\*\*Last Updated:\*\* (\d{4}-\d{2}-\d{2})[ \t]*$/;
const VERSION = /^\*\*Version:\*\* (\d+\.\d+\.\d{8}\.\d+)[ \t]*$/;
const FRONT_MATTER = /^---[ \t]*\r?\n(?:[^]*?\r?\n)?(?:---|\.\.\.)[ \t]*(?:\r?\n|$)/;
const H1_LINE_LIMIT = 30;

// The document's top-level blocks, each with the tokens inside it.
function topLevelBlocks(tokens) {
  const blocks = [];
  for (let i = 0; i < tokens.length; i++) {
    const open = tokens[i];
    let end = i;
    if (open.nesting === 1) {
      while (!(tokens[end].level === 0 && tokens[end].nesting === -1)) {
        end++;
      }
    }
    blocks.push({ open, inner: tokens.slice(i + 1, end) });
    i = end;
  }
  return blocks;
}

function isComment(block) {
  return block !== undefined && block.open.type === 'html_block' && block.open.content.trimStart().startsWith('<!--');
}

function isHeading(block, tag) {
  return block !== undefined && block.open.type === 'heading_open' && block.open.tag === tag;
}

// The first line of a paragraph block, or null for any other block.
function paragraphLine(block) {
  if (block === undefined || block.open.type !== 'paragraph_open') {
    return null;
  }
  return block.inner[0].content.split('\n')[0];
}

// Last Updated from a top-level `-` list: the first paragraph line of each item.
function listField(block) {
  if (block === undefined || block.open.type !== 'bullet_list_open' || block.open.markup !== '-') {
    return null;
  }
  for (let i = 0; i < block.inner.length; i++) {
    const token = block.inner[i];
    // list_item_open (level 1), paragraph_open (level 2), inline (level 3).
    if (token.type === 'inline' && token.level === 3 && block.inner[i - 2].type === 'list_item_open') {
      const m = LAST_UPDATED.exec(token.content.split('\n')[0]);
      if (m) {
        return m[1];
      }
    }
  }
  return null;
}

function metadata(tokens) {
  const blocks = topLevelBlocks(tokens);
  let at = blocks.findIndex((b) => isHeading(b, 'h1') && b.open.map[0] < H1_LINE_LIMIT);
  let version = null;
  if (at >= 0) {
    at++;
    while (isComment(blocks[at])) {
      at++;
    }
    const m = VERSION.exec(paragraphLine(blocks[at]) || '');
    if (m && blocks[at].inner[0].content.indexOf('\n') < 0) {
      version = m[1];
      at++;
    }
    while (isComment(blocks[at])) {
      at++;
    }
    if (isHeading(blocks[at], 'h2') && blocks[at].inner[0].content.trim() === 'Metadata') {
      at++;
    }
  } else {
    at = 0;
  }
  while (isComment(blocks[at])) {
    at++;
  }
  return { lastUpdated: listField(blocks[at]), version };
}

function describe(text) {
  const tokens = md.parse(text, {});
  const html = md.renderer.render(tokens, md.options, {})
    .split('\n')
    .map((line) => line.replace(/[ \t]+$/, ''))
    .join('\n')
    .replace(/\n+$/, '');
  const frontMatter = FRONT_MATTER.exec(text);
  const body = frontMatter ? md.parse(text.slice(frontMatter[0].length), {}) : tokens;
  return { html, ...metadata(body) };
}

const input = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
input.on('line', (line) => {
  process.stdout.write(JSON.stringify(describe(JSON.parse(line))) + '\n');
});
