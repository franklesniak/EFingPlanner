#!/usr/bin/env node

/**
 * Read Markdown blocks, and the text they print, for the `X, not Y` recount
 *
 * check-x-not-y.py uses this helper so that a page is read by a CommonMark
 * parser instead of hand-written rules. Each such rule was followed by the next
 * case it missed: a fence opened on a list-item line, a link reference
 * definition, a comment that runs over several lines, a shortcut reference
 * link, a backslash line break. The helper reads one JSON object per line on
 * stdin, `{"text": <Markdown document>}`, and writes one JSON object per line
 * on stdout: `{"error": <message>}` when it cannot read the document, or else
 * `{"blocks": [...]}`, one entry per block in document order:
 *
 *   type     paragraph, heading, html_block, fence, code_block, table, hr,
 *            bullet_list, ordered_list or blockquote. A list or a block quote
 *            is given where it opens, before the blocks inside it.
 *   start    the block's first source line, counting from 1.
 *   end      the block's last source line.
 *   quote    the number of the innermost block quote around the block, or null.
 *            Block quotes are numbered from 0 in document order.
 *   list     the number of the innermost list around the block, or null.
 *   item     true for the first block of a list item.
 *   level    a heading's level, 1 to 6.
 *   content  a paragraph's or a heading's inline source, less the block quote
 *            prefixes, list markers and indentation around it, one source line
 *            per line; or an HTML block's, a fence's or a code block's text.
 *   text     a paragraph's or a heading's printed text, one source line per
 *            line, so line N of `text` is what line N of `content` prints.
 *
 * The printed text is what the page shows as prose. Emphasis marks print
 * nothing; a link prints its label, whether it is inline or a reference; an
 * image, a comment and an HTML tag print nothing, except that `<br>` prints a
 * space; a character reference or a backslash escape prints its character; a code span prints `‹code›`, because
 * code is not prose; and a line break, soft or hard, is a new line. A code
 * span, an image or a link's destination can run over a line break that then
 * prints nothing, so the line breaks it consumed follow it, and each printed
 * line stays on its source line. A paragraph whose printed text has another
 * number of lines than its source is an error.
 *
 * The parser is markdown-it in CommonMark mode with GitHub's tables, as
 * render-markdown.js and the repository's markdownlint read the same pages. A
 * link reference definition is not a block: it prints nothing, so it is not
 * given.
 *
 * Usage:
 *   node .github/scripts/x-not-y-blocks.js < requests.jsonl
 */

const readline = require('readline');
const MarkdownIt = require('markdown-it');

const md = new MarkdownIt('commonmark').enable(['table']);
const CODE = ' ‹code› ';
const newlines = (text) => text.split('\n').length - 1;

// Returns markdown-it's own function for one inline rule, through the ruler's
// public methods: an instance with only that rule enabled lists only it.
function inlineRule(name) {
  const only = new MarkdownIt('commonmark');
  only.inline.ruler.enableOnly([name]);
  return only.inline.ruler.getRules('')[0];
}

// A code span, a link and an image print fewer line breaks than they can
// consume. Each of these rules is wrapped so that the last token it adds
// records how many source line breaks the rule consumed.
['backticks', 'link', 'image'].forEach((name) => {
  const rule = inlineRule(name);
  md.inline.ruler.at(name, (state, silent) => {
    const from = state.pos;
    const count = state.tokens.length;
    const ok = rule(state, silent);
    if (ok && !silent && state.tokens.length > count) {
      const last = state.tokens[state.tokens.length - 1];
      last.meta = { ...(last.meta || {}), lines: newlines(state.src.slice(from, state.pos)) };
    }
    return ok;
  });
});

// Returns the text an inline run prints, with one line per source line.
function printed(children) {
  let out = '';
  const links = [];
  for (const token of children || []) {
    switch (token.type) {
      case 'text':
        // `&#10;` prints a line feed, which a browser shows as a space.
        out += token.content.replace(/\n/g, ' ');
        break;
      case 'softbreak':
      case 'hardbreak':
        out += '\n';
        break;
      case 'code_inline':
        out += CODE + '\n'.repeat(token.meta ? token.meta.lines : 0);
        break;
      case 'image':
        out += '\n'.repeat(token.meta ? token.meta.lines : 0);
        break;
      case 'html_inline':
        out += (/^<br\b/i.test(token.content) ? ' ' : '') + '\n'.repeat(newlines(token.content));
        break;
      case 'link_open':
        links.push(newlines(out));
        break;
      case 'link_close': {
        // The label's own line breaks are already printed; the rest were in
        // its destination, its title or its reference label.
        const printedInLabel = newlines(out) - links.pop();
        const consumed = token.meta ? token.meta.lines : 0;
        out += '\n'.repeat(Math.max(0, consumed - printedInLabel));
        break;
      }
      default:
        break;
    }
  }
  return out;
}

// Returns the printed text of an inline token, checked against its source:
// line N of the text must be line N of the source.
function printedLines(inline) {
  const text = printed(inline.children);
  if (newlines(text) !== newlines(inline.content)) {
    throw new Error(`printed text has ${newlines(text) + 1} lines for ${newlines(inline.content) + 1} source lines`);
  }
  return text;
}

function readBlocks(text) {
  const tokens = md.parse(text, {});
  const blocks = [];
  const quotes = [];
  const lists = [];
  let nextQuote = 0;
  let nextList = 0;
  let itemOpen = false;
  const top = (stack) => (stack.length ? stack[stack.length - 1] : null);
  const add = (token, fields) => {
    blocks.push({
      start: token.map[0] + 1,
      end: token.map[1],
      quote: top(quotes),
      list: top(lists),
      item: itemOpen,
      ...fields,
    });
    itemOpen = false;
  };
  tokens.forEach((token, index) => {
    switch (token.type) {
      case 'blockquote_open':
        add(token, { type: 'blockquote' });
        quotes.push(nextQuote);
        nextQuote += 1;
        break;
      case 'blockquote_close':
        quotes.pop();
        break;
      case 'bullet_list_open':
      case 'ordered_list_open': {
        const opensItem = itemOpen;
        add(token, { type: token.type.replace('_open', '') });
        blocks[blocks.length - 1].item = opensItem;
        lists.push(nextList);
        nextList += 1;
        break;
      }
      case 'bullet_list_close':
      case 'ordered_list_close':
        lists.pop();
        break;
      case 'list_item_open':
        itemOpen = true;
        break;
      case 'paragraph_open': {
        const inline = tokens[index + 1];
        add(token, { type: 'paragraph', content: inline.content, text: printedLines(inline) });
        break;
      }
      case 'heading_open': {
        const inline = tokens[index + 1];
        add(token, {
          type: 'heading', level: Number(token.tag.slice(1)), content: inline.content, text: printedLines(inline),
        });
        break;
      }
      case 'html_block':
      case 'fence':
      case 'code_block':
        add(token, { type: token.type, content: token.content });
        break;
      case 'hr':
        add(token, { type: 'hr' });
        break;
      case 'table_open':
        add(token, { type: 'table' });
        break;
      default:
        break;
    }
  });
  return blocks;
}

const input = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
input.on('line', (line) => {
  if (!line.trim()) return;
  let answer;
  try {
    answer = { blocks: readBlocks(JSON.parse(line).text) };
  } catch (error) {
    // A page this helper cannot read is reported, so the recount stops and names it.
    answer = { error: error instanceof Error ? error.message : String(error) };
  }
  process.stdout.write(JSON.stringify(answer) + '\n');
});
