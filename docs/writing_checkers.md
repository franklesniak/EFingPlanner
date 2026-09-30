<!-- markdownlint-disable MD013 -->

# Writing a Checker

## Metadata

- **Status:** Active
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-09-30
- **Scope:** Seven rules for writing or changing a check in this repository: a gate script under `.github/scripts/`, or a test under `tests/` that checks the repository's files. Each rule has one example from this repository. It does not cover what the curriculum's pages say, which the style law in `framework/docs/build_style_and_vocab.md` governs.
- **Related:** [ADR-0002: the three gates keep their own Markdown parsers](adr/ADR-0002-three-gates-keep-their-markdown-parsers.md), [Contributing](../CONTRIBUTING.md)

## How to Use This Page

Read this page before you write a new check or change one. The docstring of each gate this repository wrote points here. A check that breaks one of these rules can report success on something it never examined, which is the defect this repository has recorded most often.

This page records seven rules, and it is not a complete list of what makes a check correct. A check that needs a rule this page does not have SHOULD add it here, with an example.

## 1. Read Logical Units

A check that matches prose MUST read it in logical units: a paragraph, a list item, a table cell or a heading. It MUST NOT match prose one physical line at a time, because a sentence that wraps across two lines holds its subject on one and its predicate on the next, and a pattern written against one line sees neither. A check that reads Markdown SHOULD read it through the markdown-it page model, as ADR-0002 says a new tool does.

Example: `.github/scripts/x-not-y-blocks.js` hands the `X, not Y` recount and the trope-density gate each block of a page, with the text the block prints, line by line. A sentence that wraps is still one paragraph.

## 2. Prefer a Rule With Nothing to Enumerate

A rule that lists the shapes it handles is only as complete as its list, and a list looks complete to the person who wrote it. Normalise the input first, then apply one rule to what is left.

Example: `.github/scripts/check-session-structure.py` peels the block quote and list-item prefixes off a line (`container_line`) before it decides what the line is. So `> <!-- no-source-check: ... -->` is the same comment as the form with no prefix, and no rule lists the containers a marker may sit in.

## 3. Re-Derive a Claim From the Repository

Where a claim is derived from the repository, such as a count, a list of files or where something sits, the check MUST derive it again and compare. A pinned string proves that the text did not move. It does not prove that the text is true. Pin a string only where the string itself is the requirement: a canonical phrase, a banned token or an exact heading.

Example: `tests/test_check_session_structure.py` compares the sessions the structure gate reads with the sessions `framework/PROJECT_ROADMAP.md` links, and checks that their numbers run from 00 with no gap. A fixed count of sessions would need raising by hand, and would stay green for a session saved in the wrong folder. `tests/test_required_wording.py` pins strings instead, because each one is wording a build brief or the specification requires word for word.

## 4. State the Vocabulary, and Measure Its Recall

A check recognises only the words and shapes it was written for. State that vocabulary where the check is. Then measure its recall: build a set of cases by hand that the check must find, and prove that it finds each one. A clean result from a check whose vocabulary is not stated means only that nothing in its dictionary was broken.

Example: the destination rule in `.github/scripts/check-leaks.py` holds its five built-in names in `DESTINATION_NAMES`, and reads the rest from the list in each destination pack's `README.md`. `tests/test_check_leaks.py` proves that the walk finds each of them, in any case, and that other words are not taken for one.

## 5. Measure Clearing and Exemption Rules the Same Way

The rules that say "this instance is fine" need the same measurement as the rules that match. A clearing rule MUST NOT clear its subject: a rule that clears every line naming the thing the check is about reports clean by construction. An exemption names the one occurrence it is for, and a test proves that the occurrence still occurs.

Example: `tests/fixtures/self_contained_references/exemptions.tsv` names each exempted occurrence with the words around it and a count. `test_every_exempt_occurrence_still_occurs` in `tests/test_self_contained_references.py` fails a row whose count no longer matches. The exempted strings live in that fixture, outside the files the scan reads.

## 6. Give Every Pattern a Positive Control

A matching rule is not believed until it has matched something. Every pattern MUST have a positive control, an input it must fire on, beside a negative control, an input it must not fire on. A check with only negative controls cannot be told from a broken one.

Example: `test_every_metadata_pattern_rejects_its_own_valueless_form` in `tests/test_check_session_structure.py` gives each parent-strip field pattern its empty forms, which must not match, and a real value, which must.

## 7. Keep Two Runs Apart, and Compare Their Failures

A harness that compares two runs MUST write each run to a path nothing else writes to, and MUST check that both outputs exist and are not empty before it compares them. Compare the sets of failures, by name. Two runs can report the same total and still differ.

Example: `--grade-report BASE` in `.github/scripts/check-trope-density.py` reads the two versions of each changed page from their own Git objects, never from one working file. It reports each page whose grade rose, by its path.
