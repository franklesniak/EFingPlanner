"""Check child-facing Markdown for reading level.

The curriculum targets a fourth-to-sixth-grade reading level for the text a
child reads. This script measures two things that a human cannot eyeball
reliably across dozens of files:

* **Flesch-Kincaid grade level** -- the US school grade needed to read the text.
* **Average sentence length** -- the single strongest lever on the grade score,
  reported separately so an author knows *why* a file scored high.

The checker carries one dependency and no more: PyYAML, which decides whether a
block between two delimiters is front matter. That question is a YAML question,
and a hand-written grammar for it drew three reviewer findings in two rounds,
against four of its own alternatives, before the last of them proved it could
not be written: whether an indented line is YAML depends on the line above it,
which a line-regular pattern cannot see. PyYAML is already pinned in this
repository for two other local hooks and is installed by the workflow that runs
this script. Everything else here stays on the standard library, like the
prohibited-placeholder hook beside it, so the rest of the checker runs on
Windows, macOS, Linux, and WSL with no install step.

Scoring prose only
------------------
Markdown is not prose. Headings, tables, code fences, URLs, and navigation
lines are not sentences a child reads aloud, and leaving them in produces
meaningless scores. Everything in ``STRIPPING`` below is removed before
measurement. Parent-facing regions inside an otherwise child-facing session
(the "For parents" strip near the top, and the "Parent Notes" section at the
bottom) are removed too: adults may read at an adult level. What survives is
then decoded: a character reference such as ``&nbsp;`` is one character on the
page, so counting its name as a word measures text nobody reads.

One line of the extracted prose is one sentence unit. A Markdown paragraph may
be hard-wrapped over several source lines, so the continuation lines of a
paragraph are joined back into one unit before sentences are counted; without
that, reflowing a paragraph would lower its score without changing a word. A
blockquote is a container, not a unit, so the same joining applies inside one.
A blank line, a heading, a table, a code fence, a new list item, and a new
quoted paragraph each start a new unit, which keeps one worksheet prompt or one
list item counting as one sentence.

Audience
--------
Only child-facing paths are scored by default (see ``DEFAULT_INCLUDE_GLOBS``).
A directory argument selects from that same set, so ``check-readability.py .``
is the default scan and not a wider one. A named *file* is an explicit request
for that one file and is scored even when it sits outside those globs --
with one limit: the adult- and builder-facing trees in
``ALWAYS_EXCLUDED_PREFIXES`` are never scored, however the path arrives. Naming
one of those files does not make it child-facing.
A file can also opt out of scoring by carrying an audience marker anywhere in
its text::

    <!-- audience: adult -->

The marker counts only where CommonMark would render it as a comment: one shown
as an example inside a code fence or a code span is literal text on the page and
exempts nothing.

Per-file audience is declared **only** by that marker. There is deliberately no
second hard-coded exclusion list to keep in sync: an adult-facing file that sits
inside a child-facing tree says so in its own text, where an author editing the
file can see it.

Thresholds
----------
Two bands per metric. A *warning* means the file is above target but still
publishable; a *failure* means it is far enough out that it must be fixed.
Warnings do not change the exit code unless ``--strict`` is passed, which keeps
the CI step advisory while still failing on genuinely unreadable text.

Both measures are rounded to two decimal places once, before the thresholds are
applied, so the number that is compared is the same number that is stored and
printed.

File access
-----------
Only Markdown files that resolve inside the repository are read. An absolute
path outside the repository, a path that climbs out with ``..``, and a symlink
are all refused -- including a symlink committed into a scanned tree, which the
default scan would otherwise follow. A file that is selected but cannot be read
stops the run with one message and a non-zero exit code, because a corpus that
was not checked in full must never report success.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field, replace
from html.entities import html5
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]

#: Spaces and tabs, the only whitespace CommonMark and YAML treat as
#: horizontal. ``str.strip`` with no argument also removes U+00A0 and the
#: rest of Unicode, which is how a non-delimiter became a delimiter.
ASCII_HORIZONTAL_WHITESPACE = " \t"

# --------------------------------------------------------------------------
# Thresholds
# --------------------------------------------------------------------------

#: Flesch-Kincaid grade at or above which a file is only warned about.
GRADE_WARN = 6.9
#: Flesch-Kincaid grade at or above which a file fails.
GRADE_FAIL = 7.5
#: Average words per sentence at or above which a file is only warned about.
SENTENCE_WARN = 14.0
#: Average words per sentence at or above which a file fails.
SENTENCE_FAIL = 18.0

#: Below this many prose words a score is statistically meaningless, so the
#: file is reported as "not scored" rather than given a misleading grade.
MIN_WORDS_TO_SCORE = 40

# --------------------------------------------------------------------------
# Scope
# --------------------------------------------------------------------------

#: Child-facing trees, scanned when no explicit paths are given.
DEFAULT_INCLUDE_GLOBS = (
    "framework/sessions/**/*.md",
    "framework/student_guide/**/*.md",
    "framework/templates/**/*.md",
    "destinations/*/session_inserts/**/*.md",
    "destinations/*/reference/*.md",
)

#: Trees that are adult-facing or builder-facing by definition. A path under
#: any of these is never scored, even if passed explicitly.
ALWAYS_EXCLUDED_PREFIXES = (
    "framework/parent_guide/",
    "framework/docs/",
    "docs/",
    ".github/",
    "templates/",
    "schemas/",
    "tests/",
    "node_modules/",
)

#: An audience marker may carry a trailing reason, so an author reading the file
#: can see *why* it is exempt:
#:     <!-- audience: adult -- this session is adult-only setup -->
#: ``re.DOTALL`` because a comment may hold a line ending and still be one
#: comment: the marker scans hand over the comment text the renderer produces,
#: line breaks included, and ``.*?`` stops at the first one without it. The
#: reluctant quantifier still stops at the first ``-->``, so a match that
#: *starts* inside a comment cannot leave it.
#:
#: Starting is the half that needed guarding, and the control that found it is
#: in the suite: the reason's first character is ``\S``, which the ``-`` of an
#: immediately following ``-->`` satisfies -- so ``<!-- no-source-check: -->``,
#: a marker with no reason at all, would have reached across to the next
#: comment's closer for one. The lookahead refuses that character, and an empty
#: reason is no marker again.
AUDIENCE_ADULT_PATTERN = re.compile(
    r"<!--\s*audience:\s*(?:adult|parent|builder)\b.*?-->", re.IGNORECASE | re.DOTALL
)

# --------------------------------------------------------------------------
# Stripping
# --------------------------------------------------------------------------

#: Opening code fence. This name, the container helpers below, and the two
#: fence helpers below are kept identical to
#: ``.github/scripts/check-prohibited-placeholders.py``, so a search for either
#: name finds both copies of the same CommonMark rule.
FENCE_OPEN_PATTERN = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})")
#: One blockquote container prefix, peeled before a fence is parsed. This is the
#: fence-parsing copy of ``BLOCKQUOTE_PATTERN`` below, spelled exactly as the
#: placeholder checker spells it so that the two scripts agree on what a fence
#: is. ``BLOCKQUOTE_PATTERN`` stays the prose-stripping copy.
BLOCK_QUOTE_PREFIX_PATTERN = re.compile(r"^ {0,3}>[ \t]?")
LIST_ITEM_PATTERN = re.compile(r"^(?P<indent> {0,3})(?P<marker>[-*+]|\d{1,9}[.)])(?P<spacing>[ \t]+)")
#: A list item with nothing on its own line. ``LIST_ITEM_PATTERN`` above wants
#: whitespace after the marker, which a marker at the end of a line does not
#: have, so the container walk does not see one here -- and a table's header
#: row is where that gap becomes visible. Measured on GitHub's own renderer:
#: ``-``, ``*``, ``+``, ``1.`` and ``1)`` over a delimiter row form no table,
#: because each is an empty list item rather than a paragraph, while ``-x``
#: over the same row forms one.
#: https://spec.commonmark.org/0.31.2/#list-items
EMPTY_LIST_ITEM_PATTERN = re.compile(r"^ {0,3}(?:[-*+]|\d{1,9}[.)])[ \t]*$")
#: Two of the shapes that end the paragraph above them, spelled as
#: ``.github/scripts/check-session-structure.py`` spells them so that the
#: hooks share one notion of where a paragraph ends. ``HEADING_PATTERN`` and
#: ``THEMATIC_BREAK_PATTERN`` below stay the prose-stripping copies, which
#: ask a narrower question of a line already known to be prose.
#: ``SETEXT_UNDERLINE_PATTERN``, a third shape, is defined with them.
#: https://spec.commonmark.org/0.31.2/#atx-headings
ATX_HEADING_LINE_PATTERN = re.compile(r"^ {0,3}#{1,6}(?:[ \t]|$)")
THEMATIC_BREAK_LINE_PATTERN = re.compile(
    r"^ {0,3}(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$"
)
#: The element names CommonMark lists for HTML block start condition 6. Kept
#: identical to the constant in ``.github/scripts/check-session-structure.py``
#: and in ``.github/scripts/check-prohibited-placeholders.py``.
#: https://spec.commonmark.org/0.31.2/#html-blocks
HTML_BLOCK_ELEMENT_NAMES = (
    "address|article|aside|base|basefont|blockquote|body|caption|center|col|"
    "colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|"
    "footer|form|frame|frameset|h1|h2|h3|h4|h5|h6|head|header|hr|html|iframe|"
    "legend|li|link|main|menu|menuitem|nav|noframes|ol|optgroup|option|p|"
    "param|search|section|summary|table|tbody|td|tfoot|th|thead|title|tr|"
    "track|ul"
)
#: CommonMark starts an HTML block on a line whose *content* begins with
#: ``<!--`` and ends it on the line that carries ``-->``. Every line of that
#: block is raw HTML, so nothing on it is read by the Markdown inline rules --
#: not even text after the ``-->``, which prints as the literal characters the
#: author typed.
#: https://spec.commonmark.org/0.31.2/#html-blocks
HTML_BLOCK_COMMENT_START_PATTERN = re.compile(r"^ {0,3}<!--")

#: CommonMark HTML block start condition 7: a complete open or closing tag,
#: alone on its line. It is the one condition that may not interrupt a
#: paragraph, which is why the classifier below is given the paragraph state.
#: Conditions 1 to 6 are tried first, so an opening ``<script>`` never reaches
#: this pattern. Kept identical to the constants in the sibling hooks.
#: https://spec.commonmark.org/0.31.2/#html-blocks
HTML_BLOCK_TAG_NAME = r"[A-Za-z][A-Za-z0-9-]*"
HTML_BLOCK_ATTRIBUTE = (
    r"[ \t]+[_:A-Za-z][A-Za-z0-9_.:-]*"
    r"""(?:[ \t]*=[ \t]*(?:[^ \t\r\n"'=<>`]+|'[^']*'|"[^"]*"))?"""
)
HTML_BLOCK_TYPE_SEVEN_PATTERN = re.compile(
    rf"^ {{0,3}}(?:<{HTML_BLOCK_TAG_NAME}(?:{HTML_BLOCK_ATTRIBUTE})*[ \t]*/?>"
    rf"|</{HTML_BLOCK_TAG_NAME}[ \t]*>)[ \t]*$"
)
HEADING_PATTERN = re.compile(r"^ {0,3}#{1,6}[ \t]")
TABLE_ROW_PATTERN = re.compile(r"^ {0,3}\|")
TABLE_DELIMITER_PATTERN = re.compile(
    r"^ {0,3}\|?[ \t]*:?-+:?[ \t]*(?:\|[ \t]*:?-+:?[ \t]*)*\|?[ \t]*$"
)
THEMATIC_BREAK_PATTERN = re.compile(r"^ {0,3}(?:-{3,}|\*{3,}|_{3,})[ \t]*$")
NAV_LINE_PATTERN = re.compile(
    r"^[ \t]*(?:You are here:|Previous:|Next:)", re.IGNORECASE
)
PARENT_STRIP_PATTERN = re.compile(r"^[ \t]*\*\*For parents:?\*\*", re.IGNORECASE)
PARENT_SECTION_PATTERN = re.compile(
    r"^ {0,3}#{1,6}[ \t]+(?:Parent Notes?|For Parents?|Notes? for Parents?)[ \t]*$",
    re.IGNORECASE,
)
HTML_COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)
#: Raw HTML as CommonMark defines it: an open or closing tag whose name starts
#: with an ASCII letter, or a declaration, comment remnant, or processing
#: instruction. A bare ``<[^>]+>`` also eats ``Choose < 5 days and > 2 days``,
#: which is child-visible prose, not markup.
#: https://spec.commonmark.org/0.31.2/#raw-html
HTML_TAG_PATTERN = re.compile(
    r"</?[A-Za-z][A-Za-z0-9-]*(?:[ \t][^<>]*)?/?>|<[!?][^>]*>"
)
#: One inline HTML tag, open or closing, matched from a known position rather
#: than searched for. The code-span scan skips a whole tag at a time with it, so
#: that a backtick inside an attribute value is read as part of the attribute,
#: which is what CommonMark does with it. ``HTML_TAG_PATTERN`` above cannot do
#: that job: its ``[^<>]*`` attribute run stops at the first ``>``, so
#: ``<span title="a>b">`` would end one character early and put the rest of the
#: tag back into the scan. Kept identical to the constant in
#: ``.github/scripts/check-session-structure.py``.
#: https://spec.commonmark.org/0.31.2/#raw-html
#: A ``<`` an HTML parser reads as the start of a tag, however malformed the
#: rest of it is. CommonMark's raw-HTML grammar above is stricter, and inside
#: a raw HTML block the page's grammar is the one that decides: the block is
#: passed through untouched and the browser tokenizes it.
#: https://html.spec.whatwg.org/multipage/parsing.html#tag-open-state
MALFORMED_TAG_START_PATTERN = re.compile(r"</?[A-Za-z]")

INLINE_HTML_TAG_PATTERN = re.compile(
    r"""
    <
    (?: [A-Za-z][A-Za-z0-9-]*                      # an open tag
        (?: [ \t]+ [_:A-Za-z][A-Za-z0-9_.:-]*      # an attribute name
            (?: [ \t]*=[ \t]*                      # an attribute value
                (?: [^ \t\r\n"'=<>`]+ | '[^']*' | "[^"]*" ) )?
        )*
        [ \t]* /? >
      | / [A-Za-z][A-Za-z0-9-]* [ \t]* >           # a closing tag
    )
    """,
    re.VERBOSE,
)

#: An autolink: an absolute URI or an email address between angle brackets.
#: Everything between them is destination data -- the renderer puts it in the
#: element's ``href`` and prints the same characters as the link's text -- so a
#: backtick in one opens no code span. The scan consumes a whole autolink for
#: the same reason it consumes a whole tag, and tries the two in the order
#: markdown-it 14.3.0 tries them: an autolink first, because a tag name may not
#: hold a colon and a URI autolink must. Kept identical to the constant in
#: ``.github/scripts/check-readability.py`` and in
#: ``.github/scripts/check-session-structure.py``.
#:
#: The scheme is two to thirty-two characters and the rest of a URI is every
#: character but ``<``, ``>``, a space and a C0 control character; the email
#: form is the HTML5 address the spec names. markdown-it additionally refuses
#: to *link* the ``javascript:``, ``vbscript:``, ``file:`` and most ``data:``
#: schemes, which it documents as a deliberate departure -- "CommonMark allows
#: too much in links" -- and which is a sanitizer rather than a parser:
#: CommonMark 0.31.2 says nothing about the scheme's spelling and micromark
#: 4.0.2 reads ``<data:x>`` as an autolink. This follows the spec and the
#: second renderer, so a backtick inside a blocked-scheme autolink is
#: destination data here and a code-span delimiter to markdown-it; the shape
#: is not one this repository writes.
#: <https://spec.commonmark.org/0.31.2/#autolinks>
AUTOLINK_PATTERN = re.compile(
    r"""
    <
    (?: [A-Za-z][A-Za-z0-9+.-]{1,31} :                  # a scheme, then a URI
        [^<>\x00-\x20]*
      | [A-Za-z0-9.!\#$%&'*+/=?^_`{|}~-]+               # an email address
        @ [A-Za-z0-9] (?: [A-Za-z0-9-]{0,61} [A-Za-z0-9] )?
        (?: \. [A-Za-z0-9] (?: [A-Za-z0-9-]{0,61} [A-Za-z0-9] )? )*
    )
    >
    """,
    re.VERBOSE,
)
#: The three raw HTML forms whose content is characters rather than inline
#: content, each as the pattern that opens it and the string that closes it. A
#: processing instruction runs to ``?>``, a declaration to the first ``>``, and
#: a CDATA section to ``]]>``; CommonMark forbids each closing string inside
#: its own form, so the first one found is the one that closes it. An open tag,
#: a closing tag and a comment are the other three forms and are matched
#: separately. Each of these crosses a soft line break, so the scan looks on
#: past the end of the line for the closer exactly as it does for a comment.
#: Kept identical to the constant in the sibling hook.
#: https://spec.commonmark.org/0.31.2/#raw-html
RAW_HTML_RUN_PATTERNS = (
    (re.compile(r"<\?"), "?>"),
    (re.compile(r"<!\[CDATA\["), "]]>"),
    (re.compile(r"<![A-Za-z]"), ">"),
)
#: The same three with the comment in front of them, for a scan that reads one
#: line rather than one paragraph. The comment is first because it is the one
#: of the four whose opener another of them could also match, and because that
#: is the order ``scan_inline_run`` asks in.
#: https://spec.commonmark.org/0.31.2/#raw-html
RAW_HTML_INLINE_RUNS = ((re.compile(r"<!--"), "-->"),) + RAW_HTML_RUN_PATTERNS
#: The raw HTML runs whose content is not markup. What sits inside one is
#: characters the page shows as they stand or drops altogether, so a
#: ``<!-- ... -->`` written there is displayed text rather than a comment and
#: declares nothing.
#:
#: Two families, and each is a rule from a different place. The element names
#: are HTML's raw text and escapable raw text content models, measured against
#: Python's ``html.parser``, which reports the run as data for every name here
#: and as a comment inside ``pre`` and ``div``; ``noscript`` is left out
#: because whether its content is raw text depends on whether scripting is
#: enabled. The other three are CommonMark's own raw HTML forms -- a
#: processing instruction, a CDATA section and a declaration -- which the
#: renderer passes through untouched and an HTML parser then reads as one
#: token each.
#:
#: Each opener is anchored at the start of the line, because these are the
#: *block* forms: HTML block conditions 1, 3, 4 and 5 all begin a line. A run
#: that opens part way along a line of prose is inline raw HTML and is a
#: question for the inline scan.
#:
#: An open comment is tracked beside them, and is the one run here whose
#: content *is* markup: a marker inside a comment is the comment it looks
#: like. It is in the list because a raw HTML block may not start inside
#: another one, so a ``<script>`` line written inside a comment opens no run
#: -- which is the rule ``html_block_state`` states for the conditions it
#: tracks.
#: https://html.spec.whatwg.org/multipage/parsing.html#rawtext-state
#: https://spec.commonmark.org/0.31.2/#html-blocks
COMMENT_RUN = "comment"
#: The characters HTML5's tokenizer reads as whitespace inside a tag. The
#: Markdown layer's ``ASCII_HORIZONTAL_WHITESPACE`` is a different set for a
#: different question: this one carries the line ending and the form feed,
#: because a tag may hold either. Kept identical to the constant in the
#: sibling hooks.
#: https://html.spec.whatwg.org/multipage/parsing.html#tag-open-state
HTML_TAG_WHITESPACE = "\t\n\f\r "
RAW_TEXT_ELEMENT_NAMES = (
    "script",
    "style",
    "textarea",
    "title",
    "xmp",
    "iframe",
    "noembed",
    "noframes",
)
RAW_TEXT_RUNS = tuple(
    (
        name,
        re.compile(rf"^ {{0,3}}<{name}(?=[ \t/>]|$)", re.IGNORECASE),
        re.compile(rf"</{name}(?=[ \t/>]|$)", re.IGNORECASE),
    )
    for name in RAW_TEXT_ELEMENT_NAMES
) + (
    ("processing instruction", re.compile(r"^ {0,3}<\?"), re.compile(r"\?>")),
    ("CDATA section", re.compile(r"^ {0,3}<!\[CDATA\["), re.compile(r"\]\]>")),
    ("declaration", re.compile(r"^ {0,3}<![A-Za-z]"), re.compile(r">")),
    (COMMENT_RUN, re.compile(r"^ {0,3}<!--"), re.compile(r"-->")),
)
RAW_TEXT_CLOSERS = {key: closer for key, _, closer in RAW_TEXT_RUNS}
#: HTML5's tag-state machine, entered where a tag's name has just ended.
#: ``html_tag_close_state`` names its states as the standard names them and
#: hands the state back, because a tag may end on a line below the one it
#: started on and the machine has to be resumed where it stopped.
#: https://html.spec.whatwg.org/multipage/parsing.html#before-attribute-name-state
TAG_STATE_START = "before-attribute-name"
#: The prefix of a run state that is an unfinished *end tag* rather than a run
#: of raw text. No element name and none of the other four run keys begins with
#: it, so the one state field still holds one thing at a time. What it records
#: is the half-open tag's own tokenizer state, so that a quoted attribute value
#: carried across a line break is resumed rather than restarted.
CLOSING_TAG_RUN_PREFIX = "</"
#: Of those runs, the ones a browser *paints in the page body*. This is a
#: different question from the one ``RAW_TEXT_ELEMENT_NAMES`` answers, and the
#: two were briefly conflated here: that tuple says a comment-shaped run inside
#: one of these elements is displayed text rather than a comment, and deleting
#: the displayed text from the prose contradicts its own premise. A file whose
#: worksheet prompt sits in a ``<textarea>`` then extracted zero words and left
#: the gate in silence, under ``MIN_WORDS_TO_SCORE``.
#:
#: The split is the HTML Standard's own, from the rendering section rather
#: than from the tokenizer. ``script``, ``style``, ``noembed``, ``noframes``
#: and ``title`` are ``display: none`` there, and ``iframe`` is a replaced
#: element whose children are fallback for a browser that cannot render a
#: frame. ``title`` is the case worth naming rather than lumping: its text is
#: real and a reader does see it, in the browser chrome, which is not the page
#: a reading score is about. ``textarea`` shows its content as a form
#: control's value and ``xmp`` renders it as preformatted text, beside ``pre``
#: -- which is why ``xmp`` is kept, so the two preformatted elements of block
#: condition 1 are read the same way.
#:
#: The three raw HTML *block* forms in ``RAW_TEXT_RUNS`` -- the processing
#: instruction, the CDATA section and the declaration -- are absent for the
#: same reason: a browser paints none of them.
#: https://html.spec.whatwg.org/multipage/rendering.html#hidden-elements
DISPLAYED_RAW_TEXT_ELEMENT_NAMES = ("textarea", "xmp")
#: The displayed elements' own tags, and nothing else. A line a ``<textarea>``
#: or an ``<xmp>`` holds is painted character for character, so the only markup
#: on it is the element's own opener and closer: everything between them is
#: text, however it is spelled.
#:
#: This replaces a pattern that removed *any* angle-bracketed run on such a
#: line, which was two errors deep. The first was recorded as a residual and
#: reasoned about wrongly -- ``a <b> inside a <textarea> is removed, and its
#: letters are a tag name rather than words a child reads``. The letters are
#: not the problem. ``[ \t][^<>]*`` matches an *attribute run*, which is
#: arbitrary text: forty-five words written inside ``<note visible visible
#: ... >`` are painted by the element and were removed by this substitution,
#: which left the document under ``MIN_WORDS_TO_SCORE`` and out of the gate in
#: silence. A list looks complete from the inside, and so does a residual.
#:
#: What is left is recorded and is the other direction: markup written *after*
#: the element's closing tag on the same line is text to this pattern, so a
#: ``<b>`` there raises the count by one token rather than lowering it by
#: forty-five. ``MD033/no-inline-html`` refuses every one of these constructs
#: in every tracked file.
#: https://html.spec.whatwg.org/multipage/parsing.html#rawtext-state
DISPLAYED_RAW_TEXT_TAG_PATTERN = re.compile(
    r"</?(?:" + "|".join(DISPLAYED_RAW_TEXT_ELEMENT_NAMES) + r")(?:[ \t][^<>]*)?/?>",
    re.IGNORECASE,
)
#: The two invisible halves of an inline link: its destination and its optional
#: title. Neither is rendered, so both go with the brackets and only the label
#: is prose. A destination is either the pointy ``<...>`` form or a bare run
#: that may carry backslash escapes and balanced parentheses; a title is
#: delimited by ``"``, ``'`` or ``()``.
#:
#: A ``[^)]*`` destination stops at the first ``)``, so
#: ``[the guide](/path_(foo) "Official guidance")`` loses its destination and
#: leaves the title's two words -- and a stray ``)`` -- standing in prose a
#: child never sees. CommonMark nests those parentheses without limit and ``re``
#: cannot recurse, so three levels are spelled out here. A target nested deeper
#: than that simply does not match, which leaves the whole link visible: more
#: words, never fewer, and never a half-eaten one.
#:
#: What a bare destination may *hold* is spelled the way CommonMark spells it:
#: anything but a space, an ASCII control character, and an unescaped
#: parenthesis. The control characters matter, and ``\s`` does not cover them:
#: ``[the guide](fo\x01o "a title")`` is not a link to markdown-it 14.3.0 or to
#: micromark 4.0.2, both of which print the brackets and the title as text a
#: child reads -- and this pattern was deleting them. A bare destination may
#: not *start* with ``<`` either, which is what the lookahead below says; it
#: may hold one further along, and both renderers link ``[x](foo< "t")``
#: happily. Kept in step with the class in
#: ``.github/scripts/check-session-structure.py``.
#: https://spec.commonmark.org/0.31.2/#link-destination
_DESTINATION_CHARACTER = r"(?:[^ \x00-\x1f\x7f()\\]|\\.)"
#: The same rule, as a set rather than as a character class, for the
#: hand-written scan in ``inline_link_end``: every character that ends a bare
#: destination. Spelled as a range so the C0 control characters are named once
#: and none is missed, with U+007F beside them because CommonMark counts it as
#: a control character and ``\x00-\x1f`` does not reach it. Kept identical to
#: the constant in ``.github/scripts/check-session-structure.py``.
#: https://spec.commonmark.org/0.31.2/#link-destination
DESTINATION_STOP_CHARACTERS = frozenset(
    [chr(code) for code in range(0x21)] + ["\x7f"]
)
#: The characters CommonMark allows *between* the parts of an inline link's
#: target -- after the ``(``, between the destination and the title, and
#: before the ``)``. A line ending is one of them: ``[x](url`` with
#: ``"title")`` on the next line is one link with a title, measured on
#: markdown-it 14.3.0 and on GitHub's own renderer. The destination itself may
#: not hold one, which is why this set is written here rather than folded into
#: ``DESTINATION_STOP_CHARACTERS`` above -- the two rules point opposite ways
#: at the same character.
#: https://spec.commonmark.org/0.31.2/#links
LINK_TARGET_WHITESPACE = " \t\n"
_DESTINATION_DEPTH_0 = rf"{_DESTINATION_CHARACTER}*"
_DESTINATION_DEPTH_1 = rf"(?:{_DESTINATION_CHARACTER}|\({_DESTINATION_DEPTH_0}\))*"
_DESTINATION_DEPTH_2 = rf"(?:{_DESTINATION_CHARACTER}|\({_DESTINATION_DEPTH_1}\))*"
_LINK_DESTINATION = (
    rf"(?:<[^<>\n]*>|(?!<)(?:{_DESTINATION_CHARACTER}|\({_DESTINATION_DEPTH_2}\))+)"
)
_LINK_TITLE = r"(?:\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*'|\((?:[^()\\]|\\.)*\))"
#: A whole inline target, ``(destination "title")``, with every part optional:
#: ``[label]()`` is a link too.
_LINK_TARGET = (
    rf"\([ \t]*(?:{_LINK_DESTINATION}(?:[ \t]+{_LINK_TITLE})?|{_LINK_TITLE})?[ \t]*\)"
)
IMAGE_PATTERN = re.compile(rf"!\[[^\]]*\]{_LINK_TARGET}")
LINK_PATTERN = re.compile(rf"\[([^\]]*)\]{_LINK_TARGET}")
#: A bare URL or an autolink. Trailing punctuation is *not* part of a bare
#: URL: GFM's autolink extension trims ``?!.,:;'"`` from the end, so
#: "Read https://example.com. Then pick a city." keeps the period that ends
#: its first sentence. A ``\S+`` pattern eats that period, and the two
#: sentences are then measured as one, which overstates sentence length.
#: https://github.github.com/gfm/#autolinks-extension-
BARE_URL_PATTERN = re.compile(
    r"<https?://[^\s<>]*>"
    r"|https?://[^\s<>]*[^\s<>.,:;!?'\"]"
    r"|https?://"
)
#: A list marker at the head of a line of prose. The ordered form accepts the
#: same one-to-nine-digit marker ``LIST_ITEM_PATTERN`` accepts, because
#: CommonMark draws the line there and nowhere else: ``123456789.`` opens a
#: list and ``1234567890.`` is an ordinary paragraph. A narrower rule leaves
#: ``1000.`` standing in the prose, where it splits off as a one-word sentence
#: and halves the reported words-per-sentence of every prompt below it.
#: https://spec.commonmark.org/0.31.2/#list-items
LIST_MARKER_PATTERN = re.compile(r"^ {0,8}(?:[-*+]|\d{1,9}[.)])[ \t]+")
BLOCKQUOTE_PATTERN = re.compile(r"^ {0,3}>[ \t]?")
EMPHASIS_PATTERN = re.compile(r"[*_]{1,3}")
#: A Setext heading underline. A run of ``=`` or ``-`` under a paragraph turns
#: that whole paragraph into a heading, so neither the text nor the underline is
#: prose. A ``-`` run is a Setext underline only when a paragraph is open; with
#: nothing open it is the thematic break ``THEMATIC_BREAK_PATTERN`` already
#: drops, which is why the two checks are ordered.
#: https://spec.commonmark.org/0.31.2/#setext-headings
SETEXT_UNDERLINE_PATTERN = re.compile(r"^ {0,3}(?:=+|-+)[ \t]*$")
#: A reference link, full ``[text][label]`` or collapsed ``[text][]``. Only the
#: text is rendered, so the label is words a child never reads. A *shortcut*
#: reference (``[text]``) needs no handling here: its brackets carry no word of
#: their own. https://spec.commonmark.org/0.31.2/#reference-link
REFERENCE_IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\[[^\]]*\]")
REFERENCE_LINK_PATTERN = re.compile(r"\[([^\]]*)\]\[[^\]]*\]")
#: A link reference definition. It renders as nothing at all, so neither its
#: label nor its destination is prose. CommonMark does not let one interrupt a
#: paragraph, so this is consulted only when no unit is open.
#:
#: The destination and its optional title must fill the line. Validating only
#: the front of it -- a label, a colon, then any nonblank character -- drops
#: ``[Note]: choose a city with your family today.``, where ``choose`` looks
#: like a destination but the unquoted words after it make the line an
#: ordinary paragraph. The renderer shows that sentence and the checker
#: deletes it, which is the direction that takes a file under the 40-word
#: minimum. A definition whose destination sits on the *following* line is
#: still not recognized, and still errs the safe way: the line keeps its words.
#: https://spec.commonmark.org/0.31.2/#link-reference-definitions
LINK_DEFINITION_PATTERN = re.compile(
    rf"^ {{0,3}}\[[^\]]+\]:[ \t]*{_LINK_DESTINATION}"
    rf"(?:[ \t]+{_LINK_TITLE})?[ \t]*$"
)
#: A link reference definition's optional title, on the line after the
#: destination. It renders as nothing either, so it is consumed with the
#: definition it belongs to; left behind it becomes a short phantom sentence
#: unit that pulls the average sentence length down. The title runs to the end
#: of its line, in matching ``"``, ``'`` or ``()`` delimiters, at any indent.
#: https://spec.commonmark.org/0.31.2/#link-reference-definitions
LINK_DEFINITION_TITLE_PATTERN = re.compile(
    r"^[ \t]*(?:\"[^\"]*\"|'[^']*'|\([^()]*\))[ \t]*$"
)

#: How long a link label may be. CommonMark caps it at 999 characters between
#: the brackets, and the cap decides what a reference *is*: a label one
#: character too long is no reference at all, so the brackets stay on the page
#: and a marker inside them is a comment the child's page really carries. Kept
#: identical to the constant in
#: ``.github/scripts/check-session-structure.py``.
#: https://spec.commonmark.org/0.31.2/#link-label
#: A link label's maximum length, measured on GitHub's own renderer rather
#: than taken from CommonMark's prose, which says 999. A 1,000-character label
#: resolves there, as a definition and as a use, and a 1,001-character one
#: does not; markdown-it 14.3.0 enforces no bound at all. The renderer that
#: decides what the page carries decides this, and erring the other way is the
#: permissive direction: a bound one character too tight reads a resolved
#: reference as literal brackets and honours a marker the page hides.
#: https://spec.commonmark.org/0.31.2/#link-label
LINK_LABEL_MAXIMUM_CHARACTERS = 1000

#: Every character markdown-it 14.3.0 reads as nothing at all inside a link
#: label, measured one at a time rather than taken from a class. CommonMark's
#: prose says a label needs "at least one character that is not a space, tab, or
#: line ending", and the renderer is stricter than those words: it folds the
#: label with a Unicode trim first, so ``[\u00a0]: /url`` is a paragraph and not
#: a definition. Python's ``\s`` is a third set again -- it matches U+0085,
#: which the renderer keeps as a label, and misses U+FEFF, which the renderer
#: drops -- so the set is written out rather than spelled ``\s``. U+200B and
#: U+180E are deliberately absent: the renderer keeps a label made of either.
#: Measured one character at a time through markdown-it 14.3.0.
#: https://spec.commonmark.org/0.31.2/#link-label
_LINK_LABEL_BLANK = (
    " \t\x0b\f\r\n\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000\ufeff"
)
#: One run of those blanks, for the fold ``normalize_link_label`` performs.
_LINK_LABEL_BLANK_RUN = re.compile(f"[{_LINK_LABEL_BLANK}]+")
#: A link reference definition as the marker scan reads one: the whole line
#: renders nothing at all, so a marker anywhere on it is metadata rather than a
#: comment. ``LINK_DEFINITION_PATTERN`` above stays the prose-stripping copy,
#: which asks a narrower question of a line already known to be prose. Kept
#: identical to the constant in
#: ``.github/scripts/check-session-structure.py``.
#: https://spec.commonmark.org/0.31.2/#link-reference-definitions
LINK_REFERENCE_DEFINITION_PATTERN = re.compile(
    rf"""
    ^\ {{0,3}}                               # at most three spaces of indent
    \[ (?=[^\]]*[^{_LINK_LABEL_BLANK}\]])    # a label with one nonblank
       (?P<label> (?: [^\[\]\\] | \\. )+ ) \]
    :[ \t]*                                  # the colon, then spaces or tabs
    {_LINK_DESTINATION}                      # the destination
    (?P<title> [ \t]+                        # an optional title
        (?: " (?: [^"\\] | \\. )* "
          | ' (?: [^'\\] | \\. )* '
          | \( (?: [^()\\] | \\. )* \) )
    )?
    [ \t]*$
    """,
    re.VERBOSE,
)

#: A definition's label and colon, matched however the rest of it is laid out.
#: This reads the label out of a definition ``reference_definition_span`` has
#: already parsed whole. A reference whose label has a definition renders as a
#: link or an image, so the label itself becomes nothing; a reference with no
#: definition renders as the brackets the author typed, and a marker inside
#: *that* is a comment on the page. Kept identical to the constant in
#: ``.github/scripts/check-session-structure.py``.
LINK_REFERENCE_LABEL_PATTERN = re.compile(r"^ {0,3}\[(?P<label>(?:[^\[\]\\]|\\.)+)\]:")

#: A definition's label and colon with nothing after them. CommonMark lets the
#: destination sit on the following line, and the construct still renders
#: nothing at all. Kept identical to the constant in
#: ``.github/scripts/check-session-structure.py``.
LINK_REFERENCE_LABEL_LINE_PATTERN = re.compile(
    rf"^ {{0,3}}\[(?=[^\]]*[^{_LINK_LABEL_BLANK}\]])"
    r"(?P<label>(?:[^\[\]\\]|\\.)+)\]:[ \t]*$"
)

#: A definition's destination, alone on its own line, with the optional title
#: that may follow it there. Conservative for the reason the full pattern is:
#: ``Real visible prose.`` under a label line is prose rather than a
#: destination, which is what the renderer makes of it. Kept identical to the
#: constant in ``.github/scripts/check-session-structure.py``.
LINK_REFERENCE_DESTINATION_LINE_PATTERN = re.compile(
    rf"""
    ^[ \t]*
    {_LINK_DESTINATION}                      # the destination
    (?P<title> [ \t]+                        # an optional title
        (?: " (?: [^"\\] | \\. )* "
          | ' (?: [^'\\] | \\. )* '
          | \( (?: [^()\\] | \\. )* \) )
    )?
    [ \t]*$
    """,
    re.VERBOSE,
)

#: A definition's label, colon and destination, with whatever follows them
#: left unread. The full pattern above anchors at the end of the line, because
#: a same-line title that is followed by text makes the whole thing no
#: definition at all -- measured on both renderers, which read
#: ``[x]: /url "a" ok`` as a paragraph. A title that has merely not *closed*
#: yet is a different thing, and this is what hands it to the title scanner.
#: Kept identical to the constant in the sibling hook.
#: https://spec.commonmark.org/0.31.2/#link-reference-definitions
LINK_REFERENCE_DEFINITION_HEAD_PATTERN = re.compile(
    rf"""
    ^\ {{0,3}}                               # at most three spaces of indent
    \[ (?=[^\]]*[^{_LINK_LABEL_BLANK}\]])    # a label with one nonblank
       (?P<label> (?: [^\[\]\\] | \\. )+ ) \]
    :[ \t]*                                  # the colon, then spaces or tabs
    {_LINK_DESTINATION}                      # the destination
    """,
    re.VERBOSE,
)
#: The same, for a destination sitting alone on the line under a label line.
#: Kept identical to the constant in the sibling hook.
LINK_REFERENCE_DESTINATION_HEAD_PATTERN = re.compile(
    rf"^[ \t]*{_LINK_DESTINATION}", re.VERBOSE
)
#: What opens a definition's title, and what closes each opener. CommonMark
#: allows all three spellings and allows a line ending inside any of them.
#: Kept identical to the constant in the sibling hook.
#: https://spec.commonmark.org/0.31.2/#link-reference-definitions
LINK_REFERENCE_TITLE_DELIMITERS = {'"': '"', "'": "'", "(": ")"}
#: A YAML front-matter delimiter. Front matter is permitted on any Markdown
#: file in this repository, and its keys are publishing metadata, not text a
#: child reads.
FRONT_MATTER_DELIMITER_PATTERN = re.compile(r"^(?:-{3}|\.{3})[ \t]*$")
#: The kind of the sentence unit that is still open for a wrapped line to join.
#: A blockquote line may join only an open *quoted* unit: a blockquote that
#: opens directly under an ordinary paragraph is a new block, not a wrapped
#: continuation of that paragraph.
UNIT_KIND_PROSE = "prose"
UNIT_KIND_QUOTE = "quote"

#: A word, as a reader counts one. Letters are Unicode letters, not ASCII ones:
#: an ASCII-only class splits ``Montréal`` into ``Montr`` and ``al`` and makes
#: ``café`` into ``caf``, so one word becomes two and a word written entirely
#: outside ASCII disappears from the count altogether. This curriculum is about
#: Japan; ``Ōsaka``, ``Gion`` and ``Kyōto`` are the words it is made of.
#: ``[^\W\d_]`` is "any Unicode letter": a word character that is neither a digit
#: nor an underscore.
WORD_PATTERN = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)*|\d+(?:[.,]\d+)*")
#: The quotation marks and brackets that open and close a quoted span. Both the
#: ASCII and the typographic forms are listed, because a word processor produces
#: the typographic ones and an author drafting a session in one and pasting it
#: here produces them without deciding to. An ASCII-only closing class reads
#: ``She asked “Where?” Then we picked a city.`` as one sentence instead of two;
#: an ASCII-only opening class fails to see the abbreviation in ``“e.g. Tokyo”``
#: and splits a sentence that should not split. Both mistakes lower the reported
#: measures, which is the direction that lets hard text through the gate.
_OPENING_QUOTES = "\"'(\\[“‘"
_CLOSING_QUOTES = "\"')\\]”’"
#: A character reference: a decimal reference, a hexadecimal one, or an HTML5
#: entity name, each closed by a semicolon. CommonMark renders one as the
#: character it names, so its *name* is never text a child reads -- ``A&nbsp;or``
#: is three words on the page and five to a matcher that never decodes it, and a
#: file padded with them can clear the 40-word floor without gaining a word.
#:
#: The semicolon is required and the name must be one HTML5 defines, which is
#: narrower than ``html.unescape``: CommonMark leaves ``Fish &amp chips`` showing
#: a visible ``amp``, and decoding it would delete a word the child reads. A
#: reference behind a backslash is literal text for the same reason.
#: https://spec.commonmark.org/0.31.2/#entity-and-numeric-character-references
CHARACTER_REFERENCE_PATTERN = re.compile(
    r"(?<!\\)&(?:#(?P<decimal>[0-9]{1,7})"
    r"|#[Xx](?P<hexadecimal>[0-9A-Fa-f]{1,6})"
    r"|(?P<name>[A-Za-z][A-Za-z0-9]{1,31}));"
)
#: A sentence break: terminal punctuation, any closing quotes or brackets that
#: belong to it, then whitespace. The closers are captured because whether they
#: are present decides one of the two cases in ``ends_a_sentence`` below.
SENTENCE_SPLIT_PATTERN = re.compile(
    rf"(?<=[.!?])(?P<closers>[{_CLOSING_QUOTES}]*)\s+"
)

#: Abbreviations whose period never ends an English sentence, so ``The U.S.
#: Department of State`` is one sentence and not two. Splitting there inflates
#: the sentence count, which lowers *both* reported measures -- the direction
#: that lets genuinely long sentences through the gate.
ABBREVIATION_PATTERN = re.compile(
    rf"(?:^|[\s{_OPENING_QUOTES}])"
    r"(?:U\.S\.|U\.K\.|e\.g\.|i\.e\.|vs\.|Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.|St\.)"
    r"$"
)

#: Abbreviations that *can* end a sentence, so they are not in the list above:
#: "14:00 means 2 p.m. After noon, subtract 12." is two sentences. They end a
#: sentence unless a lowercase word follows, as in "a map, a pen, etc. before
#: you leave".
AMBIGUOUS_ABBREVIATION_PATTERN = re.compile(
    rf"(?:^|[\s{_OPENING_QUOTES}])"
    r"(?:etc\.|a\.m\.|p\.m\.|incl\.|approx\.|No\.)$"
)
#: The abbreviations above that are also complete noun phrases, so English
#: *can* end a sentence with one: "This family lives in the U.S." Every other
#: entry is a bound prefix (``Mr.``) or a connective (``e.g.``) that no English
#: sentence ends with. One of these ends a sentence only when a closed-class
#: word opens the next one; see ``ends_a_sentence`` for what that cannot do.
FREESTANDING_ABBREVIATION_PATTERN = re.compile(
    rf"(?:^|[\s{_OPENING_QUOTES}])(?:U\.S\.|U\.K\.)$"
)

#: Closed-class English words -- articles, demonstratives, pronouns,
#: possessives, conjunctions, subordinators and interrogatives. A capitalized
#: one of these opens a new sentence, because a closed-class word is never the
#: second element of an English proper-noun compound. Content words are
#: deliberately absent: "the U.S. Department of State" and "lives in the U.S.
#: Travel starts tomorrow" are both an initialism followed by a capitalized
#: content word, and nothing available here tells those two apart.
SENTENCE_OPENER_PATTERN = re.compile(
    r"(?:The|This|That|These|Those|There|Then|Thus|It|Its|He|She|They|We|You|I|"
    r"His|Her|Their|Our|Your|My|If|When|While|Where|Because|Since|Although|"
    r"Though|But|And|Or|So|After|Before|Once|Also|However|Now|Here|Both|Each|"
    r"Every|Some|Any|All|Most|Many|Another|Other|Such|Who|What|Why|How)"
    r"(?:[^A-Za-z0-9]|$)"
)
#: A contraction whose ``n't`` is a spoken syllable of its own. It is one
#: whenever a consonant letter precedes the ``n``: "does-n't", "is-n't",
#: "could-n't", "did-n't" are each two syllables, and that second syllable has
#: no vowel letter for the vowel-group pass to find. After a vowel letter the
#: contraction is one syllable ("can't", "won't", "don't") and that vowel is
#: already counted, so nothing is added.
SYLLABIC_NT_PATTERN = re.compile(r"[bcdfghjklmnpqrstvwxz]n['’]t$")
VOWEL_GROUP_PATTERN = re.compile(r"[aeiouy]+")


@dataclass(frozen=True)
class FileScore:
    """The measured reading level of one Markdown file."""

    display_path: str
    words: int
    sentences: int
    syllables: int
    grade: float
    words_per_sentence: float
    failures: tuple[str, ...] = field(default=())
    warnings: tuple[str, ...] = field(default=())
    scored: bool = True
    skip_reason: str = ""

    @property
    def status(self) -> str:
        """Return ``fail``, ``warn``, ``ok`` or ``skip`` for this file."""
        if not self.scored:
            return "skip"
        if self.failures:
            return "fail"
        if self.warnings:
            return "warn"
        return "ok"


class FileReadError(RuntimeError):
    """Raised when a candidate Markdown file cannot be read."""

    def __init__(self, display_path: str, error: Exception) -> None:
        # Only OSError carries ``strerror``. A UnicodeDecodeError does not, and
        # reading it unconditionally turned a readable failure into an
        # AttributeError traceback, which is the opposite of what this class is
        # for.
        detail = getattr(error, "strerror", None) or str(error) or "I/O error"
        error_summary = f"{type(error).__name__}: {detail}"
        super().__init__(f"{display_path}: unable to read file ({error_summary})")


CONTAINER_KIND_LIST = "list"
CONTAINER_KIND_BLOCK_QUOTE = "blockquote"


@dataclass(frozen=True)
class Container:
    """A peelable Markdown container prefix on a line.

    A ``list`` container consumes ``indent`` leading spaces from its parent
    container's interior. A ``blockquote`` container consumes a single
    ``BLOCK_QUOTE_PREFIX_PATTERN`` match (``>`` optionally followed by a
    space) at the start of its parent's interior; ``indent`` is unused.

    ``ordered_start`` is an ordered list item's start number, and ``None`` for
    a bullet list item and for a blockquote. It is kept out of the comparison
    because a containment path is a path: two items of one list are the same
    container at the same depth, and a path comparison that read the start
    number would call every sibling item a different container and cut every
    list in half.
    """

    kind: str
    indent: int = 0
    ordered_start: int | None = field(default=None, compare=False)
    bullet: str | None = field(default=None, compare=False)


@dataclass(frozen=True)
class FenceLine:
    """A Markdown line normalized for fenced code block detection."""

    content: str
    containment_path: tuple[Container, ...] = ()
    #: The containers that opened on this line rather than above it. A list
    #: item among them starts a block, whatever the line goes on to hold.
    opened: tuple[Container, ...] = ()


@dataclass(frozen=True)
class ActiveFence:
    """The active fenced code block marker and containing Markdown context."""

    character: str
    minimum_length: int
    containment_path: tuple[Container, ...] = ()


@dataclass(frozen=True)
class ListContext:
    """An active Markdown list, identified by its full containment path from the document root."""

    containment_path: tuple[Container, ...]


@dataclass(frozen=True)
class HtmlBlockCondition:
    """One CommonMark HTML block condition: how it starts and how it ends.

    ``end`` is the pattern that closes the block on the line carrying it, or
    ``None`` for the conditions a blank line closes; the blank line itself is
    outside the block, which is why it is tested before the start conditions
    are. ``interrupts_paragraph`` is false for condition 7 alone, which is what
    the spec says of it. Kept identical to the record in the sibling hooks.
    https://spec.commonmark.org/0.31.2/#html-blocks
    """

    name: str
    start: re.Pattern[str]
    end: re.Pattern[str] | None
    interrupts_paragraph: bool = True


@dataclass(frozen=True)
class ActiveHtmlBlock:
    """The open HTML block's condition and the container holding it.

    The containment path is here for the reason ``ActiveFence`` carries one:
    CommonMark ends a leaf block with its containing block, so an unclosed
    ``<script>`` opened inside a blockquote ends where the blockquote does
    rather than running to the end of the document. Kept identical to the
    record in the sibling hooks.
    """

    condition: HtmlBlockCondition
    containment_path: tuple[Container, ...] = ()


#: The name condition 2 answers to. The comment is a condition of this machine
#: rather than a state beside it, which is what keeps a ``<script>`` line
#: *inside* a comment from opening a second block that outlives the comment.
HTML_BLOCK_COMMENT = "comment"

#: Condition 4 asks for an *uppercase* ASCII letter after ``<!``. That is the
#: rule markdown-it 14.3.0 carries, and markdown-it is what this repository
#: measures a rendered page against. The CommonMark 0.31.2 prose says "an ASCII
#: letter" instead, and micromark-core-commonmark 2.0.3 reads it that way, so
#: the two really do part over a lowercase ``<!doctype html>``. Following the
#: renderer is also the safe way round: a lowercase declaration that opens no
#: block leaves the paragraph above it open, and a marker below it is read by
#: the inline rules that really do apply there. Kept identical to the machine
#: in the sibling hooks.
#: https://spec.commonmark.org/0.31.2/#html-blocks
HTML_BLOCK_CONDITIONS: tuple[HtmlBlockCondition, ...] = (
    HtmlBlockCondition(
        "script",
        re.compile(r"^ {0,3}<(?:script|pre|style|textarea)(?:[ \t>]|$)", re.IGNORECASE),
        re.compile(r"</(?:script|pre|style|textarea)>", re.IGNORECASE),
    ),
    HtmlBlockCondition(HTML_BLOCK_COMMENT, HTML_BLOCK_COMMENT_START_PATTERN, re.compile(r"-->")),
    HtmlBlockCondition("instruction", re.compile(r"^ {0,3}<\?"), re.compile(r"\?>")),
    HtmlBlockCondition("declaration", re.compile(r"^ {0,3}<![A-Z]"), re.compile(r">")),
    HtmlBlockCondition("cdata", re.compile(r"^ {0,3}<!\[CDATA\["), re.compile(r"\]\]>")),
    HtmlBlockCondition(
        "element",
        re.compile(
            rf"^ {{0,3}}</?(?:{HTML_BLOCK_ELEMENT_NAMES})(?:[ \t>]|/>|$)",
            re.IGNORECASE,
        ),
        None,
    ),
    HtmlBlockCondition("tag", HTML_BLOCK_TYPE_SEVEN_PATTERN, None, interrupts_paragraph=False),
)


@dataclass(frozen=True)
class ParagraphLine:
    """One line of a paragraph, placed in the document it came from.

    ``start`` is the line's offset in the document and ``content_start`` the
    column where its container prefixes end, so a range the code-span scan
    reports is an offset a caller can use against the document it holds.
    """

    start: int
    text: str
    content_start: int


def normalize_line_endings(text: str) -> str:
    """Return ``text`` with every CommonMark line ending written as ``\\n``.

    CommonMark counts a line feed, a carriage return, and a carriage return
    followed by a line feed as one line ending each, so a document saved on
    Windows holds exactly the lines a document saved anywhere else does. The
    translation happens once, here, where a document enters this module --
    never in the predicates below, which would each have to spell ``\\r`` and
    would each be a place to forget it. A closing fence carrying a stray
    ``\\r`` does not close, and every word after it is swallowed as code.

    ``Path.read_text`` translates both forms already, so a file this hook reads
    from disk arrives normalized whatever an editor wrote. This is what makes
    the same true for a caller that hands the document over directly.
    Kept identical to the helper in the sibling hooks.
    https://spec.commonmark.org/0.31.2/#line-ending
    """
    if "\r" not in text:
        return text
    return text.replace("\r\n", "\n").replace("\r", "\n")


def count_leading_spaces(line: str) -> int:
    """Return the number of leading space characters in a line."""
    return len(line) - len(line.lstrip(" "))


def count_indent_columns(line: str) -> int:
    """Return how many *columns* of indentation ``line`` opens with.

    Not the number ``count_leading_spaces`` above returns, and the difference
    is the tab. CommonMark measures indentation in columns and expands a tab
    to the next multiple of four, so a line beginning with one tab starts at
    column four and is an indented code block -- while a count of *characters*
    reads zero and the line is classified as prose. A comment written there is
    text the page prints inside a ``<pre>`` rather than a comment the page
    hides, and honouring an ``audience: adult`` marker on such a line took a
    child-facing document out of the reading gate without a word in the
    report. Measured on both renderers: markdown-it 14.3.0 and GitHub's own
    renderer each put a tab-indented marker line in a code block.

    The two counts are kept apart rather than merged, because their callers
    ask different questions of them. ``peel_containers`` counts characters
    because it then *slices* them, and a column count cannot slice a tab in
    half; this counts columns because it then *classifies* a line, which is
    what CommonMark states in columns. Merging them would have made the
    container walk cut a tab it cannot cut. Kept identical to the helper in
    ``.github/scripts/check-session-structure.py``.
    https://spec.commonmark.org/0.31.2/#tabs
    """
    columns = 0
    for character in line:
        if character == " ":
            columns += 1
        elif character == "\t":
            columns += 4 - columns % 4
        else:
            break
    return columns


def indented_code_rows(contents: Sequence[str]) -> frozenset[int]:
    """Return the rows of one run that CommonMark reads as an indented code block.

    An indented code block may not interrupt a paragraph, and a run holds no
    blank line, so the only row in a run where one can *begin* is the first;
    it then continues for as long as the rows stay indented. A row indented
    four columns under an open paragraph is that paragraph's own continuation
    line, and every inline rule applies to it: ``Intro`` over a tab-indented
    ``<!-- audience: adult -->`` really does carry the marker, and skipping it
    took an adult-facing document into the child gate.

    The indent is counted in columns rather than characters, so a leading tab
    reaches column four and a line beginning with one is code. Kept identical
    to the helper in the sibling hook.
    https://spec.commonmark.org/0.31.2/#indented-code-blocks
    """
    rows: set[int] = set()
    started = False
    for row, content in enumerate(contents):
        if not started and not content.strip(ASCII_HORIZONTAL_WHITESPACE):
            # A run begins with the blank lines that closed the run above it,
            # and a blank line begins no code block. Counting one as the run's
            # first row made every code block that followed a blank line
            # invisible to this helper, which is every one that is not the
            # first thing in the document.
            continue
        started = True
        if count_indent_columns(content) < 4:
            break
        rows.add(row)
    return frozenset(rows)


def peel_containers(line: str, path: tuple[Container, ...]) -> tuple[str, int]:
    """Peel container prefixes from ``line`` in order; return ``(remaining, peeled_count)``.

    A list container consumes ``container.indent`` leading spaces (or fails if
    the line has fewer). A blockquote container consumes one
    ``BLOCK_QUOTE_PREFIX_PATTERN`` match (or fails if the line does not start
    with one in its current coordinate system). Peeling stops at the first
    container that cannot be consumed; the caller can compare ``peeled_count``
    to ``len(path)`` to detect partial peels.
    """
    for index, container in enumerate(path):
        if container.kind == CONTAINER_KIND_LIST:
            if count_leading_spaces(line) < container.indent:
                return line, index
            line = line[container.indent :]
        else:
            match = BLOCK_QUOTE_PREFIX_PATTERN.match(line)
            if match is None:
                return line, index
            line = line[match.end() :]
    return line, len(path)


def prune_inactive_list_contexts(line: str, list_contexts: list[ListContext]) -> None:
    """Drop active list contexts that a nonblank Markdown line has outdented past."""
    if not line.strip(ASCII_HORIZONTAL_WHITESPACE):
        return

    while list_contexts:
        top = list_contexts[-1]
        remaining, peeled_count = peel_containers(line, top.containment_path)
        if peeled_count == len(top.containment_path):
            return
        # The line did not peel cleanly to this list's interior. Decide
        # whether the partial peel still keeps the list active.
        if not remaining.strip(ASCII_HORIZONTAL_WHITESPACE):
            # A blank line inside a partly-peeled container is a continuation.
            return
        failed_container = top.containment_path[peeled_count]
        if (
            failed_container.kind == CONTAINER_KIND_LIST
            and BLOCK_QUOTE_PREFIX_PATTERN.match(remaining) is not None
        ):
            # A deeper blockquote nested inside the list keeps the list active;
            # the list's content indent is not meaningful in that deeper
            # coordinate system.
            return
        list_contexts.pop()


def spacing_columns(match: re.Match[str]) -> int:
    """Return the column just past a list marker's spacing.

    A tab is not one column. CommonMark measures a list item's content indent
    in columns and expands a tab to the next multiple of four, so ``-`` and a
    tab put the content at column 4 exactly as ``-`` and three spaces do --
    which is why the two render identically and why a fenced block indented
    four spaces under either of them is the item's content rather than code.
    Kept identical to the helper in the sibling hooks.
    https://spec.commonmark.org/0.31.2/#tabs
    """
    column = match.end("marker")
    for character in match.group("spacing"):
        column = column + 4 - (column % 4) if character == "\t" else column + 1
    return column


def list_content_indent(match: re.Match[str]) -> int:
    """Return the list-item content indent relative to the marker's parent interior."""
    marker_end_column = match.end("marker")
    spacing_width = spacing_columns(match) - marker_end_column
    content_padding = spacing_width if spacing_width <= 4 else 1
    return marker_end_column + content_padding


