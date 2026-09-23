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
 *                Raw HTML URL attributes are decoded by the HTML spec's
 *                attribute-value rules and written in one form (lowercase name,
 *                double-quoted value). A raw HTML tag the helper cannot fully
 *                resolve (a `base`, `meta`, `script` or `style` element, or an
 *                attribute that is neither a URL attribute nor one that never
 *                holds a URL, such as `style` or `srcdoc`) is tied to the
 *                directory of `path`, so a move changes its html. HTML comments
 *                and text are left as they are.
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
const { decodeHTMLAttribute } = require('entities');

const md = new MarkdownIt('commonmark');
const LAST_UPDATED = /^\*\*Last Updated:\*\* (\d{4}-\d{2}-\d{2})[ \t]*$/;
const LAST_UPDATED_ITEM = /^\*\*Last Updated:\*\*[ \t]*(.*?)[ \t]*$/;
const VERSION = /^\*\*Version:\*\* (\d+\.\d+\.\d{8}\.\d+)[ \t]*$/;
const FRONT_MATTER = /^---[ \t]*\r?\n(?:[^]*?\r?\n)?(?:---|\.\.\.)[ \t]*(?:\r?\n|$)/;
const H1_LINE_LIMIT = 30;
// The metadata header block's required fields beside Last Updated (the docs guide's Tier 1 list).
const REQUIRED_FIELDS = ['Status', 'Owner', 'Scope'];
// HTML attributes whose values hold URLs (HTML Living Standard, attributes index), plus the
// obsolete `background` and `longdesc`, which browsers still honor, and SVG's `xlink:href`.
// `itemtype` is left out: its URLs must be absolute.
const URL_ATTRIBUTES = new Set([
  'action', 'background', 'cite', 'data', 'formaction', 'href', 'imagesrcset', 'itemid', 'longdesc', 'ping', 'poster',
  'src', 'srcset', 'xlink:href',
]);
// Attributes whose values never hold a URL. Any other attribute, such as `style`, `srcdoc`,
// `content` or an event handler, may hold one the helper does not parse, so it ties the tag to
// the document's directory (see canonicalTag).
const PLAIN_ATTRIBUTES = new Set([
  'abbr', 'align', 'alt', 'as', 'async', 'autoplay', 'border', 'cellpadding', 'cellspacing', 'charset', 'checked',
  'class', 'color', 'cols', 'colspan', 'controls', 'coords', 'crossorigin', 'datetime', 'decoding', 'default', 'defer',
  'dir', 'disabled', 'download', 'fetchpriority', 'headers', 'height', 'hidden', 'hreflang', 'id', 'imagesizes',
  'integrity', 'itemprop', 'itemscope', 'itemtype', 'kind', 'label', 'lang', 'loading', 'loop', 'media', 'muted', 'name',
  'nowrap', 'open', 'playsinline', 'preload', 'referrerpolicy', 'rel', 'reversed', 'role', 'rows', 'rowspan', 'scope',
  'sizes', 'span', 'srclang', 'start', 'summary', 'tabindex', 'target', 'title', 'type', 'usemap', 'valign', 'value',
  'width',
]);
const PLAIN_ATTRIBUTE_PREFIX = /^(?:aria|data)-/;
// Elements whose content or effect can hold URLs the helper does not parse: CSS, scripts, a
// `<base>` that changes how every relative URL resolves, and a `<meta>` refresh.
const DIRECTORY_BOUND_ELEMENTS = new Set(['base', 'meta', 'script', 'style']);
// A URL with a scheme, a root-relative or protocol-relative path, or only a query or fragment
// does not depend on the document's directory.
const NOT_RELATIVE = /^(?:[A-Za-z][A-Za-z0-9+.-]*:|\/|#|\?|$)/;
// The base every relative reference resolves against; the host only makes it a full URL.
const BASE_ORIGIN = 'https://repository.invalid';
// Raw HTML pieces: a comment, or a start tag whose quoted values may hold `>`.
const COMMENT_OR_TAG = /<!--[^]*?-->|<[A-Za-z][A-Za-z0-9-]*(?:[^>"']|"[^"]*"|'[^']*')*>/g;
// A whole HTML comment, including the empty forms `<!-->` and `<!--->` (CommonMark 0.31.2).
const COMMENT = /<!--(?:-?>|[^]*?-->)/g;
// One attribute inside a start tag, from the current position (CommonMark 0.31.2, raw HTML).
// White space here, as everywhere below, is ASCII whitespace, which is what HTML and URL
// parsing use; JavaScript's `\s` and `trim()` also take in U+00A0 and other Unicode spaces.
const ATTRIBUTE = /([\t\n\f\r ]+)([A-Za-z_:][A-Za-z0-9_.:-]*)(?:([\t\n\f\r ]*=[\t\n\f\r ]*)("[^"]*"|'[^']*'|[^\t\n\f\r "'=<>`]+))?/y;

function resolveUrl(url, directory) {
  // The URL Standard strips leading and trailing C0 controls and spaces before it looks for
  // a scheme; it also removes ASCII tabs and newlines inside, which the parse below does.
  const trimmed = url.replace(/^[\u0000-\u0020]+|[\u0000-\u0020]+$/g, '');
  if (NOT_RELATIVE.test(trimmed)) {
    return url;
  }
  const cut = trimmed.search(/[?#]/);
  const target = cut < 0 ? trimmed : trimmed.slice(0, cut);
  const rest = cut < 0 ? '' : trimmed.slice(cut);
  // Resolve by the URL Standard's path rules, as a browser does: `%2e` segments are dots, `\`
  // is `/`, and `..` stops at the root. Each directory name is encoded so that a `#` or `?` in
  // it stays part of the path. A target the parser reads as absolute, such as `\\host\x` or a
  // scheme split by a newline, keeps its whole URL, so a change of host is still a change.
  const folder = directory === '.' ? '' : directory.split('/').map(encodeURIComponent).join('/') + '/';
  try {
    const resolved = new URL(target, BASE_ORIGIN + '/' + folder);
    return (resolved.origin === BASE_ORIGIN ? resolved.pathname : resolved.href) + rest;
  } catch (error) {
    return '/' + folder + target + rest;   // unreadable as a URL: tie it to the directory
  }
}

// A srcset value is a list of image candidates, split as the HTML Living Standard's "parse a
// srcset attribute" does: a URL runs to the next whitespace, so a data URL keeps its comma;
// commas at the URL's end close the candidate; otherwise descriptors run to the next comma
// outside parentheses.
function resolveSrcset(value, directory) {
  const candidates = [];
  let at = 0;
  while (at < value.length) {
    at += /^[\t\n\f\r ,]*/.exec(value.slice(at))[0].length;
    if (at >= value.length) {
      break;
    }
    let url = /^[^\t\n\f\r ]*/.exec(value.slice(at))[0];
    at += url.length;
    let descriptors = '';
    const commas = /,+$/.exec(url);
    if (commas) {
      url = url.slice(0, url.length - commas[0].length);
    } else {
      const start = at;
      let inParentheses = false;
      while (at < value.length && !(value[at] === ',' && !inParentheses)) {
        if (value[at] === '(') {
          inParentheses = true;
        } else if (value[at] === ')') {
          inParentheses = false;
        }
        at++;
      }
      descriptors = value.slice(start, at).replace(/^[\t\n\f\r ]+|[\t\n\f\r ]+$/g, '');
      at++;
    }
    candidates.push(resolveUrl(url, directory) + (descriptors ? ' ' + descriptors : ''));
  }
  return candidates.join(', ');
}

function resolveAttribute(name, value, directory) {
  if (name === 'srcset' || name === 'imagesrcset') {
    return resolveSrcset(value, directory);
  }
  if (name === 'ping') {
    // A set of URLs separated by ASCII whitespace.
    return value.split(/[\t\n\f\r ]+/).filter((url) => url !== '').map((url) => resolveUrl(url, directory)).join(' ');
  }
  return resolveUrl(value, directory);
}

// A start tag with each URL attribute resolved and written as name="value". Values are decoded
// by the HTML spec's attribute-value rules first, as a browser decodes them. A tag the helper
// cannot fully resolve (a directory-bound element, an attribute outside both lists, or text it
// cannot read as attributes) is tied to the document's directory, so moving the file changes it.
function canonicalTag(tag, directory) {
  const name = /^<[A-Za-z][A-Za-z0-9-]*/.exec(tag)[0];
  let bound = DIRECTORY_BOUND_ELEMENTS.has(name.slice(1).toLowerCase());
  let out = name;
  let at = name.length;
  ATTRIBUTE.lastIndex = at;
  let m;
  while ((m = ATTRIBUTE.exec(tag)) !== null) {
    const attribute = m[2].toLowerCase();
    if (m[4] !== undefined && URL_ATTRIBUTES.has(attribute)) {
      const quoted = m[4][0] === '"' || m[4][0] === "'";
      const value = decodeHTMLAttribute(quoted ? m[4].slice(1, -1) : m[4]);
      out += ' ' + attribute + '="' + resolveAttribute(attribute, value, directory).replace(/"/g, '&quot;') + '"';
    } else {
      bound = bound || !(URL_ATTRIBUTES.has(attribute) || PLAIN_ATTRIBUTES.has(attribute) ||
        PLAIN_ATTRIBUTE_PREFIX.test(attribute));
      out += m[0];
    }
    at = ATTRIBUTE.lastIndex;
  }
  const rest = tag.slice(at);
  bound = bound || !/^[\t\n\f\r ]*\/?>$/.test(rest);
  return out + (bound ? ' data-directory="' + directory + '"' : '') + rest;
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

// An HTML block that renders nothing: only whole comments and white space. Text after a
// comment's `-->` on the same line belongs to the block and renders, so it does not count.
function isComment(block) {
  return block !== undefined && block.open.type === 'html_block' &&
    /^[\t\n\f\r ]*$/.test(block.open.content.replace(COMMENT, ''));
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
  resolveReferences(tokens, path.posix.dirname(filePath));
  const html = md.renderer.render(tokens, md.options, {})
    .split('\n')
    .map((line) => line.replace(/[ \t]+$/, ''))
    .join('\n')
    .replace(/\n+$/, '');
  const skip = frontMatterLength(text);
  const body = skip ? md.parse(text.slice(skip), {}) : tokens;
  return { html, ...metadata(body) };
}

const input = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
input.on('line', (line) => {
  const request = JSON.parse(line);
  process.stdout.write(JSON.stringify(describe(request.text, request.path)) + '\n');
});
