"""Check child-facing Markdown for reading level.

The curriculum targets a fourth-to-sixth-grade reading level for the text a
child reads. This script measures two things that a human cannot eyeball
reliably across dozens of files:

* **Flesch-Kincaid grade level** -- the US school grade needed to read the text.
* **Average sentence length** -- the single strongest lever on the grade score,
  reported separately so an author knows *why* a file scored high.

The checker intentionally stays dependency-free, like the prohibited-placeholder
hook beside it, so it runs in the repo-local hook environment on Windows,
macOS, Linux, and WSL with no install step.

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
from dataclasses import dataclass, field
from html.entities import html5
from pathlib import Path

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
AUDIENCE_ADULT_PATTERN = re.compile(
    r"<!--\s*audience:\s*(?:adult|parent|builder)\b.*?-->", re.IGNORECASE
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
BLOCK_QUOTE_PREFIX_PATTERN = re.compile(r"^ {0,3}> ?")
LIST_ITEM_PATTERN = re.compile(r"^(?P<indent> {0,3})(?P<marker>[-*+]|\d{1,9}[.)])(?P<spacing> +)")
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
#: The six HTML block start conditions that may interrupt a paragraph. A line
#: matching one of them ends the paragraph above it, so it is where a code span
#: stops looking for its closing run. Measured at the commit this fixes: ``Use
#: `open`` on one line and ``<!-- audience: adult -->`` on the next were read
#: as one paragraph, the two lines paired their backticks across the comment,
#: and the marker was blanked -- so an adult-facing document walked into the
#: child reading gate.
#:
#: Condition 7 is deliberately absent. It is the one condition that may *not*
#: interrupt a paragraph, so adding it here would end paragraphs CommonMark
#: leaves open; where no paragraph is open there is nothing for it to end.
#: Condition 4 asks for an uppercase letter after ``<!`` because markdown-it
#: 14.3.0 asks for one and this repository measures a rendered page against
#: markdown-it; the CommonMark 0.31.2 prose says "an ASCII letter" and
#: micromark-core-commonmark 2.0.3 reads it that way, and the sibling hooks
#: carry the same note beside the same choice.
#:
#: The sibling hooks carry the whole ``HTML_BLOCK_CONDITIONS`` machine, with
#: the end patterns and the open-block state, because they have to know which
#: lines are *inside* a block. This module asks a narrower question -- where
#: does a paragraph end -- so it needs the start conditions and nothing else.
#: https://spec.commonmark.org/0.31.2/#html-blocks
HTML_BLOCK_START_PATTERNS = (
    re.compile(r"^ {0,3}<(?:script|pre|style|textarea)(?:[ \t>]|$)", re.IGNORECASE),
    re.compile(r"^ {0,3}<!--"),
    re.compile(r"^ {0,3}<\?"),
    re.compile(r"^ {0,3}<![A-Z]"),
    re.compile(r"^ {0,3}<!\[CDATA\["),
    re.compile(
        rf"^ {{0,3}}</?(?:{HTML_BLOCK_ELEMENT_NAMES})(?:[ \t>]|/>|$)",
        re.IGNORECASE,
    ),
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
LINK_LABEL_MAXIMUM_CHARACTERS = 999

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
    \[ (?=[^\]]*[^ \t\r\n\]])              # a label with at least one nonblank
       (?P<label> (?: [^\[\]\\] | \\. )+ ) \]
    :\ *                                     # the colon, then optional spaces
    {_LINK_DESTINATION}                      # the destination
    (?P<title> \ +                           # an optional title
        (?: " (?: [^"\\] | \\. )* "
          | ' (?: [^'\\] | \\. )* '
          | \( (?: [^()\\] | \\. )* \) )
    )?
    \ *$
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
    r"^ {0,3}\[(?=[^\]]*[^ \t\r\n\]])(?P<label>(?:[^\[\]\\]|\\.)+)\]:[ \t]*$"
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

#: A title alone on its own line, which the definition above it takes. Kept
#: identical to the constant in
#: ``.github/scripts/check-session-structure.py``.
LINK_REFERENCE_TITLE_LINE_PATTERN = re.compile(
    r"""
    ^[ \t]*
    (?: " (?: [^"\\] | \\. )* "
      | ' (?: [^'\\] | \\. )* '
      | \( (?: [^()\\] | \\. )* \) )
    [ \t]*$
    """,
    re.VERBOSE,
)
#: A YAML front-matter delimiter. Front matter is permitted on any Markdown
#: file in this repository, and its keys are publishing metadata, not text a
#: child reads.
FRONT_MATTER_DELIMITER_PATTERN = re.compile(r"^(?:-{3}|\.{3})[ \t]*$")
#: One YAML plain scalar, as the grammar draws one: a run that never holds
#: ``": "``, never ends on a bare ``:``, and never holds `` #``. It is spelled
#: once and used for a key and for a value, because YAML says the same of both.
#: https://yaml.org/spec/1.2.2/#733-plain-style
_YAML_PLAIN_SCALAR = r"(?: (?!:[ \t]) (?!:$) (?![ \t]\#) [^\n] )*"
#: One YAML double-quoted scalar, and one single-quoted one. Both carry an
#: escape and a pattern that stops at the first quote cannot read either: a
#: backslash escapes the character after it in the double-quoted style, and a
#: doubled quote is the only escape the single-quoted style has. So ``title: "A
#: \"quoted\" trip"`` and ``title: 'It''s a trip'`` are one scalar each, and
#: PyYAML reads both. Measured at the commit this fixes: neither line matched,
#: the block stopped being front matter, and the title, the key and the
#: delimiter walked into the child's prose -- 38 words became 42 and the grade
#: moved from 0.0 to -0.33. Reading the escape closes the other direction too:
#: ``title: "unclosed \"`` is not a YAML scalar at all, and the old pattern
#: accepted it.
#: https://yaml.org/spec/1.2.2/#732-single-quoted-style
#:
#: https://yaml.org/spec/1.2.2/#731-double-quoted-style
_YAML_DOUBLE_QUOTED = r'"(?:[^"\\]|\\.)*"'
_YAML_SINGLE_QUOTED = r"'(?:[^']|'')*'"
#: One character inside a YAML flow collection: a quoted scalar read whole, or
#: any character that is neither a collection delimiter nor a quote. The quoted
#: forms are read whole so that a delimiter inside one does not end the
#: collection: ``{note: "a } b"}`` is one mapping and not a broken one.
#: https://yaml.org/spec/1.2.2/#74-flow-collection-styles
_YAML_FLOW_ITEM = (
    "(?:" + _YAML_DOUBLE_QUOTED + "|" + _YAML_SINGLE_QUOTED + "|" + r"[^\n{}\[\]'\"]" + ")"
)
#: How many levels of nesting a flow collection may hold and still be read as
#: one. Python's ``re`` has no recursion, so the nesting is unrolled to a fixed
#: depth; three covers the publishing metadata a Markdown file carries, and a
#: deeper one falls to the strict side -- the block stops being front matter and
#: its lines are scored as prose, which is the error this whole pattern exists
#: to avoid, in a rarer shape.
_YAML_FLOW_NESTING_DEPTH = 3


def _yaml_flow_collection(depth: int) -> str:
    """Return the pattern for a YAML flow collection nested ``depth`` deep.

    A flow mapping ``{...}`` or a flow sequence ``[...]``. It is spelled here
    because the plain-scalar rule cannot hold one: a plain scalar may never
    carry ``": "``, and ``trip: {city: Tokyo, days: 5}`` is a mapping whose
    value carries one. Without this the line is not front matter, the block
    around it stops being front matter with it, and the publishing metadata and
    the ``...`` delimiter are counted as words a child reads.
    """
    item = _YAML_FLOW_ITEM
    for _ in range(depth):
        item = "(?:" + item + r"|\{" + item + r"*\}|\[" + item + r"*\])"
    return r"(?:\{" + item + r"*\}|\[" + item + r"*\])"


_YAML_FLOW_COLLECTION = _yaml_flow_collection(_YAML_FLOW_NESTING_DEPTH)
#: A line a YAML front-matter block can hold: a mapping key, a sequence item, an
#: indented continuation, or a comment. A plain key may hold spaces --
#: ``session title: Trip plan`` is a mapping with one key -- so what separates
#: front matter from prose is the block frame around it and the plain-scalar
#: rule above, not a ban on internal whitespace. Measured against PyYAML over
#: this repository's own lines the two agree, including on the navigation line
#: every session carries: ``You are here: Phase 0 (Setup). Previous: none`` is
#: not YAML, because a plain *value* may not hold ``": "`` either.
#:
#: A document that merely opens with a thematic break is still safe, for a
#: reason worth writing down. Its second ``---`` is a Setext underline rather
#: than a second break, so CommonMark turns the text between them into a
#: heading -- and ``extract_prose`` drops a heading whether or not this pattern
#: matched the line. The shapes where the block really does print a paragraph
#: are the ones that end on ``...``, and the ones that hold a blank line; there
#: this pattern is what keeps the words, and a mapping-shaped sentence closed
#: by ``...`` stays genuinely ambiguous, because it is a YAML document end and
#: a CommonMark paragraph at once. YAML wins that tie, since front matter is a
#: YAML convention and not a CommonMark one.
#:
#: A mapping line may end on a comment, and ``title: Trip plan # editorial
#: note`` is a line this pattern has to recognise or the whole block stops
#: being front matter. That matters only for the two shapes that really print:
#: a block closed by ``...``, and a block holding a blank line. There the title,
#: the note and the delimiter walked into the child's prose and moved the
#: reading score. The space before the ``#`` is required, because YAML requires
#: it: ``version: 1.0#2`` is the plain scalar ``1.0#2`` and not a comment.
#:
#: A value may also be a flow collection, which is why ``_YAML_FLOW_COLLECTION``
#: is one of the alternatives. The collection has to be balanced and has to
#: fill the value to the end of the line, which is what keeps the widening from
#: reaching prose: ``[Tokyo](https://example.com "a title: here")`` is a
#: Markdown link, not a flow sequence, and it stays rejected.
#: https://yaml.org/spec/1.2.2/#66-comments
FRONT_MATTER_LINE_PATTERN = re.compile(
    rf"""
    ^(?:
        [ \t]                                     # an indented continuation
      | \#                                        # a comment
      | -[ \t]                                    # a sequence item
      | (?: {_YAML_DOUBLE_QUOTED} | {_YAML_SINGLE_QUOTED}   # a quoted key
          | [^ \t\r\n#:'"]{_YAML_PLAIN_SCALAR} )           # or a plain one
        :
        (?: [ \t]+ (?: {_YAML_DOUBLE_QUOTED}                # a quoted value
                     | {_YAML_SINGLE_QUOTED}
                     | {_YAML_FLOW_COLLECTION}                # a flow collection
                     | [^ \t\r\n#'"]{_YAML_PLAIN_SCALAR} ) )?
        (?: [ \t]+ \# [^\n]* )?                     # and then a comment
        [ \t]*$
    )
    """,
    re.VERBOSE,
)

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
    """

    kind: str
    indent: int = 0


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


def list_content_indent(match: re.Match[str]) -> int:
    """Return the list-item content indent relative to the marker's parent interior."""
    marker_end_column = match.end("marker")
    spacing_width = len(match.group("spacing"))
    content_padding = spacing_width if spacing_width <= 4 else 1
    return marker_end_column + content_padding


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
        extras.append(Container(kind=CONTAINER_KIND_LIST, indent=content_indent_rel))
        relative_line = (
            relative_line[content_indent_rel:] if len(relative_line) >= content_indent_rel else ""
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


def is_table_delimiter(line: str) -> bool:
    """Return ``True`` when a line is a Markdown table delimiter row.

    Outer pipe characters are optional in a Markdown table, so ``--- | ---``
    is a delimiter row in the same way that ``| --- | --- |`` is. A line with
    no pipe character is a thematic break, not a table.
    """
    return "|" in line and TABLE_DELIMITER_PATTERN.match(line) is not None


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


def starts_a_block(
    content: str,
    containment_path: tuple[Container, ...],
    opened: tuple[Container, ...],
    previous_path: tuple[Container, ...],
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

    A raw HTML block ends one too. Six of the seven start conditions may
    interrupt a paragraph, and a line that opens one is raw HTML rather than
    the next line of the prose above it; ``HTML_BLOCK_START_PATTERNS`` names
    them. Condition 7 is not among them, because it is the one that may not
    interrupt a paragraph.

    ``check-session-structure.py`` asks this question under this name, of the
    first six shapes, so the two hooks cannot disagree about where a paragraph
    ends. The HTML block start is the seventh shape and it is asked here alone:
    that hook runs a full ``HTML_BLOCK_CONDITIONS`` machine beside this
    question and ends its scan on any line that machine calls raw HTML, so
    asking again there would be a second, weaker copy of a rule it already
    models. This module has no such machine, and this is where it says where a
    paragraph ends.

    It is not the question ``opens_a_paragraph`` asks there -- that one asks
    whether a paragraph is open *below* a line, which HTML block condition 7
    needs, and a Setext underline is where the two answers part.
    https://spec.commonmark.org/0.31.2/#paragraphs
    https://spec.commonmark.org/0.31.2/#html-blocks
    """
    if not content.strip(ASCII_HORIZONTAL_WHITESPACE):
        return True
    if ATX_HEADING_LINE_PATTERN.match(content) is not None:
        return True
    if THEMATIC_BREAK_LINE_PATTERN.match(content) is not None:
        return True
    if SETEXT_UNDERLINE_PATTERN.match(content) is not None:
        return True
    if any(pattern.match(content) is not None for pattern in HTML_BLOCK_START_PATTERNS):
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

    A bare destination ends at every character in
    ``DESTINATION_STOP_CHARACTERS``: the space and the ASCII control
    characters, which is the set CommonMark forbids it. An unbalanced
    parenthesis and an unclosed title each mean no link at all, and the caller
    is then right to read the characters as ordinary text.
    https://spec.commonmark.org/0.31.2/#links
    """
    length = len(line)
    index = open_index + 1
    while index < length and line[index] in " \t":
        index += 1

    if index < length and line[index] == "<":
        cursor = index + 1
        while cursor < length and line[cursor] not in "<>":
            cursor += 2 if line[cursor] == "\\" else 1
        if cursor >= length or line[cursor] != ">":
            return -1
        index = cursor + 1
    else:
        depth = 0
        while index < length:
            character = line[index]
            if character == "\\":
                index += 2
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
    while spaced < length and line[spaced] in " \t":
        spaced += 1
    if index < spaced < length and line[spaced] in "\"'(":
        closer = {'"': '"', "'": "'", "(": ")"}[line[spaced]]
        cursor = spaced + 1
        while cursor < length and line[cursor] != closer:
            cursor += 2 if line[cursor] == "\\" else 1
        if cursor >= length:
            return -1
        index = cursor + 1

    while index < length and line[index] in " \t":
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

    Kept identical to the helper in
    ``.github/scripts/check-session-structure.py``.
    """
    return " ".join(label.split()).casefold()


def is_link_label(label: str) -> bool:
    """Return whether ``label`` is short enough to be a link label at all.

    Kept identical to the helper in
    ``.github/scripts/check-session-structure.py``.
    """
    return len(label) <= LINK_LABEL_MAXIMUM_CHARACTERS


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
    definition = LINK_REFERENCE_DEFINITION_PATTERN.match(line)
    if definition is not None and is_link_label(definition.group("label")):
        return ((0, len(line)),)

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
            # target. The two are tried in the order ``scan_inline_run`` tries
            # them, and for the same reason: a tag name may not hold a colon
            # and a URI autolink must, so only one of the two can match here.
            # <https://spec.commonmark.org/0.31.2/#raw-html>
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
                if normalize_link_label(label) in defined_labels:
                    metadata, consumed = (after, label_close + 1), label_close + 1
        elif normalize_link_label(line[text_start:index]) in defined_labels:
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
        if destination is None:
            return 0
        if destination.group("title") is None and (
            LINK_REFERENCE_TITLE_LINE_PATTERN.match(line_at(2)) is not None
        ):
            return 3
        return 2

    definition = LINK_REFERENCE_DEFINITION_PATTERN.match(line_at(0))
    if definition is None or not is_link_label(definition.group("label")):
        return 0
    if definition.group("title") is None and (
        LINK_REFERENCE_TITLE_LINE_PATTERN.match(line_at(1)) is not None
    ):
        return 2
    return 1


def collect_reference_labels(contents: Sequence[str]) -> frozenset[str]:
    """Return every link label the document defines, normalized.

    A label is defined only where a whole definition parses. CommonMark wants a
    destination for that, so ``[x]:`` with a line of prose under it defines
    nothing at all: the brackets stay on the page, a reference to ``x`` below
    them is the characters the author typed, and a marker inside one of those
    is a comment the child's page really carries.

    The lines a definition fills are skipped with it, so a destination or a
    title sitting on its own line is never read as a second label. A line
    inside a fenced block enters this walk empty, which no part of a definition
    matches. Kept identical to the helper in
    ``.github/scripts/check-session-structure.py``.
    https://spec.commonmark.org/0.31.2/#link-reference-definitions
    """
    labels: set[str] = set()
    row = 0

    while row < len(contents):
        span = reference_definition_span(contents, row)
        if span == 0:
            row += 1
            continue
        match = LINK_REFERENCE_LABEL_PATTERN.match(contents[row])
        if match is not None:
            labels.add(normalize_link_label(match.group("label")))
        row += span

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

        if index == 0 and count_leading_spaces(line[content_start:]) >= 4:
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
                target_end = inline_link_end(line, index + 1)
                if target_end != -1:
                    index = target_end
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

    skips: dict[int, tuple[tuple[int, int], ...]] = {}
    for row, line in enumerate(lines):
        start = line.content_start
        regions = link_metadata_regions("".join(masked[row])[start:], defined_labels)
        if regions:
            skips[row] = tuple((left + start, right + start) for left, right in regions)
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

    Ranges are half open and are offsets into ``text``.
    https://spec.commonmark.org/0.31.2/#fenced-code-blocks
    https://spec.commonmark.org/0.31.2/#code-spans
    """
    fenced: list[tuple[int, int]] = []
    runs: list[tuple[list[ParagraphLine], list[int]]] = []
    contents: list[str] = []
    comment_lines: list[str] = []
    paragraph: list[ParagraphLine] = []
    rows: list[int] = []
    active_fence: ActiveFence | None = None
    list_contexts: list[ListContext] = []
    previous_path: tuple[Container, ...] = ()
    offset = 0

    def close_paragraph() -> None:
        nonlocal paragraph, rows, previous_path
        if paragraph:
            runs.append((paragraph, rows))
        paragraph = []
        rows = []
        previous_path = ()

    for number, raw_line in enumerate(text.split("\n")):
        line_start = offset
        offset += len(raw_line) + 1
        line = raw_line.rstrip(ASCII_HORIZONTAL_WHITESPACE)
        contents.append("")
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
            continue

        fence_line = normalize_for_fence_opening(line, list_contexts)
        opening_fence = parse_opening_fence(fence_line.content)
        if opening_fence is not None:
            active_fence = build_active_fence(opening_fence, fence_line)
            fenced.append((line_start, line_start + len(raw_line)))
            close_paragraph()
            continue

        contents[number] = fence_line.content
        if starts_a_block(
            fence_line.content,
            fence_line.containment_path,
            fence_line.opened,
            previous_path,
        ):
            close_paragraph()
        previous_path = fence_line.containment_path
        paragraph.append(
            ParagraphLine(
                start=line_start,
                text=line,
                content_start=len(line) - len(fence_line.content),
            )
        )
        rows.append(number)

    close_paragraph()

    defined_labels = collect_reference_labels(contents)
    spans: list[tuple[int, int]] = []
    for run_lines, run_rows in runs:
        comments, code_spans = paragraph_inlines(run_lines, defined_labels)
        spans.extend(code_spans)
        for row, comment in zip(run_rows, comments, strict=True):
            comment_lines[row] = comment

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
    spans: list[tuple[int, int]] = []
    search_from = 0

    while True:
        start = search_from
        while True:
            start = working.find("<!--", start)
            if start == -1 or not mask[start]:
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

    kept: list[str] = []
    index = 0
    for start, end in spans:
        kept.append(text[index:start])
        kept.append(" ")
        index = end

    kept.append(text[index:])
    return "".join(kept)


def strip_front_matter(text: str) -> str:
    """Remove a YAML front-matter block from the start of a document.

    A front-matter block opens with ``---`` on the very first line and closes
    on the next line that is exactly ``---`` or ``...``. Its keys are
    publishing metadata, not prose. The opening line must be followed by a
    nonblank line, so a document that merely begins with a thematic break keeps
    all of its text.

    The opening delimiter is not enough on its own, so every nonblank line of
    the block has to look like front matter before any of it is removed. Which
    shapes that guard actually protects is worth stating precisely, because an
    earlier version of this note had it wrong. A document that opens with
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
            return "\n".join(lines[index + 1 :])
        if (
            line.strip(ASCII_HORIZONTAL_WHITESPACE)
            and FRONT_MATTER_LINE_PATTERN.match(line) is None
        ):
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
    table_container: tuple[Container, ...] = ()
    after_link_definition = False
    open_unit: str | None = None

    lines = text.split("\n")
    for index, raw_line in enumerate(lines):
        line = raw_line.rstrip(ASCII_HORIZONTAL_WHITESPACE)

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
        opening_fence = parse_opening_fence(fence_line.content)
        if opening_fence is not None:
            active_fence = build_active_fence(opening_fence, fence_line)
            open_unit = None
            continue

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
            if (
                table_line.strip(ASCII_HORIZONTAL_WHITESPACE)
                and "|" in table_line
                and fence_line.containment_path == table_container
            ):
                open_unit = None
                continue
            in_table = False
        if table_line.strip(ASCII_HORIZONTAL_WHITESPACE) and "|" in table_line:
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
            if (
                next_fence_line.containment_path == fence_line.containment_path
                and is_table_delimiter(next_fence_line.content)
            ):
                in_table = True
                table_container = fence_line.containment_path
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
        line = HTML_TAG_PATTERN.sub(" ", line)
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