def list_content_offset(match: re.Match[str]) -> int:
    """Return where a list item's content starts on its own line, in characters.

    This is the second of the two numbers a list item's marker produces, and
    keeping them apart is the whole point. ``list_content_indent`` is a
    *column*, because that is what the lines below the marker are measured in.
    This is a *character* offset into the marker's own line, because that is
    what a slice of that line is measured in. A tab is one character and up to
    four columns, so the two numbers part company exactly where a tab appears
    -- and using either one for both jobs loses a cell: the column slices two
    characters of the item's text away, and the character count puts the
    content column at 2 where CommonMark puts it at 4.
    Kept identical to the helper in the sibling hooks.
    https://spec.commonmark.org/0.31.2/#tabs
    """
    marker_end_column = match.end("marker")
    if spacing_columns(match) - marker_end_column <= 4:
        return match.end("spacing")
    # More than four columns of spacing is one space of content indent and the
    # rest is the item's own first line, so the content begins one character
    # past the marker.
    return marker_end_column + 1


def bullet_marker(match: re.Match[str]) -> str | None:
    """Return a bullet list item's marker character, or ``None`` if ordered.

    It travels on the container for the reason ``ordered_list_start`` gives,
    and it is read for one question: ``-`` with nothing after it is both an
    empty list item and a level 2 Setext underline, and while a paragraph is
    open CommonMark reads it as the heading. ``*`` and ``+`` underline
    nothing, so only this one marker needs telling apart. Kept identical to the
    helper in the sibling hooks.
    <https://spec.commonmark.org/0.31.2/#setext-headings>
    """
    marker = match.group("marker")
    return marker if marker[0] in "-*+" else None


