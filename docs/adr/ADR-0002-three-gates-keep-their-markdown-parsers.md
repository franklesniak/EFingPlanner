<!-- markdownlint-disable MD013 -->

# ADR-0002: The Three Gates Keep Their Own Markdown Parsers

## Metadata

- **Status:** Accepted
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-09-29
- **Scope:** Records why the readability gate, the session-structure gate and the prohibited-placeholder hook keep the CommonMark readers they carry, how a new tool reads Markdown, and how two of the gates are held to markdown-it's reading of every page. It does not change what any gate checks.
- **Related:** [Readability gate](../../.github/scripts/check-readability.py), [Session-structure gate](../../.github/scripts/check-session-structure.py), [Placeholder hook](../../.github/scripts/check-prohibited-placeholders.py), [Block reader](../../.github/scripts/x-not-y-blocks.js), [Writing a checker](../writing_checkers.md), [Issue 27: the parser question and its evaluation](https://github.com/franklesniak/EFingPlanner/issues/27)

**Date:** 2026-09-29

## Context

Three gates read Markdown with a CommonMark reader written by hand in Python: `.github/scripts/check-readability.py`, `.github/scripts/check-session-structure.py` and `.github/scripts/check-prohibited-placeholders.py`. None of them starts Node.js. The placeholder hook runs under pre-commit, and the pre-commit workflow in CI installs no Node modules. The placeholder hook and its suite come from the upstream template, with local changes.

Every Markdown reader written after them reads through markdown-it, a CommonMark parser that `npm ci` installs from the repository's lock file:

- The Last Updated check, `.github/scripts/check-last-updated.py`, through `.github/scripts/render-markdown.js`.
- The `X, not Y` recount, `.github/scripts/check-x-not-y.py`, through `.github/scripts/x-not-y-blocks.js`.
- The trope-density gate, `.github/scripts/check-trope-density.py`, which reads each page through the recount's page model.

Review of the hand-written readers kept finding CommonMark constructs they misread. Most were constructs no page in this repository uses, and fixing them one at a time did not converge. The question was whether the three gates should move to markdown-it too.

On 2026-09-29, all 207 tracked Markdown pages under `framework/` and `destinations/` were read by the gates and by `x-not-y-blocks.js`:

- The session-structure gate found the same headings as markdown-it, at the same lines and levels, on 207 of 207 pages.
- The session-structure gate's scan hid every line of every fenced block markdown-it found on 207 of 207 pages. It hid nothing outside fenced blocks, HTML blocks and lines that print nothing.
- The readability gate read the same fenced-block lines as markdown-it on 207 of 207 pages.

## Decision

- The three gates keep their parsers.
- A new tool that reads Markdown reads it through markdown-it, as the recount, the trope-density gate and the Last Updated check do.
- A gate whose CommonMark reading must change moves to markdown-it, and its parser is not patched. A reading must change when the gate reads a tracked page otherwise than markdown-it does and the difference changes what the gate reports.
- Two tests hold two of the gates to markdown-it's reading of every tracked page under `framework/` and `destinations/`, each through one Node.js process:
  - `test_the_gate_reads_every_page_as_markdown_it_does` in `tests/test_check_session_structure.py` compares the headings and the hidden lines.
  - `test_the_gate_reads_every_page_s_fences_as_markdown_it_does` in `tests/test_check_readability.py` compares the fenced-block lines.
- Each test fails when Node.js or `node_modules` is missing, with a message that names `npm ci`. Neither test skips.
- A difference the gate keeps on purpose, such as a reading that follows GitHub's renderer where markdown-it does not, is named in the allow-list beside its test, with its reason. An entry whose difference no longer occurs fails the test.

## Consequences

Positive:

- The gates and their suites stay as they are, and on the date above they agree with markdown-it on every page.
- The placeholder hook keeps running under pre-commit without Node.js, and its template-managed files do not change.
- A claim about a gate's CommonMark reading is settled by the two tests on the real pages, or by this record. It does not need another review.

Negative:

- The tests compare block structure only. They do not compare inline rules, such as a comment inside a line of text or a code span.
- The placeholder hook is not compared. It exposes no line map, and adding one would change a template-managed file.
- The repository keeps two kinds of Markdown reader. The gates' copies of their shared helpers can still drift apart, which `test_the_gates_shared_helpers_are_the_same_code` in `tests/test_check_session_structure.py` catches.
- The readability and structure suites now need Node.js and `node_modules`, as the recount's suites do. The Markdown workflow runs `npm ci` before it runs them.

## Alternatives Considered

- **Keep the parsers and record nothing.** The question stays open, so the next review raises it again.
- **Keep the parsers, and test them against generated inputs.** A seeded alphabet of snippets, each read by a gate helper and by markdown-it, samples constructs no page uses. That is how the earlier fixes stopped converging.
- **Move the structure gate, then the readability gate, to markdown-it now.** This rewrites about 11,300 lines of reviewed code that already agrees with markdown-it on every page.
- **Move all three gates now.** This also puts Node.js under the placeholder hook's pre-commit run, which the pre-commit workflow does not install, and changes template-managed files.
- **Rewrite the gates in Node.js.** This has the costs of moving all three, and more.
- **Add `markdown-it-py`, a Python port, as a new dependency.** This adds a second markdown-it implementation, which can read a page otherwise than the one the other tools use.

## For Reviewers and Agents

A CommonMark construct that no tracked page uses is not, on its own, a reason to change a gate's parser. If a page needs the construct, or a test fails on a page for a difference the gate does not keep on purpose, the gate moves to markdown-it as the Decision says. If the owner changes this decision, a new ADR supersedes this one.
