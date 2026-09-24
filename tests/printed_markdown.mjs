#!/usr/bin/env node
/**
 * Read Markdown as the page prints it, one source line at a time.
 *
 * tests/test_self_contained_references.py asks this program, rather than
 * rules of its own, what a Markdown page prints, because each hand-written
 * rule for that question was followed by the next case it missed. It reads
 * one JSON object per line on stdin, {"text": <a Markdown document>}, and
 * writes one JSON object per line on stdout. It also answers {"urls": [...]}
 * with {"hosts": [...]}: for each URL, [protocol, hostname, port] as the
 * WHATWG parser a browser uses reads it, or null when a browser refuses it.
 * For a document:
 *
 *   lines     one entry per line of the document, as the text splits on
 *             "\n": [printed, hidden, destinations, bare]. printed is what
 *             the page shows from that line; hidden is the text of an HTML
 *             comment on it; destinations are the targets of the links whose
 *             text is on it -- an inline link, over every line its label
 *             covers, and an HTML "a" tag, over every line up to its end tag
 *             -- decoded as the page decodes them; and bare holds each bare
 *             URL GitHub links on it, as written, before the prose around it
 *             is trimmed off.
 *   fences    [info, first, content] for each fenced code block: the first
 *             word of its info string, in lower case, the line its content
 *             starts on, and the content itself.
 *   unmapped  the first line of every inline run whose characters this
 *             program could not place on their lines. Such a run is given
 *             its source lines as they stand, which reads more, never less.
 *
 * The parser is markdown-it in CommonMark mode, with GitHub's tables and
 * strikethrough. Markup that forms markup prints nothing, and a marker
 * that forms none prints as itself. A character reference and a backslash
 * escape print their character, a code span its content, and a <br> tag a
 * space; any other tag prints nothing. A line no block covers, such as a
 * link reference definition, is given as it stands.
 *
 * GitHub finds a bare URL in a paragraph's source text, as its autolink
 * extension does, not in the printed text: it starts where the text is plain
 * -- not in code, a link's label, an image's alternative text or an
 * autolink -- after no letter or digit, and it runs over the characters
 * written there, markup and character references included, to the next space
 * or "<". In an HTML block GitHub links a bare URL in the text, with its
 * character references decoded, outside an "a", "code", "pre" or "kbd"
 * element. An image links nothing: GitHub wraps it in a link to the image
 * itself, through its image proxy for another host, not to a page. Each of
 * these was checked against GitHub's own renderer, through its Markdown API.
 */

import { createInterface } from 'node:readline';
import MarkdownIt from 'markdown-it';

const md = new MarkdownIt('commonmark').enable(['table', 'strikethrough']);
// Keep an escape or a character reference as a token of its own, so its
// source spelling can be found on its line.
md.core.ruler.disable('text_join');