def ordered_list_start(match: re.Match[str]) -> int | None:
    """Return an ordered list item's start number, or ``None`` for a bullet.

    A list may interrupt a paragraph only when an ordered one starts at 1, so
    the number has to travel on the container the marker opens:
    ``starts_a_block`` is handed the line's interior, past the marker, and
    cannot read it back off the line. Kept identical to the helper in the
    sibling hooks.
    https://spec.commonmark.org/0.31.2/#list-items
    """
    marker = match.group("marker")
    return None if marker[0] in "-*+" else int(marker[:-1])


def normalize_for_fence_opening(line: str, list_contexts: list[ListContext]) -> FenceLine:
    """Return a line normalized to its current Markdown container content column."""
    prune_inactive_list_contexts(line, list_contexts)

    active_path = list_contexts[-1].containment_path if list_contexts else ()
    relative_line, peeled_count = peel_containers(line, active_path)
    effective_path = active_path[:peeled_count]

    # Containers alternate freely on one line: ``> - item``, ``- > quoted``,
    # and ``- - item`` are all valid CommonMark. Peeling every blockquote and
    # then at most one list item handles only the first of those; the rest
    # leave a container prefix in front of the fence, so the fence is missed
    # and the fence state stays wrong for the rest of the file.
    # https://spec.commonmark.org/0.31.2/#container-blocks
    extras: list[Container] = []
    while True:
        quote_match = BLOCK_QUOTE_PREFIX_PATTERN.match(relative_line)
        if quote_match is not None:
            extras.append(Container(kind=CONTAINER_KIND_BLOCK_QUOTE))
            relative_line = relative_line[quote_match.end() :]
            continue

        list_match = LIST_ITEM_PATTERN.match(relative_line)
        if list_match is None:
            break

        content_indent_rel = list_content_indent(list_match)
        extras.append(
            Container(
                kind=CONTAINER_KIND_LIST,
                indent=content_indent_rel,
                ordered_start=ordered_list_start(list_match),
                bullet=bullet_marker(list_match),
            )
        )
        content_offset_rel = list_content_offset(list_match)
        relative_line = (
            relative_line[content_offset_rel:]
            if len(relative_line) >= content_offset_rel
            else ""
        )
        list_contexts.append(ListContext(containment_path=effective_path + tuple(extras)))

    return FenceLine(
        content=relative_line,
        containment_path=effective_path + tuple(extras),
        opened=tuple(extras),
    )


def normalize_for_fence_closing(line: str, active_fence: ActiveFence) -> str:
    """Return a fenced-block line normalized to the opening fence's container."""
    peeled, peeled_count = peel_containers(line, active_fence.containment_path)
    if peeled_count < len(active_fence.containment_path):
        return line
    return peeled


def build_active_fence(
    opening_fence: tuple[str, int],
    fence_line: FenceLine,
) -> ActiveFence:
    """Return active fenced code block state for a detected opening fence."""
    fence_character, minimum_length = opening_fence
    return ActiveFence(
        character=fence_character,
        minimum_length=minimum_length,
        containment_path=fence_line.containment_path,
    )


def strip_block_quote_prefixes(line: str) -> str:
    """Return ``line`` with every leading blockquote prefix removed.

    A table may sit inside a blockquote, where its header row and its delimiter
    row both carry a ``>``. The delimiter row is the only thing that marks a
    table, so without peeling the prefix first the table is never recognized and
    its prompts and cell text are scored as prose.
    https://spec.commonmark.org/0.31.2/#block-quotes
    """
    while True:
        match = BLOCK_QUOTE_PREFIX_PATTERN.match(line)
        if match is None:
            return line
        line = line[match.end() :]


def table_row_cells(content: str) -> tuple[tuple[int, str], ...]:
    """Return each cell of one GFM table row as ``(offset, text)``.

    The offsets are into ``content``. A leading pipe is a delimiter rather than
    an empty first cell, and a pipe an author escaped is a pipe the cell holds:
    GFM reads the table before it reads any inline, so ``\\|`` is a cell
    character even where a code span would otherwise claim it.

    The leading pipe is still the leading pipe when the row is indented, and a
    row asked about at character zero counted its own indentation as a first
    cell: a table whose header and delimiter row were indented differently was
    refused outright, and one indented alike was recognized with a column count
    one too high, which is the number a body row's excess cells are measured
    against.

    The leading pipe is a delimiter only up to three columns of indentation,
    which is where GFM lets a table begin. That is the whole of this helper's
    indent rule, and claiming more than it was the defect: the sentence above
    used to end "a fourth is an indented code block and no table row at all",
    and this body parses such a line's cells like any other.

    Both halves of that sentence are wrong here, and the two errors point in
    opposite directions. A row indented four columns is not always code --
    where a paragraph is open above it the line is that paragraph's lazy
    continuation, and ``Intro.`` over a four-space ``| a |`` over ``| - |`` is
    a one-column table on GitHub's own renderer, measured, which the cap above
    refuses by reading the indentation as a cell. And where no paragraph is
    open the line is code and no row at all, which nothing here enforces: a
    pipeless four-space header over a pipeless delimiter row agrees about the
    column count and opens a table this helper never sees a reason to refuse.

    Neither is closed here, because the rule belongs to the paragraph and the
    three walks that look a delimiter row ahead carry no paragraph state --
    ``extract_prose`` carries none at all. What indentation does decide is
    settled where the state already is: ``opens_a_paragraph`` opens no
    paragraph on an indented line, and ``is_table_delimiter`` refuses an
    indented delimiter row.

    The reason a row has to be split at all is that a cell is its own inline
    context. A backtick left unmatched in one cell cannot pair with one in
    another, because the renderer never offers it the chance -- and a scan that
    put every row of a table into one paragraph did offer it, formed a code
    span across the boundary, and masked a real comment between them. Kept
    identical to the helper in the sibling hook.
    https://github.github.com/gfm/#tables-extension-
    """
    cells: list[tuple[int, str]] = []
    indent = len(content) - len(content.lstrip(" "))
    start = indent + 1 if indent < 4 and content[indent:].startswith("|") else 0
    index = start
    while index < len(content):
        if content[index] == "|" and (index == 0 or content[index - 1] != "\\"):
            cells.append((start, content[start:index]))
            start = index + 1
        index += 1
    if start < len(content):
        cells.append((start, content[start:]))
    return tuple(cells)


def table_column_count(content: str) -> int:
    """Return how many cells GFM reads in one table row."""
    return len(table_row_cells(content.rstrip(ASCII_HORIZONTAL_WHITESPACE)))


def table_columns(header: str, delimiter: str) -> int:
    """Return a table's column count, or ``0`` when this is not a table at all.

    A delimiter row under a pipe-bearing line is not enough. GFM: "The header
    row must match the delimiter row in the number of cells. If not, a table
    will not be recognized." A three-cell header over a two-cell delimiter row
    is an ordinary paragraph, so its backticks pair the way a paragraph's do
    and a marker standing between them is inside a code span the renderer
    really does form -- where a scanner that split the line into cells read the
    marker as a real comment and let a document out of its gate on it.

    The count is also what a body row is measured against: "The remainder of
    the table's rows may vary in the number of cells. If a row has fewer cells
    than the header row, empty cells are inserted. If a row has greater, the
    excess is ignored." Cells past the header's count are not on the page, so
    nothing in them is either. Kept identical to the helper in the sibling
    hook.
    https://github.github.com/gfm/#tables-extension-
    """
    count = table_column_count(header)
    return count if count == table_column_count(delimiter) else 0


def is_table_delimiter(line: str) -> bool:
    """Return ``True`` when a line is a Markdown table delimiter row.

    Outer pipe characters are optional in a Markdown table, so ``--- | ---``
    is a delimiter row in the same way that ``| --- | --- |`` is -- and so,
    for a one-column table, is a row with no pipe at all.

    Two lines match the pattern and are still not delimiter rows. Both were
    found by generating rows rather than by enumerating GFM's prose, and both
    were settled against GitHub's own renderer:

    * **A pipeless row is a delimiter row only when it is not also a Setext
      underline.** ``--`` under ``| a |`` is the underline, the heading wins
      and no table forms; ``-:`` under the same header is a one-column table.
      Refusing every pipeless row -- which this helper did, on the ground that
      such a row is a thematic break -- lost the colon-bearing case and kept
      the other by accident.
    * **A row indented four columns is no delimiter row**, whatever else is
      open. ``x`` over a four-space ``-:`` is one paragraph of two lines on
      GitHub's own renderer and ``x`` over a three-space ``-:`` is a table,
      measured; a leading tab reaches column four and does the same. The
      pattern's own ``^ {0,3}`` does not say this, because the ``[ \t]*`` that
      follows the optional pipe absorbs the fourth space, and it counts no tab
      at all.
    * **A row a list item could open is a list item.** ``- |`` matches the
      delimiter pattern and renders as a bullet, because the block parser
      reaches the list before the table extension does.

    Kept identical to the helper in the sibling hooks.
    https://github.github.com/gfm/#tables-extension-
    https://spec.commonmark.org/0.31.2/#setext-headings
    """
    if count_indent_columns(line) >= 4:
        return False
    if TABLE_DELIMITER_PATTERN.match(line) is None:
        return False
    if LIST_ITEM_PATTERN.match(line) is not None:
        return False
    return "|" in line or SETEXT_UNDERLINE_PATTERN.match(line) is None


def table_starts_here(header: str, delimiter: str) -> int:
    """Return the column count of the table ``delimiter`` opens under ``header``.

    Zero where the two lines open none. This is GFM's whole precondition in
    one place -- the delimiter row's own shape, and its agreement with the
    header row about the number of cells -- so that every caller asks one
    question rather than assembling its own. The header needs no pipe of its
    own: ``x`` over ``-:`` is a one-column table on GitHub's own renderer,
    measured rather than assumed.

    What the header may not be is a list item with nothing on its line. A bare
    ``-`` is an empty list item and no paragraph at all, so nothing above the
    delimiter row can be consumed into a table -- and ``LIST_ITEM_PATTERN``
    does not see it, because that pattern wants whitespace after the marker.
    This is the one place the gap shows, so it is named here rather than
    widened there.

    Nor may the header be a line the block grammar has already classified as
    something other than a paragraph. GFM builds a table out of a *paragraph*
    whose last line is followed by a delimiter row, so an ATX heading over
    ``--- | ---`` is a heading and its backticks pair as a heading's do:
    measured on GitHub's own renderer, which paints ``# `a | <!-- x --> `b``
    over ``--- | ---`` as one heading holding one code span, so the marker
    between the backticks is printed rather than read. Splitting it into cells
    exposed the marker and let a session out of its gate on it. A thematic break
    is refused for the same reason and measured the same way.

    **This is the fifth place markdown-it 14.3.0 and the production renderer
    have been measured to part, and the proxy is on the wrong side of it**:
    markdown-it orders its table rule ahead of its heading rule, so it reads the
    same two lines as a table. The indent rule is the residual left standing
    here -- a header indented four columns is an indented code block and this
    helper does not yet say so, because two of the three walks that ask it have
    no paragraph state to condition it on.

    Kept identical to the helper in the sibling hooks.
    https://github.github.com/gfm/#tables-extension-
    """
    if EMPTY_LIST_ITEM_PATTERN.match(header) is not None:
        return 0
    if ATX_HEADING_LINE_PATTERN.match(header) is not None:
        return 0
    if THEMATIC_BREAK_LINE_PATTERN.match(header) is not None:
        return 0
    return table_columns(header, delimiter) if is_table_delimiter(delimiter) else 0


def container_path_ended(line: str, containment_path: tuple[Container, ...]) -> bool:
    """Return whether ``line`` has left the container holding an open block.

    CommonMark ends a leaf block at the end of its containing block, so a block
    opened inside a list item or a blockquote does not run to the end of the
    document once the document outdents past that container. A nonblank line
    that does not peel to the block's container has left it. A blank line has
    left a blockquote, which a blank line ends, but not a list item, where a
    blank line is ordinary content. Kept identical to the helper in the sibling
    hooks. https://spec.commonmark.org/0.31.2/#container-blocks
    """
    _, peeled_count = peel_containers(line, containment_path)
    if peeled_count == len(containment_path):
        return False
    if line.strip(ASCII_HORIZONTAL_WHITESPACE):
        return True
    return containment_path[peeled_count].kind == CONTAINER_KIND_BLOCK_QUOTE


def fence_container_ended(line: str, active_fence: ActiveFence) -> bool:
    """Return whether ``line`` has left the container holding the open fence.

    A fenced block is one of the leaf blocks ``container_path_ended`` speaks
    for; the rule is the container's, not the fence's.
    https://spec.commonmark.org/0.31.2/#fenced-code-blocks
    """
    return container_path_ended(line, active_fence.containment_path)


def parse_opening_fence(line: str) -> tuple[str, int] | None:
    """Return the opening fence marker character and length, if present.

    The info string of a *backtick* fence may not itself contain a
    backtick, so a line whose marker is followed by a code span opens no
    fence: it is an ordinary paragraph. Without this check the checker
    drops every following line until another matching fence or the end of
    the file. A tilde fence carries no such restriction.
    https://spec.commonmark.org/0.31.2/#fenced-code-blocks
    """
    match = FENCE_OPEN_PATTERN.match(line)
    if match is None:
        return None

    marker = match.group("marker")
    if marker[0] == "`" and "`" in line[match.end() :]:
        return None
    return marker[0], len(marker)


def is_closing_fence(line: str, fence_character: str, minimum_length: int) -> bool:
    """Return whether a line closes the active fenced code block.

    CommonMark closes a fenced block only on a fence of the same character that
    is at least as long as the opening fence and that carries nothing but
    spaces or tabs after it. Both parts matter here. This repository documents
    Markdown inside Markdown, so a three-backtick fence often sits inside a
    four-backtick example; a shorter fence must not close the longer one, or
    the example code leaks into the score and the prose after it is dropped.

    Spaces and tabs, and not a whitespace class. Python reads ``\\s`` as Unicode
    whitespace, so a nonbreaking space or a form feed after the backticks closes
    the block here while the renderer keeps every line below it inside the code.
    Measured against markdown-it 14.3.0: a fence followed by U+00A0 does not
    close.
    Kept in step with the sibling hooks.
    https://spec.commonmark.org/0.31.2/#fenced-code-blocks
    """
    closing_pattern = re.compile(
        rf"^ {{0,3}}{re.escape(fence_character)}{{{minimum_length},}}[ \t]*$"
    )
    return closing_pattern.match(line) is not None


def decode_character_references(text: str) -> str:
    """Return ``text`` with every HTML character reference replaced by its character.

    A reference is invisible as written: ``A&nbsp;or&nbsp;B`` is three words on
    the page, and a matcher that never decodes it counts five. Only references
    CommonMark actually recognizes are decoded -- see
    ``CHARACTER_REFERENCE_PATTERN`` for why that is narrower than
    ``html.unescape``.
    """
    return CHARACTER_REFERENCE_PATTERN.sub(replace_character_reference, text)


def replace_character_reference(match: re.Match[str]) -> str:
    """Return the character one matched reference names, or the reference itself."""
    name = match.group("name")
    if name is not None:
        # ``html5`` holds both ``nbsp`` and ``nbsp;``; only the second spelling
        # is a reference CommonMark decodes, so the semicolon is looked up too.
        decoded = html5.get(f"{name};")
        if decoded is None:
            return match.group(0)
    else:
        decimal = match.group("decimal")
        code_point = (
            int(decimal) if decimal is not None else int(match.group("hexadecimal"), 16)
        )
        # CommonMark renders an out-of-range, zero, or surrogate code point as
        # U+FFFD rather than failing.
        decoded = (
            chr(code_point)
            if 0 < code_point < 0x110000 and not 0xD800 <= code_point <= 0xDFFF
            else "\ufffd"
        )
    # A reference may name a line break. One line of the extracted prose is one
    # sentence unit, so a decoded newline becomes a space rather than splitting
    # the unit in two.
    return decoded.replace("\r", " ").replace("\n", " ")


def closing_backtick_run(line: str, start: int, length: int) -> int:
    """Return the end of the next backtick run of exactly ``length``, or -1.

    A code span closes on a run of the same length and on no other, so
    ````the `--strict` flag```` is one span and not two. Scanning run by run
    rather than searching for the substring is what keeps that true: a rule
    that lets a shorter run close a longer one deletes words CommonMark leaves
    visible, which can push a file under the 40-word minimum and out of the
    gate entirely. Kept identical to the helper in
    ``.github/scripts/check-session-structure.py``.
    https://spec.commonmark.org/0.31.2/#code-spans
    """
    index = start
    while index < len(line):
        if line[index] != "`":
            index += 1
            continue
        run_end = index
        while run_end < len(line) and line[run_end] == "`":
            run_end += 1
        if run_end - index == length:
            return run_end
        index = run_end
    return -1


