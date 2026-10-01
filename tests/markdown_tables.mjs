#!/usr/bin/env node
/**
 * Read a Markdown page's headings and tables, as markdown-it reads them.
 *
 * tests/test_routing_mirror.py compares two tables on two pages. ADR-0002
 * says a new tool reads Markdown through markdown-it, so the suite asks this
 * program, and no rule of its own, where each heading and each table is. It
 * reads one JSON object per line on stdin, {"text": <a Markdown document>},
 * and writes one JSON object per line on stdout: {"error": <message>} when it
 * cannot read the request, or else {"blocks": [...]}, one entry for each
 * heading and each table, in document order:
 *
 *   {"type": "heading", "level": <1 to 6>, "text": <what it prints>}
 *   {"type": "table", "rows": [[<what each cell prints>, ...], ...]},
 *   with the header row first
 *
 * A blank line gets no answer.
 *
 * A heading's or a cell's text is what it prints, on one line, except that a
 * code span prints its code between backticks, so two filenames in code stay
 * apart. A link prints its label, inline or by reference, so a linked filename
 * reads the same as the name in a code span. Emphasis marks, an image, a
 * comment and an HTML tag print nothing; a character reference or a backslash
 * escape prints its character; a line break prints a space; and each run of
 * white space is one space. A heading or a table inside a fenced block, a code
 * block or an HTML block, such as a comment, is not given.
 *
 * The parser is markdown-it in CommonMark mode with GitHub's tables, as
 * .github/scripts/x-not-y-blocks.js reads the same pages.
 *
 * Usage:
 *   node tests/markdown_tables.mjs < requests.jsonl
 */

import { createInterface } from 'node:readline';
import MarkdownIt from 'markdown-it';

const md = new MarkdownIt('commonmark').enable(['table']);

// What an inline token list prints, on one line.
function printed(children) {
  let text = '';
  for (const token of children) {
    if (token.type === 'text') text += token.content;
    else if (token.type === 'code_inline') text += '`' + token.content + '`';
    else if (token.type === 'softbreak' || token.type === 'hardbreak') text += ' ';
  }
  return text.replace(/\s+/g, ' ').trim();
}

// Each heading and each table of a document, in document order.
function blocks(text) {
  const tokens = md.parse(text, {});
  const found = [];
  let table = null;
  let row = null;
  tokens.forEach((token, index) => {
    if (token.type === 'heading_open') {
      found.push({ type: 'heading', level: Number(token.tag.slice(1)), text: printed(tokens[index + 1].children) });
    } else if (token.type === 'table_open') {
      table = { type: 'table', rows: [] };
      found.push(table);
    } else if (token.type === 'table_close') {
      table = null;
    } else if (token.type === 'tr_open' && table) {
      row = [];
      table.rows.push(row);
    } else if (token.type === 'tr_close') {
      row = null;
    } else if (token.type === 'inline' && row) {
      row.push(printed(token.children));
    }
  });
  return found;
}

const input = createInterface({ input: process.stdin, crlfDelay: Infinity });
input.on('line', (line) => {
  if (!line.trim()) return;
  let answer;
  try {
    const request = JSON.parse(line);
    if (typeof request.text !== 'string') throw new Error('the request has no "text" string');
    answer = { blocks: blocks(request.text) };
  } catch (error) {
    answer = { error: String(error && error.message ? error.message : error) };
  }
  process.stdout.write(JSON.stringify(answer) + '\n');
});