const LINE_BREAK_TAG = /^<br\b/i;
const A_TAG = /^<a\s/i;
const A_END_TAG = /^<\/a\s*>/i;
const HREF = /\shref\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))/i;
const TAG = /<[^<>]*>/g;
const CHARACTER_REFERENCE = /&[a-z#][a-z0-9]{1,31};/gi;
// The elements of an HTML block whose text GitHub links no URL in.
const QUIET_START_TAG = /^<(a|code|pre|kbd)(?=[\s>\/])(?![^>]*\/>)/i;
const QUIET_END_TAG = /^<\/(a|code|pre|kbd)\s*>/i;
// A bare URL as the scan's own pattern starts one, running to the next space
// or "<" as GitHub's autolink extension runs one.
const BARE_URL = /(?<![\p{L}\p{N}+.\/@-])(?:https?:\/\/|www\.)[^\s<]*/giu;

class Unmapped extends Error {}

// Every bare URL in a line read as plain text, as written.
const bareIn = (line) => [...line.matchAll(BARE_URL)].map((match) => match[0]);

function readDocument(text) {
  const source = text.split('\n');
  const printed = new Array(source.length).fill(null);
  const hidden = new Array(source.length).fill('');
  const destinations = source.map(() => []);
  const bare = source.map(() => []);
  const plain = new Array(source.length).fill(false);
  const unmapped = [];

  const fences = [];
  const print = (line, characters) => {
    if (line < source.length) printed[line] = (printed[line] ?? '') + characters;
  };
  // A link covers its text: its destination is given to each line from the
  // first to the last, once.
  const link = (href, from, to) => {
    for (let line = from; line <= to && line < source.length; line += 1) {
      if (!destinations[line].includes(href)) destinations[line].push(href);
    }
  };
  const cover = (from, to) => {
    for (let line = from; line < Math.min(to, source.length); line += 1) {
      if (printed[line] === null) printed[line] = '';
    }
  };
  // Returns an "a" tag's destination, decoded as a browser decodes an
  // attribute: its character references, and nothing else.
  const tagInto = (tag, line) => {
    if (LINE_BREAK_TAG.test(tag)) print(line, ' ');
    if (!A_TAG.test(tag)) return null;
    const href = HREF.exec(tag);
    if (!href) return null;
    const value = (href[1] ?? href[2] ?? href[3]).replace(
      CHARACTER_REFERENCE,
      (reference) => md.utils.unescapeAll(reference),
    );
    link(value, line, line);
    return value;
  };

  // Raw HTML, a line at a time: comments are hidden, tags print nothing, and
  // the rest prints with its character references decoded. An "a" tag's
  // destination covers every line up to its end tag, and a bare URL in the
  // text outside a quiet element links.
  const htmlLines = (lines, first) => {
    let inComment = false;
    let open = null;
    let quiet = 0;
    lines.forEach((raw, offset) => {
      const line = first + offset;
      if (open !== null) link(open, line, line);
      let rest = raw;
      if (inComment) {
        const end = rest.indexOf('-->');
        if (end === -1) {
          hidden[line] += rest;
          return;
        }
        hidden[line] += rest.slice(0, end);
        rest = rest.slice(end + 3);
        inComment = false;
      }
      let shown = '';
      let index = 0;
      while (index < rest.length) {
        const start = rest.indexOf('<!--', index);
        const upTo = start === -1 ? rest.length : start;
        shown += rest.slice(index, upTo);
        if (start === -1) break;
        const close = rest.indexOf('-->', start + 4);
        if (close === -1) {
          hidden[line] += rest.slice(start + 4);
          inComment = true;
          break;
        }
        hidden[line] += ' ' + rest.slice(start + 4, close) + ' ';
        index = close + 3;
      }
      // The text between two tags, with its character references decoded:
      // a bare URL there links unless a quiet element holds it.
      const textInto = (segment) => {
        if (quiet > 0) return;
        const decoded = segment.replace(CHARACTER_REFERENCE, (reference) => md.utils.unescapeAll(reference));
        bare[line].push(...bareIn(decoded));
      };
      let last = 0;
      for (const match of shown.matchAll(TAG)) {
        textInto(shown.slice(last, match.index));
        const tag = match[0];
        const href = tagInto(tag, line);
        if (href !== null) open = href;
        else if (A_END_TAG.test(tag)) open = null;
        if (QUIET_START_TAG.test(tag)) quiet += 1;
        else if (QUIET_END_TAG.test(tag)) quiet = Math.max(0, quiet - 1);
        last = match.index + tag.length;
      }
      textInto(shown.slice(last));
      print(line, md.utils.unescapeAll(shown.replace(TAG, (tag) => (LINE_BREAK_TAG.test(tag) ? ' ' : ''))));
    });
  };

  const inlineRun = (token, first) => {
    const content = token.content;
    const breaks = [];
    for (let at = content.indexOf('\n'); at !== -1; at = content.indexOf('\n', at + 1)) breaks.push(at);
    const lineAt = (position) => {
      let count = 0;
      while (count < breaks.length && breaks[count] < position) count += 1;
      return first + count;
    };
    let cursor = 0;
    // Inside an autolink the printed text is the URL itself, which the page
    // shows as a link: it is a destination, and it prints as a space.
    let inAutolink = false;
    // An image's alternative text is printed where the image fails. It is
    // text: no bare URL starts in it.
    let inImage = false;
    // A link's label is the link's text: a URL written there links to the
    // destination, not to itself. The line its label starts on.
    let label = null;
    // An "a" tag this run has opened: its destination and its line.
    let anchor = null;
    // Where the last bare URL ended: no other starts inside it.
    let bareEnd = 0;
    const find = (needle) => {
      const at = content.indexOf(needle, cursor);
      if (at === -1) throw new Unmapped();
      return at;
    };
    const skipBlank = (position) => {
      let at = position;
      while (at < content.length && ' \t\n'.includes(content[at])) at += 1;
      return at;
    };
    // The bare URLs that start in plain text between from and to, each run
    // over the characters written after it.
    const findBare = (from, to) => {
      const pattern = new RegExp(BARE_URL.source, BARE_URL.flags);
      pattern.lastIndex = Math.max(from, bareEnd);
      for (let match = pattern.exec(content); match && match.index < to; match = pattern.exec(content)) {
        bare[lineAt(match.index)].push(match[0]);
        bareEnd = match.index + match[0].length;
      }
    };
    // After a link's or an image's closing bracket: an inline destination is
    // a URL written in the source; a reference label points elsewhere. A
    // link's destination covers every line from its label's first.
    const afterLabel = (from) => {
      if (content[cursor] === '(') {
        const start = skipBlank(cursor + 1);
        const target = md.helpers.parseLinkDestination(content, start, content.length);
        if (!target.ok) throw new Unmapped();
        if (target.str && from !== null) link(target.str, from, lineAt(start));
        let at = skipBlank(target.pos);
        if (at < content.length && content[at] !== ')') {
          const title = md.helpers.parseLinkTitle(content, at, content.length);
          if (!title.ok) throw new Unmapped();
          at = skipBlank(title.pos);
        }
        if (content[at] !== ')') throw new Unmapped();
        cursor = at + 1;
      } else if (content[cursor] === '[') {
        cursor = find(']') + 1;
      }
    };
    const walk = (children) => {
      for (const child of children) {
        switch (child.type) {
          case 'text': {
            if (!child.content) break;
            const at = find(child.content);
            if (inAutolink) {
              destinations[lineAt(at)].push(child.content);
              print(lineAt(at), ' ');
            } else {
              print(lineAt(at), child.content);
              if (!inImage && label === null) findBare(at, at + child.content.length);
              if (anchor !== null) link(anchor.href, anchor.line, lineAt(at));
            }
            cursor = at + child.content.length;
            break;
          }
          case 'text_special': {
            const at = find(child.markup);
            print(lineAt(at), child.content);
            cursor = at + child.markup.length;
            break;
          }
          case 'softbreak':
          case 'hardbreak':
            cursor = find('\n') + 1;
            break;
          case 'code_inline': {
            const open = find(child.markup);
            let close = content.indexOf(child.markup, open + child.markup.length);
            while (close !== -1 && (content[close - 1] === '`' || content[close + child.markup.length] === '`')) {
              let end = close;
              while (content[end] === '`') end += 1;
              close = content.indexOf(child.markup, end);
            }
            if (close === -1) throw new Unmapped();
            let at = open + child.markup.length;
            for (const part of content.slice(at, close).split('\n')) {
              print(lineAt(at), part);
              at += part.length + 1;
            }
            cursor = close + child.markup.length;
            break;
          }
          case 'html_inline': {
            const at = find(child.content);
            if (child.content.startsWith('<!--')) {
              let position = at + 4;
              const inner = child.content.replace(/^<!--/, '').replace(/-->$/, '');
              for (const part of inner.split('\n')) {
                hidden[lineAt(position)] += ' ' + part + ' ';
                position += part.length + 1;
              }
            } else {
              const href = tagInto(child.content, lineAt(at));
              if (href !== null) anchor = { href, line: lineAt(at) };
              else if (A_END_TAG.test(child.content)) {
                if (anchor !== null) link(anchor.href, anchor.line, lineAt(at));
                anchor = null;
              }
            }
            cursor = at + child.content.length;
            break;
          }
          case 'link_open':
            inAutolink = child.markup === 'autolink';
            cursor = find(inAutolink ? '<' : '[') + 1;
            if (!inAutolink) label = lineAt(cursor - 1);
            break;
          case 'link_close':
            if (child.markup === 'autolink') {
              inAutolink = false;
              cursor = find('>') + 1;
            } else {
              const from = label;
              label = null;
              cursor = find(']') + 1;
              afterLabel(from);
            }
            break;
          case 'image':
            cursor = find('![') + 2;
            // The alternative text is read, as the page shows it when the
            // image does not load: reading it can report more, never less.
            inImage = true;
            walk(child.children ?? []);
            inImage = false;
            cursor = find(']') + 1;
            afterLabel(null);
            break;
          default:
            if (child.markup) cursor = find(child.markup) + child.markup.length;
        }
      }
    };
    try {
      walk(token.children ?? []);
    } catch (error) {
      if (!(error instanceof Unmapped)) throw error;
      unmapped.push(first + 1);
      for (let line = first; line <= first + breaks.length && line < source.length; line += 1) {
        printed[line] = source[line];
        destinations[line] = [];
        bare[line] = [];
        plain[line] = true;
      }
    }
  };

  // A table cell's inline run has no line map of its own, so it takes its
  // row's, and a cell after the first is set apart as the page sets it apart.
  let row = null;
  let cellsInRow = 0;
  for (const token of md.parse(text, {})) {
    if (token.type === 'tr_open') {
      row = token.map[0];
      cellsInRow = 0;
      continue;
    }
    if (token.type === 'th_open' || token.type === 'td_open') {
      if (cellsInRow > 0) print(row, ' | ');
      cellsInRow += 1;
      continue;
    }
    if (token.type === 'inline' && !token.map && row !== null) {
      inlineRun(token, row);
      continue;
    }
    if (!token.map) continue;
    const [from, to] = token.map;
    if (token.type === 'table_open' || token.type === 'heading_open') {
      // The delimiter row and a setext underline print nothing.
      cover(from, to);
    } else if (token.type === 'inline') {
      cover(from, to);
      inlineRun(token, from);
    } else if (token.type === 'fence') {
      cover(from, to);
      const parts = token.content.replace(/\n$/, '').split('\n');
      parts.forEach((part, offset) => print(from + 1 + offset, part));
      fences.push([token.info.trim().split(/\s+/)[0].toLowerCase(), from + 1, token.content]);
    } else if (token.type === 'code_block') {
      cover(from, to);
      token.content.replace(/\n$/, '').split('\n').forEach((part, offset) => print(from + offset, part));
    } else if (token.type === 'html_block') {
      cover(from, to);
      htmlLines(token.content.replace(/\n$/, '').split('\n'), from);
    }
  }
  // A line given as it stands is read as plain text, bare URLs and all.
  const lines = source.map((raw, line) => {
    if (printed[line] === null || plain[line]) return [raw, hidden[line], destinations[line], bareIn(raw)];
    return [printed[line], hidden[line], destinations[line], bare[line]];
  });
  return { lines, unmapped, fences };
}

// A URL as the WHATWG parser a browser uses reads it: its scheme, its host
// and its port, or null when a browser refuses it.
const hostOf = (url) => {
  try {
    const parsed = new URL(url);
    return [parsed.protocol, parsed.hostname, parsed.port];
  } catch {
    return null;
  }
};

const input = createInterface({ input: process.stdin, crlfDelay: Infinity });
input.on('line', (line) => {
  if (!line.trim()) return;
  const request = JSON.parse(line);
  const answer = 'urls' in request ? { hosts: request.urls.map(hostOf) } : readDocument(request.text);
  process.stdout.write(JSON.stringify(answer) + '\n');
});