def following_backtick_run(
    lines: Sequence[ParagraphLine], row: int, length: int
) -> tuple[int, int]:
    """Return where a code span opened on ``row`` closes, or ``(-1, -1)``.

    A code span crosses a soft line break: CommonMark closes it on the next run
    of the same length anywhere in the same paragraph. So the search runs on
    past the end of the line and stops where the paragraph does -- which is the
    end of ``lines``, because the caller hands this one paragraph at a time.
    Past that the opening run is literal text and the lines below it are prose
    again. Kept in step with the helper in
    ``.github/scripts/check-session-structure.py``.
    https://spec.commonmark.org/0.31.2/#code-spans
    """
    for next_row in range(row + 1, len(lines)):
        closer = closing_backtick_run(
            lines[next_row].text, lines[next_row].content_start, length
        )
        if closer != -1:
            return next_row, closer
    return -1, -1


def html_block_state(
    content: str,
    containment_path: tuple[Container, ...],
    open_block: ActiveHtmlBlock | None,
    paragraph_open: bool,
) -> tuple[ActiveHtmlBlock | None, ActiveHtmlBlock | None]:
    """Return the state after one line, and the block the line itself is in.

    Two values because they are two questions. The state after the line is what
    the next line inherits; the block the line is *in* is what says whether this
    line is raw HTML, and a block that ends on its own last line is still the
    block that line belonged to.

    ``content`` is the line with its container prefixes already peeled, for the
    reason ``normalize_for_fence_opening`` returns one: CommonMark decides a
    line's block type from what is left once the prefixes are consumed. The
    caller is responsible for ending a block whose container has ended, which it
    does before calling this. Kept identical to the helper in the sibling hooks.
    https://spec.commonmark.org/0.31.2/#html-blocks
    """
    if (
        open_block is not None
        and open_block.condition.end is None
        and not content.strip(ASCII_HORIZONTAL_WHITESPACE)
    ):
        # A blank line closes the conditions that have no end tag, and the
        # blank line is not itself part of the block.
        open_block = None

    if open_block is None:
        # No start condition is tried while a block is open, which is what the
        # spec says and is also what keeps a ``<script>`` line inside an open
        # comment from opening a block that survives the ``-->``.
        for condition in HTML_BLOCK_CONDITIONS:
            if paragraph_open and not condition.interrupts_paragraph:
                continue
            if condition.start.match(content) is not None:
                open_block = ActiveHtmlBlock(
                    condition=condition, containment_path=containment_path
                )
                break

    line_block = open_block
    if open_block is not None and open_block.condition.end is not None:
        if open_block.condition.end.search(content) is not None:
            open_block = None

    return open_block, line_block


def container_interrupts_paragraph(container: Container, content: str) -> bool:
    """Return whether a container opening on a line may interrupt a paragraph.

    A blockquote always may. A list needs two things, and CommonMark states
    them as one rule with two clauses.

    **The item may not be empty.** "In order for a list to interrupt a
    paragraph, the list must not begin with a blank first block." A marker with
    nothing after it is the paragraph's own characters, so ``Words`` then
    ``*`` on the line below is one paragraph of two lines -- and the line after
    *that* is still inside it, which is what keeps a ``<x>`` there from opening
    a type 7 block and hiding the heading under it. ``content`` is the line
    past every container prefix, so a blank one is an empty item.

    **An ordered list must start at 1**, so that a sentence hard-wrapped before
    ``14.`` keeps the number in the sentence instead of turning the rest of the
    document into a list.

    A list that may not interrupt opens nothing at all, and its marker is the
    paragraph's own text. Kept identical to the helper in the sibling hooks.
    https://spec.commonmark.org/0.31.2/#list-items
    """
    if container.kind != CONTAINER_KIND_LIST:
        return True
    if not content.strip(ASCII_HORIZONTAL_WHITESPACE):
        # One marker is an exception and it is an exception for a reason that
        # is not about lists at all: ``-`` with nothing after it is also a
        # level 2 Setext underline, and while a paragraph is open CommonMark
        # reads it as the heading. The heading does start a block, so the
        # answer here is the same one the underline would have given.
        # Measured with markdown-it 14.3.0: ``Words`` over ``-`` is an
        # ``<h2>``, while ``Words`` over ``*`` is one paragraph of two lines.
        return container.bullet == "-"
    return container.ordered_start is None or container.ordered_start == 1


def is_link_reference_definition(content: str) -> bool:
    """Return whether a whole link reference definition fits on this line.

    A definition is a leaf block and not a paragraph: it renders nothing at
    all and leaves no paragraph open below it, which is what lets HTML block
    condition 7 open on the line under it. One may not interrupt a paragraph
    either, so the caller asks this only with nothing open.

    Only the one-line form is read. CommonMark lets the destination sit on the
    line below the label, and this answers ``False`` there -- the liberal side,
    where a paragraph stays open and condition 7 stays shut, which is what the
    whole fallback did before. Kept identical to the helper in the sibling
    hooks.
    https://spec.commonmark.org/0.31.2/#link-reference-definitions
    """
    match = LINK_REFERENCE_DEFINITION_PATTERN.match(content)
    return match is not None and is_link_label(match.group("label"))


def opens_a_paragraph(
    content: str, paragraph_open: bool, previous_content: str = ""
) -> bool:
    """Return whether a line of document text leaves a paragraph open below it.

    ``starts_a_block`` below needs this for the two shapes CommonMark makes
    conditional on an open paragraph. The test is deliberately liberal:
    anything nonblank that is not a heading, a thematic break, a Setext
    underline or a link reference definition leaves a paragraph open. Lines
    inside a fence or a raw-text element never reach here; their caller closes
    the paragraph outright. Kept identical to the helper in the sibling hooks,
    which ask it of HTML block condition 7 as well -- the one condition that
    may not interrupt a paragraph, and a machine this module does not carry.

    The underline needs the state coming in, which is the one thing the line
    alone does not say. ``=====`` under a paragraph is that paragraph's
    heading underline and closes it; ``=====`` with nothing open is an
    ordinary paragraph of its own, and leaves one open below it.

    A link reference definition is the one other leaf block this has to name.
    It is not a paragraph, so a bare tag on the line below it opens the HTML
    block condition 7 that may not interrupt one -- and the liberal fallback
    was holding that block shut and counting a heading the page never shows.

    An indented code block is the fourth shape that needs the state coming in,
    and it is the one the liberal fallback was wrong about in the direction this
    fallback is not allowed to be wrong in. A line indented four columns opens a
    code block only where no paragraph is open; where one is, the line is that
    paragraph's lazy continuation and every rule applies to it. Reading such a
    line as a paragraph held the HTML block condition 7 below it shut and
    counted a ``## Goal`` the page never paints -- measured on GitHub's own
    renderer, which reads a four-space ``x`` over ``<custom>`` over ``## Goal``
    as a code block, an open condition 7 and no heading at all. The indent is
    counted in columns, so a leading tab reaches column four.
    <https://spec.commonmark.org/0.31.2/#indented-code-blocks>

    A table's delimiter row is the third shape that needs the state coming in,
    and it is the Setext underline's twin: it consumes the line above it into
    a table exactly as an underline consumes it into a heading, and leaves no
    paragraph below. ``previous_content`` is that line above, already peeled,
    and is empty when there is none or when the line above sits in a different
    container -- because GFM reads the header row as the line immediately
    above the delimiter row, and the two must agree about the number of cells
    or no table forms at all. Without this the liberal fallback held one
    paragraph open across a whole table, the HTML block condition 7 below it
    was refused, and a ``## Goal`` the page never paints was counted.

    This one is settled against GitHub's own renderer rather than against
    markdown-it 14.3.0, which reads the type-seven tag below a table as a
    *table row* and paints the heading. It is the first place in this module's
    history where the arbiter and the production renderer have been measured
    to part, and the page is what counts.
    https://github.github.com/gfm/#tables-extension-

    ``starts_a_block`` asks the other half of the question -- whether a line
    closes the paragraph *above* it -- and the Setext underline is where the
    two answers part: it closes the one above and opens none below.
    https://spec.commonmark.org/0.31.2/#setext-headings
    """
    if not content.strip(ASCII_HORIZONTAL_WHITESPACE):
        return False
    if not paragraph_open and count_indent_columns(content) >= 4:
        return False
    if ATX_HEADING_LINE_PATTERN.match(content) is not None:
        return False
    if THEMATIC_BREAK_LINE_PATTERN.match(content) is not None:
        return False
    if paragraph_open and SETEXT_UNDERLINE_PATTERN.match(content) is not None:
        return False
    if paragraph_open and table_starts_here(previous_content, content):
        return False
    if not paragraph_open and is_link_reference_definition(content):
        return False
    return True


def starts_a_block(
    content: str,
    containment_path: tuple[Container, ...],
    opened: tuple[Container, ...],
    previous_path: tuple[Container, ...],
    paragraph_open: bool,
    previous_content: str = "",
) -> bool:
    """Return whether a line begins a block rather than continuing the one above.

    This is where a paragraph ends, and therefore where a code span stops
    looking for its closing run. A blank line ends a paragraph, and so do a
    heading, a thematic break and a Setext underline. So does a container: a
    list item that opens on this line is a new block whatever it holds, and a
    line whose container path is neither the path above it nor a prefix of that
    path has left the paragraph. A prefix *is* a continuation -- an unprefixed
    line under a quoted or listed paragraph is the lazy continuation CommonMark
    reads it as, and treating it as a new block would cut a paragraph in half.

    A raw HTML block ends one too, and it is not asked about here: this module
    now runs the same ``HTML_BLOCK_CONDITIONS`` machine its siblings do, and
    the walk that calls this ends its paragraph on any line that machine calls
    raw HTML. Asking again here would be a second, weaker copy of a rule
    already modelled -- which is what the six start patterns that used to sit
    at the bottom of this function were, and they went wrong in the direction
    a partial copy goes wrong: they said where a block *starts* and could not
    say which lines are inside one, so the Markdown inline rules went on
    applying inside a block the renderer passes through untouched.

    All three hooks now ask this question under this name, of the same shapes,
    so none of them can disagree about where a paragraph ends.

    It is not the question ``opens_a_paragraph`` asks above -- that one asks
    whether a paragraph is open *below* a line, which HTML block condition 7
    needs, and a Setext underline is where the two answers part.

    Two of those shapes need the paragraph state, because CommonMark makes both
    of them conditional on one being open. An ordered list may interrupt a
    paragraph only when it starts at 1, so ``2.`` under a sentence is that
    sentence's own text and opens nothing; the rule is the *list's* and not the
    item's, so a ``3.`` under a list already open is its next item and does
    start a block. And a Setext underline may never be a lazy continuation
    line: ``===`` outdented from a quoted or listed paragraph has no root
    paragraph to underline and stays inside the one above it.
    https://spec.commonmark.org/0.31.2/#paragraphs
    https://spec.commonmark.org/0.31.2/#html-blocks
    https://spec.commonmark.org/0.31.2/#list-items
    """
    lazy_continuation = (
        paragraph_open
        and len(containment_path) < len(previous_path)
        and containment_path == previous_path[: len(containment_path)]
    )
    if paragraph_open:
        for offset, container in enumerate(opened):
            if container.kind != CONTAINER_KIND_LIST:
                continue
            if container_interrupts_paragraph(container, content):
                break
            depth = len(containment_path) - len(opened) + offset
            if (
                len(previous_path) > depth
                and previous_path[depth].kind == CONTAINER_KIND_LIST
            ):
                # The list is already open above this line, so this is its
                # next item rather than a new list interrupting anything.
                break
            return False
    if not content.strip(ASCII_HORIZONTAL_WHITESPACE):
        return True
    if ATX_HEADING_LINE_PATTERN.match(content) is not None:
        return True
    if THEMATIC_BREAK_LINE_PATTERN.match(content) is not None:
        return True
    if SETEXT_UNDERLINE_PATTERN.match(content) is not None and not lazy_continuation:
        return True
    if table_starts_here(previous_content, content) and not lazy_continuation:
        # A delimiter row consumes the line above it into a table, which is the
        # Setext underline's rule at a different block. Both halves are needed
        # and for the same reason the underline needs both: this says the
        # paragraph above has ended, and ``opens_a_paragraph`` says none is
        # open below. Answering only the second left ``paragraph_open`` true
        # through ``(paragraph_open and not block_starts)``, and the HTML block
        # condition 7 under the table stayed shut.
        # https://github.github.com/gfm/#tables-extension-
        return True
    if any(container.kind == CONTAINER_KIND_LIST for container in opened):
        return True
    return containment_path != previous_path[: len(containment_path)]


def inline_link_end(line: str, open_index: int) -> int:
    """Return the index just past the ``)`` of an inline link, or -1.

    Neither half of what sits between those parentheses is on the page: the
    destination becomes the element's ``href`` or ``src`` and the title becomes
    its ``title``. Both are scanned as characters rather than as inline
    content, so a backtick inside either opens no code span -- which is the one
    thing this module asks of them. Kept identical to the helper in
    ``.github/scripts/check-session-structure.py``.

    The target may cross a soft line break, so this is given the paragraph's
    joined text rather than one physical line, by both passes. A title holds a
    line ending happily, and so does the whitespace around the destination --
    ``[x](url`` over ``"title")`` is one link -- while the destination itself
    may hold none, bare or angle-bracketed. Those are the three places
    ``LINK_TARGET_WHITESPACE`` is spelled and the one place it is not.

    A backslash escapes the character after it, and in a *bare* destination a
    line ending is the one character it cannot escape: ``\\`` at the end of a
    line is a hard line break there. Reading it as an escape let a target
    swallow the break and close on a parenthesis two lines down that the
    production renderer never reached -- which the two hooks answered
    differently, because one of them strips a line's trailing spaces and the
    other does not, and the backslash only lands against the line ending once
    the space behind it is gone. Inside ``<...>`` the rule is the other way and
    both renderers agree on it, so the escape there is unconditional; the
    difference is measured rather than reasoned and is written at each of the
    two loops.

    A bare destination ends at every character in
    ``DESTINATION_STOP_CHARACTERS``: the space and the ASCII control
    characters, which is the set CommonMark forbids it. An unbalanced
    parenthesis and an unclosed title each mean no link at all, and the caller
    is then right to read the characters as ordinary text.
    https://spec.commonmark.org/0.31.2/#links
    """
    length = len(line)
    index = open_index + 1
    while index < length and line[index] in LINK_TARGET_WHITESPACE:
        index += 1

    if index < length and line[index] == "<":
        cursor = index + 1
        while cursor < length and line[cursor] not in "<>\n":
            # A backslash escapes whatever follows it here, the line ending
            # included: both renderers read ``<\`` over ``` `> ``` as one
            # destination and put a ``%0A`` in the href. An *unescaped* line
            # ending is what ends the attempt, which is why it is in the set
            # above and not in this one.
            cursor += 2 if line[cursor] == "\\" else 1
        if cursor >= length or line[cursor] != ">":
            return -1
        index = cursor + 1
    else:
        depth = 0
        while index < length:
            character = line[index]
            if character == "\\":
                index += 1 if line[index + 1 : index + 2] == "\n" else 2
                continue
            if character in DESTINATION_STOP_CHARACTERS:
                break
            if character == "(":
                depth += 1
            elif character == ")":
                if depth == 0:
                    break
                depth -= 1
            index += 1
        if depth != 0:
            return -1

    spaced = index
    while spaced < length and line[spaced] in LINK_TARGET_WHITESPACE:
        spaced += 1
    if index < spaced < length and line[spaced] in "\"'(":
        opener = line[spaced]
        closer = {'"': '"', "'": "'", "(": ")"}[opener]
        cursor = spaced + 1
        while cursor < length and line[cursor] != closer:
            # A parenthesised title may hold a parenthesis only backslashed, so
            # a second ``(`` is not title text: it means no link at all, and the
            # characters are the ones the author typed. This is the rule
            # ``reference_title_span`` already spells for a definition's title,
            # and the two are the same construct.
            # https://spec.commonmark.org/0.31.2/#link-title
            if line[cursor] == opener == "(":
                return -1
            cursor += 2 if line[cursor] == "\\" else 1
        if cursor >= length:
            return -1
        index = cursor + 1

    while index < length and line[index] in LINK_TARGET_WHITESPACE:
        index += 1
    return index + 1 if index < length and line[index] == ")" else -1


def matching_bracket(line: str, open_index: int) -> int:
    """Return the index of the ``]`` closing the ``[`` at ``open_index``, or -1.

    Kept identical to the helper in
    ``.github/scripts/check-session-structure.py``.
    """
    depth = 0
    index = open_index
    while index < len(line):
        character = line[index]
        if character == "\\":
            index += 2
            continue
        if character == "[":
            depth += 1
        elif character == "]":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    return -1


def normalize_link_label(label: str) -> str:
    """Return a link label in the form CommonMark matches definitions by.

    The blanks a label folds are the ones ``_LINK_LABEL_BLANK`` names, which is
    the set markdown-it 14.3.0 trims and collapses -- and neither ``str.split``
    nor Python's whitespace class is that set. Measured both ways, one character
    at a time: ``[a\u0085b]`` and ``[a b]`` are two labels to the renderer and
    one to ``str.split``, while ``[a\ufeffb]`` and ``[a b]`` are one label to the
    renderer and two to ``str.split``. Whether a reference resolves decides
    whether its label is rendered away or printed as the brackets the author
    typed, and a marker inside printed brackets is a comment on the page.
    <https://spec.commonmark.org/0.31.2/#matches>

    Kept identical to the helper in
    ``.github/scripts/check-session-structure.py``.
    """
    return _LINK_LABEL_BLANK_RUN.sub(" ", label).strip(" ").casefold()


def is_link_label(label: str) -> bool:
    """Return whether ``label`` is short enough to be a link label at all.

    Kept identical to the helper in
    ``.github/scripts/check-session-structure.py``.
    """
    return len(label) <= LINK_LABEL_MAXIMUM_CHARACTERS


def raw_html_run_end(line: str, index: int) -> int:
    """Return where the raw HTML run opened at ``index`` ends, or ``-1``.

    A comment, a processing instruction, a declaration and a CDATA section are
    the four raw HTML productions whose content is characters rather than
    inline content. What sits inside one is data: a ``[`` there opens no link,
    a backtick opens no code span, and a ``<!--`` begins no second comment.

    Only a run that closes on this line is reported. This helper reads one line
    because its caller does, and a run that crosses a soft line break is the
    caller's recorded limit rather than this one's; answering ``-1`` there
    leaves the characters to be read as text, which is what they are when the
    run never closes at all. Kept identical to the helper in the sibling hook.
    <https://spec.commonmark.org/0.31.2/#raw-html>
    """
    for opener, closer in RAW_HTML_INLINE_RUNS:
        match = opener.match(line, index)
        if match is None:
            continue
        end = line.find(closer, match.end())
        if end == -1:
            return -1
        return end + len(closer)
    return -1


def link_reference_definition_region(line: str) -> tuple[int, int] | None:
    """Return the region a whole-line link reference definition renders nothing in.

    ``None`` where the line is not one. This is the one region the metadata
    walk finds that is *not* an inline construct: a definition is a block, it
    is anchored at the start of its line and it ends at the end of it, so it is
    the one region that has to keep being asked a line at a time while the
    inline questions are asked of the paragraph. Its two callers are
    ``link_metadata_regions`` and the walk that gathers a paragraph for it, and
    they share this so there is one spelling of the rule. Kept identical to the
    helper in the sibling hook.
    https://spec.commonmark.org/0.31.2/#link-reference-definitions
    """
    definition = LINK_REFERENCE_DEFINITION_PATTERN.match(line)
    if definition is None or not is_link_label(definition.group("label")):
        return None
    return (0, len(line))


def link_metadata_regions(
    line: str, defined_labels: frozenset[str]
) -> tuple[tuple[int, int], ...]:
    """Return the ranges on one line that render as metadata rather than as text.

    A link's destination and title, an image's alt text, a reference label the
    document defines, and a link reference definition end to end all become an
    attribute of an element or nothing at all. A marker inside one of those is
    not a comment and declares nothing. A *link's* text is deliberately not
    here: it is inline content, and markdown-it 14.3.0 renders a comment inside
    it as a comment.

    Links may not nest, so forming one deactivates every link opener still on
    the stack. That is not a nicety. ``[a [b](u.md) c](v.md "<!-- x -->")``
    renders with the marker visible, because the inner link wins and the outer
    brackets are literal text; a pass that matched brackets naively hid a real
    marker and then took a child-facing document out of the reading gate as
    though it had declared itself adult-facing. Kept identical to the helper in
    ``.github/scripts/check-session-structure.py``.
    https://spec.commonmark.org/0.31.2/#links
    """
    definition = link_reference_definition_region(line)
    if definition is not None:
        return (definition,)

    regions: list[tuple[int, int]] = []
    openers: list[tuple[int, bool, bool]] = []
    index = 0
    length = len(line)

    while index < length:
        character = line[index]
        if character == "\\":
            index += 2
            continue
        if character == "<":
            # A bracket inside raw HTML is not a link opener. CommonMark reads
            # an attribute value and an autolink's destination as data, so
            # ``<span title="[">text](url "<!-- x -->")`` holds no link at all
            # and the marker in the parentheses is a comment the page prints.
            # Recording the attribute's bracket masked that marker as a link
            # target. Raw HTML has six productions and a bracket is data in
            # every one of them, so all six are asked about here: a comment, a
            # processing instruction, a declaration and a CDATA section first,
            # because none of the four can also be an autolink or a tag, then
            # an autolink before a tag -- a tag name may not hold a colon and a
            # URI autolink must, so only one of those two can match.
            # ``Text <!--[-->text](u "<!-- audience: adult -->")`` holds no
            # link either, and the marker in the parentheses is a real one.
            # <https://spec.commonmark.org/0.31.2/#raw-html>
            run_end = raw_html_run_end(line, index)
            if run_end != -1:
                index = run_end
                continue
            autolink = AUTOLINK_PATTERN.match(line, index)
            if autolink is not None:
                index = autolink.end()
                continue
            tag = INLINE_HTML_TAG_PATTERN.match(line, index)
            if tag is not None:
                index = tag.end()
                continue
        if line.startswith("![", index):
            openers.append((index, True, True))
            index += 2
            continue
        if character == "[":
            openers.append((index, False, True))
            index += 1
            continue
        if character != "]" or not openers:
            index += 1
            continue

        opener, is_image, is_active = openers.pop()
        after = index + 1
        text_start = opener + (2 if is_image else 1)
        metadata: tuple[int, int] | None = None
        consumed = after

        if after < length and line[after] == "(":
            end = inline_link_end(line, after)
            if end != -1:
                metadata, consumed = (after, end), end
        elif after < length and line[after] == "[":
            label_close = matching_bracket(line, after)
            if label_close != -1:
                label = line[after + 1 : label_close] or line[text_start:index]
                # The length bound is the label's own, before folding: a
                # reference whose label is too long is no reference at all,
                # however the definition spells itself. Matching first and
                # bounding never let a 1,001-character label resolve, and the
                # construct it resolved into was an image -- whose description
                # is an attribute, so a comment written there stopped being a
                # comment and the document left its gate on alt text.
                if is_link_label(label) and normalize_link_label(label) in defined_labels:
                    metadata, consumed = (after, label_close + 1), label_close + 1
        elif is_link_label(line[text_start:index]) and (
            normalize_link_label(line[text_start:index]) in defined_labels
        ):
            metadata, consumed = (after, after), after

        if metadata is None or not is_active:
            index = after
            continue

        if is_image:
            # The alt text is an attribute, so the whole construct goes.
            regions.append((opener, consumed))
        else:
            if metadata[0] != metadata[1]:
                regions.append(metadata)
            openers[:] = [
                (start, image, image and active) for start, image, active in openers
            ]
        index = consumed

    return tuple(regions)


def reference_title_span(lines: Sequence[str], row: int, index: int) -> int:
    """Return how many lines the definition title opening at ``index`` fills.

    Zero where no title opens there or none closes. CommonMark puts no line
    bound on a title: ``"first`` on one line and ``second"`` on the next is one
    title carrying a line ending, and both renderers resolve the definition
    that holds it. A line-local match refused the whole definition, the label
    was never defined, and the ``![<!-- audience: adult -->][x]`` below it --
    which the page renders as an image's description, where a marker is
    attribute data -- was read as a comment the child's page carried.

    Three rules bound it and each was measured on both renderers. A blank line
    ends the block, so a title reaching one closes nothing. Anything but
    whitespace after the closing delimiter makes the whole construct a
    paragraph rather than a definition. And an unescaped ``(`` inside a
    parenthesised title is not allowed, which is why ``(a`` / ``(b)`` / ``c)``
    is prose on both. Kept identical to the helper in the sibling hook.
    https://spec.commonmark.org/0.31.2/#link-reference-definitions
    """
    line = lines[row] if row < len(lines) else ""
    opener = line[index] if 0 <= index < len(line) else ""
    closer = LINK_REFERENCE_TITLE_DELIMITERS.get(opener)
    if closer is None:
        return 0
    position = index + 1
    offset = 0
    while row + offset < len(lines):
        line = lines[row + offset]
        if offset and not line.strip(ASCII_HORIZONTAL_WHITESPACE):
            return 0
        while position < len(line):
            character = line[position]
            if character == "\\":
                position += 2
                continue
            if character == closer:
                rest = line[position + 1 :]
                if rest.strip(ASCII_HORIZONTAL_WHITESPACE):
                    return 0
                return offset + 1
            if character == opener == "(":
                return 0
            position += 1
        offset += 1
        position = 0
    return 0


