#!/usr/bin/env node

/**
 * Render Markdown for the Last Updated check
 *
 * check-last-updated.py uses this helper so that its decisions follow a real
 * CommonMark parser instead of hand-written rules. It reads one JSON object per
 * line on stdin, `{"text": <Markdown document>, "path": <its repository path>}`,
 * and writes one JSON object per line on stdout:
 *
 *   html         the document rendered with markdown-it in CommonMark mode, with
 *                trailing spaces and tabs removed from each output line and
 *                trailing blank lines removed. Two versions of a document whose
 *                html is equal differ only in ways that do not render, which is
 *                what the documentation style guide calls mechanical. Every
 *                relative URL, in a Markdown link or image or in a URL attribute
 *                of a raw HTML tag, is rewritten to a path from the repository
 *                root, resolved from the directory of `path`. So a relative
 *                reference compares by the file it points to, and moving a file
 *                changes its html exactly when a reference now points elsewhere.
 *                Raw HTML URL attributes are also written in one form (lowercase
 *                name, double-quoted value). HTML comments and text are left as
 *                they are.
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

const path = require('path');
const readline = require('readline');
const MarkdownIt = require('markdown-it');

const md = new MarkdownIt('commonmark');
const LAST_UPDATED = /^\*\*Last Updated:\*\* (\d{4}-\d{2}-\d{2})[ \t]*$/;
const VERSION = /^\*\*Version:\*\* (\d+\.\d+\.\d{8}\.\d+)[ \t]*$/;
const FRONT_MATTER = /^---[ \t]*\r?\n(?:[^]*?\r?\n)?(?:---|\.\.\.)[ \t]*(?:\r?\n|$)/;
const H1_LINE_LIMIT = 30;

// HTML attributes whose values are URLs (HTML Living Standard, attributes index).
const URL_ATTRIBUTES = new Set(['action', 'background', 'cite', 'data', 'formaction', 'href', 'longdesc',
  'poster', 'src', 'srcset']);
// A URL with a scheme, a root-relative or protocol-relative path, or only a query or fragment
// does not depend on the document's directory.
const NOT_RELATIVE = /^(?:[A-Za-z][A-Za-z0-9+.-]*:|\/|#|\?|$)/;
// Raw HTML pieces: a comment, or a start tag whose quoted values may hold `>`.
const COMMENT_OR_TAG = /<!--[^]*?-->|<[A-Za-z][A-Za-z0-9-]*(?:[^>"']|"[^"]*"|'[^']*')*>/g;
// One attribute inside a start tag, from the current position (CommonMark 0.31.2, raw HTML).
const ATTRIBUTE = /(\s+)([A-Za-z_:][A-Za-z0-9_.:-]*)(?:(\s*=\s*)("[^"]*"|'[^']*'|[^\s"'=<>`]+))?/y;

function resolveUrl(url, directory) {
  const trimmed = url.trim();
  if (NOT_RELATIVE.test(trimmed)) {
    return url;
  }
  const cut = trimmed.search(/[?#]/);
  const target = cut < 0 ? trimmed : trimmed.slice(0, cut);
  const rest = cut < 0 ? '' : trimmed.slice(cut);
  return '/' + path.posix.normalize(path.posix.join(directory, target)) + rest;
}

// A srcset value is a comma-separated list of candidates, each a URL and an optional descriptor.
function resolveSrcset(value, directory) {
  return value.split(',').map((candidate) => {
    const [url, ...descriptor] = candidate.trim().split(/\s+/);
    return [resolveUrl(url, directory), ...descriptor].join(' ');
  }).join(', ');
}

function resolveAttribute(name, value, directory) {
  return name === 'srcset' ? resolveSrcset(value, directory) : resolveUrl(value, directory);
}

// A start tag with each URL attribute resolved and written as name="value".
function canonicalTag(tag, directory) {
  const name = /^<[A-Za-z][A-Za-z0-9-]*/.exec(tag)[0];
  let out = name;
  let at = name.length;
  ATTRIBUTE.lastIndex = at;
  let m;
  while ((m = ATTRIBUTE.exec(tag)) !== null) {
    const attribute = m[2].toLowerCase();
    if (m[4] !== undefined && URL_ATTRIBUTES.has(attribute)) {
      const quoted = m[4][0] === '"' || m[4][0] === "'";
      const value = quoted ? m[4].slice(1, -1) : m[4];
      out += ' ' + attribute + '="' + resolveAttribute(attribute, value, directory).replace(/"/g, '&quot;') + '"';
    } else {
      out += m[0];
    }
    at = ATTRIBUTE.lastIndex;
  }
  return out + tag.slice(at);
}

function canonicalHtml(html, directory) {
  return html.replace(COMMENT_OR_TAG, (piece) => (piece.startsWith('<!--') ? piece : canonicalTag(piece, directory)));
}

// Resolve relative references in Markdown links, images and raw HTML, in place.
function resolveReferences(tokens, directory) {
  for (const token of tokens) {
    if (token.type === 'link_open' || token.type === 'image') {
      const attribute = token.type === 'link_open' ? 'href' : 'src';
      token.attrSet(attribute, resolveUrl(token.attrGet(attribute), directory));
    } else if (token.type === 'html_block' || token.type === 'html_inline') {
      token.content = canonicalHtml(token.content, directory);
    }
    if (token.children) {
      resolveReferences(token.children, directory);
    }
  }
}

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

function describe(text, filePath) {
  const tokens = md.parse(text, {});
  resolveReferences(tokens, path.posix.dirname(filePath));
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
  const request = JSON.parse(line);
  process.stdout.write(JSON.stringify(describe(request.text, request.path)) + '\n');
});
