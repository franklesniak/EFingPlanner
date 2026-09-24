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
 *             "\n": [printed, hidden, destinations, bare, written]. printed is what
 *             the page shows from that line; hidden is the text of an HTML
 *             comment on it; destinations are the targets of the links whose
 *             content is on it -- an inline link or an HTML "a" tag, on each
 *             line where the link's text, code or image stands, and on no
 *             line when the link shows nothing -- decoded as the page decodes
 *             them; bare holds each bare URL GitHub links on it, as
 *             written, before the prose around it is trimmed off; and
 *             written holds, once for each time it is written there, the
 *             source spelling of each destination that links and is written
 *             on the line -- a Markdown link's, an autolink's or an "a" tag's
 *             "href" -- so a caller can tell a linked copy of a URL from an
 *             unlinked copy of the same URL on one line.
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
 *
 * Raw HTML is read as a browser reads it, because the page is what a browser
 * builds from it. A tag ends at the first ">" outside a quoted attribute
 * value, and may run over lines. A comment ends at the first "-->" or "--!>",
 * and "<!-->" and "<!--->" are empty comments, so text after any of these
 * prints, in a paragraph as in an HTML block. An "a" tag that ends "/>" is an
 * empty link, and an "a" start tag closes an open one. A character reference
 * in raw HTML is decoded as GitHub's renderer decodes it there: a name only
 * with its ";", and a number with or without one.
 *
 * GitHub filters nine tags before a browser sees them (GFM's tagfilter):
 * "title", "textarea", "style", "xmp", "iframe", "noembed", "noframes",
 * "script" and "plaintext" have their "<" written as "&lt;". So none of them
 * opens an element on the page: the tag prints as text, and what it holds is
 * ordinary HTML, printed, with its URLs linked. In an HTML block GitHub finds a
 * bare URL in each text node of the parsed page, so a URL runs on through a
 * filtered tag, through a "<" written as "&lt;", and through an end tag that
 * closes nothing, and stops at white space. In a paragraph a URL stops at "<",
 * and a bare URL inside a raw "a" tag is linked on its own: the page closes the
 * open link where the new one starts. Measured through GitHub's Markdown API.
 * https://github.github.com/gfm/#disallowed-raw-html-extension-
 *
 * Where markdown-it and GitHub's renderer part, the reader follows GitHub, as
 * the repository's hooks do. GitHub reads a declaration by an older CommonMark
 * grammar: an HTML block needs a capital letter after "<!", and inline raw HTML
 * needs capital letters and then white space. So "<!doctype html>" is text on
 * GitHub, and markdown-it 15.0.2 reads it as raw HTML.
 */

import { createInterface } from 'node:readline';
import MarkdownIt from 'markdown-it';

const md = new MarkdownIt('commonmark').enable(['table', 'strikethrough']);
// Keep an escape or a character reference as a token of its own, so its
// source spelling can be found on its line.
md.core.ruler.disable('text_join');

// A declaration as GitHub's renderer reads one, measured through its Markdown
// API: an HTML block needs a capital letter after "<!", and inline raw HTML
// needs capital letters and then white space. markdown-it 15.0.2 takes any
// letter, as CommonMark 0.31.2 says, for both.
const DECLARATION_START = /<![A-Za-z]/y;
const GITHUB_BLOCK_DECLARATION = /<![A-Z]/y;
const GITHUB_INLINE_DECLARATION = /<![A-Z]+[\t\n\f\r ]/y;
const startsAt = (pattern, text, position) => {
  pattern.lastIndex = position;
  return pattern.test(text);
};
// Refuses one of markdown-it's own rules where GitHub reads the text another
// way, and runs it everywhere else. The ruler's rule list is read for the rule
// to wrap: markdown-it 15 exports no rule on its own.
const refuseWhere = (ruler, name, refused) => {
  const rule = ruler.__rules__.find((candidate) => candidate.name === name);
  const read = rule.fn;
  ruler.at(name, (state, ...rest) => (refused(state, ...rest) ? false : read(state, ...rest)), { alt: rule.alt });
};
refuseWhere(md.block.ruler, 'html_block', (state, startLine) => {
  const start = state.bMarks[startLine] + state.tShift[startLine];
  return startsAt(DECLARATION_START, state.src, start) && !startsAt(GITHUB_BLOCK_DECLARATION, state.src, start);
});
refuseWhere(md.inline.ruler, 'html_inline', (state) =>
  startsAt(DECLARATION_START, state.src, state.pos) && !startsAt(GITHUB_INLINE_DECLARATION, state.src, state.pos));

// A character reference as GitHub's renderer reads one in raw HTML, measured
// through its Markdown API: a name only with its ";", so "&copy 2026" and
// "&copyright;" stay as written, and a number with or without one, so "&#x41"
// is "A" as "&#x41;" is. That is neither the HTML Standard's rule, which
// decodes a legacy name such as "&copy" without its ";", nor markdown-it's,
// which wants every ";".
const REFERENCE = /&(?:#[0-9]+;?|#[xX][0-9A-Fa-f]+;?|[A-Za-z][A-Za-z0-9]*;)/g;
// The elements of HTML text GitHub links no URL in.
const QUIET_ELEMENTS = new Set(['a', 'code', 'pre', 'kbd']);
// The tags GFM's tagfilter writes as text, "<" as "&lt;".
const FILTERED_TAGS = new Set(['title', 'textarea', 'style', 'xmp', 'iframe', 'noembed', 'noframes', 'script', 'plaintext']);
// The elements that hold nothing, so a start tag opens none.
const VOID_ELEMENTS = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']);
// A bare URL in a text node of an HTML block: it runs to white space, since a
// "<" there is a character of the text.
const BARE_URL_IN_TEXT = /(?<![\p{L}\p{N}+.\/@-])(?:https?:\/\/|www\.)\S*/giu;
// A bare URL as the scan's own pattern starts one, running to the next space
// or "<" as GitHub's autolink extension runs one.
const BARE_URL = /(?<![\p{L}\p{N}+.\/@-])(?:https?:\/\/|www\.)[^\s<]*/giu;
// A character a reader sees. A link that holds none, only white space or an
// invisible format character, shows the reader nothing to follow.
const VISIBLE = /[^\s\p{Cf}]/u;
// The white space the HTML tokenizer skips inside a tag.
const TAG_SPACE = /[\t\n\f\r ]/;
// The characters that end a tag name, an attribute name and an unquoted value.
const TAG_NAME_END = /[\t\n\f\r />]/;
const ATTRIBUTE_NAME_END = /[\t\n\f\r />=]/;
const UNQUOTED_VALUE_END = /[\t\n\f\r >]/;
// Where the page ends a comment: the first "-->", or the "--!>" the HTML
// tokenizer also accepts.
const COMMENT_CLOSER = /--!?>/g;

class Unmapped extends Error {}

// GitHub writes "[" and "]" in a Markdown link's destination, and in an
// autolink's, as "%5B" and "%5D", measured through its Markdown API. So a URL
// whose host is an IPv6 address in brackets is no URL a browser opens there,
// and GitHub links no bare URL with such a host at all, in a paragraph or an
// HTML block. Only a raw HTML "href" keeps the brackets.
const githubHref = (url) => url.replace(/\[/g, '%5B').replace(/\]/g, '%5D');
const BRACKETED_HOST = /^(?:https?:\/\/)\[/i;
const linksBare = (url) => !BRACKETED_HOST.test(url);

// Every bare URL GitHub links in a line read as plain text, as written.
const bareIn = (line, pattern = BARE_URL) => [...line.matchAll(pattern)].map((match) => match[0]).filter(linksBare);

// Raw HTML text, or an attribute value, with its character references decoded
// as GitHub's renderer decodes them, and nothing else: a backslash is a
// character here, and GitHub prints it.
const decodeHtml = (text) =>
  text.replace(REFERENCE, (reference) => md.utils.unescapeAll(reference.endsWith(';') ? reference : reference + ';'));

// The tag that starts at text[start], read as the HTML tokenizer reads one:
// its name in lower case, whether it is an end tag, whether it ends "/>", its
// attributes (the first of each name), and the index after its ">". A ">" in
// a quoted value belongs to the value, and a tag may run over lines. Returns
// null when no tag starts there, or when the text ends inside one.
// https://html.spec.whatwg.org/multipage/parsing.html#tag-open-state
const readTag = (text, start) => {
  let at = start + 1;
  const closing = text[at] === '/';
  if (closing) at += 1;
  if (!/[A-Za-z]/.test(text[at] ?? '')) return null;
  const nameStart = at;
  while (at < text.length && !TAG_NAME_END.test(text[at])) at += 1;
  const tag = {
    name: text.slice(nameStart, at).toLowerCase(),
    closing,
    selfClosing: false,
    attributes: new Map(),
    valuesAt: new Map(),
    end: -1,
  };
  for (;;) {
    while (at < text.length && TAG_SPACE.test(text[at])) at += 1;
    if (at >= text.length) return null;
    if (text[at] === '>') {
      tag.end = at + 1;
      return tag;
    }
    if (text[at] === '/') {
      at += 1;
      if (text[at] === '>') {
        tag.selfClosing = true;
        tag.end = at + 1;
        return tag;
      }
      continue;
    }
    // An attribute name runs to white space, "/", ">" or "=", and its first
    // character may be any of the others, "=" included.
    const nameAt = at;
    at += 1;
    while (at < text.length && !ATTRIBUTE_NAME_END.test(text[at])) at += 1;
    const name = text.slice(nameAt, at).toLowerCase();
    while (at < text.length && TAG_SPACE.test(text[at])) at += 1;
    let value = '';
    let valueAt = at;
    if (text[at] === '=') {
      at += 1;
      while (at < text.length && TAG_SPACE.test(text[at])) at += 1;
      valueAt = at;
      if (text[at] === '"' || text[at] === "'") {
        valueAt = at + 1;
        const close = text.indexOf(text[at], at + 1);
        if (close === -1) return null;
        value = text.slice(at + 1, close);
        at = close + 1;
      } else {
        while (at < text.length && !UNQUOTED_VALUE_END.test(text[at])) at += 1;
        value = text.slice(valueAt, at);
      }
    }
    if (!tag.attributes.has(name)) {
      tag.attributes.set(name, value);
      tag.valuesAt.set(name, valueAt);
    }
  }
};

// An "a" start tag's destination, decoded as GitHub decodes raw HTML in a
// file (decodeHtml), or null for a tag that opens no link: an end tag, one
// with no href, or one that ends "/>", which GitHub renders as an empty link.
const destinationOf = (tag) => {
  if (tag.name !== 'a' || tag.closing || tag.selfClosing) return null;
  const href = tag.attributes.get('href');
  return href === undefined ? null : decodeHtml(href);
};

// The comment that opens at text[start], as the page reads it: where its text
// ends and where the comment ends. "<!-->" and "<!--->" are empty, and any
// other runs to the first "-->" or "--!>". Null when it runs to the end.
// https://html.spec.whatwg.org/multipage/parsing.html#comment-start-state
const commentEnd = (text, start) => {
  if (text.startsWith('<!-->', start)) return [start + 4, start + 5];
  if (text.startsWith('<!--->', start)) return [start + 4, start + 6];
  COMMENT_CLOSER.lastIndex = start + 4;
  const closer = COMMENT_CLOSER.exec(text);
  return closer === null ? null : [closer.index, closer.index + closer[0].length];
};

function readDocument(text) {
  const source = text.split('\n');
  const printed = new Array(source.length).fill(null);
  const hidden = new Array(source.length).fill('');
  const destinations = source.map(() => []);
  const bare = source.map(() => []);
  const written = source.map(() => []);
  // The source spelling of a destination that links, on the line it is
  // written on, once for each time it is written there.
  const spell = (line, spelling) => {
    if (line < source.length) written[line].push(spelling);
  };
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
  // A run of raw HTML, read as a browser reads it, one tag, comment or run of
  // text at a time. lineOf gives the source line of a position in the run.
  // A comment is hidden, a tag prints nothing but a <br>'s space, and text
  // prints with its character references decoded. A bare URL in the text
  // links outside a quiet element. An "a" tag's destination is given to each
  // line where its content stands, text a reader sees or an image, and
  // shown(line) is told of every such line, for a link the run sits inside.
  const readHtml = (text, lineOf, shown = () => {}) => {
    // The open "a" tag: its destination, where its href is written, and
    // whether its content has been seen, which is when its href links.
    let anchor = null;
    // The elements open on the page, innermost last. An end tag that closes
    // none of them is dropped by the page's parser, so it ends no text node.
    const open = [];
    const content = (line) => {
      if (anchor !== null) {
        link(anchor.href, line, line);
        if (!anchor.spelled) {
          spell(anchor.line, anchor.written);
          anchor.spelled = true;
        }
      }
      shown(line);
    };
    const hide = (from, to) => {
      let at = from;
      for (const part of text.slice(from, to).split('\n')) {
        hidden[lineOf(at)] += ' ' + part + ' ';
        at += part.length + 1;
      }
    };
    // The text of the current text node on its current line, not yet read
    // for bare URLs, and whether a quiet element holds it.
    // A "<" or ">" in such a URL is text, and GitHub writes it as "&lt;" or
    // "&gt;", so it is given back that way: the scan's trimming reads a bare
    // "<" as the end of an autolink.
    let node = null;
    const endNode = () => {
      if (node !== null && !node.quiet) {
        for (const url of bareIn(node.text, BARE_URL_IN_TEXT)) {
          bare[node.line].push(url.replace(/</g, '&lt;').replace(/>/g, '&gt;'));
        }
      }
      node = null;
    };
    const quiet = () => open.some((name) => QUIET_ELEMENTS.has(name));
    const textBetween = (from, to) => {
      let at = from;
      text.slice(from, to).split('\n').forEach((part, index) => {
        const line = lineOf(at);
        const decoded = decodeHtml(part);
        print(line, decoded);
        if (index > 0 || (node !== null && node.line !== line)) endNode();
        if (node === null) node = { line, text: '', quiet: quiet() };
        node.text += decoded;
        if (VISIBLE.test(decoded)) content(line);
        at += part.length + 1;
      });
    };
    const closeTo = (name) => {
      const index = open.lastIndexOf(name);
      if (index === -1) return false;
      open.length = index;
      return true;
    };
    let from = 0;
    for (let at = text.indexOf('<'); at !== -1; at = text.indexOf('<', at + 1)) {
      if (at < from) continue;
      let end = -1;
      if (text.startsWith('<!--', at)) {
        const [textEnd, commentStop] = commentEnd(text, at) ?? [text.length, text.length];
        textBetween(from, at);
        endNode();
        hide(at + 4, textEnd);
        end = commentStop;
      } else if (text.startsWith('</>', at)) {
        textBetween(from, at);
        end = at + 3;
      } else if (/^<(?:[!?]|\/[^A-Za-z])/.test(text.slice(at, at + 3))) {
        // A declaration, a processing instruction or a malformed end tag is a
        // comment to the browser, running to the next ">".
        const close = text.indexOf('>', at);
        textBetween(from, at);
        endNode();
        hide(at + 2, close === -1 ? text.length : close);
        end = close === -1 ? text.length : close + 1;
      } else {
        const tag = readTag(text, at);
        if (tag !== null && !FILTERED_TAGS.has(tag.name)) {
          textBetween(from, at);
          const line = lineOf(at);
          if (tag.closing) {
            // An end tag that closes nothing is dropped, and the text on
            // either side of it is one text node.
            if (closeTo(tag.name)) endNode();
            if (tag.name === 'a') anchor = null;
            if (tag.name === 'br') {
              endNode();
              print(line, ' ');
            }
          } else {
            endNode();
            if (tag.name === 'br') print(line, ' ');
            if (tag.name === 'a') {
              // An "a" start tag closes an open one.
              closeTo('a');
              const href = destinationOf(tag);
              anchor = href === null ? null : {
                href,
                written: tag.attributes.get('href'),
                line: lineOf(at + tag.valuesAt.get('href')),
                spelled: false,
              };
            }
            if (!tag.selfClosing && !VOID_ELEMENTS.has(tag.name)) open.push(tag.name);
            if (tag.name === 'img') content(line);
          }
          end = tag.end;
        }
      }
      if (end !== -1) from = end;
    }
    textBetween(from, text.length);
    endNode();
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
    // destination, not to itself. The first and last lines where the label
    // shows something, which are all the lines its destination is given to;
    // both stay null for a label that shows nothing.
    let label = null;
    // The "a" tag this run has opened: its destination, where its href is
    // written, and whether its content has been seen.
    let anchor = null;
    // Content a reader sees stands on these lines: the open "a" tag's
    // destination is given to them, and the open label covers them.
    const standsOn = (from, to) => {
      if (anchor !== null) {
        link(anchor.href, from, to);
        if (!anchor.spelled) {
          spell(anchor.line, anchor.written);
          anchor.spelled = true;
        }
      }
      if (label !== null) {
        label.first = label.first === null ? from : Math.min(label.first, from);
        label.last = label.last === null ? to : Math.max(label.last, to);
      }
    };
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
    // over the characters written after it. GitHub links one inside an open
    // "a" tag on its own, and the page's parser then closes the open link
    // where the new one starts: the text before the URL is the open link's,
    // and the text after it is no link's. Returns where the first URL starts,
    // or to when there is none.
    const findBare = (from, to) => {
      const pattern = new RegExp(BARE_URL.source, BARE_URL.flags);
      pattern.lastIndex = Math.max(from, bareEnd);
      let first = to;
      for (let match = pattern.exec(content); match && match.index < to; match = pattern.exec(content)) {
        if (linksBare(match[0])) {
          bare[lineAt(match.index)].push(match[0]);
          if (first === to) first = match.index;
        }
        bareEnd = match.index + match[0].length;
      }
      return first;
    };
    // After a link's or an image's closing bracket: an inline destination is
    // a URL written in the source; a reference label points elsewhere. A
    // link's destination covers the lines where its label shows something,
    // and no line when it shows nothing: GitHub renders "[](url)" as an
    // empty link.
    const afterLabel = (shown) => {
      if (content[cursor] === '(') {
        const start = skipBlank(cursor + 1);
        const target = md.helpers.parseLinkDestination(content, start, content.length);
        if (!target.ok) throw new Unmapped();
        if (target.str && shown !== null && shown.first !== null) {
          link(githubHref(target.str), shown.first, shown.last);
          // As written, on the line it is written on.
          const writtenAs = content.slice(start, target.pos);
          spell(lineAt(start), writtenAs.startsWith('<') && writtenAs.endsWith('>') ? writtenAs.slice(1, -1) : writtenAs);
        }
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
              destinations[lineAt(at)].push(githubHref(child.content));
              print(lineAt(at), ' ');
              // As written: between the autolink's "<" and ">".
              spell(lineAt(at), content.slice(cursor, content.indexOf('>', cursor)));
            } else {
              print(lineAt(at), child.content);
              const end = at + child.content.length;
              const url = !inImage && label === null ? findBare(at, end) : end;
              // Before a bare URL the text is the open anchor's; the URL
              // closes the anchor, and its own link is the bare URL.
              if (VISIBLE.test(content.slice(at, url))) standsOn(lineAt(at), lineAt(at));
              if (url < end) {
                anchor = null;
                if (VISIBLE.test(content.slice(url, end))) standsOn(lineAt(at), lineAt(at));
              }
            }
            cursor = at + child.content.length;
            break;
          }
          case 'text_special': {
            const at = find(child.markup);
            print(lineAt(at), child.content);
            if (VISIBLE.test(child.content)) standsOn(lineAt(at), lineAt(at));
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
              if (VISIBLE.test(part)) standsOn(lineAt(at), lineAt(at));
              at += part.length + 1;
            }
            cursor = close + child.markup.length;
            break;
          }
          case 'html_inline': {
            const at = find(child.content);
            const tag = readTag(child.content, 0);
            if (child.content.startsWith('<!--')) {
              // Hidden to where the page ends the comment. markdown-it runs
              // it to "-->", and whatever follows an earlier "--!>" is HTML
              // the page shows.
              const [textEnd, stop] = commentEnd(child.content, 0) ?? [child.content.length - 3, child.content.length];
              let position = at + 4;
              for (const part of child.content.slice(4, textEnd).split('\n')) {
                hidden[lineAt(position)] += ' ' + part + ' ';
                position += part.length + 1;
              }
              readHtml(child.content.slice(stop), (offset) => lineAt(at + stop + offset), (line) => standsOn(line, line));
            } else if (tag !== null && FILTERED_TAGS.has(tag.name)) {
              // GFM's tagfilter writes the tag as text, and the page prints it.
              let position = at;
              for (const part of child.content.split('\n')) {
                print(lineAt(position), part);
                if (VISIBLE.test(part)) standsOn(lineAt(position), lineAt(position));
                position += part.length + 1;
              }
            } else if (tag !== null) {
              if (tag.name === 'br' && !tag.closing) print(lineAt(at), ' ');
              if (tag.name === 'a') {
                const href = destinationOf(tag);
                anchor = href === null ? null : {
                  href,
                  written: tag.attributes.get('href'),
                  line: lineAt(at + tag.valuesAt.get('href')),
                  spelled: false,
                };
              }
              if (tag.name === 'img' && !tag.closing) standsOn(lineAt(at), lineAt(at));
            } else {
              // A declaration, a processing instruction or a CDATA section,
              // each a comment to the browser.
              readHtml(child.content, (offset) => lineAt(at + offset));
            }
            cursor = at + child.content.length;
            break;
          }
          case 'link_open':
            inAutolink = child.markup === 'autolink';
            cursor = find(inAutolink ? '<' : '[') + 1;
            if (!inAutolink) label = { first: null, last: null };
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
            // An image is content a reader sees, and follows, in a link.
            standsOn(lineAt(cursor - 2), lineAt(cursor - 2));
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
        written[line] = [];
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
      const block = token.content.replace(/\n$/, '');
      const breaks = [];
      for (let at = block.indexOf('\n'); at !== -1; at = block.indexOf('\n', at + 1)) breaks.push(at);
      readHtml(block, (position) => {
        let count = 0;
        while (count < breaks.length && breaks[count] < position) count += 1;
        return from + count;
      });
    }
  }
  // A line given as it stands is read as plain text, bare URLs and all.
  const lines = source.map((raw, line) => {
    if (printed[line] === null || plain[line]) return [raw, hidden[line], destinations[line], bareIn(raw), []];
    return [printed[line], hidden[line], destinations[line], bare[line], written[line]];
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