def reference_title_line_span(lines: Sequence[str], row: int) -> int:
    """Return how many lines a title beginning on its own line ``row`` fills.

    Zero where that line opens no title. This is the multi-line generalization
    of a pattern anchored to one line, and it subsumes it: a title that closes
    where it opened returns ``1``. Kept identical to the helper in the sibling
    hook.
    """
    line = lines[row] if row < len(lines) else ""
    start = len(line) - len(line.lstrip(ASCII_HORIZONTAL_WHITESPACE))
    return 0 if start == len(line) else reference_title_span(lines, row, start)


def reference_title_opens_at(line: str, after: int) -> int:
    """Return where a title opens after a destination ending at ``after``.

    ``-1`` where the characters between are not a run of spaces or tabs
    followed by a title delimiter. CommonMark requires at least one blank
    between a destination and its title. Kept identical to the helper in the
    sibling hook.
    """
    index = after
    while index < len(line) and line[index] in ASCII_HORIZONTAL_WHITESPACE:
        index += 1
    if index == after or index >= len(line):
        return -1
    return index if line[index] in LINK_REFERENCE_TITLE_DELIMITERS else -1


def reference_definition_span(lines: Sequence[str], index: int) -> int:
    """Return how many lines the link reference definition at ``index`` fills.

    Zero where there is none. CommonMark lets the destination sit on the line
    after the label, and the title on the line after the destination, and the
    whole construct renders nothing at all. The longest form that parses
    exactly is the one taken, because that is what the renderer does. Kept
    identical to the helper in
    ``.github/scripts/check-session-structure.py``.
    https://spec.commonmark.org/0.31.2/#link-reference-definitions
    """

    def line_at(offset: int) -> str:
        position = index + offset
        return lines[position] if position < len(lines) else ""

    label_line = LINK_REFERENCE_LABEL_LINE_PATTERN.match(line_at(0))
    if label_line is not None and is_link_label(label_line.group("label")):
        destination = LINK_REFERENCE_DESTINATION_LINE_PATTERN.match(line_at(1))
        if destination is not None:
            if destination.group("title") is None:
                title = reference_title_line_span(lines, index + 2)
                if title:
                    return 2 + title
            return 2
        head = LINK_REFERENCE_DESTINATION_HEAD_PATTERN.match(line_at(1))
        if head is None:
            return 0
        opens = reference_title_opens_at(line_at(1), head.end())
        title = reference_title_span(lines, index + 1, opens)
        return 1 + title if title else 0

    definition = LINK_REFERENCE_DEFINITION_PATTERN.match(line_at(0))
    if definition is not None and is_link_label(definition.group("label")):
        if definition.group("title") is None:
            title = reference_title_line_span(lines, index + 1)
            if title:
                return 1 + title
        return 1

    head = LINK_REFERENCE_DEFINITION_HEAD_PATTERN.match(line_at(0))
    if head is None or not is_link_label(head.group("label")):
        return 0
    opens = reference_title_opens_at(line_at(0), head.end())
    return reference_title_span(lines, index, opens)


def collect_reference_labels(
    contents: Sequence[str], starts: Sequence[bool]
) -> frozenset[str]:
    """Return every link label the document defines, normalized.

    A label is defined only where a whole definition parses. CommonMark wants a
    destination for that, so ``[x]:`` with a line of prose under it defines
    nothing at all: the brackets stay on the page, a reference to ``x`` below
    them is the characters the author typed, and a marker inside one of those
    is a comment the child's page really carries.

    The lines a definition fills are skipped with it, so a destination or a
    title sitting on its own line is never read as a second label. A line
    inside a fenced block enters this walk empty, which no part of a definition
    matches.

    And a definition may not interrupt a paragraph, so this walk carries the
    paragraph state rather than reading every line alike. ``Intro text.`` above
    ``[x]: /url`` defines nothing on either renderer -- the two lines are one
    paragraph and the brackets stay on the page -- while the walk defined ``x``
    anyway, and the ``![<!-- audience: adult -->][x]`` below it then read as
    resolved image metadata rather than as the comment the page really carries.
    An adult-facing document went through the child gate on it.

    ``opens_a_paragraph`` is the same helper the document walk uses, and it
    already knows that a definition is a leaf block rather than a paragraph, so
    definitions written one under another all define. ``starts`` is that same
    walk's own ``starts_a_block`` answer for each line, carried here rather than
    recomputed, because a paragraph also ends where the container changes and
    this walk has no container of its own. ``Intro`` over ``> [x]: /url``
    defines ``x`` on both renderers -- the blockquote interrupts the paragraph
    -- and without the flag the walk held the paragraph open, defined nothing,
    and read the ``![<!-- audience: adult -->][x]`` below it as a comment the
    page never carries. The other direction is already right and stays right:
    ``> Intro`` over an unquoted ``[x]: /url`` is the lazy continuation
    CommonMark reads it as, defines nothing, and ``starts_a_block`` says so.

    What is left is ``previous_content``, which is the line above as it stands
    rather than as it peels. It is consulted only for the table rule. Kept
    identical to the helper in
    ``.github/scripts/check-session-structure.py``.
    https://spec.commonmark.org/0.31.2/#link-reference-definitions
    """
    labels: set[str] = set()
    paragraph_open = False
    previous_content = ""
    row = 0

    while row < len(contents):
        content = contents[row]
        if starts[row]:
            paragraph_open = False
            previous_content = ""
        if not paragraph_open:
            span = reference_definition_span(contents, row)
            if span:
                match = LINK_REFERENCE_LABEL_PATTERN.match(content)
                if match is not None:
                    labels.add(normalize_link_label(match.group("label")))
                row += span
                previous_content = ""
                continue
        paragraph_open = opens_a_paragraph(content, paragraph_open, previous_content)
        previous_content = content
        row += 1

    return frozenset(labels)


def following_comment_end(
    lines: Sequence[ParagraphLine], row: int, index: int
) -> tuple[int, int]:
    """Return where the comment opened at ``index`` closes, or ``(-1, -1)``.

    A comment crosses a soft line break the way a code span does, and it ends
    where the paragraph ends: an unclosed ``<!--`` is not a comment at all, so
    the caller is right to read the characters after it as ordinary text.
    """
    closer = lines[row].text.find("-->", index + len("<!--"))
    if closer != -1:
        return row, closer + len("-->")
    for next_row in range(row + 1, len(lines)):
        closer = lines[next_row].text.find("-->", lines[next_row].content_start)
        if closer != -1:
            return next_row, closer + len("-->")
    return -1, -1




def following_tag_end(
    lines: Sequence[ParagraphLine], row: int, index: int
) -> tuple[int, int]:
    """Return where the tag opened at ``index`` closes, or ``(-1, -1)``.

    CommonMark lets an open tag hold a line ending, in the whitespace between
    attributes and inside a quoted attribute value, so a tag crosses a soft
    line break the way a comment does and ends where the paragraph does. One
    that never closes is no tag at all, and the caller is then right to read
    its characters as text. Kept in step with the helper in
    ``.github/scripts/check-session-structure.py``.
    https://spec.commonmark.org/0.31.2/#raw-html
    """
    prefix = html_tag_prefix(lines[row].text, index)
    if prefix is None:
        return -1, -1
    for next_row in range(row + 1, len(lines)):
        start = lines[next_row].content_start
        position, prefix, matched = html_tag_continue(prefix, lines[next_row].text[start:])
        if not matched:
            return -1, -1
        if prefix is None:
            return next_row, start + position
    return -1, -1


def following_link_end(
    lines: Sequence[ParagraphLine], row: int, index: int
) -> tuple[int, int]:
    """Return where the link target opened at ``index`` closes, or ``(-1, -1)``.

    A link's target crosses a soft line break the way a comment and a tag do.
    Its destination may hold no line ending, but the whitespace around the
    destination may hold one and a title may hold as many as the paragraph
    has: ``[x](url "title`` over ``continued")`` is one link with one title,
    measured on markdown-it 14.3.0 and on GitHub's own renderer. A first pass
    that read one physical line rejected that target, left the backtick inside
    the title standing as ordinary text, and paired it with a backtick further
    down -- so a real ``audience: adult`` comment between them was read as a
    code span and a child-facing document was taken out of the reading gate.

    The rows are joined with the line endings they had and handed to
    ``inline_link_end``, which is the same helper the second pass already runs
    over the same joined text: there is one grammar here and not two. One that
    never closes is no link at all, and the caller is then right to read its
    characters as text. Kept in step with the helper in
    ``.github/scripts/check-session-structure.py``.
    https://spec.commonmark.org/0.31.2/#links
    """
    joined = lines[row].text[index:]
    starts = [0]
    for next_row in range(row + 1, len(lines)):
        starts.append(len(joined) + 1)
        joined += "\n" + lines[next_row].text[lines[next_row].content_start :]
    end = inline_link_end(joined, 0)
    if end == -1:
        return -1, -1
    for offset in range(len(starts) - 1, -1, -1):
        if end > starts[offset]:
            if offset == 0:
                return row, index + end
            closing = lines[row + offset]
            return row + offset, closing.content_start + end - starts[offset]
    return -1, -1


def following_raw_html_end(
    lines: Sequence[ParagraphLine], row: int, index: int
) -> tuple[int, int]:
    """Return where the raw HTML run opened at ``index`` closes, or ``(-1, -1)``.

    A processing instruction, a declaration and a CDATA section are raw HTML:
    what sits between their delimiters is characters the renderer passes
    through, so a backtick in one opens no code span and a ``<!--`` in one
    begins no comment. Each crosses a soft line break the way a comment does
    and ends where the paragraph does; one that never closes is not raw HTML
    at all, and the caller is then right to read its characters as text. Kept
    in step with the helper in
    ``.github/scripts/check-session-structure.py``.
    https://spec.commonmark.org/0.31.2/#raw-html
    """
    line = lines[row].text
    for opener, closer in RAW_HTML_RUN_PATTERNS:
        match = opener.match(line, index)
        if match is None:
            continue
        found = line.find(closer, match.end())
        if found != -1:
            return row, found + len(closer)
        for next_row in range(row + 1, len(lines)):
            found = lines[next_row].text.find(closer, lines[next_row].content_start)
            if found != -1:
                return next_row, found + len(closer)
        return -1, -1
    return -1, -1


def comment_open_below(content: str, position: int) -> str | None:
    """Return ``COMMENT_RUN`` when a comment is still open past ``position``.

    A comment is the one run in ``RAW_TEXT_RUNS`` that can close and open again
    on a single line, so the line has to be walked rather than tested once:
    ``<!-- one --> words <!-- two`` opens a block comment, ends it, and leaves a
    second one open below. Reading only the first delimiter pair answered "no
    run open" there, and a ``<textarea>`` on the next line then opened a run
    inside a comment the page never shows -- so a ``TBD`` written in that
    comment was reported as a placeholder.
    Kept identical to the helper in the sibling hooks.
    https://spec.commonmark.org/0.31.2/#html-blocks
    """
    while True:
        start = content.find("<!--", position)
        if start == -1:
            return None
        end = content.find("-->", start + len("<!--"))
        if end == -1:
            return COMMENT_RUN
        position = end + len("-->")


def raw_text_run_state(
    content: str, open_run: str | None, opens_html_block: bool
) -> tuple[str | None, str | None]:
    """Return the raw HTML run open below a line, and the run the line is in.

    Two values because they are two questions, the pair ``html_block_state``
    asks in the same shape: what the next line inherits, and which run this
    line's characters belong to. A line carrying the closing delimiter is still
    the run's last line, and so is a line carrying both delimiters:
    ``<script><!-- no-source-check: offline --></script>`` holds script data
    rather than a comment, and answering "no run at all" for that line let every
    caller read the body as markup and honour the marker written in it.

    ``opens_html_block`` is whether CommonMark reads this line as part of a raw
    HTML block, and a run may open only where one does. These are the *block*
    forms of raw HTML, so a line that CommonMark keeps inside the paragraph
    above it opens no run: ``<xmp>`` and ``<noembed>`` are in neither HTML block
    condition 1 nor condition 6, so a bare opener on its own line is condition 7
    and may not interrupt a paragraph -- and an ``<xmp>`` written inside an open
    HTML comment therefore opens nothing, while a ``<script>`` written in the
    same place opens condition 1, ends the paragraph, and really does hold raw
    text. Answering that from the element name alone got both of those wrong in
    opposite directions. The caller passes ``line_html_block is not None``.

    The run is returned rather than a bare "yes, this is text" because the two
    callers ask two different things of it. Whether the characters are text
    rather than markup is ``raw_text_run_holds_text`` below, and every hook
    asks it. Whether the page *paints* that text is a second question, asked
    only where a reading score is computed, and it is answered per element
    from the HTML Standard's own rendering rules rather than from this set.

    An opener line is the run's own first line, whether the run closes on it
    or below it. ``<script><!-- no-source-check: offline -->`` with its closer
    two lines down holds script data on that first line exactly as it does on
    the next, and answering "no run here" for the opener let every caller read
    the body as markup. The two branches were settled one round apart, and why
    the second waited is worth recording: returning the run for *every* line
    was scored and rejected because it would have left a run open below a line
    that already closed it. That objection is about the branch above, where
    ``closing`` is found; in this branch the run really is open below, so the
    line and the state agree.

    An open comment is carried in the same state and is the one run whose
    content is markup: a marker inside a comment is the comment it looks like,
    which is why ``raw_text_run_holds_text`` answers ``False`` for it. It is
    tracked so that a ``<script>`` line written inside a comment opens no run of
    its own -- and so that a run and a comment can never both be open, which is
    what lets a caller strip comments and classify runs in one fixed order
    instead of an order each caller chose for itself.

    The same field carries a third thing, and it is neither a run nor a comment:
    an end tag that has started and not finished. ``</script title="`` ends the
    element's raw text and leaves an HTML parser inside a tag, where the lines
    below are attribute data until the tag's own ``>`` arrives --
    ``closing_tag_run`` spells that state and ``closing_tag_state`` reads it
    back. It is in this field rather than beside it for the reason the comment
    is: three states that exclude one another are one state, and a caller that
    held them apart would have to choose an order to ask them in.
    Kept identical to the helper in the sibling hooks.
    https://html.spec.whatwg.org/multipage/parsing.html#rawtext-state
    """
    below, line_run, _ = raw_text_run_boundary(content, open_run, opens_html_block)
    return below, line_run


def raw_text_content_start(content: str, match: "re.Match[str]", key: str) -> int:
    """Return where a raw-text run's *content* begins on its opening line.

    A run opened by one of the eight element names begins after that element's
    own start tag, and an HTML parser reads the whole tag -- name, attributes,
    quoted values and all -- before it enters raw text. So the end-tag spelling
    written inside a quoted attribute value is data:
    ``<script title="</script>">`` opens a run that never closes, and every
    line below it to the end of the file is script data. The other four runs --
    a processing instruction, a CDATA section, a declaration and a comment --
    have no tag to read, so their content begins where their opener ends.

    Measured against ``html.parser``, and this is a place where the two layers
    part company on purpose. CommonMark's HTML block condition 1 ends on a line
    that *contains* ``</script>``, so markdown-it 14.3.0 ends the Markdown block
    on that line and writes an ``<h2>`` under it -- and the page never paints
    that heading, because the browser is still in script data. The block is
    CommonMark's and the run is the page's, and this helper answers for the
    run. Kept identical to the helper in the sibling hooks.
    https://html.spec.whatwg.org/multipage/parsing.html#rawtext-state
    """
    if key not in RAW_TEXT_ELEMENT_NAMES:
        return match.end()
    start_tag = RAW_TEXT_START_TAG_PATTERN.match(content, match.start())
    return match.end() if start_tag is None else start_tag.end()


def html_tag_close(content: str, index: int) -> int:
    """Return the offset past the ``>`` closing a tag whose name ended at ``index``.

    ``-1`` where the tag does not close in ``content``. This is HTML5's own
    tag-state machine and not a search for a ``>``, because the two give
    different answers and the page follows the machine: a ``>`` written inside a
    quoted attribute value is attribute data, so ``</script title="> x">``
    closes at the *last* ``>`` and not the first. Searching for the character
    ended the tag inside the value and handed the rest of it back to the
    caller as though a reader saw it -- which let a comment spelled in an
    attribute grant an exemption the page never carried.

    The quote characters only open a value after ``=``: HTML5 reads the ``"``
    in ``</script a"b>`` as part of the attribute *name*, so a scanner that
    treated every quote as a delimiter would run past the tag's real end. The
    states below are the spec's, named as the spec names them, and the helper
    is measured against ``html.parser`` rather than reasoned about. Kept
    identical to the helper in the sibling hooks.
    A tag may also *not* end on the line it starts on, and the machine then has
    to be resumed rather than restarted: a line ending inside a quoted attribute
    value is value data, and a line ending between attributes is whitespace.
    ``html_tag_close_state`` is that machine and this is the one-line reading of
    it. Kept identical to the helper in the sibling hooks.
    https://html.spec.whatwg.org/multipage/parsing.html#tag-open-state
    """
    return html_tag_close_state(content, index, TAG_STATE_START)[0]


def html_tag_close_state(content: str, index: int, state: str) -> tuple[int, str]:
    """Return where a tag resumed at ``state`` ends, and the state it ends in.

    The offset is ``-1`` where the tag does not close in ``content``, and the
    second value is then the state the next line has to resume from. This is
    ``html_tag_close``'s own machine with its entry state made a parameter and
    its exit state reported, so that an end tag spanning lines is read as one
    tag: ``</script title="`` leaves the machine inside a double-quoted value,
    and every character on the lines below it -- a ``<!--`` included -- is that
    value's data until the quote closes. Kept identical to the helper in the
    sibling hooks.
    https://html.spec.whatwg.org/multipage/parsing.html#tag-open-state
    """
    position = index
    while position < len(content):
        character = content[position]
        if state in ("before-attribute-name", "after-attribute-value"):
            if character == ">":
                return position + 1, state
            if character in HTML_TAG_WHITESPACE or character == "/":
                position += 1
                continue
            state = "attribute-name"
            # An ``=`` here is a parse error and becomes the *name*, which is
            # the one character this state may not hand to the state below:
            # reconsumed as a name character it would open a value, and
            # ``</script ="><!-- ... -->`` then lost the ``>`` that ends the
            # tag. Every other character is reconsumed.
            if character == "=":
                position += 1
            continue
        if state == "attribute-name":
            if character == ">":
                return position + 1, state
            if character == "=":
                state = "before-attribute-value"
            elif character in HTML_TAG_WHITESPACE:
                state = "after-attribute-name"
            elif character == "/":
                state = "before-attribute-name"
        elif state == "after-attribute-name":
            if character == ">":
                return position + 1, state
            if character == "=":
                state = "before-attribute-value"
            elif character in HTML_TAG_WHITESPACE:
                pass
            elif character == "/":
                state = "before-attribute-name"
            else:
                state = "attribute-name"
        elif state == "before-attribute-value":
            if character == ">":
                return position + 1, state
            if character == '"':
                state = "attribute-value-double-quoted"
            elif character == "'":
                state = "attribute-value-single-quoted"
            elif character in HTML_TAG_WHITESPACE:
                pass
            else:
                state = "attribute-value-unquoted"
        elif state == "attribute-value-double-quoted":
            if character == '"':
                state = "after-attribute-value"
        elif state == "attribute-value-single-quoted":
            if character == "'":
                state = "after-attribute-value"
        else:  # attribute-value-unquoted
            if character == ">":
                return position + 1, state
            if character in HTML_TAG_WHITESPACE:
                state = "before-attribute-name"
        position += 1
    return -1, state


def raw_text_run_tail(content: str, closer_end: int, key: str) -> int:
    """Return where a closed raw-text run stops holding the line's characters.

    The eight element closers are spelled ``</name`` with a lookahead, so that
    ``</script/`` and ``</script foo>`` close the run as an HTML parser closes
    it. That match ends at the name, and the *tag* ends at its ``>``, so the
    characters a reader sees begin one character further on. The other four
    runs carry their whole delimiter in the match -- ``?>``, ``]]>``, ``>``,
    ``-->`` -- and end where it ends.

    Where the end tag does not close on this line at all, the line has no tail:
    every character after ``</name`` is the tag's own, and handing them back
    read ``</script title="a`` as words a child sees and as a place a comment
    could stand. The other reading -- hand the rest of the line back, which is
    what this helper did before -- was built rather than argued about, and put
    to a generator of 1,536 end tags: it disagrees with ``html.parser`` on 12
    rows against this form's 8, at the same instrument score and the same
    suites.

    Handing the whole line back is only half of what an unfinished end tag
    needs. The other half is the state *below* it, which is
    ``raw_text_run_boundary``'s: an HTML parser goes on reading the tag on the
    lines below, and a comment may not open inside one. Kept identical to the
    helper in the sibling hooks.
    https://html.spec.whatwg.org/multipage/parsing.html#end-tag-open-state
    """
    if key not in RAW_TEXT_ELEMENT_NAMES:
        return closer_end
    tag_end = html_tag_close(content, closer_end)
    return len(content) if tag_end == -1 else tag_end


def closing_tag_run(state: str) -> str:
    """Return the run state an end tag left half-read at ``state`` carries.

    Kept identical to the helper in the sibling hooks.
    """
    return CLOSING_TAG_RUN_PREFIX + state


def closing_tag_state(run: str | None) -> str | None:
    """Return the tag state ``run`` carries, or ``None`` where it carries none.

    Kept identical to the helper in the sibling hooks.
    """
    if run is None or not run.startswith(CLOSING_TAG_RUN_PREFIX):
        return None
    return run[len(CLOSING_TAG_RUN_PREFIX) :]

def raw_text_run_boundary(
    content: str, open_run: str | None, opens_html_block: bool
) -> tuple[str | None, str | None, int]:
    """Return a line's raw HTML run state, and where the run ends on this line.

    The first two values are ``raw_text_run_state``'s, unchanged and documented
    there. The third is the offset just past the run's closing delimiter when
    the run closes on this line, and ``-1`` when it does not.

    That third value exists because a run closing is not the same event as a
    line ending. ``<script></script> We plan the trip together`` holds an empty
    script and then twelve words a child reads, and a caller that dropped the
    whole line dropped the words with it -- enough of them to take a document
    under the scoring floor and out of the gate in silence. Only the prose
    extractor asks, for the same reason only it asks
    ``raw_text_run_is_displayed``: the two marker scans care that the
    characters are not markup, and not where the reader's part of the line
    starts. Kept identical to the helper in the sibling hooks.
    https://html.spec.whatwg.org/multipage/parsing.html#rawtext-state
    """
    if open_run is not None:
        pending = closing_tag_state(open_run)
        if pending is not None:
            # The line is the middle of an end tag that began above it. A tag
            # holds a line ending the way it holds a space -- inside a quoted
            # value it is value data -- so the machine is resumed at the state
            # the line above left it in, with that line ending fed to it.
            end, below = html_tag_close_state(content + "\n", 0, pending)
            if end == -1:
                return closing_tag_run(below), open_run, -1
            end = min(end, len(content))
            return comment_open_below(content, end), open_run, end
        closer = RAW_TEXT_CLOSERS[open_run].search(content)
        if closer is None:
            return open_run, open_run, -1
        tail = raw_text_run_tail(content, closer.end(), open_run)
        end, below = html_tag_close_state(
            content + "\n", closer.end(), TAG_STATE_START
        )
        if open_run in RAW_TEXT_ELEMENT_NAMES and end == -1:
            # The closer started and its *tag* has not finished on this line,
            # which ``raw_text_run_tail`` already says by handing back the whole
            # line. The state below has to say it too: an HTML parser is still
            # reading the tag, so nothing below here opens a comment until the
            # tag's own ``>`` arrives. Clearing the run there read
            # ``</script title="`` over a marker line as a run that had closed
            # and a comment that had opened, and ``has_adult_marker`` skipped a
            # child-facing document on a declaration the page never carried.
            return closing_tag_run(below), open_run, tail
        return (
            comment_open_below(content, closer.end()),
            open_run,
            tail,
        )
    if not opens_html_block:
        return None, None, -1
    for key, opener, closer in RAW_TEXT_RUNS:
        match = opener.match(content)
        if match is None:
            continue
        if key == COMMENT_RUN:
            return comment_open_below(content, match.start()), None, -1
        closing = closer.search(content, raw_text_content_start(content, match, key))
        if closing is not None:
            return (
                comment_open_below(content, closing.end()),
                key,
                raw_text_run_tail(content, closing.end(), key),
            )
        return key, key, -1
    return None, None, -1


def raw_text_run_holds_text(run: str | None) -> bool:
    """Return whether a line inside ``run`` carries text rather than markup.

    Every run in ``RAW_TEXT_RUNS`` but one holds characters the page shows as
    they stand or drops altogether; in neither case is a comment-shaped run on
    the line a comment. The exception is the comment itself, which is in that
    tuple only so that a raw HTML block cannot start inside another one.
    Kept identical to the helper in the sibling hooks.
    """
    return run is not None and run != COMMENT_RUN


