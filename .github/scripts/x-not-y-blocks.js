#!/usr/bin/env node

/**
 * Read Markdown blocks for the `X, not Y` recount
 *
 * check-x-not-y.py uses this helper so that the page's block structure comes
 * from a CommonMark parser instead of hand-written line rules. Each such rule
 * was followed by the next case it missed: a fence opened on a list-item line,
 * a link reference definition, a comment that runs over several lines, a loose
 * list, a lazy continuation line. The helper reads one JSON object per line on
 * stdin, `{"text": <Markdown document>}`, and writes one JSON object per line
 * on stdout, `{"blocks": [...]}`, one entry per block in document order:
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
 *
 * The parser is markdown-it in CommonMark mode with GitHub's tables, as
 * render-markdown.js and the repository's markdownlint read the same pages. A
 * link reference definition is not a block: it prints nothing, so it is not
 * given. The inline source is given as written, so the recount can key each
 * sentence by its own words.
 *
 * Usage:
 *   node .github/scripts/x-not-y-blocks.js < requests.jsonl
 */

const readline = require('readline');
const MarkdownIt = require('markdown-it');

const md = new MarkdownIt('commonmark').enable(['table']);

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
      case 'paragraph_open':
        add(token, { type: 'paragraph', content: tokens[index + 1].content });
        break;
      case 'heading_open':
        add(token, { type: 'heading', level: Number(token.tag.slice(1)), content: tokens[index + 1].content });
        break;
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
  const { text } = JSON.parse(line);
  process.stdout.write(JSON.stringify({ blocks: readBlocks(text) }) + '\n');
});
