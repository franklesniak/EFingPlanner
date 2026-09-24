#!/usr/bin/env node
/**
 * Read Markdown as the page prints it, one source line at a time.
 *
 * tests/test_self_contained_references.py asks this program, rather than
 * rules of its own, what a Markdown page prints, because each hand-written
 * rule for that question was followed by the next case it missed. It reads
 * one JSON object per line on stdin, {"text": <a Markdown document>}, and
 * writes one JSON object per line on stdout:
 *
 *   lines     one entry per line of the document, as the text splits on
 *             "\n": [printed, hidden, destinations, unlinked, cuts]. printed
 *             is what the page shows from that line; hidden is the text of
 *             an HTML comment on it; destinations are the link targets
 *             written on it, for an inline link, an image and an HTML "a"
 *             tag, decoded as the page decodes them; unlinked holds [start,
 *             end] ranges of printed that link nothing of their own: a code
 *             span, a fenced or indented code block, an image's alternative
 *             text, a link's label and raw HTML text; and cuts holds each
 *             position in printed where markup ends one run of text and the
 *             next begins. GitHub finds a bare URL inside one run of text, so
 *             a URL stops at a cut.
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
 */

import { createInterface } from 'node:readline';
import MarkdownIt from 'markdown-it';

const md = new MarkdownIt('commonmark').enable(['table', 'strikethrough']);
// Keep an escape or a character reference as a token of its own, so its
// source spelling can be found on its line.
md.core.ruler.disable('text_join');

const LINE_BREAK_TAG = /^<br\b/i;
const A_TAG = /^<a\s/i;
const HREF = /\shref\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))/i;
const TAG = /<[^<>]*>/g;
const CHARACTER_REFERENCE = /&[a-z#][a-z0-9]{1,31};/gi;

class Unmapped extends Error {}

function readDocument(text) {
  const source = text.split('\n');
  const printed = new Array(source.length).fill(null);
  const hidden = new Array(source.length).fill('');
  const destinations = source.map(() => []);
  const unmapped = [];

  const unlinked = source.map(() => []);
  const cuts = source.map(() => []);
  const fences = [];
  const print = (line, characters) => {
    if (line < source.length) printed[line] = (printed[line] ?? '') + characters;
  };
  // A range counts code points, as Python indexes a string; a JavaScript
  // length counts UTF-16 units, and a character outside the Basic
  // Multilingual Plane is two of them.
  const printUnlinked = (line, characters) => {
    if (line >= source.length) return;
    const start = [...(printed[line] ?? '')].length;
    print(line, characters);
    unlinked[line].push([start, start + [...characters].length]);
  };
  const cut = (line) => {
    if (line < source.length) cuts[line].push([...(printed[line] ?? '')].length);
  };
  const cover = (from, to) => {
    for (let line = from; line < Math.min(to, source.length); line += 1) {
      if (printed[line] === null) printed[line] = '';
    }
  };
  const tagInto = (tag, line) => {
    if (LINE_BREAK_TAG.test(tag)) print(line, ' ');
    if (A_TAG.test(tag)) {
      const href = HREF.exec(tag);
      if (href) {
        const value = href[1] ?? href[2] ?? href[3];
        destinations[line].push(value.replace(CHARACTER_REFERENCE, (reference) => md.utils.unescapeAll(reference)));
      }
    }
  };

  // Raw HTML, a line at a time: comments are hidden, tags print nothing, and
  // the rest prints with its character references decoded.
  const htmlLines = (lines, first) => {
    let inComment = false;
    lines.forEach((raw, offset) => {
      const line = first + offset;
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
        const open = rest.indexOf('<!--', index);
        const upTo = open === -1 ? rest.length : open;
        shown += rest.slice(index, upTo);
        if (open === -1) break;
        const close = rest.indexOf('-->', open + 4);
        if (close === -1) {
          hidden[line] += rest.slice(open + 4);
          inComment = true;
          break;
        }
        hidden[line] += ' ' + rest.slice(open + 4, close) + ' ';
        index = close + 3;
      }
      for (const tag of shown.match(TAG) ?? []) tagInto(tag, line);
      printUnlinked(line, md.utils.unescapeAll(shown.replace(TAG, (tag) => (LINE_BREAK_TAG.test(tag) ? ' ' : ''))));
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
    // An image's alternative text is printed where the image fails, and it
    // is no link.
    let inImage = false;
    // A link's label is the link's text: a URL written there links to the
    // destination, not to itself.
    let inLink = false;
    // Whether the text printed last belongs to the run the next text joins.
    // An escape or a character reference is part of its run; any markup
    // ends the run.
    let joined = false;
    const printText = (line, characters) => {
      if (!joined) cut(line);
      joined = true;
      if (inImage || inLink) printUnlinked(line, characters);
      else print(line, characters);
    };
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
    // After a link's or an image's closing bracket: an inline destination is
    // a URL written on its own line; a reference label points elsewhere.
    const afterLabel = () => {
      if (content[cursor] === '(') {
        const start = skipBlank(cursor + 1);
        const target = md.helpers.parseLinkDestination(content, start, content.length);
        if (!target.ok) throw new Unmapped();
        if (target.str) destinations[lineAt(start)].push(target.str);
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
        if (child.type !== 'text' && child.type !== 'text_special') joined = false;
        switch (child.type) {
          case 'text': {
            if (!child.content) break;
            const at = find(child.content);
            if (inAutolink) {
              destinations[lineAt(at)].push(child.content);
              print(lineAt(at), ' ');
            } else {
              printText(lineAt(at), child.content);
            }
            cursor = at + child.content.length;
            break;
          }
          case 'text_special': {
            const at = find(child.markup);
            printText(lineAt(at), child.content);
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
              printUnlinked(lineAt(at), part);
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
              tagInto(child.content, lineAt(at));
            }
            cursor = at + child.content.length;
            break;
          }
          case 'link_open':
            inAutolink = child.markup === 'autolink';
            inLink = !inAutolink;
            cursor = find(inAutolink ? '<' : '[') + 1;
            break;
          case 'link_close':
            if (child.markup === 'autolink') {
              inAutolink = false;
              cursor = find('>') + 1;
            } else {
              inLink = false;
              cursor = find(']') + 1;
              afterLabel();
            }
            break;
          case 'image':
            cursor = find('![') + 2;
            // The alternative text is read, as the page shows it when the
            // image does not load: reading it can report more, never less.
            inImage = true;
            walk(child.children ?? []);
            inImage = false;
            joined = false;
            cursor = find(']') + 1;
            afterLabel();
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
        unlinked[line] = [];
        cuts[line] = [];
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
      parts.forEach((part, offset) => printUnlinked(from + 1 + offset, part));
      fences.push([token.info.trim().split(/\s+/)[0].toLowerCase(), from + 1, token.content]);
    } else if (token.type === 'code_block') {
      cover(from, to);
      token.content.replace(/\n$/, '').split('\n').forEach((part, offset) => printUnlinked(from + offset, part));
    } else if (token.type === 'html_block') {
      cover(from, to);
      htmlLines(token.content.replace(/\n$/, '').split('\n'), from);
    }
  }
  const lines = source.map((raw, line) => [printed[line] ?? raw, hidden[line], destinations[line], unlinked[line], cuts[line]]);
  return { lines, unmapped, fences };
}

const input = createInterface({ input: process.stdin, crlfDelay: Infinity });
input.on('line', (line) => {
  if (!line.trim()) return;
  const { text } = JSON.parse(line);
  process.stdout.write(JSON.stringify(readDocument(text)) + '\n');
});