def raw_text_run_is_displayed(run: str | None) -> bool:
    """Return whether the page paints the characters of a line inside ``run``.

    ``raw_text_run_holds_text`` says those characters are text rather than
    markup; this says whether a reader ever reads them. Only the prose
    extractor asks, because only a reading score depends on the answer: the
    two marker scans care that the characters are not markup and not whether
    they are painted. The sibling hooks therefore do not carry this helper,
    and that asymmetry is the question each hook asks rather than a copy that
    drifted.
    https://html.spec.whatwg.org/multipage/rendering.html#hidden-elements
    """
    return run in DISPLAYED_RAW_TEXT_ELEMENT_NAMES


#: One attribute of an HTML tag, with a line ending allowed wherever CommonMark
#: allows whitespace. This is the same grammar ``INLINE_HTML_TAG_PATTERN``
#: carries, written once so the multiline forms below cannot drift from it.
#: https://spec.commonmark.org/0.31.2/#raw-html
_TAG_ATTRIBUTE = r"""
    [ \t\n]+ [_:A-Za-z][A-Za-z0-9_.:-]*             # an attribute name
    (?: [ \t\n]*=[ \t\n]*                          # an attribute value
        (?: [^ \t\r\n"'=<>`]+ | '[^']*' | "[^"]*" ) )?
"""
#: A whole tag that may hold line endings. CommonMark lets an open tag carry a
#: line ending in the whitespace between attributes and inside a quoted
#: attribute value, so a tag is not a line-local construct: a scan that stops
#: at the end of a line reads the rest of the tag as text, and a backtick in an
#: attribute then opens a code span the renderer never opens.
#: https://spec.commonmark.org/0.31.2/#raw-html
MULTILINE_HTML_TAG_PATTERN = re.compile(
    rf"""
    <
    (?: [A-Za-z][A-Za-z0-9-]*                      # an open tag
        (?: {_TAG_ATTRIBUTE} )*
        [ \t\n]* /? >
      | / [A-Za-z][A-Za-z0-9-]* [ \t\n]* >         # a closing tag
    )
    """,
    re.VERBOSE,
)
#: A *prefix* of such a tag: everything a tag may be so far, with the ``>`` yet
#: to come. A line that ends inside a tag ends on one of these, and a line that
#: ends on anything else was never inside a tag -- which is what keeps
#: ``<no spaces allowed`>`` and ``<a:`>`` ordinary text with their backticks
#: intact, as markdown-it 14.3.0 reads them.
HTML_TAG_PREFIX_PATTERN = re.compile(
    rf"""
    <
    /? [A-Za-z][A-Za-z0-9-]*
    (?: {_TAG_ATTRIBUTE} )*
    (?: [ \t\n]+ [_:A-Za-z][A-Za-z0-9_.:-]*         # a half-written attribute
        (?: [ \t\n]*=?[ \t\n]*
            (?: [^ \t\r\n"'=<>`]* | '[^']* | "[^"]* )? )? )?
    [ \t\n]* /?
    $
    """,
    re.VERBOSE,
)
#: A raw-text element's own opening tag, whole. The closing delimiter of a
#: raw-text run is searched for *past* this, because an HTML parser reads the
#: start tag before it enters raw text: in ``<script title="</script>">`` the
#: end-tag spelling is an attribute value, the element never closes, and
#: everything below it to the end of the file is script data. Searching from the
#: element's name instead closed a run that had not begun, and a ``## Goal``
#: under it was reported as a heading the page never paints. Built from
#: ``_TAG_ATTRIBUTE`` so this spelling of "a tag" cannot drift from the others.
#: https://html.spec.whatwg.org/multipage/parsing.html#tag-open-state
RAW_TEXT_START_TAG_PATTERN = re.compile(
    rf"""
    < [A-Za-z][A-Za-z0-9-]*                        # the element's own name
    (?: {_TAG_ATTRIBUTE} )*
    [ \t\n]* /? >
    """,
    re.VERBOSE,
)


def html_tag_prefix(text: str, index: int) -> str | None:
    """Return the tag prefix beginning at ``index``, if the text ends inside one.

    ``None`` when the characters from ``index`` are not the beginning of a tag,
    in which case the caller is right to read them as text. Kept identical to
    the helper in the sibling hooks.
    https://spec.commonmark.org/0.31.2/#raw-html
    """
    if HTML_TAG_PREFIX_PATTERN.match(text, index) is None:
        return None
    return text[index:]


def html_tag_continue(prefix: str, line: str) -> tuple[int, str | None, bool]:
    """Carry an unfinished tag onto ``line``.

    Returns ``(position, prefix, matched)``. ``matched`` is ``False`` when the
    line makes the whole thing no tag at all, and the caller then reads the
    characters as text. Otherwise ``prefix`` is ``None`` and ``position`` is
    the offset in ``line`` just past the tag's ``>``, or ``prefix`` is the
    longer prefix and the tag is still open below this line. Kept identical to
    the helper in the sibling hooks.
    https://spec.commonmark.org/0.31.2/#raw-html
    """
    joined = f"{prefix}\n{line}"
    match = MULTILINE_HTML_TAG_PATTERN.match(joined)
    if match is not None:
        return match.end() - len(prefix) - 1, None, True
    if HTML_TAG_PREFIX_PATTERN.match(joined) is not None:
        return len(line), joined, True
    return 0, None, False


def raw_html_comment_spans(
    line: str,
    is_in_comment: bool,
    open_tag: str | None = None,
    in_bogus_run: bool = False,
) -> tuple[str, bool, str | None, bool]:
    """Return the HTML comment text on one line of a raw HTML block.

    Two contexts bind inside a raw HTML block and only two: an open comment,
    and a complete tag, whose attribute values are attribute values rather than
    markup. Nothing Markdown would otherwise read on the line means anything
    here, because the block is passed through to the page as it stands. That
    cuts both ways, and both ways are measured against markdown-it 14.3.0: a
    comment inside a ``<div>`` block is still a comment and still declares an
    audience, while ``<div title="<!-- audience: adult -->">`` yields nothing at
    all, because the delimiters are inside the tag and the renderer puts them in
    the ``title`` attribute. Kept identical to the helper in
    ``.github/scripts/check-session-structure.py``.
    https://spec.commonmark.org/0.31.2/#html-blocks

    A tag may hold a line ending, so the tag state crosses lines the way the
    comment state does: ``open_tag`` is ``None`` outside a tag and otherwise
    holds the characters of the tag so far, which is what lets the next line
    be matched against the whole tag rather than guessed at. Without it a
    ``<span`` on one line and a ``title=`` holding a marker on the next read
    as a real comment, and a document left its gate on attribute data.

    ``in_bogus_run`` is the third of those cross-line states and it is the same
    fact told about a different run: a bogus comment and a malformed tag each
    end at the next ``>``, wherever that ``>`` is, and neither is obliged to
    put one on the line it opens. Reading the next line afresh made
    ``<div>`` / ``before <?foo`` / a marker line / ``?>`` carry an audience the
    page never showed, because the whole of it is one node to an HTML parser
    and the marker's own ``-->`` merely supplies the ``>`` that ends it.
    """
    spans: list[str] = []
    index = 0

    if in_bogus_run:
        # A run that ends at the next ``>`` was left open on the line above:
        # a bogus comment, or a tag too malformed for the grammar above to
        # read. Every character up to that ``>`` is the run's, so a ``<!--``
        # among them opens nothing.
        bogus_end = line.find(">")
        if bogus_end == -1:
            return "", False, None, True
        index = bogus_end + 1
    elif open_tag is not None:
        # A tag left open on the line above continues here, and everything
        # until its ``>`` is the tag's own characters. A ``<!--`` written in
        # a quoted attribute value is attribute data, exactly as it is when
        # the whole tag fits on one line.
        #
        # A line that makes the whole thing no tag *to CommonMark* does not
        # make it no tag to the page, and the page is what this helper answers
        # for. ``html_tag_prefix`` only ever opens on a ``<`` and a letter, and
        # that is a tag to an HTML parser however the rest of it is spelled --
        # the same rule the malformed-tag fallback below applies within a
        # line. So the run goes on to its ``>`` rather than starting over:
        # ``before <a--`` above a marker line is one tag with the marker's
        # words as attribute names, and reading the line afresh found a
        # comment inside a tag that the page still had open.
        index, open_tag, matched = html_tag_continue(open_tag, line)
        if not matched:
            bogus_end = line.find(">")
            if bogus_end == -1:
                return "", False, None, True
            index = bogus_end + 1
        elif open_tag is not None:
            return "", False, open_tag, False

    while index < len(line):
        if is_in_comment:
            comment_end = line.find("-->", index)
            if comment_end == -1:
                spans.append(line[index:])
                return "".join(spans), True, None, False
            spans.append(line[index : comment_end + len("-->")])
            index = comment_end + len("-->")
            is_in_comment = False
            continue

        if line.startswith("<!--", index):
            spans.append("<!--")
            index += len("<!--")
            is_in_comment = True
            continue

        if line[index] == "<":
            # A processing instruction, a declaration and a CDATA section are
            # raw HTML whose content is characters, exactly as they are in the
            # Markdown inline walk -- this is the same helper
            # ``link_metadata_regions`` asks there. A ``<!--`` written inside
            # one begins no second comment: an HTML parser reads
            # ``<?foo <!-- audience: adult --> ?>`` as one run and there is no
            # comment node spelled the way the marker is, so lifting a marker
            # out of it granted an exemption the page never carried and took a
            # child-facing document out of its gate. The comment itself is
            # answered above, before this branch, so the run found here is
            # never the comment.
            if line.startswith("<?", index) or (
                line.startswith("<!", index) and not line.startswith("<!--", index)
            ):
                # HTML5's bogus comment. A raw HTML block is passed through to
                # the page as it stands, so what ends one of these runs is the
                # browser's rule and not CommonMark's: ``<?``, ``<!`` that is
                # not ``<!--``, and ``<![CDATA[`` each run to the first ``>``,
                # however their own delimiters are spelled. Measured on
                # GitHub's own renderer, whose sanitizer removes the whole of
                # ``<?foo <!-- audience: adult --> ?>`` and leaves the ``?>``
                # standing: the run swallowed the marker's closing ``>``.
                #
                # The run is skipped rather than reported, because the node it
                # makes is not the marker -- its text merely holds the marker's
                # characters -- and honouring it exempted a document whose
                # author declared nothing. A run with no ``>`` on this line
                # does not end there: it is handed to the next line as
                # ``in_bogus_run``, because the page goes on reading it.
                bogus_end = line.find(">", index)
                if bogus_end == -1:
                    return "".join(spans), False, None, True
                index = bogus_end + 1
                continue
            tag = INLINE_HTML_TAG_PATTERN.match(line, index)
            if tag is not None:
                index = tag.end()
                continue
            open_tag = html_tag_prefix(line, index)
            if open_tag is not None:
                return "".join(spans), False, open_tag, False
            if MALFORMED_TAG_START_PATTERN.match(line, index) is not None:
                # A ``<`` followed by a letter, or by ``/`` and a letter, is a
                # tag to an HTML parser whether or not CommonMark's raw-HTML
                # grammar accepts it, and a tag runs to its ``>``.
                # ``<a<!-- audience: adult -->`` is one malformed start tag
                # with four attributes, measured on ``html.parser``, and the
                # ``<!--`` inside it is an attribute name rather than a
                # comment -- so reading a marker out of it exempted a document
                # whose author declared nothing. The well-formed grammar is
                # asked first, and the unfinished-tag state above it, so this
                # only ever catches what neither could, and it ends where a
                # tag ends rather than where the line does: a ``<a<!--`` with
                # no ``>`` after it goes on being a tag on the line below.
                tag_end = line.find(">", index)
                if tag_end == -1:
                    return "".join(spans), False, None, True
                index = tag_end + 1
                continue

        index += 1

    return "".join(spans), is_in_comment, None, False


def scan_paragraph_inlines(
    lines: Sequence[ParagraphLine],
    skips: dict[int, tuple[tuple[int, int], ...]] | None,
) -> tuple[list[str], list[tuple[int, int, int]]]:
    """Walk one paragraph left to right, one context at a time.

    Returns two things: the text CommonMark reads as an HTML comment on each
    line, and every code span the walk consumed, as ``(row, start, end)`` in
    that row's own coordinates -- one range per physical line, because a span
    that crosses a soft line break is one span and two rows.

    ``skips`` holds, per row, the ranges this walk is to read as link metadata
    rather than as text. ``None`` runs the walk with no link model at all. That
    is not a convenience: CommonMark takes whichever of a code span, a raw HTML
    tag, an autolink and a link starts first, so the code spans have to be
    known *before* the link metadata is computed, and the only way to know them
    is to walk once without it. ``paragraph_metadata_skips`` does exactly that.

    "No link model" means no *defined labels* and no image rule; it does not
    mean no brackets. The walk counts the brackets it passes and hands the
    target of a ``](`` that closes one to ``inline_link_end``, because a
    destination and a title are scanned as characters rather than as inline
    content and a backtick in either opens nothing. A ``[`` a code span
    swallowed is never counted, which is what still leaves ``` `[a](u` x) ```
    a code span and not a link.

    The bracket walk runs in that first pass and in no other, because it is
    half a link model and the second pass has a whole one. Links may not nest,
    so forming one deactivates every opener still open above it:
    ``[a [b](u) c](v "<!-- x -->")`` is an inner link and then literal text,
    and the marker in those literal parentheses is a comment the page carries.
    ``link_metadata_regions`` knows that and knows which labels the document
    defines; this walk knows neither, and running it in both passes hid that
    marker and took a child-facing document out of the gate.

    Four contexts bind at least as tightly as a code span and are consumed
    whole where they start first: a comment, an autolink, a raw HTML tag, and a
    backslash escape. A line indented four spaces past its container is code
    rather than a paragraph, so nothing on it is read at all. Kept in step with
    ``scan_inline_run`` in ``.github/scripts/check-session-structure.py``.
    https://spec.commonmark.org/0.31.2/#code-spans
    https://spec.commonmark.org/0.31.2/#links
    https://spec.commonmark.org/0.31.2/#autolinks
    https://spec.commonmark.org/0.31.2/#raw-html
    """
    comments: list[list[str]] = [[] for _ in lines]
    code_spans: list[tuple[int, int, int]] = []
    indented_code = indented_code_rows(
        [line.text[line.content_start :] for line in lines]
    )
    row = 0
    index = 0
    open_brackets = 0

    while row < len(lines):
        line = lines[row].text
        content_start = lines[row].content_start

        if index >= len(line):
            row += 1
            index = 0
            continue

        if index == 0 and row in indented_code:
            row += 1
            continue

        if skips is not None:
            regions = skips.get(row, ())
            skipped = next(
                (end for start, end in regions if start <= index < end), index
            )
            if skipped > index:
                index = skipped
                continue

        character = line[index]

        if character == "\\":
            # The escape and the character it escapes are one unit, so a
            # backtick behind a backslash is never read as a run at all.
            index += 2
            continue

        if character == "`":
            run_end = index
            while run_end < len(line) and line[run_end] == "`":
                run_end += 1
            run_length = run_end - index
            closer = closing_backtick_run(line, run_end, run_length)
            if closer != -1:
                code_spans.append((row, index, closer))
                index = closer
                continue
            close_row, close_index = following_backtick_run(lines, row, run_length)
            if close_row == -1:
                index = run_end
                continue
            code_spans.append((row, index, len(line)))
            for middle in range(row + 1, close_row):
                code_spans.append(
                    (middle, lines[middle].content_start, len(lines[middle].text))
                )
            code_spans.append(
                (close_row, lines[close_row].content_start, close_index)
            )
            row, index = close_row, close_index
            continue

        if skips is None and character == "[":
            open_brackets += 1
            index += 1
            continue

        if skips is None and character == "]" and open_brackets:
            # The target of a link that closes here is characters rather than
            # inline content, so nothing in it opens a span.
            open_brackets -= 1
            if index + 1 < len(line) and line[index + 1] == "(":
                # The target may cross a soft line break: a title holds one,
                # and so does the whitespace around the destination. Reading
                # only this physical line rejected such a target, left the
                # backtick inside the title standing as text, and paired it
                # with a backtick below -- masking the comment between them.
                target_row, target_end = following_link_end(lines, row, index + 1)
                if target_row != -1:
                    row, index = target_row, target_end
                    continue
            index += 1
            continue

        if character == "<":
            if line.startswith("<!--", index):
                # A comment that closes inside this paragraph is consumed
                # whole, because it started first. One that does not close is
                # no comment at all, so its characters are scanned as text.
                close_row, close_index = following_comment_end(lines, row, index)
                if close_row != -1:
                    if close_row == row:
                        comments[row].append(line[index:close_index])
                    else:
                        comments[row].append(line[index:])
                        for middle in range(row + 1, close_row):
                            middle_line = lines[middle]
                            comments[middle].append(
                                middle_line.text[middle_line.content_start :]
                            )
                        close_line = lines[close_row]
                        comments[close_row].append(
                            close_line.text[close_line.content_start : close_index]
                        )
                    row, index = close_row, close_index
                    continue
            else:
                # A processing instruction, a declaration and a CDATA section
                # are raw HTML whose content is characters, and none of the
                # three can also be an autolink or a tag, so they are asked
                # about first and cost nothing when they do not match.
                raw_row, raw_index = following_raw_html_end(lines, row, index)
                if raw_row != -1:
                    row, index = raw_row, raw_index
                    continue
                # An autolink is asked about before a tag, because a tag name
                # may not hold a colon and a URI autolink must, so only one of
                # the two can match here.
                autolink = AUTOLINK_PATTERN.match(line, index)
                if autolink is not None:
                    index = autolink.end()
                    continue
                tag = INLINE_HTML_TAG_PATTERN.match(line, index)
                if tag is not None:
                    index = tag.end()
                    continue
                # A tag that does not close on this line is not finished: it
                # closes on a later line of the same paragraph, the way a
                # comment and the other raw HTML runs already do here.
                # Reading only this line left a backtick inside a multiline
                # attribute standing as text, and it then paired with a
                # backtick below and masked a real comment.
                tag_row, tag_index = following_tag_end(lines, row, index)
                if tag_row != -1:
                    row, index = tag_row, tag_index
                    continue

        index += 1

    return ["".join(parts) for parts in comments], code_spans


def paragraph_metadata_skips(
    lines: Sequence[ParagraphLine], defined_labels: frozenset[str]
) -> dict[int, tuple[tuple[int, int], ...]]:
    """Return, per row, the ranges of one paragraph that render as metadata.

    The code spans are found first, with no link model at all, and blanked
    before a link is looked for -- because a code span that opens before a
    ``[`` swallows the bracket, so the link is never there to have metadata.
    Computing the metadata over the raw line read ``` `![alt](url` "<!-- x -->")
    ``` as an image running to the final ``)``, and the marker the renderer
    really does print went with it. It closes the other way round too:
    ``![a`b](u) <!-- x --> c` `` is an image to a raw-line pass and a code span
    to the renderer.

    Blanking rather than deleting is what keeps the ranges usable: they are
    offsets into the real line, so they have to stay the offsets the real line
    has. The regions are computed from each line's *content* -- past its
    blockquote and list-item prefixes -- because CommonMark classifies a line
    from what is left once the prefixes are gone, and shifted back to the
    line's own coordinates for the walk that reads them. Kept in step with
    ``code_span_masked_lines`` and ``text_marker_spans`` in
    ``.github/scripts/check-session-structure.py``.
    """
    _, code_spans = scan_paragraph_inlines(lines, None)
    masked = [list(line.text) for line in lines]
    for row, start, end in code_spans:
        masked[row][start:end] = " " * (end - start)

    # The rows are joined and walked once, rather than walked one at a time.
    # A link is not a line-local construct: markdown-it 14.3.0 reads
    # ``[help`` / ``continued](url "<!-- audience: adult -->")`` as one link
    # whose title is an attribute, and a walk that started again on the second
    # line had no opening bracket to close, found no link, and read the title
    # as a real comment. An ``audience: adult`` marker invented there takes a
    # child-facing document out of the reading gate without a word in the
    # report, which is the one direction this module never errs in.
    #
    # A link reference definition is the exception and keeps its own line: it
    # is a block construct anchored to the start of a line and ending at the
    # end of it, so it is found per row and blanked out of the joined text
    # before the inline walk reads it.
    skips: dict[int, tuple[tuple[int, int], ...]] = {}
    pieces: list[str] = []
    starts: list[int] = []
    offset = 0
    for row, line in enumerate(lines):
        content = "".join(masked[row])[line.content_start :]
        if link_reference_definition_region(content) is not None:
            skips[row] = ((line.content_start, line.content_start + len(content)),)
            content = " " * len(content)
        pieces.append(content)
        starts.append(offset)
        offset += len(content) + 1

    for left, right in link_metadata_regions("\n".join(pieces), defined_labels):
        for row, line in enumerate(lines):
            low = max(left, starts[row])
            high = min(right, starts[row] + len(pieces[row]))
            if low >= high:
                continue
            shift = line.content_start - starts[row]
            skips[row] = skips.get(row, ()) + ((low + shift, high + shift),)
    return skips


def paragraph_inlines(
    lines: Sequence[ParagraphLine], defined_labels: frozenset[str]
) -> tuple[list[str], list[tuple[int, int]]]:
    """Return one paragraph's comment text per line, and its code spans.

    The ranges are half open and are offsets into the document the lines came
    from, so a caller can blank every one of them and still hold the document
    with its line breaks, its line count and its columns intact.
    """
    skips = paragraph_metadata_skips(lines, defined_labels)
    comments, code_spans = scan_paragraph_inlines(lines, skips)
    return comments, [
        (lines[row].start + start, lines[row].start + end)
        for row, start, end in code_spans
    ]


@dataclass(frozen=True)
class DocumentInlines:
    """One inline walk over a document, and the three answers it yields.

    ``fenced`` and ``code_spans`` are the literal code a document *prints*
    rather than means. ``comment_lines`` holds, for each line, only what
    CommonMark reads there as an HTML comment: a marker in a fenced block, in a
    code span -- including one that closes on a later line -- behind a
    backslash escape, inside a tag's attribute, inside an autolink, in an
    image's alt text, in a link's destination or title, in a reference label
    the document defines, in a link reference definition, or indented four
    spaces prints as characters on the page or hands them to an element as an
    attribute. It is prose *about* a marker, and it declares nothing.
    """

    fenced: tuple[tuple[int, int], ...]
    code_spans: tuple[tuple[int, int], ...]
    comment_lines: tuple[str, ...]


