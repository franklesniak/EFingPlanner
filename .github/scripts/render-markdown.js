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
 *                relative URL in a Markdown link or image is rewritten to a path
 *                from the repository root, resolved from the directory of `path`
 *                by the URL Standard's rules. So a relative reference compares
 *                by the file it points to, and moving a file changes its html
 *                exactly when a reference now points elsewhere. A directory name
 *                byte that is not UTF-8 is written as %XX, as in the file's URL.
 *                Raw HTML is not read: the repository's markdownlint
 *                configuration rejects it (MD033), and reading it as a browser
 *                does takes the whole HTML parser. It is kept as written, and
 *                when raw HTML other than comments holds a tag, a line naming
 *                the directory of `path` is added, so moving the file changes
 *                its html.
 *   lastUpdated  YYYY-MM-DD from the `- **Last Updated:** YYYY-MM-DD` item of the
 *                metadata header block, or the item's value as written when it
 *                has another shape (so the check can report it), or null.
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
const YAML = require('yaml');

const md = new MarkdownIt('commonmark');
// markdown-it's own escaping: `&`, `<`, `>` and `"`. The directory line uses it, so no two
// directories are written alike.
const { escapeHtml } = md.utils;
const LAST_UPDATED = /^\*\*Last Updated:\*\* (\d{4}-\d{2}-\d{2})[ \t]*$/;
const LAST_UPDATED_ITEM = /^\*\*Last Updated:\*\*[ \t]*(.*?)[ \t]*$/;
const VERSION = /^\*\*Version:\*\* (\d+\.\d+\.\d{8}\.\d+)[ \t]*$/;
const FRONT_MATTER = /^---[ \t]*\r?\n(?:[^]*?\r?\n)?(?:---|\.\.\.)[ \t]*(?:\r?\n|$)/;
const H1_LINE_LIMIT = 30;
// The metadata header block's required fields beside Last Updated (the docs guide's Tier 1 list).
const REQUIRED_FIELDS = ['Status', 'Owner', 'Scope'];
// A URL with a scheme, a root-relative or protocol-relative path, or only a query or fragment
// does not depend on the document's directory.
const NOT_RELATIVE = /^(?:[A-Za-z][A-Za-z0-9+.-]*:|\/|#|\?|$)/;
// The base every relative reference resolves against; the host only makes it a full URL.
const BASE_ORIGIN = 'https://repository.invalid';
// A whole HTML comment, as the HTML tokenizer ends one: at `-->` or `--!>`, as the empty forms
// `<!-->` and `<!--->`, or, when it is never closed, at the end of the page (see onlyComments).
const COMMENT = /<!--(?:-?>|[^]*?--!?>|[^]*$)/g;
// Raw HTML that holds a tag. Outside a piece of only comments, the tag counts wherever it is,
// even inside a comment, a value or other markup, because none of that is read.
const RAW_TAG = /<[A-Za-z]/;

// Python carries each byte of a name that is not UTF-8 as a lone surrogate, U+DC80 to U+DCFF
// (PEP 383), and encodeURIComponent() throws on one. Such a byte is written as %XX, as it is in
// the file's URL. The `u` flag keeps a valid surrogate pair, such as an emoji, whole.
const ESCAPED_BYTE = /([\uDC80-\uDCFF])/u;

function encodeName(name) {
  return name.split(ESCAPED_BYTE).map((part, i) => (i % 2 === 1
    ? '%' + (part.charCodeAt(0) - 0xDC00).toString(16).toUpperCase()
    : encodeURIComponent(part))).join('');
}

// A Markdown link or image target, which markdown-it has already percent-encoded, so it holds no
// white space, control character or backslash.
function resolveUrl(url, directory) {
  if (NOT_RELATIVE.test(url)) {
    return url;
  }
  const cut = url.search(/[?#]/);
  const target = cut < 0 ? url : url.slice(0, cut);
  const rest = cut < 0 ? '' : url.slice(cut);
  // Resolve by the URL Standard's path rules, as a browser does: `%2e` segments are dots, and `..`
  // stops at the root. Each directory name is encoded so that a `#` or `?` in it stays part of
  // the path. A relative target keeps the base's origin, so only its path is kept.
  const folder = directory === '.' ? '' : directory.split('/').map(encodeName).join('/') + '/';
  return new URL(target, BASE_ORIGIN + '/' + folder).pathname + rest;
}

// Resolve relative references in Markdown links and images, in place. Returns whether any raw
// HTML holds a tag.
function resolveReferences(tokens, directory) {
  let raw = false;
  for (const token of tokens) {
    if (token.type === 'link_open' || token.type === 'image') {
      const attribute = token.type === 'link_open' ? 'href' : 'src';
      token.attrSet(attribute, resolveUrl(token.attrGet(attribute), directory));
    } else if (token.type === 'html_block' || token.type === 'html_inline') {
      raw = raw || (!onlyComments(token.content) && RAW_TAG.test(token.content));
    }
    if (token.children && resolveReferences(token.children, directory)) {
      raw = true;
    }
  }
  return raw;
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

// Raw HTML of only whole comments and white space, which renders nothing and holds no tag a
// browser reads. Text after a comment's end belongs to the piece and renders, so it does not count.
function onlyComments(content) {
  return /^[\t\n\f\r ]*$/.test(content.replace(COMMENT, ''));
}

// An HTML block that renders nothing.
function isComment(block) {
  return block !== undefined && block.open.type === 'html_block' && onlyComments(block.open.content);
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

// Last Updated from a top-level `-` list: the first paragraph line of each item. The list is
// the metadata header block only when it also carries every required field; a list that does
// not is ordinary content, even if one of its lines looks like the field.
function listField(block) {
  if (block === undefined || block.open.type !== 'bullet_list_open' || block.open.markup !== '-') {
    return null;
  }
  const lines = [];
  for (let i = 0; i < block.inner.length; i++) {
    const token = block.inner[i];
    // list_item_open (level 1), paragraph_open (level 2), inline (level 3).
    if (token.type === 'inline' && token.level === 3 && block.inner[i - 2].type === 'list_item_open') {
      lines.push(token.content.split('\n')[0]);
    }
  }
  if (!REQUIRED_FIELDS.every((name) => lines.some((line) => line.startsWith('**' + name + ':**')))) {
    return null;
  }
  for (const line of lines) {
    const m = LAST_UPDATED.exec(line);
    if (m) {
      return m[1];
    }
  }
  // A Last Updated item of another shape is still the block's field: return it as written, so
  // the check reports it instead of reading the block as having no field.
  for (const line of lines) {
    const m = LAST_UPDATED_ITEM.exec(line);
    if (m) {
      return m[1];
    }
  }
  return null;
}

// The length of the YAML front matter at the start of `text`, or 0. A leading thematic break
// followed by a later one looks the same, so the block counts only when it parses as a YAML
// mapping.
function frontMatterLength(text) {
  const m = FRONT_MATTER.exec(text);
  if (!m) {
    return 0;
  }
  const inner = m[0].replace(/^---[ \t]*\r?\n/, '').replace(/(?:---|\.\.\.)[ \t]*(?:\r?\n)?$/, '');
  try {
    const data = YAML.parse(inner);
    return data !== null && typeof data === 'object' && !Array.isArray(data) ? m[0].length : 0;
  } catch (error) {
    return 0;
  }
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
  const directory = path.posix.dirname(filePath);
  const raw = resolveReferences(tokens, directory);
  const html = md.renderer.render(tokens, md.options, {})
    .split('\n')
    .map((line) => line.replace(/[ \t]+$/, ''))
    .join('\n')
    .replace(/\n+$/, '') + (raw ? '\n<!-- raw HTML, read from ' + escapeHtml(directory) + ' -->' : '');
  const skip = frontMatterLength(text);
  const body = skip ? md.parse(text.slice(skip), {}) : tokens;
  return { html, ...metadata(body) };
}

const input = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
input.on('line', (line) => {
  const request = JSON.parse(line);
  process.stdout.write(JSON.stringify(describe(request.text, request.path)) + '\n');
});
