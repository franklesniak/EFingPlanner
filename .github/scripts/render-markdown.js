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
 *   lastUpdated  YYYY-MM-DD from a top-level `- **Last Updated:** YYYY-MM-DD`
 *                list item, or null. Text in code blocks, HTML blocks, comments,
 *                block quotes and nested lists is never read.
 *   version      YYYYMMDD from a `**Version:** <major>.<minor>.<YYYYMMDD>.<revision>`
 *                line of a top-level paragraph, or null.
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
const VERSION = /^\*\*Version:\*\* \d+\.\d+\.(\d{8})\.\d+[ \t]*$/;

function describe(text) {
  const tokens = md.parse(text, {});
  let lastUpdated = null;
  let version = null;
  tokens.forEach((token, i) => {
    if (token.type !== 'inline') {
      return;
    }
    const lines = token.content.split('\n');
    // A top-level `-` list item's first paragraph: bullet_list_open (level 0),
    // list_item_open (level 1), paragraph_open (level 2), inline (level 3).
    const item = tokens[i - 2];
    if (lastUpdated === null && token.level === 3 && item && item.type === 'list_item_open'
        && item.markup === '-') {
      const m = LAST_UPDATED.exec(lines[0]);
      if (m) {
        lastUpdated = m[1];
      }
    }
    // A top-level paragraph: paragraph_open (level 0), inline (level 1).
    if (version === null && token.level === 1 && tokens[i - 1].type === 'paragraph_open') {
      for (const line of lines) {
        const m = VERSION.exec(line);
        if (m) {
          version = m[1];
          break;
        }
      }
    }
  });
  const html = md.renderer.render(tokens, md.options, {})
    .split('\n')
    .map((line) => line.replace(/[ \t]+$/, ''))
    .join('\n')
    .replace(/\n+$/, '');
  return { html, lastUpdated, version };
}

const input = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
input.on('line', (line) => {
  process.stdout.write(JSON.stringify(describe(JSON.parse(line))) + '\n');
});