def scan_document_inlines(text: str) -> DocumentInlines:
    """Walk a document once for its fences, its code spans and its comments.

    Two walks in one, because they are two different shapes. A fence is a line
    block, so the fence walk reads one line at a time -- the walk
    ``extract_prose`` does, with the same helpers, so the two passes over a
    document cannot disagree about where the fences are. A code span and a
    comment are inline and cross a soft line break, so the lines a fence does
    not claim are gathered into paragraphs and scanned a paragraph at a time.

    A paragraph is where a code span stops looking for its closing run, so the
    run handed to the inline walk is one block and no more; ``starts_a_block``
    is what records where one ends. The labels the document defines are
    collected between the two, because a reference's label is metadata only
    where a definition for it parses, and that question is answered by the
    whole document rather than by the line in hand.

    A third state runs beside those two: ``html_block_state``, which says which
    lines are *inside* a raw HTML block. The Markdown inline rules do not reach
    inside one -- the renderer passes the block through as it stands -- so
    those lines are scanned for the two things that do bind there, an open
    comment and a complete tag, and are kept out of the paragraph runs and out
    of the reference-label collection. It is the same classification
    ``collect_marker_lines`` makes in
    ``.github/scripts/check-session-structure.py``.

    Ranges are half open and are offsets into ``text``.
    https://spec.commonmark.org/0.31.2/#fenced-code-blocks
    https://spec.commonmark.org/0.31.2/#code-spans
    """
    fenced: list[tuple[int, int]] = []
    runs: list[tuple[list[ParagraphLine], list[int]]] = []
    contents: list[str] = []
    starts: list[bool] = []
    comment_lines: list[str] = []
    paragraph: list[ParagraphLine] = []
    rows: list[int] = []
    active_fence: ActiveFence | None = None
    list_contexts: list[ListContext] = []
    previous_path: tuple[Container, ...] = ()
    # The line above, carried for the delimiter-row rule in
    # ``opens_a_paragraph``: its peeled content and the container it sat in.
    # Cleared at the top of every iteration, so that any branch which leaves
    # the loop early leaves no header row behind it.
    previous_content = ""
    previous_container: tuple[Container, ...] = ()
    paragraph_open = False
    raw_text: str | None = None
    html_block: ActiveHtmlBlock | None = None
    is_in_comment = False
    open_tag: str | None = None
    in_bogus_run = False
    offset = 0

    def close_paragraph() -> None:
        nonlocal paragraph, rows, previous_path
        if paragraph:
            runs.append((paragraph, rows))
        paragraph = []
        rows = []
        previous_path = ()

    lines = text.split("\n")
    in_table = False
    table_columns_here = 0
    table_container: tuple[Container, ...] = ()
    table_delimiter_row = -1

    for number, raw_line in enumerate(lines):
        above_content, above_container = previous_content, previous_container
        previous_content, previous_container = "", ()
        line_start = offset
        offset += len(raw_line) + 1
        line = raw_line.rstrip(ASCII_HORIZONTAL_WHITESPACE)
        contents.append("")
        starts.append(False)
        comment_lines.append("")

        if active_fence is not None and fence_container_ended(line, active_fence):
            active_fence = None

        if active_fence is not None:
            if is_closing_fence(
                normalize_for_fence_closing(raw_line, active_fence),
                active_fence.character,
                active_fence.minimum_length,
            ):
                active_fence = None
            fenced.append((line_start, line_start + len(raw_line)))
            paragraph_open = False
            continue

        fence_line = normalize_for_fence_opening(line, list_contexts)

        if html_block is not None and container_path_ended(
            line, html_block.containment_path
        ):
            # The list item or blockquote holding the block has ended, so the
            # block ended with it, exactly as an unclosed fence does.
            html_block = None
            is_in_comment = False
            open_tag = None
            in_bogus_run = False

        # Asked before the block machine rather than after it, because
        # condition 7 is the one start that may not interrupt a paragraph and
        # has to be told when there is no longer one to interrupt.
        header_above = (
            above_content if above_container == fence_line.containment_path else ""
        )
        block_starts = starts_a_block(
            fence_line.content,
            fence_line.containment_path,
            fence_line.opened,
            previous_path,
            paragraph_open,
            header_above,
        )
        starts[number] = block_starts
        html_block, line_html_block = html_block_state(
            fence_line.content,
            fence_line.containment_path,
            html_block,
            paragraph_open and not block_starts,
        )
        # The block is asked first and the run under it, which is the order the
        # sibling hooks use: a run may open only where CommonMark opens a raw
        # HTML block, so an ``<xmp>`` on a line the paragraph above it still
        # holds opens nothing.
        raw_text, line_raw_text, raw_text_end = raw_text_run_boundary(
            fence_line.content, raw_text, line_html_block is not None
        )
        if raw_text_run_holds_text(line_raw_text) and raw_text_end != -1:
            # The run closes part way along this line, and what follows the
            # closer is not the element's content.
            # ``<script></script><!-- audience: adult -->`` holds an empty
            # script and then a real comment, and dropping the whole line
            # dropped the comment with it -- so an adult-facing document was
            # scored by the child gate in silence. The run's own span is
            # blanked and the rest of the line goes on through the walk, which
            # is what ``extract_prose`` already does with the same boundary.
            # Blanking rather than slicing keeps the columns the document's:
            # every offset below here still points where it pointed.
            prefix_length = len(line) - len(fence_line.content)
            visible = " " * raw_text_end + fence_line.content[raw_text_end:]
            line = line[:prefix_length] + visible
            fence_line = replace(fence_line, content=visible)
            line_raw_text = None

        # A line CommonMark reads as raw HTML opens no fenced block: the block
        # runs to its own end condition and every character on those lines is
        # raw HTML, backticks included. Both sibling hooks read a fence this
        # way, so leaving it out here was the one place the three could
        # disagree about which fences a document has.
        opening_fence = (
            None
            if line_html_block is not None
            else parse_opening_fence(fence_line.content)
        )
        if opening_fence is not None:
            active_fence = build_active_fence(opening_fence, fence_line)
            fenced.append((line_start, line_start + len(raw_line)))
            close_paragraph()
            paragraph_open = False
            continue

        if raw_text_run_holds_text(line_raw_text):
            # The line is a raw-text element's content. The page shows those
            # characters as they stand or drops them altogether, so nothing on
            # the line is a comment and no code span reaches across it.
            close_paragraph()
            paragraph_open = False
            continue

        if line_html_block is not None:
            # Inside a raw HTML block only two contexts bind: an open comment,
            # and a complete tag whose attribute values are attribute values
            # rather than markup. Sending the line through the Markdown inline
            # walk instead read a real comment as an image title, a code span
            # or a link destination, and an adult-facing document was scored by
            # the child gate.
            (
                comment_lines[number],
                is_in_comment,
                open_tag,
                in_bogus_run,
            ) = raw_html_comment_spans(
                fence_line.content, is_in_comment, open_tag, in_bogus_run
            )
            close_paragraph()
            paragraph_open = False
            continue
        is_in_comment = False
        open_tag = None
        in_bogus_run = False

        contents[number] = fence_line.content

        # GFM reads a table before it reads any inline, and every cell is its
        # own inline context. Gathering the rows into one paragraph run let an
        # unmatched backtick in one cell pair with an unmatched backtick in
        # another, and the ``audience: adult`` marker standing between them
        # was read as a code span's content rather than as the comment the
        # page prints -- so an adult-facing document was scored by the child
        # gate. The rows are found the way ``extract_prose`` finds them, by the
        # delimiter row under the header and by the container the table opened
        # in, so the two passes agree about which lines are a table.
        # https://github.github.com/gfm/#tables-extension-
        table_line = strip_block_quote_prefixes(line)
        has_cells = bool(table_line.strip(ASCII_HORIZONTAL_WHITESPACE)) and (
            "|" in table_line
        )
        if in_table and not (
            number == table_delimiter_row
            or (has_cells and fence_line.containment_path == table_container)
        ):
            in_table = False
        # The header row needs no pipe, here for the reason ``extract_prose``
        # gives at the same lookahead, and the two passes have to agree about
        # which lines are a table or one of them reads a cell's backticks as a
        # paragraph's.
        if not in_table and table_line.strip(ASCII_HORIZONTAL_WHITESPACE):
            next_line = (
                lines[number + 1].rstrip(ASCII_HORIZONTAL_WHITESPACE)
                if number + 1 < len(lines)
                else ""
            )
            # The lookahead gets a *copy* of the list contexts, for the reason
            # ``extract_prose`` gives at the same lookahead: normalizing a line
            # records the containers it opens, and the next iteration has to
            # start from the state this line left behind.
            next_fence_line = normalize_for_fence_opening(
                next_line, list(list_contexts)
            )
            columns = (
                table_starts_here(fence_line.content, next_fence_line.content)
                if next_fence_line.containment_path == fence_line.containment_path
                else 0
            )
            if columns:
                in_table = True
                table_columns_here = columns
                table_container = fence_line.containment_path
                table_delimiter_row = number + 1
        if in_table:
            close_paragraph()
            paragraph_open = False
            previous_path = fence_line.containment_path
            prefix = len(line) - len(fence_line.content)
            # A body row with more cells than the header has its excess
            # ignored by GFM, so those characters are not on the page and
            # nothing written in them is either.
            row_cells = table_row_cells(fence_line.content)[:table_columns_here]
            for cell_start, cell_text in row_cells:
                runs.append(
                    (
                        [
                            ParagraphLine(
                                start=line_start + prefix + cell_start,
                                text=cell_text,
                                content_start=0,
                            )
                        ],
                        [number],
                    )
                )
            continue

        if block_starts:
            close_paragraph()
        previous_path = fence_line.containment_path
        # A line that starts no block leaves the paragraph above it open,
        # whatever its content peels to. The case that needs saying is the
        # empty list item: it may not interrupt a paragraph, so its marker is
        # the paragraph's own text -- but the container walk peels the marker
        # off and hands an empty content down, which reads exactly like a
        # blank line. Measured with markdown-it 14.3.0: ``Words`` then ``*``
        # then ``<x>`` is one paragraph of three lines, and the ``## Goal``
        # below is a heading.
        paragraph_open = (paragraph_open and not block_starts) or opens_a_paragraph(
            fence_line.content, paragraph_open, header_above
        )
        previous_content = fence_line.content
        previous_container = fence_line.containment_path
        paragraph.append(
            ParagraphLine(
                start=line_start,
                text=line,
                content_start=len(line) - len(fence_line.content),
            )
        )
        rows.append(number)

    close_paragraph()

    defined_labels = collect_reference_labels(contents, starts)
    spans: list[tuple[int, int]] = []
    for run_lines, run_rows in runs:
        comments, code_spans = paragraph_inlines(run_lines, defined_labels)
        spans.extend(code_spans)
        for row, comment in zip(run_rows, comments, strict=True):
            # Added rather than assigned: one row of a table is several runs,
            # one per cell, and each contributes the comment text its own cell
            # holds. Every other line is one run, where this is an assignment
            # to an empty string by another name.
            comment_lines[row] += comment

    return DocumentInlines(tuple(fenced), tuple(spans), tuple(comment_lines))


def scan_literal_code(text: str) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """Return a document's fenced-block ranges and its code-span ranges."""
    walk = scan_document_inlines(text)
    return list(walk.fenced), list(walk.code_spans)


def document_marker_text(text: str) -> str:
    """Return only what CommonMark reads as an HTML comment in a document.

    This answers a narrower question than ``strip_html_comments``: not "what
    does the reader see", but "what here does CommonMark read as a comment".
    The difference is every context that binds tighter than raw HTML and
    therefore prints the characters the author typed, or hands them to an
    element as an attribute; ``DocumentInlines`` lists them.

    Saying it positively -- keeping the comment spans rather than subtracting
    code spans, escapes, attributes, autolinks, link metadata and indented code
    one context at a time -- is what lets one scan cover every shape. Lines are
    joined as the document holds them, so a line number is still a line number
    and a marker split over a line break is not read as one, which is what the
    sibling hook does with the same text. Kept in step with
    ``DocumentScan.marker_text`` in
    ``.github/scripts/check-session-structure.py``.
    """
    return "\n".join(scan_document_inlines(text).comment_lines)


def literal_code_regions(text: str) -> list[tuple[int, int]]:
    """Return the character ranges of every fenced block line and code span.

    Literal code is the text a document *prints* rather than means. Finding it
    first is what lets the two callers below tell a marker from an example of
    one, and a comment delimiter from a picture of a comment delimiter.

    Ranges are half open and are offsets into ``text``, so a caller can rebuild
    the document with its line breaks, its line count and its columns intact.
    A code span that crosses a soft line break arrives as one range per
    physical line, which is what keeps that promise.

    Indented code blocks are deliberately not included. Telling one from an
    indented list continuation needs the full block parse this module does not
    do, guessing wrong means an adult-facing file gets scored, and every code
    block in this repository is fenced.
    https://spec.commonmark.org/0.31.2/#code-spans
    """
    fenced, spans = scan_literal_code(text)
    return sorted(fenced + spans)


def code_span_regions(text: str) -> list[tuple[int, int]]:
    """Return the character ranges of every code span, fenced blocks aside."""
    return scan_literal_code(text)[1]


def strip_code_spans(text: str) -> str:
    """Return ``text`` with every code span blanked, its line breaks intact.

    A code span is not prose: it is characters a document prints, and the
    reading score is about the words a child reads. Blanking rather than
    deleting keeps every line break and every column where the document has
    them, so the walk that reads this back still sees the document it came
    from -- its fences, its list markers and its blockquote markers all in the
    columns they started in.
    """
    kept = list(text)
    for start, end in code_span_regions(text):
        kept[start:end] = " " * (end - start)
    return "".join(kept)


def literal_code_mask(text: str) -> bytearray:
    """Return one byte per character, nonzero where the character is literal code."""
    mask = bytearray(len(text))
    for start, end in literal_code_regions(text):
        mask[start:end] = b"\x01" * (end - start)
    return mask


def raw_text_run_mask(text: str) -> bytearray:
    """Return one byte per character, nonzero where a raw-text run holds it.

    A comment delimiter a raw-text element *prints* is not a delimiter, exactly
    as a delimiter inside literal code is not one. ``<textarea>`` and ``<xmp>``
    show their content to the reader and the rest of the set drops it, and in
    neither case is a comment-shaped run inside one a comment. Measured at the
    commit this fixes: forty-three words of worksheet prose written inside a
    ``<textarea>`` between ``<!--`` and ``-->`` left **zero** prose words, and
    the gate reported success on a page it never read.

    The run state is the one the document walks use, so the two cannot disagree
    about which lines a run holds, and the line is peeled to its container
    content before the question is asked -- the same normalization the document
    walks use, for the same reason. One thing this pass still does not have is
    recorded rather than hoped over: it carries no HTML block machine, so it
    tells the run state that any line may open one, and the residual is an
    opener on a line CommonMark keeps inside the paragraph above it. That
    leaves a real comment removed, which is the direction this pass ran in
    before it asked the question at all.
    """
    mask = bytearray(len(text))
    list_contexts: list[ListContext] = []
    open_run: str | None = None
    offset = 0
    for line in text.split("\n"):
        # The run state is asked about the line's *content*, past its
        # blockquote and list-item prefixes, because CommonMark classifies a
        # line from what is left once the prefixes are gone. Asking about the
        # raw line meant ``> <textarea>`` opened no run at all, so the comment
        # remover below deleted forty words the page prints -- and a document
        # that loses that many can fall under the word floor and leave the
        # gate in silence. The mask still covers the whole raw line: a
        # container prefix holds no delimiter, and the offsets have to stay
        # the document's.
        open_run, line_run = raw_text_run_state(
            normalize_for_fence_opening(line, list_contexts).content, open_run, True
        )
        if raw_text_run_holds_text(line_run):
            mask[offset : offset + len(line)] = b"\x01" * len(line)
        offset += len(line) + 1
    return mask


def strip_html_comments(text: str) -> str:
    """Remove HTML comments, including ones that span lines.

    A comment delimiter a document *prints* is not a delimiter. An unmatched
    ``<!--`` inside a fenced example, or inside a code span, pairs with the next
    real ``-->`` below it, and a document-wide substitution then deletes every
    word between them. Measured at the commit this fixes: one fenced example
    holding an unmatched opener took a whole document's prose to nothing,
    because the substitution ate the example's closing fence and the opening
    fence then swallowed the rest of the file. A document that loses words that
    way can fall under ``MIN_WORDS_TO_SCORE`` and leave the gate in silence.

    So the literal code is found first and an *opener* starting inside it is
    left alone. A closer is a different question. Nothing is parsed inside an
    open comment, so the first ``-->`` after a real opener ends it wherever it
    sits, backticks and fence lines included: CommonMark reads the two
    constructs in the order they are written and whichever opens first takes
    the characters after it. Measured against markdown-it 14.3.0,
    ``<!-- hidden `-->` visible text`` is a comment through that first ``-->``
    and visible text after it, while ``Say `<!-- a` then -->`` holds no comment
    at all. Looking for the closer outside the code regions found the first one
    and refused it, so the whole comment stayed in the document and the words
    inside it -- words no reader sees -- were scored.

    The regions are recomputed after a comment that overlapped one is removed,
    because a backtick run inside a comment is not a code-span delimiter and
    must not pair with a run below it. Blanking the comment to spaces of its own
    length keeps every offset, so the rescan reads the same lines in the same
    places. A comment is still removed as one span, line breaks included, so a
    paragraph wrapped around a multi-line comment stays one sentence unit. An
    unterminated ``<!--`` outside literal code is left in place, which is what
    the substitution this replaces did.
    https://spec.commonmark.org/0.31.2/#raw-html
    """
    working = text
    mask = literal_code_mask(working)
    # A run of raw text is masked beside the literal code, for the same reason
    # and against the same mistake: an opener the page *prints* is not an
    # opener. The two masks are separate because only the literal one is
    # recomputed when a comment overlapping it is blanked.
    raw_text = raw_text_run_mask(working)
    spans: list[tuple[int, int]] = []
    search_from = 0

    while True:
        start = search_from
        while True:
            start = working.find("<!--", start)
            if start == -1 or not (mask[start] or raw_text[start]):
                break
            start += 1
        if start == -1:
            break

        end = working.find("-->", start + len("<!--"))
        if end == -1:
            break
        end += len("-->")
        spans.append((start, end))
        search_from = end

        if b"\x01" in mask[start:end]:
            working = f"{working[:start]}{' ' * (end - start)}{working[end:]}"
            mask = literal_code_mask(working)
            raw_text = raw_text_run_mask(working)

    kept: list[str] = []
    index = 0
    for start, end in spans:
        kept.append(text[index:start])
        kept.append(" ")
        index = end

    kept.append(text[index:])
    return "".join(kept)


def front_matter_is_yaml_mapping(block: str) -> bool:
    """Return whether ``block`` is the YAML mapping a front-matter block is.

    Two conditions, and each closes a different error.

    **It has to parse.** Front matter is a YAML convention, so YAML decides,
    and a hand-written line grammar kept deciding differently: an unbalanced
    flow collection, an undefined escape in a double-quoted scalar and a tab
    used as indentation are all shapes a pattern accepted and a parser refuses.
    A block that no parser can read is not metadata a publishing tool will ever
    consume; it is text on the page, and removing it takes words out of a
    child's reading score without anyone seeing it go.

    **It has to be a mapping.** Parsing alone is not enough, and this is where
    a parser on its own would be worse than the pattern it replaces: ``Japan
    trip`` is a perfectly good YAML document -- one plain scalar -- so a
    thematic break over a sentence, closed by ``...``, would parse and the
    sentence would vanish. Front matter is a block of keys, every consumer of
    it reads a mapping, and requiring one keeps that shape out. Measured: the
    two shapes an earlier round recorded as deliberately rejected, ``-- not a
    sequence`` and ``-notaspace``, are plain scalars rather than mappings, so
    they stay rejected and that verdict is unchanged.

    **Every failure is one answer.** An unreadable block is exactly the block
    this returns ``False`` for, so the handler is that rule rather than a list
    of classes -- and a list is what it was, which is how a document could stop
    the whole run. ``safe_load`` parses and then *constructs*, and the
    constructors call ordinary Python conversions that raise ordinary Python
    exceptions: measured over PyYAML 6.0.3's twelve standard tags, four classes
    reach the caller past ``yaml.YAMLError``. ``date: 9999-99-99`` is the
    plainest of them -- no tag, no quoting, the implicit timestamp resolver --
    and it raised ``ValueError: month must be in 1..12`` out of this helper,
    out of ``scan_files`` and out of ``main``, so one malformed document ended
    the run in a traceback and **no file was scored at all**.

    | what a value holds | what escapes ``yaml.YAMLError`` |
    | --- | --- |
    | ``date: 9999-99-99``; ``n: !!int "abc"``; an integer of more than 4,300 digits | ``ValueError`` |
    | ``flag: !!bool "maybe"`` | ``KeyError`` |
    | ``n: !!int ""`` | ``IndexError`` |
    | ``when: !!timestamp "abc"`` | ``AttributeError`` |

    Catching ``Exception`` is right here and would be wrong three lines either
    side of it: the guarded statement is one call into a third-party parser and
    holds none of this module's own logic, so there is no bug of ours for the
    handler to hide. ``RecursionError`` -- which a deeply nested flow collection
    raises -- is inside ``Exception`` and stays covered. ``safe_load`` is used
    rather than ``load``: a document in this repository is not a place to
    construct Python objects from.

    A gate that crashes still fails closed in CI, so nothing unsafe shipped.
    What it stops being is *readable*: a traceback tells a builder the tool is
    broken, where a refusal tells them which file to fix.
    https://yaml.org/spec/1.2.2/
    """
    try:
        loaded = yaml.safe_load(block)
    except Exception:
        return False
    return isinstance(loaded, dict)


def strip_front_matter(text: str) -> str:
    """Remove a YAML front-matter block from the start of a document.

    A front-matter block opens with ``---`` on the very first line and closes
    on the next line that is exactly ``---`` or ``...``. Its keys are
    publishing metadata, not prose. The opening line must be followed by a
    nonblank line, so a document that merely begins with a thematic break keeps
    all of its text.

    The opening delimiter is not enough on its own, so the block between the
    delimiters has to *be* front matter -- a YAML mapping, read by a YAML
    parser -- before any of it is removed. Which shapes that guard actually
    protects is worth stating precisely, because an earlier version of this
    note had it wrong. A document that opens with
    ``---``, carries one paragraph, and carries a second ``---`` below it does
    *not* hold two thematic breaks: measured against markdown-it 14.3.0 the
    second ``---`` is a Setext underline, so the text between them is a heading
    and the walk below drops it either way. The shapes that really do print a
    paragraph are the block that ends on ``...``, which is a YAML document end
    and an ordinary line of text at the same time, and the block that holds a
    blank line, where everything above the last paragraph is on the page.
    Removing those can take a file under ``MIN_WORDS_TO_SCORE`` and out of the
    gate, which is the one direction this module never errs in. Blank lines are
    allowed between the delimiters: the block ends at its delimiter, not at the
    first blank line.
    Trimming here is ASCII horizontal whitespace only. ``str.strip`` removes
    every Unicode space, so a line reading ``---`` followed by U+00A0 trimmed
    down to ``---`` and opened a block that is not one. The closing-fence rule
    in this same module was already narrowed to spaces and tabs for exactly
    that reason; this is the same rule one function away.
    https://spec.commonmark.org/0.31.2/#setext-headings
    """
    lines = text.split("\n")
    if not lines or lines[0].rstrip(ASCII_HORIZONTAL_WHITESPACE) != "---":
        return text
    if len(lines) < 2 or not lines[1].strip(ASCII_HORIZONTAL_WHITESPACE):
        return text
    for index in range(1, len(lines)):
        line = lines[index].rstrip(ASCII_HORIZONTAL_WHITESPACE)
        if FRONT_MATTER_DELIMITER_PATTERN.match(line):
            if front_matter_is_yaml_mapping("\n".join(lines[1:index])):
                return "\n".join(lines[index + 1 :])
            return text
    return text


def extract_prose(text: str) -> str:
    """Return only the child-facing prose of a Markdown document.

    Removes code fences, tables, headings, navigation lines, thematic breaks,
    images, URLs, inline code, HTML tags, and the two parent-facing regions a
    session carries. List markers and blockquote markers are removed but the
    text after them is kept, because that text is prose a child reads.

    One line of the returned text is one sentence unit. A Markdown paragraph
    can be hard-wrapped over many source lines, so the continuation lines of a
    paragraph are joined back into one line; a blockquote is a container, not a
    unit, so its wrapped lines are joined the same way. A blank line, a heading,
    a table, a code fence, a new list item, and a new quoted paragraph all start
    a new unit, which keeps one worksheet prompt or one list item counting as
    one sentence.

    A document enters this module here, so this is where its line endings are
    made one thing; see ``normalize_line_endings``.
    """
    text = normalize_line_endings(text)
    text = strip_front_matter(text)
    text = strip_html_comments(text)
    # The code spans are found once, over the whole document, because one of
    # them can cross a soft line break and a line read alone cannot see that.
    # Reading each line alone both leaves a multi-line span standing in the
    # prose and pairs the wrong two backtick runs on the line below it, which
    # deletes an ordinary word between two real spans. Blanking keeps every
    # line break and every column, so the walk below reads the same lines in
    # the same places.
    blanked_lines = strip_code_spans(text).split("\n")

    units: list[str] = []
    active_fence: ActiveFence | None = None
    list_contexts: list[ListContext] = []
    in_parent_strip = False
    in_parent_section = False
    in_table = False
    raw_text: str | None = None
    table_container: tuple[Container, ...] = ()
    table_delimiter_row = -1
    after_link_definition = False
    open_unit: str | None = None

    lines = text.split("\n")
    for index, raw_line in enumerate(lines):
        line = raw_line.rstrip(ASCII_HORIZONTAL_WHITESPACE)
        # Per line, and reset here rather than carried: a raw-text run's span
        # belongs to the line the run closes on and to no other.
        raw_text_blank_to = 0

        # Code fences: drop the fence markers and everything between them.
        # The active fence is tested before the opening pattern, so while a
        # block is open only a genuine closing fence ends it. An info string
        # or a trailing comment on a fence line cannot close the block.
        # Both fence lines are normalized to their container first, so a fence
        # inside a blockquote or inside a list item is still a fence.
        if active_fence is not None and fence_container_ended(line, active_fence):
            # The container holding the fence has ended, so the fence
            # ended with it and this line is document text again.
            active_fence = None

        if active_fence is not None:
            # The closing test reads ``raw_line`` rather than ``line``. Python's
            # ``str.rstrip()`` strips Unicode whitespace, so a nonbreaking space
            # after the backticks would be gone before ``is_closing_fence``
            # could refuse it -- and CommonMark permits only spaces and tabs
            # there.
            if is_closing_fence(
                normalize_for_fence_closing(raw_line, active_fence),
                active_fence.character,
                active_fence.minimum_length,
            ):
                active_fence = None
            open_unit = None
            continue
        fence_line = normalize_for_fence_opening(line, list_contexts)
        # This walk carries no HTML block machine -- it is a second pass with its
        # own cascade of tables, headings, parent sections and list units, and
        # the block state belongs with ``scan_document_inlines`` -- so the run
        # is told that every line may open one. The residual is recorded: an
        # ``<xmp>`` opener on a line CommonMark keeps inside the paragraph above
        # it opens a run here that the marker scans refuse. It runs on text
        # whose comments are already removed, so the comment half of the same
        # question cannot arise.
        raw_text, line_raw_text, run_end = raw_text_run_boundary(
            fence_line.content, raw_text, True
        )
        # Asked before the fence, as both sibling hooks ask it: a line a raw-text
        # run holds opens no fenced block, because every character on it is the
        # element's content. Reading the fence first let three backticks a
        # ``<textarea>`` prints open one and swallow the words below them, and
        # the three hooks are meant to agree about which fences a document has.
        opening_fence = (
            None
            if raw_text_run_holds_text(line_raw_text)
            else parse_opening_fence(fence_line.content)
        )
        if opening_fence is not None:
            active_fence = build_active_fence(opening_fence, fence_line)
            open_unit = None
            continue

        if raw_text_run_holds_text(line_raw_text) and not raw_text_run_is_displayed(
            line_raw_text
        ):
            # A script, a stylesheet, a processing instruction, a CDATA
            # section, a declaration, a frame's fallback content and a
            # ``<title>`` are all characters the page drops from its body.
            # None is prose a child reads, and scoring a stylesheet as a
            # sentence lowers the reported grade of every document carrying
            # one. A ``<textarea>`` and an ``<xmp>`` are the other way round
            # -- the reader sees every word -- so their lines fall through to
            # the walk below and are scored.
            #
            # What the element drops is its *content*, and its content ends at
            # its closing tag rather than at the end of the line.
            # ``<script></script> We plan the trip together`` is an empty
            # script and then twelve words a child reads, and dropping the
            # whole line dropped the words too -- the direction that takes a
            # document under ``MIN_WORDS_TO_SCORE`` and out of the gate in
            # silence, which is the one direction this module never errs in.
            # So the run's own span is blanked and the rest of the line goes on
            # through the walk, as the reviewer's note asks. Blanking rather
            # than slicing is what keeps the columns the document's: the
            # container prefix in front of the content is untouched, and every
            # offset below here still points where it pointed.
            if run_end == -1:
                open_unit = None
                continue
            visible = " " * run_end + fence_line.content[run_end:]
            if not visible.strip(ASCII_HORIZONTAL_WHITESPACE):
                open_unit = None
                continue
            raw_text_blank_to = len(line) - len(fence_line.content) + run_end
            line = line[: len(line) - len(fence_line.content)] + visible
            fence_line = replace(fence_line, content=visible)

        # Tables, with or without outer pipe characters. A table is found by
        # its delimiter row. The header line above that row and the body rows
        # below it are part of the same table.
        #
        # A table belongs to the container it opened in and ends where that
        # container ends. ``fence_line.containment_path`` is the same notion of
        # "inside a container" the fence code and the heading check use, so a
        # quoted or a listed table is recognized as the table it is *and* stops
        # at the outdent. Matching on the pipe alone keeps swallowing rows past
        # that point: an unquoted ``Compare option A | option B with your
        # family.`` under a quoted table is a paragraph GFM renders outside the
        # blockquote, and discarding it lowers the word count -- the direction
        # that can take a file under the 40-word minimum and out of the gate.
        # At the *same* container the swallowing is right: GFM really does read
        # a pipe-bearing line under an unquoted table as one more row.
        # https://github.github.com/gfm/#tables-extension-
        table_line = strip_block_quote_prefixes(line)
        if in_table:
            # The delimiter row is the table's own second line and belongs to
            # it however it is spelled: ``| zulu |`` over ``-:`` is a table on
            # GitHub's own renderer, and asking the body-row rule for a pipe
            # left the ``-:`` standing in the prose as a sentence of its own.
            if index == table_delimiter_row or (
                table_line.strip(ASCII_HORIZONTAL_WHITESPACE)
                and "|" in table_line
                and fence_line.containment_path == table_container
            ):
                open_unit = None
                continue
            in_table = False
        # The header row needs no pipe of its own, and asking for one was this
        # walk assembling a precondition its own helpers do not have.
        # ``table_starts_here`` is GFM's whole precondition in one place and
        # the two sibling hooks already ask it: a pipeless header over ``-:``
        # is a one-column table on GitHub's own renderer, measured, and a
        # header long enough to matter was being scored as child-facing prose
        # -- which moves a grade, and can carry a document over the 40-word
        # floor it should never have reached.
        #
        # A table's *body* rows still need a pipe, one line below. That is the
        # same rule in the other direction and it is deliberately not changed
        # here: a pipeless line continues a table body on GitHub, and reading
        # it as one needs a body terminator this walk does not have.
        if table_line.strip(ASCII_HORIZONTAL_WHITESPACE):
            next_line = (
                lines[index + 1].rstrip(ASCII_HORIZONTAL_WHITESPACE)
                if index + 1 < len(lines)
                else ""
            )
            # The lookahead gets a *copy* of the list contexts: normalizing a
            # line records the containers it opens, and the next iteration has
            # to start from the state this line left behind, not that one.
            next_fence_line = normalize_for_fence_opening(
                next_line, list(list_contexts)
            )
            if next_fence_line.containment_path == fence_line.containment_path and (
                table_starts_here(fence_line.content, next_fence_line.content)
            ):
                in_table = True
                table_container = fence_line.containment_path
                table_delimiter_row = index + 1
                open_unit = None
                continue

        # An ATX heading may sit inside a container, where every one of its
        # lines carries that container's prefix. ``fence_line.content`` is the
        # line already peeled to its container's content column -- the same
        # notion of "inside a container" the fence code uses -- so a quoted or
        # a listed heading is recognized as the heading it is. Matching the
        # raw line instead leaves the heading text to be scored as prose and
        # joined to the quoted paragraph under it.
        # https://spec.commonmark.org/0.31.2/#atx-headings
        is_heading = bool(HEADING_PATTERN.match(fence_line.content))

        # A parent-facing section runs from its heading to the next heading.
        if PARENT_SECTION_PATTERN.match(line):
            in_parent_section = True
            open_unit = None
            continue
        if in_parent_section:
            if is_heading:
                in_parent_section = False
            else:
                open_unit = None
                continue

        # The "For parents" strip runs from its bold label to the next heading.
        if PARENT_STRIP_PATTERN.match(line):
            in_parent_strip = True
            open_unit = None
            continue
        if in_parent_strip:
            if is_heading:
                in_parent_strip = False
            else:
                open_unit = None
                continue

        if is_heading:
            open_unit = None
            continue
        if TABLE_ROW_PATTERN.match(table_line):
            open_unit = None
            continue
        # A Setext underline turns the paragraph above it into a heading, so
        # that paragraph is not prose after all and is taken back out. This is
        # tested before the thematic break, because CommonMark reads ``---``
        # under a paragraph as a heading underline and only otherwise as a
        # break. https://spec.commonmark.org/0.31.2/#setext-headings
        if open_unit is not None and units:
            setext_line = table_line if open_unit == UNIT_KIND_QUOTE else line
            if SETEXT_UNDERLINE_PATTERN.match(setext_line):
                units.pop()
                open_unit = None
                continue
        if THEMATIC_BREAK_PATTERN.match(line):
            open_unit = None
            continue
        if NAV_LINE_PATTERN.match(line):
            open_unit = None
            continue
        # A link reference definition renders as nothing. CommonMark does not
        # let one interrupt a paragraph, so an open unit means this line is a
        # wrapped continuation and not a definition.
        # https://spec.commonmark.org/0.31.2/#link-reference-definitions
        if open_unit is None and LINK_DEFINITION_PATTERN.match(table_line):
            after_link_definition = True
            continue
        # A definition's title may sit on the line below its destination, and
        # renders as nothing just as the rest of the definition does.
        if after_link_definition and LINK_DEFINITION_TITLE_PATTERN.match(table_line):
            after_link_definition = False
            continue
        after_link_definition = False

        # The spans go now, and not before. Everything above reads a line as
        # the document holds it, and two of those readings turn on a
        # character a span can carry: a backtick fence whose info string
        # holds a backtick opens no fence, and a pipe inside a span is still
        # a cell delimiter to GFM, which reads a table before it reads any
        # inline.
        # https://github.github.com/gfm/#tables-extension-
        line = blanked_lines[index].rstrip(ASCII_HORIZONTAL_WHITESPACE)
        # The line is re-read from the code-span-blanked document here, so a
        # raw-text run's own characters have to be taken out again: everything
        # above reads the document's line, and this is the point at which the
        # line becomes the text that is scored. The same column serves both
        # blankings, because neither pass changes the document's width.
        if raw_text_blank_to:
            line = " " * min(raw_text_blank_to, len(line)) + line[raw_text_blank_to:]

        # A new list item starts its own unit. A plain line that follows prose
        # is a wrapped continuation of that prose.
        #
        # A blockquote is a container, not a sentence unit: consecutive quoted
        # lines are one wrapped quoted paragraph, so a quoted line continues an
        # open quoted unit. It starts a new unit when nothing quoted is open,
        # when the quote marker carries no text (the blank ``>`` line that ends
        # a quoted paragraph), or when its interior starts its own list item.
        # Without this, re-wrapping a quote would lower its score without
        # changing a word, exactly as re-wrapping a paragraph once did.
        quote_match = BLOCKQUOTE_PATTERN.match(line)
        if quote_match is not None:
            interior = line[quote_match.end() :]
            starts_block = (
                open_unit != UNIT_KIND_QUOTE
                or not interior.strip(ASCII_HORIZONTAL_WHITESPACE)
                or bool(LIST_MARKER_PATTERN.match(interior))
            )
            line = interior
        else:
            starts_block = bool(LIST_MARKER_PATTERN.match(line))

        line = LIST_MARKER_PATTERN.sub("", line)
        line = IMAGE_PATTERN.sub(" ", line)
        line = REFERENCE_IMAGE_PATTERN.sub(" ", line)
        line = REFERENCE_LINK_PATTERN.sub(r"\1", line)
        line = LINK_PATTERN.sub(r"\1", line)
        line = BARE_URL_PATTERN.sub(" ", line)
        # A line a displayed raw-text element holds keeps every character
        # between the element's own tags: the page prints them, so the only
        # markup on the line is the opener and the closer themselves. A
        # comment, a processing instruction, a declaration and a pseudo-tag
        # alike are words a reader reads there.
        line = (
            DISPLAYED_RAW_TEXT_TAG_PATTERN
            if raw_text_run_is_displayed(line_raw_text)
            else HTML_TAG_PATTERN
        ).sub(" ", line)
        line = EMPHASIS_PATTERN.sub("", line)
        # Decoding is last. A reference may name a Markdown character --
        # ``&#42;`` is a literal asterisk and not emphasis -- so nothing is
        # decoded until the Markdown around it has already been read.
        line = decode_character_references(line)

        if line.strip(ASCII_HORIZONTAL_WHITESPACE):
            if open_unit is not None and not starts_block:
                units[-1] = f"{units[-1]} {line.strip()}"
            else:
                units.append(line.strip())
                open_unit = (
                    UNIT_KIND_QUOTE if quote_match is not None else UNIT_KIND_PROSE
                )
        else:
            open_unit = None

    return "\n".join(units)


def count_syllables(word: str) -> int:
    """Estimate the syllables in one English word.

    A heuristic, not a dictionary. It counts vowel groups, then drops a silent
    trailing ``e`` unless the word ends in consonant + ``le``, where that ending
    is its own syllable. A word always counts as at least one syllable. Pure
    numbers count as one syllable, because a digit string has no reliable spoken
    length and numbers are rare in this curriculum's prose.
    """
    lowered = word.lower()
    if lowered[:1].isdigit():
        return 1

    # Read the contraction before the apostrophe is deleted: deleting it fuses
    # "doesn't" into "doesnt", whose one vowel group reports one syllable for a
    # word that is spoken with two. Under-counting syllables lowers the
    # Flesch-Kincaid grade, which is the direction that lets hard text through.
    syllabic_nt = SYLLABIC_NT_PATTERN.search(lowered) is not None

    # An accent is part of a letter, not a break in the word. Folding the
    # combining marks away with NFKD lets the vowel-group pass read ``Osaka``
    # in ``Ōsaka``; deleting the ``Ō`` outright reports two syllables for a
    # three-syllable name, and under-counting syllables lowers the
    # Flesch-Kincaid grade -- the direction that lets hard text through.
    lowered = "".join(
        character
        for character in unicodedata.normalize("NFKD", lowered)
        if not unicodedata.combining(character)
    )
    lowered = re.sub(r"[^a-z]", "", lowered)
    if not lowered:
        return 1

    count = len(VOWEL_GROUP_PATTERN.findall(lowered))

    # A word ending in consonant + "le" keeps that final syllable ("table",
    # "little"), so its trailing "e" is not the silent kind. Every other
    # trailing "e" is dropped ("make", "note"). The vowel-group pass has
    # already counted the "e" in both cases, so this only ever subtracts.
    syllabic_le = (
        len(lowered) > 2 and lowered.endswith("le") and lowered[-3] not in "aeiouy"
    )
    if lowered.endswith("e") and not syllabic_le and count > 1:
        count -= 1

    if syllabic_nt:
        count += 1

    return max(count, 1)


def ends_a_sentence(before: str, closers: str, after: str) -> bool:
    """Return whether one terminal-punctuation break really ends a sentence.

    Two things break a naive "split on every period" rule, and both of them
    inflate the sentence count, which lowers the reported words-per-sentence
    figure and the grade -- the direction that lets hard text through the gate.

    An abbreviation's period is usually not a sentence end: ``The U.S.
    Department of State`` is one sentence. ``U.S.`` and ``U.K.`` are the
    exception, because each is also a complete noun phrase, so they end a
    sentence when a capitalized closed-class word follows. A capitalized
    *content* word after one of them is genuinely ambiguous -- ``the U.S.
    Department of State`` and ``lives in the U.S. Travel starts tomorrow``
    have the same shape -- and is left merged on purpose: merging overstates
    sentence length, which reports the file as harder, and a gate must not err
    the other way.

    A lowercase word after a closing quote or bracket continues the sentence
    it is in: ``your "what do I do next?" page`` is one sentence, not two. The
    closer is what makes this safe to assume. A bare ``sentence. lowercase``
    is left alone, because an inline code span is replaced by a space before
    this runs, so a sentence that *starts* with one legitimately begins with a
    lowercase word here.
    """
    if ABBREVIATION_PATTERN.search(before):
        return (
            FREESTANDING_ABBREVIATION_PATTERN.search(before) is not None
            and SENTENCE_OPENER_PATTERN.match(after) is not None
        )
    if not after[:1].islower():
        return True
    return not closers and AMBIGUOUS_ABBREVIATION_PATTERN.search(before) is None


def split_sentences(prose: str) -> list[str]:
    """Split prose into sentences.

    A line that carries no terminal punctuation still counts as one sentence.
    Worksheet prompts and short list items are written that way throughout the
    curriculum, and treating a whole paragraph of them as a single enormous
    sentence would wrongly inflate every score.

    Not every terminal-punctuation break is a sentence end; see
    ``ends_a_sentence``.
    """
    sentences: list[str] = []
    for line in prose.split("\n"):
        line = line.strip()
        if not line:
            continue
        start = 0
        for match in SENTENCE_SPLIT_PATTERN.finditer(line):
            piece = line[start : match.start()]
            if not ends_a_sentence(piece, match.group("closers"), line[match.end() :]):
                continue
            if WORD_PATTERN.search(piece):
                sentences.append(piece.strip())
            start = match.end()
        tail = line[start:]
        if WORD_PATTERN.search(tail):
            sentences.append(tail.strip())
    return sentences


def score_text(text: str, display_path: str) -> FileScore:
    """Measure the reading level of one document's prose."""
    prose = extract_prose(text)
    sentences = split_sentences(prose)
    words = WORD_PATTERN.findall(prose)

    word_count = len(words)
    sentence_count = len(sentences)

    if word_count < MIN_WORDS_TO_SCORE or sentence_count == 0:
        return FileScore(
            display_path=display_path,
            words=word_count,
            sentences=sentence_count,
            syllables=0,
            grade=0.0,
            words_per_sentence=0.0,
            scored=False,
            skip_reason=(
                f"only {word_count} prose words; below the {MIN_WORDS_TO_SCORE}-word "
                "minimum for a meaningful score"
            ),
        )

    syllable_count = sum(count_syllables(word) for word in words)
    raw_words_per_sentence = word_count / sentence_count
    syllables_per_word = syllable_count / word_count

    # Round both measures once, here, so the value that is classified is the
    # same value that is reported. A raw grade of 7.485 classifies as a warning
    # but prints as "7.5", which reads as a contradiction of the 7.5 hard limit.
    words_per_sentence = round(raw_words_per_sentence, 2)
    grade = round(
        0.39 * raw_words_per_sentence + 11.8 * syllables_per_word - 15.59, 2
    )

    failures: list[str] = []
    warnings: list[str] = []

    if grade >= GRADE_FAIL:
        failures.append(
            f"Flesch-Kincaid grade {grade:.2f} is at or above the hard limit {GRADE_FAIL}"
        )
    elif grade >= GRADE_WARN:
        warnings.append(
            f"Flesch-Kincaid grade {grade:.2f} is above the target {GRADE_WARN}"
        )

    if words_per_sentence >= SENTENCE_FAIL:
        failures.append(
            f"average sentence length {words_per_sentence:.2f} words is at or above "
            f"the hard limit {SENTENCE_FAIL}"
        )
    elif words_per_sentence >= SENTENCE_WARN:
        warnings.append(
            f"average sentence length {words_per_sentence:.2f} words is above the "
            f"target {SENTENCE_WARN}"
        )

    return FileScore(
        display_path=display_path,
        words=word_count,
        sentences=sentence_count,
        syllables=syllable_count,
        grade=grade,
        words_per_sentence=words_per_sentence,
        failures=tuple(failures),
        warnings=tuple(warnings),
    )


def is_excluded_path(display_path: str) -> bool:
    """Return ``True`` when a path is adult-facing or builder-facing by location."""
    normalized = display_path.replace("\\", "/")
    return any(normalized.startswith(prefix) for prefix in ALWAYS_EXCLUDED_PREFIXES)


def has_adult_marker(text: str) -> bool:
    """Return ``True`` when a document declares itself adult-facing.

    The marker is metadata, so it counts only where CommonMark would render it
    as a comment, and ``document_marker_text`` is the one place this module
    answers that. A marker shown as an example inside a fence or a code span,
    written behind a backslash, or handed to an element as an attribute -- a
    link's title, an image's alt text, an autolink, a tag's attribute value, a
    link reference definition -- is characters on the page and declares
    nothing. Reading the whole document instead, with only its literal code
    blanked, took child-facing documents out of the reading gate in silence.

    This is the module's other door, so the document's line endings are made
    one thing here too; see ``normalize_line_endings``.
    """
    text = normalize_line_endings(text)
    return AUDIENCE_ADULT_PATTERN.search(document_marker_text(text)) is not None


def default_paths(root: Path) -> list[Path]:
    """Return every child-facing Markdown file in the repository."""
    found: set[Path] = set()
    for pattern in DEFAULT_INCLUDE_GLOBS:
        found.update(path for path in root.glob(pattern) if path.is_file())
    return sorted(found)


def default_path_set(root: Path) -> set[Path]:
    """Return the default child-facing corpus as resolved paths, for scope tests.

    A symlink is skipped here for the same reason ``resolve_candidate_path``
    refuses one: the corpus is the real files inside the repository, so a link
    must not put its target into the set.
    """
    found: set[Path] = set()
    for path in default_paths(root):
        if path.is_symlink():
            continue
        try:
            found.add(path.resolve())
        except OSError:
            continue
    return found


def is_inside(path: Path, root: Path) -> bool:
    """Return ``True`` when a path stays inside ``root`` after resolution."""
    try:
        path.resolve().relative_to(root)
    except (OSError, ValueError):
        return False
    return True


def resolve_candidate_path(
    path_argument: str | Path, root: Path
) -> tuple[Path, str] | None:
    """Resolve one path to a Markdown file that stays inside the repository.

    This mirrors the containment rule in ``check-prohibited-placeholders.py``.
    An absolute path outside the repository, a path that climbs out with
    ``..``, and a symlink are all refused, so neither command-line input nor a
    link committed into a scanned tree can make the checker read a file beyond
    the repository.
    """
    root = root.resolve()
    path = Path(path_argument)
    candidate = path if path.is_absolute() else root / path

    if candidate.is_symlink() or not candidate.is_file():
        return None
    if candidate.suffix.lower() != ".md":
        return None

    resolved_candidate = candidate.resolve()
    try:
        relative_path = resolved_candidate.relative_to(root)
    except ValueError:
        return None

    return resolved_candidate, relative_path.as_posix()


def resolve_paths(path_arguments: Sequence[str], root: Path) -> list[tuple[Path, str]]:
    """Turn command-line path arguments into contained Markdown file paths."""
    root = root.resolve()

    candidates: list[Path] = []
    in_scope: set[Path] | None = None
    if not path_arguments:
        candidates.extend(default_paths(root))
    else:
        for argument in path_arguments:
            path = Path(argument)
            candidate = path if path.is_absolute() else root / path
            if (
                candidate.is_dir()
                and not candidate.is_symlink()
                and is_inside(candidate, root)
            ):
                # A directory is a scope selector, so it selects from the same
                # child-facing corpus the default scan uses. Expanding it to
                # every Markdown file below it and then subtracting a list of
                # adult-facing prefixes cannot be kept complete: "." would
                # score every governance and contributor document in the
                # repository root. A named *file* is an explicit request for
                # that one file and is still scored.
                if in_scope is None:
                    in_scope = default_path_set(root)
                found = [
                    entry
                    for entry in sorted(candidate.rglob("*.md"))
                    if not entry.is_symlink() and entry.resolve() in in_scope
                ]
                if not found:
                    print(
                        f"{argument}: no child-facing Markdown found in this "
                        "directory; the scanned trees are DEFAULT_INCLUDE_GLOBS",
                        file=sys.stderr,
                    )
                candidates.extend(found)
                continue
            if resolve_candidate_path(candidate, root) is None:
                print(
                    f"{argument}: skipped; not a Markdown file inside the repository",
                    file=sys.stderr,
                )
                continue
            candidates.append(candidate)

    resolved: list[tuple[Path, str]] = []
    seen: set[Path] = set()
    for candidate in candidates:
        entry = resolve_candidate_path(candidate, root)
        if entry is None or entry[0] in seen:
            continue
        seen.add(entry[0])
        resolved.append(entry)
    return resolved


def scan_files(path_arguments: Sequence[str], root: Path = REPO_ROOT) -> list[FileScore]:
    """Score every in-scope Markdown file named by the arguments."""
    scores: list[FileScore] = []
    for path, display_path in resolve_paths(path_arguments, root):
        if is_excluded_path(display_path):
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            # UnicodeDecodeError is a ValueError, so ``except OSError`` never
            # caught it: a file that is not valid UTF-8 crashed the run with a
            # traceback instead of reporting one unreadable file.
            raise FileReadError(display_path, error) from error

        if has_adult_marker(text):
            continue

        scores.append(score_text(text, display_path))
    return scores


def emit_github_annotation(level: str, score: FileScore, message: str) -> None:
    """Print a GitHub Actions annotation when running inside a workflow."""
    if os.environ.get("GITHUB_ACTIONS") != "true":
        return
    print(f"::{level} file={score.display_path}::{message}")


def report_text(scores: Iterable[FileScore], show_ok: bool) -> tuple[int, int]:
    """Print a human-readable report and return the failure and warning counts."""
    failed = 0
    warned = 0

    for score in scores:
        if score.status == "skip":
            if show_ok:
                print(f"SKIP {score.display_path}: {score.skip_reason}")
            continue

        summary = (
            f"grade {score.grade:.2f}, {score.words_per_sentence:.2f} words/sentence, "
            f"{score.words} words in {score.sentences} sentences"
        )

        if score.status == "fail":
            failed += 1
            for message in score.failures:
                print(f"FAIL {score.display_path}: {message}")
                emit_github_annotation("error", score, message)
            for message in score.warnings:
                print(f"WARN {score.display_path}: {message}")
        elif score.status == "warn":
            warned += 1
            for message in score.warnings:
                print(f"WARN {score.display_path}: {message}")
                emit_github_annotation("warning", score, message)
        elif show_ok:
            print(f"OK   {score.display_path}: {summary}")

    return failed, warned


def report_json(scores: Iterable[FileScore]) -> tuple[int, int]:
    """Print the scores as JSON and return the failure and warning counts."""
    payload = []
    failed = 0
    warned = 0
    for score in scores:
        if score.status == "fail":
            failed += 1
        elif score.status == "warn":
            warned += 1
        payload.append(
            {
                "path": score.display_path,
                "status": score.status,
                "grade": score.grade,
                "words_per_sentence": score.words_per_sentence,
                "words": score.words,
                "sentences": score.sentences,
                "syllables": score.syllables,
                "failures": list(score.failures),
                "warnings": list(score.warnings),
                "skip_reason": score.skip_reason,
            }
        )
    print(json.dumps(payload, indent=2))
    return failed, warned


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Check child-facing curriculum Markdown for reading level. "
            "With no paths, scans every child-facing tree."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help=(
            "Markdown files to score, or directories to scan for child-facing "
            "Markdown. A directory keeps the default child-facing scope."
        ),
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures as well.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Report format (default: text).",
    )
    parser.add_argument(
        "--show-ok",
        action="store_true",
        help="Also list files that pass, and files skipped as too short.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None, root: Path = REPO_ROOT) -> int:
    """Run the readability check."""
    args = parse_args(argv)

    try:
        scores = scan_files(args.paths, root=root)
    except FileReadError as error:
        print(error, file=sys.stderr)
        return 1

    if args.format == "json":
        failed, warned = report_json(scores)
    else:
        failed, warned = report_text(scores, show_ok=args.show_ok)
        scored = [s for s in scores if s.scored]
        print(
            f"\nReadability: {len(scored)} file(s) scored, "
            f"{failed} failing, {warned} warning."
        )

    if failed:
        return 1
    if warned and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
