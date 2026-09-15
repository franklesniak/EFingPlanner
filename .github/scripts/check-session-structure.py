"""Check that every curriculum session carries its mandatory structure.

A session is the unit a child actually sits down with, and its shape is load
bearing rather than cosmetic. The seven mandatory fields are what make a session
startable and, more importantly, *stoppable*: a child with executive-function
difficulty needs to know where to begin, what they are making, and when they are
allowed to be finished. A session missing its Stop Point is not a stylistic
lapse; it is a session that never ends.

The style guide states the rule. This script enforces it, because the curriculum
grows to dozens of sessions and a human will not reliably notice the one that
lost its Workspace heading in an edit.

What is checked
---------------
1. The first heading in the document -- outside every fenced block -- is
   ``# Session NN: Title``, and ``NN`` matches the filename.
2. The navigation line is present in the session header -- the part of the
   document above the first level-two section -- and outside every fenced
   block. The line exists to orient the child before the work starts, so a
   file that moves it below ``## Stop Point`` has it where nobody reads it.
3. The parent metadata strip is present, outside every fenced block, and it
   carries a bullet for Status, for Estimated time, and for Parent
   involvement. Where it sits is deliberately not checked. The specification
   states that the parent-facing meta-fields "may be shown in a compact strip
   near the top ... or grouped at the bottom", so a strip below the work is
   in one of the two places the curriculum allows, and a gate that demanded
   the header would reject it.
4. The six always-mandatory sections exist: Goal, Start Here, Steps, Workspace,
   Artifact Created, Stop Point.
5. Source Check exists, unless the session is exempt (see below).
6. The scaffold sections appear in the canonical relative order, Source Check
   included. The style guide numbers it seventh, and seventh is a position, not
   a label. Other sections may be interleaved freely -- Session 00 carries
   several -- but the scaffold ones may not be reordered, because the order
   *is* the scaffold.
7. No mandatory section is empty. A body that holds only whitespace, only HTML
   comments, only a bare list marker, or only link reference definitions prints
   as a bare heading, so it counts as empty. A reference definition such as
   ``[shared]: https://example.com`` is a line in the file that puts nothing on
   the page; it is no less a definition for being written under a heading the
   child then reads as blank, and no less a definition for being written over
   two lines, with its destination indented under its label.
8. No fenced code block is used as a worksheet fill-in. Worksheet forms are
   Markdown tables; a fenced block of blanks does not print as a box, does not
   become an editable cell when the page is copied into Google Docs, and does
   not reflow on a phone. A blank is a run of four or more underscores that
   starts or ends a token, which is what a child writes on; a run with word
   characters on both sides, such as ``A____B``, is part of an identifier in a
   code example and is left alone. A fence nested in a list item or a
   blockquote is still a fence; a fence line carrying anything but whitespace
   after the backticks does not close one; a fence ends with the list item or
   blockquote that holds it, as CommonMark says it does; and a fence that is
   never closed still holds what it holds.

Source Check exemptions
-----------------------
Source Check is required only when a session has a research step. Two exemptions
are recognised, both explicit and both visible in the file:

* an adult-audience marker (``<!-- audience: adult -->``), since an adult-only
  setup session is not doing child research; or
* ``<!-- no-source-check: <reason> -->``, which states why in the file itself.

Both markers must be real markers. One document scan removes every fenced block
before any structural search runs, so a marker printed inside a fenced example
is an example of a marker, not a marker. The same scan is what the navigation
search, the parent-strip search, and the heading scan read.

That scan also removes every HTML comment span, because a comment prints as
nothing: a ``## Goal`` inside ``<!-- ... -->`` is a heading the child never
sees, and a gate that counts it reports a section that is not on the page. The
two exemption markers are themselves comments, so they are searched against a
second view of the same scan, one that keeps the comments in.

A comment is not the only raw HTML a document can hold. CommonMark opens an
HTML block on a ``<script>``, a ``<?``, a ``<!DOCTYPE``, a ``<![CDATA[``, on
any of the block-level element names, and on a complete tag alone on its line;
every line of such a block is raw HTML rather than Markdown. So ``<div>`` on
the line above ``## Goal`` means there is no Goal heading -- the child opens the
session and reads neither the element nor a section. The scan classifies those
blocks for the same reason it classifies comments: a heading Markdown does not
parse is not a section, and a gate that counts one reports a scaffold the file
does not have.

The comment is one of those conditions rather than a state beside them, and
that is load bearing: a ``<script>`` line written *inside* a comment opens no
block, because no start condition is tried while a block is open. So is the
container: a block opened inside a blockquote or a list item ends where that
container ends, exactly as an unclosed fence does, and the headings the
document outdents to are headings again.

A marker nested in a blockquote or a list item is still a marker. CommonMark
decides what a line is from what is left once the container prefixes are
consumed, so ``> <!-- no-source-check: ... -->`` is the same comment the
unindented form is, and the scan reads it the same way.

A marker is also still a marker when it follows prose on the same line.
``No research is needed. <!-- no-source-check: offline exercise -->`` is an
inline comment span, and it prints exactly as nothing as the whole-line form
does; the sibling placeholder hook documents that placement for its own
suppression marker. So the marker view keeps the comment spans a line holds,
not only the lines that are comments end to end. It keeps the spans CommonMark
reads as comments: a marker inside a code span -- including one that opens on
one line and closes on the next -- behind a backslash escape, inside an HTML
tag's attribute, in an image's alt text, in a link's destination or title, in a
reference label the document defines, or indented four spaces prints as
characters on the page or as an attribute of an element, and prose about a
marker exempts nothing.

Silence is never an exemption. If a session genuinely has no research step, it
says so.

Which files are read
--------------------
With no arguments the script walks ``framework/sessions``. It walks rather
than globs, and that is the load-bearing choice. A glob reports what it
matched and is silent about what it passed over, so everything it passes over
is invisible to the gate: ``Path.glob`` does not descend into a symbolic link
to a directory, does not match ``.MD`` on a case-sensitive filesystem, and
swallows the ``PermissionError`` from a directory it cannot read. Each of
those is a subtree the gate never opens while it prints ``all well-formed``.

So the walk enumerates directory entries and gives every entry it sees exactly
one disposition: checked, refused, descended into, or skipped for a stated
reason. The four are counted, and a run whose dispositions do not add up to
the number of entries seen fails rather than reports. An entry cannot go
missing without the arithmetic saying so.

Every path the walk accepts goes through one guard, as does every path the
run was *given* -- the scan root of a default run included. The guard refuses
a symbolic link, refuses a Windows junction, and refuses anything that
resolves outside the repository root; all three tests are needed, because a
link is not always what ``resolve()`` catches, a junction is not what
``is_symlink()`` catches, and a link that points back inside the tree is
caught by neither. The root is no exception: a linked ``framework/sessions``
is the whole corpus redirected, and a run that follows it reports on a
directory nobody asked about.

The roots are accounted for the way the entries below them are. Each root the
run was given is walked, checked, or refused, and the three are reconciled
against the number requested. A root that is walked and yields neither a
target nor a refusal is itself refused, because a path that was named and
then contributed nothing is a path the run passed over in silence -- and the
run-wide "this run checked nothing" guard stops seeing it the moment a second
argument supplies a real file.

A refused path is a violation, not a silent skip. A gate that prints ``all
well-formed`` over a session file it declined to open is telling the reader
something it does not know, so a refusal fails the run.
"""

from __future__ import annotations

import argparse
import re
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

#: Spaces and tabs, the only whitespace CommonMark and YAML treat as
#: horizontal. ``str.strip`` with no argument also removes U+00A0 and the
#: rest of Unicode, which is how a non-delimiter became a delimiter.
ASCII_HORIZONTAL_WHITESPACE = " \t"

#: The directory the default scan reads. It is a directory, not a glob,
#: because the walk below enumerates what is there and gives every entry a
#: disposition. A pattern can only report what it matched; it can never
#: report what it passed over, and what it passes over is invisible.
DEFAULT_SCAN_ROOT = "framework/sessions"

#: The extension a session file carries, compared case-insensitively. The
#: CI runner's filesystem is case-sensitive and the developer's is not, so a
#: lowercase pattern reads a different corpus in the two places. A gate that
#: checks a different set of files on CI than on the desk is not a gate.
MARKDOWN_SUFFIX = ".md"

#: The six sections every session carries, in the order they must appear.
MANDATORY_SECTIONS = (
    "Goal",
    "Start Here",
    "Steps",
    "Workspace",
    "Artifact Created",
    "Stop Point",
)

#: The seventh, required only when the session has a research step.
SOURCE_CHECK_SECTION = "Source Check"

#: Every scaffold section, in the order it must appear. Source Check is
#: conditional in *presence* -- a session with no research step does not carry
#: it -- but not in *position*. A session that carries it puts it seventh.
ORDERED_SECTIONS = MANDATORY_SECTIONS + (SOURCE_CHECK_SECTION,)

#: Matches the *title text* of a heading, not the heading line. The leading
#: hashes are consumed by HEADING_PATTERN, so there is one heading parser.
TITLE_PATTERN = re.compile(r"^Session\s+(?P<number>\d{2}):\s+\S")
FILENAME_NUMBER_PATTERN = re.compile(r"^(?P<number>\d{2})[_-]")
#: The navigation line, with its value. ``[^\\S\\r\\n]`` is horizontal
#: whitespace only, for the reason the parent-strip fields below use it: a
#: plain ``\\s*`` crosses the line break and takes the *next* line's first
#: character as the value, so ``You are here:`` with the location deleted --
#: which is what happens when it is cut from just above the parent strip --
#: passes on the strength of the strip's own asterisk. A label is not a
#: navigation line. The child reads the location or they do not.
NAV_PATTERN = re.compile(r"^You are here:[^\S\r\n]*\S", re.MULTILINE)
PARENT_STRIP_PATTERN = re.compile(r"^\*\*For parents:?\*\*", re.MULTILINE)

#: The strip's load-bearing fields. Each pattern requires a *value* after
#: the colon, on the field's own line. A bullet reading ``- Status:`` with
#: nothing after it prints a label and no fact, so a strip made of three of
#: them tells a parent exactly as much as no strip at all.
#:
#: The character classes are exact. ``[^\S\r\n]`` is horizontal
#: whitespace only: a plain ``\s*`` would cross the line break and find
#: the *next* bullet's text, so an empty field would pass anyway. And the
#: value must hold a character that is neither whitespace nor ``*``,
#: because in ``- **Status:**`` the only thing after the colon is the
#: label's own closing emphasis, which is not a value either.
#:
#: Every one of the 15 sessions carries all
#: three, and the spec names them. They are the three facts a parent needs
#: before the child starts: is this session required, how long is it, and
#: does an adult have to be there. ``Planner skill`` and ``Materials`` are
#: not required here: Session 00 carries no ``Planner skill`` line, and a
#: session can need no materials.
PARENT_STRIP_FIELDS: tuple[tuple[str, re.Pattern[str]], ...] = tuple(
    (
        field,
        re.compile(
            rf"^[ \t]*(?:[-*+]|\d{{1,9}}[.)])[ \t]+\*{{0,2}}{field}\*{{0,2}}"
            rf"[^\S\r\n]*:[^\r\n]*[^\s*\r\n]",
            re.IGNORECASE | re.MULTILINE,
        ),
    )
    for field in ("Status", "Estimated time", "Parent involvement")
)
HEADING_PATTERN = re.compile(r"^(?P<hashes>#{1,6})[ \t]+(?P<title>.+?)[ \t]*$")

#: A worksheet fill-in blank: a run of four or more underscores that starts
#: or ends a token. ``Total days ____``, ``Name:____`` and ``$____ per night``
#: are all blanks a child writes on. A run with word characters on both sides
#: is not one: ``A____B`` in a code example renders as code, and the rule this
#: script enforces prohibits underscore *forms*, not underscores.
WORKSHEET_BLANK_PATTERN = re.compile(r"(?<!\w)_{4,}|_{4,}(?!\w)")

#: CommonMark starts an HTML block on a line whose *content* begins with
#: ``<!--`` and ends it on the line that carries ``-->``. Every line of that
#: block is raw HTML, so nothing on it is a heading -- not even text after
#: the ``-->``, which prints as the literal characters the author typed.
#: Content is what is left once the blockquote and list-item prefixes are
#: consumed, which is why this is matched against ``container_content`` and
#: not against the line as the file holds it.
#: <https://spec.commonmark.org/0.31.2/#html-blocks>
HTML_BLOCK_COMMENT_START_PATTERN = re.compile(r"^ {0,3}<!--")

#: The element names CommonMark lists for HTML block start condition 6.
#: <https://spec.commonmark.org/0.31.2/#html-blocks>
HTML_BLOCK_ELEMENT_NAMES = (
    "address|article|aside|base|basefont|blockquote|body|caption|center|col|"
    "colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|"
    "footer|form|frame|frameset|h1|h2|h3|h4|h5|h6|head|header|hr|html|iframe|"
    "legend|li|link|main|menu|menuitem|nav|noframes|ol|optgroup|option|p|"
    "param|search|section|summary|table|tbody|td|tfoot|th|thead|title|tr|"
    "track|ul"
)

#: CommonMark HTML block start condition 7: a complete open or closing tag,
#: alone on its line. It is the one condition that may not interrupt a
#: paragraph, which is why the classifier below is given the paragraph state.
#: Conditions 1 to 6 are tried first, so an opening ``<script>`` never reaches
#: this pattern. Kept identical to the constants in the sibling hook.
#: <https://spec.commonmark.org/0.31.2/#html-blocks>
HTML_BLOCK_TAG_NAME = r"[A-Za-z][A-Za-z0-9-]*"
HTML_BLOCK_ATTRIBUTE = (
    r"[ \t]+[_:A-Za-z][A-Za-z0-9_.:-]*"
    r"""(?:[ \t]*=[ \t]*(?:[^ \t\r\n"'=<>`]+|'[^']*'|"[^"]*"))?"""
)
HTML_BLOCK_TYPE_SEVEN_PATTERN = re.compile(
    rf"^ {{0,3}}(?:<{HTML_BLOCK_TAG_NAME}(?:{HTML_BLOCK_ATTRIBUTE})*[ \t]*/?>"
    rf"|</{HTML_BLOCK_TAG_NAME}[ \t]*>)[ \t]*$"
)

#: The two block shapes that close a paragraph and are not themselves one.
#: They are all the paragraph tracker needs: everything else nonblank that
#: reaches it is either paragraph text or a line already known to be inside a
#: fence or an HTML block.
ATX_HEADING_LINE_PATTERN = re.compile(r"^ {0,3}#{1,6}(?:[ \t]|$)")
THEMATIC_BREAK_LINE_PATTERN = re.compile(
    r"^ {0,3}(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$"
)
#: A Setext heading underline. A run of ``=`` or ``-`` under a paragraph
#: turns that whole paragraph into a heading, so the paragraph is closed and
#: nothing below the underline continues it. A ``-`` run is a Setext
#: underline only while a paragraph is open; with nothing open it is the
#: thematic break ``THEMATIC_BREAK_LINE_PATTERN`` already names, which is why
#: the two tests are ordered. Kept identical to the constant in
#: ``.github/scripts/check-readability.py``.
#: <https://spec.commonmark.org/0.31.2/#setext-headings>
SETEXT_UNDERLINE_PATTERN = re.compile(r"^ {0,3}(?:=+|-+)[ \t]*$")

#: An inline HTML tag, open or closing. The scan skips one whole tag at a
#: time so that a ``<!--`` inside an attribute value is read as part of the
#: attribute, and a backtick inside one opens no code span, which is what
#: CommonMark does with both. Kept identical to the constant in
#: ``.github/scripts/check-readability.py``.
#: <https://spec.commonmark.org/0.31.2/#raw-html>
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
#: <https://spec.commonmark.org/0.31.2/#raw-html>
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
#: <https://html.spec.whatwg.org/multipage/parsing.html#rawtext-state>
#: <https://spec.commonmark.org/0.31.2/#html-blocks>
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

#: A list marker with nothing after it. It prints as a bullet and no words.
BARE_LIST_MARKER_PATTERN = re.compile(r"^[ \t]*(?:[-*+]|\d{1,9}[.)])[ \t]*$")

#: One character of a bare link destination, and the nesting CommonMark allows
#: around it. A bare destination "includes parentheses only if they are
#: backslash-escaped or part of a balanced pair of unescaped parentheses", so
#: ``foo)`` is not a destination and the line holding it is a paragraph the
#: child reads. ``re`` cannot recurse, so three levels of nesting are spelled
#: out, exactly as they are in ``.github/scripts/check-readability.py``; a
#: destination nested deeper than that simply does not match, which leaves the
#: line counting as content. That is this checker's safe direction: the error
#: that matters here is the one that calls a section empty when the page shows
#: something.
#:
#: What a bare destination may hold is the ASCII rule and not more: it may not
#: hold a space, and it may not hold an ASCII control character. It may not
#: *start* with ``<``, which is the lookahead below, and it may hold one
#: further along, which this class once refused. Both renderers agree on the
#: refusal being wrong: markdown-it 14.3.0 and micromark 4.0.2 each link
#: ``[x](foo< "t")``, so a definition written that way renders nothing and a
#: marker in its title is an attribute rather than a comment -- and this hook
#: was honouring it. U+007F is named beside ``\x00-\x1f`` because CommonMark
#: counts it as a control character and the range does not reach it. Kept in
#: step with the class in ``.github/scripts/check-readability.py``.
#: <https://spec.commonmark.org/0.31.2/#link-destination>
_DESTINATION_CHARACTER = r"(?:[^ \x00-\x1f\x7f()\\]|\\.)"
#: The same rule, as a set rather than as a character class, for the
#: hand-written scan in ``inline_link_end``: every character that ends a bare
#: destination. Spelled as a range so the C0 control characters are named once
#: and none is missed. Kept identical to the constant in
#: ``.github/scripts/check-readability.py``.
#: <https://spec.commonmark.org/0.31.2/#link-destination>
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

#: How long a link label may be. CommonMark caps it at 999 characters between
#: the brackets, and the cap is load-bearing here rather than a nicety: a
#: definition is the one construct a section can hold that renders nothing at
#: all, so a label one character too long turns a line that renders *nothing*
#: into a paragraph the child reads. Reported at 999 and measured at 1,000:
#: micromark 4.0.2 prints ``[aaa...]:`` and its destination as visible text,
#: and a section holding only those two lines was being called empty.
#: markdown-it 14.3.0 does not implement the cap at all, so this one rule is
#: checked against micromark and against the spec rather than against the
#: renderer this repository usually asks. The direction settles it either way:
#: honouring the cap can only make this hook call a section full, never empty,
#: and the error that matters is the one that fails a session that is fine.
#: <https://spec.commonmark.org/0.31.2/#link-label>
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
#: A CommonMark link reference definition: ``[label]: destination "title"``.
#: It is a line in the file that renders nothing at all. The destination it
#: names is used by a link somewhere else, or by nothing, so a section holding
#: only these prints to the child as a bare heading.
#:
#: The form is matched conservatively, because the error that matters here is
#: the one that fails a session that is fine: the destination must be one
#: unbroken token or the angle-bracket form, a title must be properly closed,
#: and nothing else may follow. A definition whose destination sits on the
#: following line is not matched, so a section holding one still counts as
#: content -- which is what this checker already did.
#: <https://spec.commonmark.org/0.31.2/#link-reference-definitions>
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

#: A link reference definition's label and colon, matched however the rest of
#: the definition is laid out. This reads the label out of a definition that
#: ``reference_definition_span`` has already parsed whole; on its own it says
#: nothing about whether the document defines anything. A reference whose label
#: has a definition renders as a link or an image: the label itself becomes
#: nothing, and an image's alt text becomes an attribute. A reference with no
#: definition renders as the brackets the author typed, and a marker inside
#: *that* is a comment on the page.
LINK_REFERENCE_LABEL_PATTERN = re.compile(r"^ {0,3}\[(?P<label>(?:[^\[\]\\]|\\.)+)\]:")

#: A definition's label and colon with nothing after them. CommonMark lets the
#: destination sit on the following line, and the construct still renders
#: nothing at all.
LINK_REFERENCE_LABEL_LINE_PATTERN = re.compile(
    rf"^ {{0,3}}\[(?=[^\]]*[^{_LINK_LABEL_BLANK}\]])"
    r"(?P<label>(?:[^\[\]\\]|\\.)+)\]:[ \t]*$"
)

#: A definition's destination, alone on its own line, with the optional title
#: that may follow it there. Conservative for the same reason the full pattern
#: is: the destination must be one unbroken token or the angle-bracket form,
#: and nothing else may follow, so ``Real visible prose.`` under a label line
#: is prose rather than a destination -- which is what the renderer makes of it.
#: ``foo)`` is prose too, for the same reason and by the same rule: the
#: parentheses of a bare destination have to balance.
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

#: What one line is, for the purpose of deciding what on it CommonMark reads as
#: an HTML comment. A blanked line is inside a fenced block and puts nothing on
#: the page. A raw HTML line is passed through to the page as it stands, so
#: only a tag and a comment mean anything on it. A text line is Markdown, where
#: code spans, backslash escapes, images and link metadata all bind tighter
#: than raw HTML does.
MARKER_SOURCE_BLANK = "blank"
MARKER_SOURCE_RAW_HTML = "raw-html"
MARKER_SOURCE_TEXT = "text"

#: One line as the scan records it: which rules read it, what it holds once
#: its container prefixes are peeled, and whether it begins a block of its
#: own. The last of the three is recorded here rather than worked out later
#: because only this walk holds the container path of the line above, which
#: is what tells a wrapped paragraph from a new list item.
MarkerSource = tuple[str, str, bool]

#: These three patterns, and the fence and container helpers below, are kept
#: deliberately in sync with ``.github/scripts/check-prohibited-placeholders.py``
#: and, where they exist there, with ``.github/scripts/check-readability.py``.
#: They are not all present in all three, and the comment must not claim they
#: are. Measured by comparing function bodies with the docstrings dropped:
#: ``normalize_for_fence_opening``, ``parse_opening_fence``,
#: ``normalize_for_fence_closing``, ``is_closing_fence``,
#: ``container_path_ended`` and ``fence_container_ended`` agree across all
#: three; ``container_line``, ``container_content``, ``html_block_state`` and
#: ``opens_a_paragraph`` agree across the two hooks that classify HTML blocks
#: and are absent from the readability module, which has no need of them;
#: ``strip_html_comments`` agrees between the two hooks and differs in the
#: readability module, where it answers a document-wide question rather than a
#: per-line one. Each difference is a deliberate scoping decision, not drift.
#:
#: A search for ``normalize_for_fence_opening`` still finds every copy of the
#: same CommonMark rule in this repository, which is the property that matters:
#: a change to one is visible from the others. Verify agreement by comparing
#: function bodies, never by trusting this comment.
FENCE_OPEN_PATTERN = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})")
BLOCK_QUOTE_PREFIX_PATTERN = re.compile(r"^ {0,3}>[ \t]?")
#: A GFM table's delimiter row, which is the only thing that marks a table.
#: Kept identical to the pattern in ``.github/scripts/check-readability.py``.
#: https://github.github.com/gfm/#tables-extension-
TABLE_DELIMITER_PATTERN = re.compile(
    r"^ {0,3}\|?[ \t]*:?-+:?[ \t]*(?:\|[ \t]*:?-+:?[ \t]*)*\|?[ \t]*$"
)
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
NO_SOURCE_CHECK_PATTERN = re.compile(
    r"<!--\s*no-source-check:\s*(?!-->)\S.*?-->", re.IGNORECASE | re.DOTALL
)


@dataclass(frozen=True)
class Violation:
    """One structural problem in one session file."""

    display_path: str
    line_number: int
    message: str

    def format_message(self) -> str:
        """Return the failure line for this violation."""
        return f"{self.display_path}:{self.line_number}: {self.message}"


@dataclass(frozen=True)
class Heading:
    """One ATX heading, found outside every fenced block."""

    level: int
    title: str
    line_number: int


CONTAINER_KIND_LIST = "list"
CONTAINER_KIND_BLOCK_QUOTE = "blockquote"


@dataclass(frozen=True)
class Container:
    """A peelable Markdown container prefix on a line.

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
    """An active Markdown list, identified by its containment path from the root."""

    containment_path: tuple[Container, ...]


@dataclass(frozen=True)
class HtmlBlockCondition:
    """One CommonMark HTML block condition: how it starts and how it ends.

    ``end`` is the pattern that closes the block on the line carrying it, or
    ``None`` for the conditions a blank line closes; the blank line itself is
    outside the block, which is why it is tested before the start conditions
    are. ``interrupts_paragraph`` is false for condition 7 alone, which is what
    the spec says of it. Kept identical to the record in the sibling hook.
    <https://spec.commonmark.org/0.31.2/#html-blocks>
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
    record in the sibling hook.
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
#: block leaves the paragraph above it open, and a mandatory heading below it is
#: still a heading. Reading it as a block closes that paragraph, lets the next
#: line open a type-seven block, and hides every heading down to the blank line.
#: <https://spec.commonmark.org/0.31.2/#html-blocks>
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
class DocumentScan:
    """One container-aware pass over a session document.

    ``content_lines`` holds every line a reader sees as document text. Each
    line inside a fenced block, each fence marker, and each HTML comment span
    becomes an empty string, so line numbers stay the numbers in the file. The
    heading scan, the navigation search and the parent-strip search all read
    these lines. That is what makes one fence parser and one comment parser
    govern the whole check, rather than the heading scan alone.

    ``marker_lines`` holds only what CommonMark reads as an HTML comment. The
    two Source Check exemption markers *are* comments and nothing else is one.
    A marker in a fenced block, in a code span -- including one that closes on
    a later line -- behind a backslash escape, inside an HTML tag's attribute,
    in an image's alt text, in a link's destination or title, in a reference
    label the document defines, or indented four spaces prints as characters on
    the page or hands them to an element as an attribute; it is prose *about* a
    marker, and it exempts nothing.
    """

    content_lines: tuple[str, ...]
    marker_lines: tuple[str, ...]
    worksheet_fences: tuple[int, ...]

    @property
    def text(self) -> str:
        """Return the document text a reader sees: no fences, no comments."""
        return "\n".join(self.content_lines)

    @property
    def marker_text(self) -> str:
        """Return the document text outside every fence, comments included."""
        return "\n".join(self.marker_lines)


def strip_html_comments(line: str, is_in_html_comment: bool) -> tuple[str, bool]:
    """Remove HTML comment spans from a Markdown line.

    An HTML comment prints as nothing, and it spans lines: CommonMark ends an
    HTML block opened by ``<!--`` only on the line that carries ``-->``. The
    caller threads ``is_in_html_comment`` from one line to the next, which is
    why this takes it and returns it. Kept identical to the parser in
    ``.github/scripts/check-prohibited-placeholders.py``.
    """
    uncommented_parts: list[str] = []
    index = 0

    while index < len(line):
        if is_in_html_comment:
            comment_end = line.find("-->", index)
            if comment_end == -1:
                return "".join(uncommented_parts), True
            index = comment_end + len("-->")
            is_in_html_comment = False
            continue

        comment_start = line.find("<!--", index)
        if comment_start == -1:
            uncommented_parts.append(line[index:])
            break

        uncommented_parts.append(line[index:comment_start])
        comment_end = line.find("-->", comment_start + len("<!--"))
        if comment_end == -1:
            is_in_html_comment = True
            break
        index = comment_end + len("-->")

    return "".join(uncommented_parts), is_in_html_comment


def normalize_line_endings(text: str) -> str:
    """Return ``text`` with every CommonMark line ending written as ``\\n``.

    CommonMark counts a line feed, a carriage return, and a carriage return
    followed by a line feed as one line ending each, so a document saved on
    Windows holds exactly the lines a document saved anywhere else does. The
    translation happens once, here, where a document enters this module --
    never in the predicates below, which would each have to spell ``\\r`` and
    would each be a place to forget it. A closing fence carrying a stray
    ``\\r`` does not close, and every mandatory heading below it disappears
    into the code block that never ended.

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
    """Peel container prefixes from ``line`` in order; return ``(remaining, peeled)``."""
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
        if not remaining.strip(ASCII_HORIZONTAL_WHITESPACE):
            return
        failed_container = top.containment_path[peeled_count]
        if (
            failed_container.kind == CONTAINER_KIND_LIST
            and BLOCK_QUOTE_PREFIX_PATTERN.match(remaining) is not None
        ):
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
    <https://spec.commonmark.org/0.31.2/#list-items>
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


def container_line(line: str, list_contexts: list[ListContext]) -> FenceLine:
    """Return what CommonMark reads on a line, and the containers holding it.

    A line's block type -- an HTML block among them -- is decided from what is
    left once the blockquote and list-item prefixes are consumed, so
    ``> <!-- a comment -->`` opens an HTML block exactly as the unindented form
    does. The path comes back with the content because a block opened on this
    line ends when that path ends. The list contexts are copied because this
    asks a question about one line rather than advancing the document: the
    contexts that govern the rest of the file are the ones the fence
    normalization takes below, from the span-stripped line. Kept identical to
    the helper in the sibling hook.
    """
    return normalize_for_fence_opening(line, list(list_contexts))


def container_content(line: str, list_contexts: list[ListContext]) -> str:
    """Return what CommonMark reads on a line, container prefixes peeled off."""
    return container_line(line, list_contexts).content


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
    <https://spec.commonmark.org/0.31.2/#link-reference-definitions>
    """
    match = LINK_REFERENCE_DEFINITION_PATTERN.match(content)
    return match is not None and is_link_label(match.group("label"))


def opens_a_paragraph(
    content: str, paragraph_open: bool, previous_content: str = ""
) -> bool:
    """Return whether a line of document text leaves a paragraph open below it.

    HTML block condition 7 is the one condition that may not interrupt a
    paragraph, so classifying it needs to know whether one is open. The test is
    deliberately liberal: anything nonblank that is not a heading, a thematic
    break, a Setext underline or a link reference definition leaves a paragraph
    open. Being wrong in that direction only ever *stops* condition 7 from
    opening, which is the behaviour this scan had before it classified
    condition 7 at all. Lines inside a fence, an HTML block or a raw-text
    element never reach here; their caller closes the paragraph outright. Kept
    identical to the helper in the sibling hooks.

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
    <https://spec.commonmark.org/0.31.2/#setext-headings>
    <https://spec.commonmark.org/0.31.2/#link-reference-definitions>
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
    reason ``container_line`` exists: CommonMark decides a line's block type
    from what is left once the prefixes are consumed. The caller is responsible
    for ending a block whose container has ended, which it does before calling
    this. Kept identical to the helper in the sibling hook.
    <https://spec.commonmark.org/0.31.2/#html-blocks>
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
    <https://spec.commonmark.org/0.31.2/#list-items>
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

    ``check-readability.py`` asks this question under this name, of the same
    six shapes, so the two hooks cannot disagree about where a paragraph ends.
    It is not the question ``opens_a_paragraph`` asks above.

    Two of those shapes need the paragraph state, because CommonMark makes both
    of them conditional on one being open. An ordered list may interrupt a
    paragraph only when it starts at 1, so ``2.`` under a sentence is that
    sentence's own text and opens nothing; the rule is the *list's* and not the
    item's, so a ``3.`` under a list already open is its next item and does
    start a block. And a Setext underline may never be a lazy continuation
    line: ``===`` outdented from a quoted or listed paragraph has no root
    paragraph to underline and stays inside the one above it.
    <https://spec.commonmark.org/0.31.2/#paragraphs>
    <https://spec.commonmark.org/0.31.2/#list-items>
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


def closing_backtick_run(line: str, start: int, length: int) -> int:
    """Return the end of the next backtick run of exactly ``length``, or -1.

    A code span closes on a run of the same length and on no other, so a run
    of two is not closed by a run of three. Scanning run by run rather than
    searching for the substring is what keeps that true.
    <https://spec.commonmark.org/0.31.2/#code-spans>
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


def matching_bracket(line: str, open_index: int) -> int:
    """Return the index of the ``]`` closing the ``[`` at ``open_index``, or -1."""
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
    ``.github/scripts/check-readability.py``.
    """
    return _LINK_LABEL_BLANK_RUN.sub(" ", label).strip(" ").casefold()


def is_link_label(label: str) -> bool:
    """Return whether ``label`` is short enough to be a link label at all."""
    return len(label) <= LINK_LABEL_MAXIMUM_CHARACTERS


def inline_link_end(line: str, open_index: int) -> int:
    """Return the index just past the ``)`` of an inline link, or -1.

    Neither half of what sits between those parentheses is on the page: the
    destination becomes the element's ``href`` or ``src`` and the title becomes
    its ``title``. So a comment delimiter inside one is characters in an
    attribute, which is exactly what markdown-it 14.3.0 renders for
    ``[help](page.md "<!-- no-source-check: x -->")``. Kept identical to the
    helper in ``.github/scripts/check-readability.py``.

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
    characters, which is the set CommonMark forbids it. Stopping only at a
    space and a tab accepted ``[x](fo\x01o "<!-- no-source-check: x -->")`` as
    a link, and neither renderer forms one: both print the brackets and the
    marker in them is a comment the page really does carry, so a session that
    had declared its exemption was failed for not declaring one.
    <https://spec.commonmark.org/0.31.2/#links>
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
    not a comment and exempts nothing. A *link's* text is deliberately not here:
    it is inline content, and markdown-it renders a comment inside it as a
    comment.

    Links may not nest, so forming one deactivates every link opener still on
    the stack. That is not a nicety. ``[a [b](u.md) c](v.md "<!-- x -->")``
    renders with the marker visible, because the inner link wins and the outer
    brackets are literal text; a pass that matched brackets naively would have
    hidden a real marker and then refused a session that had declared itself.
    <https://spec.commonmark.org/0.31.2/#links>
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
    comment four spaces into a ``<div>`` block is still a comment and still
    exempts, while ``<div title="<!-- no-source-check: x -->">`` yields nothing
    at all, because the delimiters are inside the tag and the renderer puts
    them in the ``title`` attribute.
    <https://spec.commonmark.org/0.31.2/#html-blocks>

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


def following_backtick_run(contents: Sequence[str], row: int, length: int) -> tuple[int, int]:
    """Return where a code span opened on ``row`` closes, or ``(-1, -1)``.

    A code span spans a soft line break: CommonMark closes it on the next run
    of the same length anywhere in the same paragraph. So the search runs on
    past the end of the line and stops where the paragraph does -- which is
    the end of ``contents``, because the caller hands this one paragraph at a
    time. Past that the opening run is literal text and the lines below it
    are prose again. Naming the block starts here instead of asking
    ``starts_a_block`` named three of its six shapes, and a code span then
    reached across a list item or a blockquote and swallowed a marker that
    exempts a session.
    <https://spec.commonmark.org/0.31.2/#code-spans>
    """
    for next_row in range(row + 1, len(contents)):
        closer = closing_backtick_run(contents[next_row], 0, length)
        if closer != -1:
            return next_row, closer
    return -1, -1




def following_comment_end(contents: Sequence[str], row: int, index: int) -> tuple[int, int]:
    """Return where the comment opened at ``index`` closes, or ``(-1, -1)``.

    A comment crosses a soft line break the way a code span does, and it ends
    where the run ends: an unclosed ``<!--`` is not a comment at all, so the
    caller is right to read the characters after it as ordinary text. Kept in
    step with the helper in ``.github/scripts/check-readability.py``.
    <https://spec.commonmark.org/0.31.2/#raw-html>
    """
    closer = contents[row].find("-->", index + len("<!--"))
    if closer != -1:
        return row, closer + len("-->")
    for next_row in range(row + 1, len(contents)):
        closer = contents[next_row].find("-->")
        if closer != -1:
            return next_row, closer + len("-->")
    return -1, -1


def following_tag_end(contents: Sequence[str], row: int, index: int) -> tuple[int, int]:
    """Return where the tag opened at ``index`` closes, or ``(-1, -1)``.

    CommonMark lets an open tag hold a line ending, in the whitespace between
    attributes and inside a quoted attribute value, so a tag crosses a soft
    line break the way a comment does and ends where the run does. One that
    never closes is no tag at all, and the caller is then right to read its
    characters as text. Kept in step with the helper in
    ``.github/scripts/check-readability.py``.
    <https://spec.commonmark.org/0.31.2/#raw-html>
    """
    prefix = html_tag_prefix(contents[row], index)
    if prefix is None:
        return -1, -1
    for next_row in range(row + 1, len(contents)):
        position, prefix, matched = html_tag_continue(prefix, contents[next_row])
        if not matched:
            return -1, -1
        if prefix is None:
            return next_row, position
    return -1, -1


def following_link_end(contents: Sequence[str], row: int, index: int) -> tuple[int, int]:
    """Return where the link target opened at ``index`` closes, or ``(-1, -1)``.

    A link's target crosses a soft line break the way a comment and a tag do.
    Its destination may hold no line ending, but the whitespace around the
    destination may hold one and a title may hold as many as the run has:
    ``[x](url "title`` over ``continued")`` is one link with one title,
    measured on markdown-it 14.3.0 and on GitHub's own renderer. A first pass
    that read one physical line rejected that target, left the backtick inside
    the title standing as ordinary text, and paired it with a backtick further
    down -- so a session that had declared its Source Check exemption between
    them was failed for not declaring one.

    The rows are joined with the line endings they had and handed to
    ``inline_link_end``, which is the same helper the second pass already runs
    over the same joined text: there is one grammar here and not two. One that
    never closes is no link at all, and the caller is then right to read its
    characters as text. Kept in step with the helper in
    ``.github/scripts/check-readability.py``.
    <https://spec.commonmark.org/0.31.2/#links>
    """
    joined = contents[row][index:]
    starts = [0]
    for next_row in range(row + 1, len(contents)):
        starts.append(len(joined) + 1)
        joined += "\n" + contents[next_row]
    end = inline_link_end(joined, 0)
    if end == -1:
        return -1, -1
    for offset in range(len(starts) - 1, -1, -1):
        if end > starts[offset]:
            if offset == 0:
                return row, index + end
            return row + offset, end - starts[offset]
    return -1, -1


def following_raw_html_end(contents: Sequence[str], row: int, index: int) -> tuple[int, int]:
    """Return where the raw HTML run opened at ``index`` closes, or ``(-1, -1)``.

    A processing instruction, a declaration and a CDATA section are raw HTML:
    what sits between their delimiters is characters the renderer passes
    through, so a backtick in one opens no code span and a ``<!--`` in one
    begins no comment. Each crosses a soft line break the way a comment does
    and ends where the run does; one that never closes is not raw HTML at all,
    and the caller is then right to read its characters as text. Kept in step
    with the helper in ``.github/scripts/check-readability.py``.
    <https://spec.commonmark.org/0.31.2/#raw-html>
    """
    line = contents[row]
    for opener, closer in RAW_HTML_RUN_PATTERNS:
        match = opener.match(line, index)
        if match is None:
            continue
        found = line.find(closer, match.end())
        if found != -1:
            return row, found + len(closer)
        for next_row in range(row + 1, len(contents)):
            found = contents[next_row].find(closer)
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
    <https://spec.commonmark.org/0.31.2/#html-blocks>
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
    <https://html.spec.whatwg.org/multipage/parsing.html#rawtext-state>
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


def scan_inline_run(
    contents: Sequence[str],
    is_in_comment: bool,
    skips: dict[int, tuple[tuple[int, int], ...]] | None,
) -> tuple[list[str], bool, list[tuple[int, int, int]]]:
    """Walk one run of document text left to right, one context at a time.

    Returns three things: the comment text found on each line, the comment
    state the run ends in, and every code span the walk consumed, as
    ``(row, start, end)`` -- one range per physical line, because a span that
    crosses a soft line break is one span and two rows.

    ``skips`` holds, per row, the ranges this run is to read as link metadata
    rather than as text. ``None`` runs the walk with no link model at all. That
    is not a convenience: CommonMark takes whichever of a code span, a raw HTML
    tag and a link starts first, so the code spans have to be known *before*
    the link metadata is computed, and the only way to know them is to walk
    once without it. ``text_marker_spans`` does exactly that.

    "No link model" means no *defined labels* and no image rule; it does not
    mean no brackets. The walk counts the brackets it passes and hands the
    target of a ``](`` that closes one to ``inline_link_end``, because a
    destination and a title are scanned as characters rather than as inline
    content and a backtick in either opens nothing. Without that,
    ``[x](u "t`")`` on one line and ``Text <!-- no-source-check: y --> tail```
    on the next paired their backticks across the marker and masked it, and a
    session that had declared its exemption was failed for not declaring one.
    A ``[`` a code span swallowed is never counted, which is what still leaves
    ``` `[a](u` x) ``` a code span and not a link.

    The bracket walk runs in that first pass and in no other, because it is
    half a link model and the second pass has a whole one. Links may not nest,
    so forming one deactivates every opener still open above it:
    ``[a [b](u.md) c](v.md "<!-- x -->")`` is an inner link and then literal
    text, and the marker in those literal parentheses is a comment the page
    carries. ``link_metadata_regions`` knows that and knows which labels the
    document defines; this walk knows neither, and running it in both passes
    masked that marker. Over-skipping in the first pass costs at worst a code
    span the walk does not find, which masks less rather than more.
    <https://spec.commonmark.org/0.31.2/#links>
    """
    spans: list[list[str]] = [[] for _ in contents]
    code_spans: list[tuple[int, int, int]] = []
    indented_code = indented_code_rows(contents)
    row = 0
    index = 0
    open_brackets = 0

    while row < len(contents):
        line = contents[row]

        if index >= len(line):
            row += 1
            index = 0
            continue

        if is_in_comment:
            comment_end = line.find("-->", index)
            if comment_end == -1:
                spans[row].append(line[index:])
                row += 1
                index = 0
                continue
            spans[row].append(line[index : comment_end + len("-->")])
            index = comment_end + len("-->")
            is_in_comment = False
            continue

        if index == 0 and row in indented_code:
            row += 1
            continue

        if skips is not None:
            regions = skips.get(row, ())
            skipped = next((end for start, end in regions if start <= index < end), index)
            if skipped > index:
                index = skipped
                continue

        character = line[index]

        if character == "\\":
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
            close_row, close_index = following_backtick_run(contents, row, run_length)
            if close_row == -1:
                index = run_end
                continue
            code_spans.append((row, index, len(line)))
            for middle in range(row + 1, close_row):
                code_spans.append((middle, 0, len(contents[middle])))
            code_spans.append((close_row, 0, close_index))
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
                target_row, target_end = following_link_end(contents, row, index + 1)
                if target_row != -1:
                    row, index = target_row, target_end
                    continue
            index += 1
            continue

        if character == "<":
            if line.startswith("<!--", index):
                # A comment that closes inside this run is consumed whole,
                # because it started first. One that does not close is no
                # comment at all: CommonMark leaves ``Text <!-- unfinished``
                # as text and markdown-it 14.3.0 escapes it into
                # ``&lt;!-- unfinished``. Collecting it anyway carried an open
                # comment into the next block, where a marker written in a code
                # span became a real comment and exempted the session from
                # Source Check -- and it put characters the page prints into
                # the marker text, where they could bridge to a later
                # comment's ``-->``. The sibling hook's paragraph walk has
                # asked this question all along.
                close_row, _ = following_comment_end(contents, row, index)
                if close_row == -1:
                    index += len("<!--")
                    continue
                spans[row].append("<!--")
                index += len("<!--")
                is_in_comment = True
                continue
            # A processing instruction, a declaration and a CDATA section
            # are raw HTML whose content is characters, and none of the three
            # can also be an autolink or a tag, so they are asked about first
            # and cost nothing when they do not match.
            raw_row, raw_index = following_raw_html_end(contents, row, index)
            if raw_row != -1:
                row, index = raw_row, raw_index
                continue
            # An autolink is asked about before a tag, because a tag name may
            # not hold a colon and a URI autolink must, so only one of the two
            # can match here. What sits between the angle brackets is the
            # destination: a backtick in it is data rather than a delimiter,
            # exactly as a backtick inside an attribute value is.
            autolink = AUTOLINK_PATTERN.match(line, index)
            if autolink is not None:
                index = autolink.end()
                continue
            tag = INLINE_HTML_TAG_PATTERN.match(line, index)
            if tag is not None:
                index = tag.end()
                continue
            # A tag that does not close on this line closes on a later line
            # of the same run, the way a comment and the other raw HTML runs
            # already do here. Reading only this line left a backtick inside
            # a multiline attribute standing as text, and it then paired with
            # a backtick below and masked a real comment.
            tag_row, tag_index = following_tag_end(contents, row, index)
            if tag_row != -1:
                row, index = tag_row, tag_index
                continue

        index += 1

    return ["".join(parts) for parts in spans], is_in_comment, code_spans


def code_span_masked_lines(contents: Sequence[str], is_in_comment: bool) -> list[str]:
    """Return the run's lines with every code span blanked, its columns intact.

    Blanking rather than deleting is what lets the masked lines be handed
    straight to ``link_metadata_regions``: the ranges it returns are offsets
    into the real line, so they have to stay the offsets the real line has.
    """
    _, _, code_spans = scan_inline_run(contents, is_in_comment, None)
    masked = [list(line) for line in contents]
    for row, start, end in code_spans:
        masked[row][start:end] = " " * (end - start)
    return ["".join(characters) for characters in masked]


def text_marker_spans(
    contents: Sequence[str], is_in_comment: bool, defined_labels: frozenset[str]
) -> tuple[list[str], bool]:
    """Return the comment text on each line of one run of document text.

    This answers a narrower question than ``strip_html_comments``: not "what
    does the reader see", but "what here does CommonMark read as a comment".
    The difference is the contexts that bind tighter than raw HTML and
    therefore print the characters the author typed, or hand them to an
    element as an attribute -- a code span, a backslash escape, an image's alt
    text, a link's destination or title, an attribute value inside a tag, and a
    line indented four spaces, which is code rather than a paragraph.

    The run is scanned whole rather than a line at a time because two of those
    contexts cross a line break. A comment does, and the caller threads
    ``is_in_comment`` in and out for the lines on either side of the run. A code
    span does too, and deciding whether one closes needs the rest of the
    paragraph rather than the rest of the line. **A link target does too**, and
    it used to be read one line at a time: a target broken over a soft line
    break left the walk with no opening bracket on the second line, so the
    title attribute there was read as a real comment, and a marker written in
    one granted an exemption the page never showed. The run is joined for that
    question as well now. What stays line-local is the link *reference
    definition*, which is a block rather than an inline and is found per row
    before the join.

    It is scanned *twice* because a code span and a link are not asked about in
    either order. CommonMark takes whichever construct starts first, and a code
    span that opens before a ``[`` swallows the bracket, so the link is never
    there to have metadata. Computing the metadata over the raw line read
    ``` `![alt](url` "<!-- no-source-check: x -->") ``` as an image running to
    the final ``)``, and the marker the renderer really does print went with
    it: a session that had declared its exemption was failed for not declaring
    one. The first pass therefore finds the code spans with no link model at
    all, and the second asks what a link is only of the characters the spans
    left. It closes the other way round too -- ``![a`b](u) <!-- x --> c` `` is
    an image to a raw-line pass and a code span to the renderer, so the marker
    inside it was granting an exemption the page never carried.

    One measured limit is deliberate. A line indented four spaces is read as
    code even where it is a lazy continuation of the paragraph above, which
    CommonMark reads as prose. That is the safe direction: it refuses to exempt
    rather than granting an exemption the file does not visibly declare.
    """
    masked = code_span_masked_lines(contents, is_in_comment)
    # Joined and walked once: a link reference definition is a block and keeps
    # its own line, and everything else a link is crosses a soft line break.
    skips: dict[int, tuple[tuple[int, int], ...]] = {}
    pieces: list[str] = []
    starts: list[int] = []
    offset = 0
    for row, line in enumerate(masked):
        definition = link_reference_definition_region(line)
        if definition is not None:
            skips[row] = (definition,)
            line = " " * len(line)
        pieces.append(line)
        starts.append(offset)
        offset += len(line) + 1

    for left, right in link_metadata_regions("\n".join(pieces), defined_labels):
        for row, piece in enumerate(pieces):
            low = max(left, starts[row])
            high = min(right, starts[row] + len(piece))
            if low < high:
                skips[row] = skips.get(row, ()) + (
                    (low - starts[row], high - starts[row]),
                )

    spans, is_in_comment, _ = scan_inline_run(contents, is_in_comment, skips)
    return spans, is_in_comment


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
    put every row of a table into one run did offer it, formed a code span
    across the boundary, and masked a real comment between them, so a session
    that had declared its Source Check exemption was failed for not declaring
    one. Kept identical to the helper in the sibling hook.
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


def gfm_table_rows(sources: Sequence[MarkerSource]) -> dict[int, int]:
    """Return every row the document reads as part of a GFM table.

    Each row maps to the table's column count, which is what tells a body row's
    cells from the excess GFM throws away.

    A table is found by its delimiter row, exactly as ``extract_prose`` in
    ``.github/scripts/check-readability.py`` finds one: the line above the
    delimiter is the header, and the rows below it belong to the table until a
    line arrives that is blank or carries no pipe. The header and the delimiter
    row must agree about how many cells there are, or GFM reads no table here
    at all -- see ``table_columns``. The contents handed in are already peeled
    to their container's content column, so a quoted or a listed table is
    recognized as the table it is.
    https://github.github.com/gfm/#tables-extension-
    """
    rows: dict[int, int] = {}
    index = 0
    while index + 1 < len(sources):
        kind, content, _ = sources[index]
        next_kind, next_content, _ = sources[index + 1]
        if not (kind == MARKER_SOURCE_TEXT and next_kind == MARKER_SOURCE_TEXT):
            index += 1
            continue
        # The header row needs no pipe of its own. ``table_starts_here`` is
        # GFM's whole precondition in one place, and this walk asking for a
        # pipe on top of it put the two passes of the sibling hook and this one
        # out of step about which lines are a table.
        columns = table_starts_here(content, next_content)
        if not columns:
            index += 1
            continue
        rows[index] = columns
        rows[index + 1] = columns
        follow = index + 2
        while (
            follow < len(sources)
            and sources[follow][0] == MARKER_SOURCE_TEXT
            and sources[follow][1].strip(ASCII_HORIZONTAL_WHITESPACE)
            and "|" in sources[follow][1]
        ):
            rows[follow] = columns
            follow += 1
        index = follow
    return rows


def collect_reference_labels(
    contents: Sequence[str], starts: Sequence[bool]
) -> frozenset[str]:
    """Return every link label the document defines, normalized.

    A label is defined only where a whole definition parses. CommonMark wants a
    destination for that, so ``[x]:`` with a line of prose under it defines
    nothing at all: the brackets stay on the page, a reference to ``x`` below
    them is the characters the author typed, and a marker inside one of those
    is a comment the child's page really carries. Reading the label off the
    front of the line was enough to throw that marker away and fail the session
    for a Source Check it had declared.

    The lines a definition fills are skipped with it, so a destination or a
    title sitting on its own line is never read as a second label. A line that
    is not document text -- a blanked fenced line, a raw HTML line -- can
    neither hold a definition nor continue one, so it enters this walk empty,
    which no part of a definition matches.

    And a definition may not interrupt a paragraph, so this walk carries the
    paragraph state rather than reading every line alike. ``Intro text.`` above
    ``[x]: /url`` defines nothing on either renderer -- the two lines are one
    paragraph and the brackets stay on the page. Collecting the label anyway
    cost this checker an exemption refused; it cost its sibling an
    adult-facing document scored by the child gate, which is why one spelling
    in both is worth more than the safe direction in one.

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
    ``.github/scripts/check-readability.py``.
    <https://spec.commonmark.org/0.31.2/#link-reference-definitions>
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


def collect_marker_lines(sources: Sequence[MarkerSource]) -> tuple[str, ...]:
    """Return, for each line, the text CommonMark reads there as an HTML comment.

    The two Source Check exemption markers *are* comments and nothing else is
    one. Saying that positively -- keeping the comment spans rather than
    subtracting code spans, escapes, attributes, link metadata and indented code
    one context at a time -- is what lets one scan cover every shape. It also
    does not demand that a marker sit alone on its line, which CommonMark has
    never required of a comment.

    This runs after the document has been classified rather than during it,
    because two of the questions it asks need more than the line in hand: which
    labels the document defines, and whether a backtick run further down the
    paragraph closes the one on this line.

    Document text is scanned a run at a time for the same reason, and a run is
    one block. A raw HTML line ends it, which is right twice over: the Markdown
    inline rules do not reach inside a raw HTML block, and a line that opens
    one ends the paragraph a code span would have needed to close in. Every
    other block start ends it too, which is what ``starts_a_block`` records as
    the document is walked.
    """
    # The walk's own ``starts_a_block`` answer travels on every source, and a
    # label collector that ignored it held a paragraph open across a container
    # boundary CommonMark ends one at.
    defined_labels = collect_reference_labels(
        [
            content if kind == MARKER_SOURCE_TEXT else ""
            for kind, content, _ in sources
        ],
        [starts for _, _, starts in sources],
    )
    table_rows = gfm_table_rows(sources)
    markers: list[str] = []
    is_in_comment = False
    open_tag: str | None = None
    in_bogus_run = False
    row = 0

    while row < len(sources):
        kind, content, _ = sources[row]

        if kind == MARKER_SOURCE_BLANK:
            markers.append("")
            open_tag = None
            in_bogus_run = False
            row += 1
            continue

        if kind == MARKER_SOURCE_RAW_HTML:
            span, is_in_comment, open_tag, in_bogus_run = (
                raw_html_comment_spans(
                    content, is_in_comment, open_tag, in_bogus_run
                )
            )
            markers.append(span)
            row += 1
            continue

        if row in table_rows:
            # A GFM table cell is its own inline context: the renderer reads
            # the table before it reads any inline, so a backtick left
            # unmatched in one cell can never pair with one in another. Scanned
            # as one run, two such backticks formed a code span across the
            # boundary and masked the marker standing between them. The comment
            # state still travels through the cells in document order, because
            # that is the order the page is written in.
            # A body row with more cells than the header has its excess
            # ignored by GFM, so those characters are not on the page and
            # nothing written in them is either.
            cell_spans: list[str] = []
            for _, cell in table_row_cells(content)[: table_rows[row]]:
                spans, is_in_comment = text_marker_spans(
                    [cell], is_in_comment, defined_labels
                )
                cell_spans.extend(spans)
            markers.append("".join(cell_spans))
            open_tag = None
            in_bogus_run = False
            row += 1
            continue

        # The run ends where the next block begins, so what reaches the scan
        # is one paragraph and a code span cannot close outside its own. A
        # table row ends it too: its cells are scanned one at a time above.
        end = row + 1
        while (
            end < len(sources)
            and sources[end][0] == MARKER_SOURCE_TEXT
            and not sources[end][2]
            and end not in table_rows
        ):
            end += 1
        run = [sources[position][1] for position in range(row, end)]
        spans, is_in_comment = text_marker_spans(run, is_in_comment, defined_labels)
        markers.extend(spans)
        row = end

    return tuple(markers)


def normalize_for_fence_closing(line: str, active_fence: ActiveFence) -> str:
    """Return a fenced-block line normalized to the opening fence's container."""
    peeled, peeled_count = peel_containers(line, active_fence.containment_path)
    if peeled_count < len(active_fence.containment_path):
        return line
    return peeled


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
    for; the rule is the container's rather than the fence's.
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
    spaces or tabs after it. An info string does not close a block, and
    trailing prose does not close one either.

    Spaces and tabs, and not a whitespace class. Python reads ``\\s`` as Unicode
    whitespace, so a nonbreaking space or a form feed after the backticks would
    close the block here while the renderer kept every line below it inside the
    code -- and a fake scaffold heading under such a fence would count as
    structure. Measured against markdown-it 14.3.0: a fence followed by U+00A0
    does not close. Kept in step with the sibling hooks.
    https://spec.commonmark.org/0.31.2/#fenced-code-blocks
    """
    closing_pattern = re.compile(
        rf"^ {{0,3}}{re.escape(fence_character)}{{{minimum_length},}}[ \t]*$"
    )
    return closing_pattern.match(line) is not None


def fence_holds_worksheet(fence_lines: Sequence[str]) -> bool:
    """Return whether the body of one fenced block reads as a worksheet fill-in."""
    return any(WORKSHEET_BLANK_PATTERN.search(line) for line in fence_lines)


def scan_document(text: str) -> DocumentScan:
    """Return the text outside every fence, and the worksheet fences in the document.

    One pass, one fence parser. A fenced block is found where Markdown finds
    one, which includes a block nested in a list item or a blockquote. The
    container machinery above is the machinery
    ``check-prohibited-placeholders.py`` uses, under the same names.

    Line endings are **not** normalized here. ``check_text`` is this module's
    single door and normalizes before it calls this function, so that the scan
    and the ``section_body`` reads that follow both see the same text. Doing it
    again here would be dead work, and saying it happened here would be wrong:
    ``check-readability.py`` really does have two entry points and normalizes at
    each, and this docstring once claimed the same shape without the same
    callers. If a second caller is ever added, it normalizes, or this becomes
    the place that does.
    """
    content_lines: list[str] = []
    marker_sources: list[MarkerSource] = []
    worksheet_fences: list[int] = []
    active_fence: ActiveFence | None = None
    list_contexts: list[ListContext] = []
    is_in_html_comment = False
    html_block: ActiveHtmlBlock | None = None
    paragraph_open = False
    previous_path: tuple[Container, ...] = ()
    # The line above, carried for the delimiter-row rule in
    # ``opens_a_paragraph``: its peeled content and the container it sat in.
    # Cleared at the top of every iteration, so that any branch which leaves
    # the loop early leaves no header row behind it.
    previous_content = ""
    previous_container: tuple[Container, ...] = ()
    raw_text: str | None = None
    fence_start = 0
    buffer: list[str] = []

    for number, raw_line in enumerate(text.split("\n"), start=1):
        above_content, above_container = previous_content, previous_container
        previous_content, previous_container = "", ()
        if active_fence is not None and fence_container_ended(raw_line, active_fence):
            # The list item or blockquote holding the fence has ended, so the
            # fence ended with it and this line is document text again.
            if fence_holds_worksheet(buffer):
                worksheet_fences.append(fence_start)
            active_fence = None
            buffer = []

        if active_fence is not None:
            closing_line = normalize_for_fence_closing(raw_line, active_fence)
            if is_closing_fence(
                closing_line, active_fence.character, active_fence.minimum_length
            ):
                if fence_holds_worksheet(buffer):
                    worksheet_fences.append(fence_start)
                active_fence = None
                buffer = []
            else:
                buffer.append(closing_line)
            content_lines.append("")
            marker_sources.append((MARKER_SOURCE_BLANK, "", True))
            paragraph_open = False
            previous_path = ()
            continue

        was_in_html_comment = is_in_html_comment
        # Fence detection reads the span-stripped line, because the sibling
        # hook reads it that way and the two must not disagree about which
        # fences exist -- which is also why the sibling carries the same
        # HTML-block machine. The structural searches read less: a whole HTML
        # block line carries no heading, even after its ``-->``. The
        # HTML-block test reads the line as the file holds it, with its
        # container prefixes peeled: CommonMark classifies a line from what is
        # left after the prefixes, so a marker inside a blockquote or a list
        # item is the same comment the unindented one is.
        block_line = container_line(raw_line, list_contexts)
        block_content = block_line.content
        if html_block is not None and container_path_ended(raw_line, html_block.containment_path):
            # The list item or blockquote holding the block has ended, so the
            # block ended with it, exactly as an unclosed fence does. Without
            # this an unclosed ``<div>`` inside a blockquote blanked every
            # heading the document outdented to, through the end of the file.
            #
            # The *block* ends here and the *run* does not, and the difference
            # is which layer each belongs to. A block is CommonMark's, so a
            # container ends it. A run is the page's: the renderer has already
            # written ``<script>`` into the output, and an HTML parser reading
            # that output stays in raw text until a closing tag it never meets.
            # Measured with markdown-it 14.3.0 read by ``html.parser``: below
            # an unclosed ``<script>`` in a blockquote no comment is a comment
            # and no heading is painted, all the way to the end of the file.
            # So ``raw_text`` is deliberately left open, and the consumers
            # below ask it as well as the block.
            html_block = None
        # Asked before the HTML block machine rather than after it, because
        # condition 7 is the one start that may not interrupt a paragraph and
        # has to be told when there is no longer one to interrupt. A line that
        # starts a block has closed the paragraph above it, and
        # ``opens_a_paragraph`` cannot say so: it reads one line and answers
        # for the line *below*, so a list item opening on this line inherited
        # the paragraph from the line above and refused the block CommonMark
        # opens inside the new item -- and an exemption marker written in that
        # block was read as fenced code and never found.
        header_above = (
            above_content if above_container == block_line.containment_path else ""
        )
        block_starts = starts_a_block(
            block_content,
            block_line.containment_path,
            block_line.opened,
            previous_path,
            paragraph_open,
            header_above,
        )
        html_block, line_html_block = html_block_state(
            block_content,
            block_line.containment_path,
            html_block,
            paragraph_open and not block_starts,
        )
        # Three pieces of state and one order, written here once so that no
        # caller has to rediscover it: CommonMark says which lines are raw HTML
        # at all, the raw-text run says which of those hold text rather than
        # markup, and only then are comments stripped from what is left. Asking
        # the run before the block opened a run on a line CommonMark keeps
        # inside the paragraph above it; stripping before the run -- which this
        # hook did -- read a comment-shaped run a ``<script>`` prints as a real
        # comment and blanked every line below it to the end of the file. The
        # sibling hooks ask in this same order.
        raw_text, line_raw_text, raw_text_end = raw_text_run_boundary(
            block_content, raw_text, line_html_block is not None
        )
        in_raw_text = raw_text_run_holds_text(line_raw_text)
        if in_raw_text and raw_text_end != -1:
            # The run closes part way along this line, and what follows the
            # closer is not the element's content.
            # ``<script></script><!-- no-source-check: offline -->`` holds an
            # empty script and then a real comment, and dropping the whole
            # line dropped the comment with it -- so a session that had
            # declared its exemption was failed for not declaring one. The
            # run's own span is blanked and the rest of the line is read as it
            # would have been; blanking rather than slicing keeps every offset
            # below here pointing where it pointed.
            prefix_length = len(raw_line) - len(block_content)
            block_content = " " * raw_text_end + block_content[raw_text_end:]
            raw_line = raw_line[:prefix_length] + block_content
            in_raw_text = False
        if in_raw_text:
            # The line is a raw-text element's content, which the page shows as
            # it stands or drops altogether. A comment-shaped run there is text
            # and opens no comment, so the line is read whole.
            visible_line = raw_line
        else:
            visible_line, is_in_html_comment = strip_html_comments(
                raw_line, was_in_html_comment
            )
        if raw_text_run_holds_text(raw_text):
            # A raw-text run is open below this line, so no comment can be open
            # inside it. Said here as well as above because a run opens part way
            # along its own line -- ``<textarea> <!-- a note``.
            is_in_html_comment = False
        # A comment is one HTML block condition; the rest are raw HTML too,
        # and a ``## Goal`` inside a ``<div>`` is no more a heading than a
        # ``## Goal`` inside a comment is. An inline comment opened part way
        # along a line is not a block, so its cross-line state is consulted
        # here too.
        in_html_block = was_in_html_comment or line_html_block is not None

        opening_fence_line = normalize_for_fence_opening(visible_line, list_contexts)
        # A line CommonMark reads as raw HTML opens no fenced block, whatever
        # backticks survive comment stripping: an HTML block runs to the line
        # carrying ``-->`` and every character on those lines is raw HTML. The
        # container state is still taken from the line, because its list and
        # blockquote prefixes are real; only the fence is not.
        opening_fence = (
            None if in_html_block else parse_opening_fence(opening_fence_line.content)
        )
        if opening_fence is not None:
            character, minimum_length = opening_fence
            active_fence = ActiveFence(
                character=character,
                minimum_length=minimum_length,
                containment_path=opening_fence_line.containment_path,
            )
            fence_start = number
            buffer = []
            content_lines.append("")
            marker_sources.append((MARKER_SOURCE_BLANK, "", True))
            paragraph_open = False
            previous_path = ()
            continue

        # A line a raw-text run holds is the element's content, whether or
        # not CommonMark still has a block open on it. The two part company
        # when the block ends first -- the container outdents, or a condition
        # 7 block meets its blank line -- and the run is still open because
        # its closing tag has not arrived. The marker classification below
        # already read the run rather than the block; this line read only the
        # block, so a ``## Goal`` under an unclosed ``<script>`` was a heading
        # here while the page painted nothing at all.
        content_lines.append("" if in_html_block or in_raw_text else visible_line)
        # A marker is a marker only where CommonMark reads it as a comment, and
        # which contexts decide that depends on what the line is. Inside a raw
        # HTML block -- the comment among the conditions -- only a tag and a
        # comment mean anything; everywhere else the Markdown inline rules
        # apply. Recording which, rather than answering now, is what lets the
        # scan below see a whole paragraph at a time; recording where each
        # block starts is what keeps that paragraph to one block, so a code
        # span cannot close outside the one that holds its opening run.
        if in_raw_text:
            # The line is a raw-text element's content. The page displays
            # those characters, so a comment-shaped run on it is text and
            # exempts nothing.
            marker_sources.append((MARKER_SOURCE_BLANK, "", True))
        elif line_html_block is not None:
            marker_sources.append((MARKER_SOURCE_RAW_HTML, block_content, block_starts))
        else:
            marker_sources.append((MARKER_SOURCE_TEXT, block_content, block_starts))
        previous_path = block_line.containment_path
        # A line that starts no block leaves the paragraph above it open,
        # whatever its content peels to. The case that needs saying is the
        # empty list item: it may not interrupt a paragraph, so its marker is
        # the paragraph's own text -- but the container walk peels the marker
        # off and hands an empty content down, which reads exactly like a
        # blank line. Measured with markdown-it 14.3.0: ``Words`` then ``*``
        # then ``<x>`` is one paragraph of three lines, and the ``## Goal``
        # below is a heading.
        paragraph_open = (
            False
            if in_html_block
            else (paragraph_open and not block_starts)
            or opens_a_paragraph(block_content, paragraph_open, header_above)
        )
        previous_content = block_content
        previous_container = block_line.containment_path

    if active_fence is not None and fence_holds_worksheet(buffer):
        worksheet_fences.append(fence_start)

    return DocumentScan(
        tuple(content_lines),
        collect_marker_lines(tuple(marker_sources)),
        tuple(worksheet_fences),
    )


def find_headings(scan: DocumentScan) -> list[Heading]:
    """Return every heading, at every level, from outside every fenced block.

    Every heading the checker looks at comes from here, the session title
    included. One fence parser means one behaviour: a heading inside a fenced
    example is an example, whether it is a ``# Session NN`` title or a
    ``## Stop Point`` section.
    """
    headings: list[Heading] = []

    for number, line in enumerate(scan.content_lines, start=1):
        heading_match = HEADING_PATTERN.match(line)
        if heading_match:
            headings.append(
                Heading(
                    level=len(heading_match.group("hashes")),
                    title=heading_match.group("title"),
                    line_number=number,
                )
            )

    return headings


def section_body(text: str, headings: list[Heading], index: int) -> str:
    """Return the text between one section heading and the next.

    Only the blank lines around the body are trimmed. Trimming the spaces as
    well would take the indent off the first line, and four spaces of indent is
    what makes a line an indented code block rather than the thing it resembles
    -- a line CommonMark prints as characters rather than reading as a link
    reference definition.
    """
    lines = text.split("\n")
    start = headings[index].line_number
    end = (
        headings[index + 1].line_number - 1 if index + 1 < len(headings) else len(lines)
    )
    return "\n".join(lines[start:end]).strip("\n")


def session_header(content_lines: tuple[str, ...], headings: list[Heading]) -> str:
    """Return the session header: everything above the first level-two section.

    The navigation line belongs here and nowhere else. It is the orientation a
    child reads before starting, so a file that keeps it below ``## Stop
    Point`` keeps it where it does no work. A document with no level-two
    heading gives the whole document, which is the safe direction: the search
    then looks at more text, not less, and the missing sections are already
    reported on their own.

    The parent strip is deliberately not bounded this way. The specification
    allows the parent-facing meta-fields near the top *or* grouped at the
    bottom, so the header is one of two legal homes for it rather than the
    only one.
    """
    end = len(content_lines)
    for heading in headings:
        if heading.level == 2:
            end = heading.line_number - 1
            break
    return "\n".join(content_lines[:end])


def parent_strip_body(
    content_lines: tuple[str, ...], headings: list[Heading], label_line: int
) -> str:
    """Return the parent strip: the label line, to the next heading.

    The strip sits between the label and the first section, so the first
    heading after the label is where it stops. A document with no heading after
    the label gives the rest of the document, which is the safe direction: the
    checker then looks at more text, not less.
    """
    end = len(content_lines)
    for heading in headings:
        if heading.line_number > label_line:
            end = heading.line_number - 1
            break
    return "\n".join(content_lines[label_line - 1 : end])


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
    whole construct renders nothing at all -- so a section holding one prints to
    the child as a bare heading however many lines it took to write.

    The longest form that parses exactly is the one taken, because that is what
    the renderer does, and only where the line below carries something the
    definition can still use: a definition that already has its title does not
    take a second one. A label line, an indented destination and then a line of
    prose is a two-line definition with the prose left over, and measured
    against markdown-it 14.3.0 that prose is an indented code block the child
    sees.
    <https://spec.commonmark.org/0.31.2/#link-reference-definitions>
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


def renders_as_content(body: str) -> bool:
    """Return whether a section body puts anything on the page.

    Whitespace, an HTML comment such as ``<!-- markdownlint-disable -->``, a
    list marker with no words after it, and a link reference definition all
    print as nothing. A section that holds only those is empty to the child,
    whatever the file holds.

    The reference-definition test reads the line as the file holds it rather
    than the comment-stripped line, and that is the load-bearing half of it. A
    comment and a definition on one line make the whole line an HTML block, and
    an HTML block prints the characters the author typed: ``<!-- c -->[shared]:
    /url`` is on the page, while ``[shared]: /url`` is not.

    It reads a definition whole rather than a line at a time, because
    CommonMark lets one run over two or three lines and the whole of it still
    renders nothing. A rule applied line by line matched neither half of
    ``[shared]:`` with its destination indented underneath, and a session whose
    Goal was a bare heading passed.
    """
    lines = body.split("\n")
    is_in_html_comment = False
    index = 0
    while index < len(lines):
        line = lines[index]
        visible, is_in_html_comment = strip_html_comments(line, is_in_html_comment)
        is_blank = not visible.strip(ASCII_HORIZONTAL_WHITESPACE)
        if is_blank or BARE_LIST_MARKER_PATTERN.match(visible):
            index += 1
            continue
        span = reference_definition_span(lines, index)
        if span:
            for offset in range(1, span):
                _, is_in_html_comment = strip_html_comments(
                    lines[index + offset], is_in_html_comment
                )
            index += span
            continue
        return True
    return False


def check_text(text: str, display_path: str, file_name: str) -> list[Violation]:
    """Return every structural violation in one session document.

    A document enters this module here, so this is where its line endings are
    made one thing; see ``normalize_line_endings``. ``section_body`` below is
    handed the same normalized text the scan was built from, which is the
    reason the translation happens before the scan rather than inside it alone.
    """
    text = normalize_line_endings(text)
    violations: list[Violation] = []

    scan = scan_document(text)
    content = scan.text

    headings = find_headings(scan)
    first_heading = headings[0] if headings else None
    title_match = (
        TITLE_PATTERN.match(first_heading.title)
        if first_heading is not None and first_heading.level == 1
        else None
    )

    if title_match is None:
        violations.append(
            Violation(
                display_path,
                first_heading.line_number if first_heading is not None else 1,
                "no session title. The first heading in the document must read "
                '"# Session NN: Title". A title inside a fenced example is an example, '
                "not the name of the session.",
            )
        )
    else:
        name_match = FILENAME_NUMBER_PATTERN.match(file_name)
        if name_match is None:
            violations.append(
                Violation(
                    display_path,
                    first_heading.line_number,
                    "the filename does not start with a two-digit session number, so the "
                    "title cannot be checked against it. Name the file NN_short_title.md, "
                    "matching every other session.",
                )
            )
        elif name_match.group("number") != title_match.group("number"):
            violations.append(
                Violation(
                    display_path,
                    first_heading.line_number,
                    f"title says Session {title_match.group('number')} but the filename says "
                    f"Session {name_match.group('number')}. They must agree.",
                )
            )

    header = session_header(scan.content_lines, headings)
    if NAV_PATTERN.search(header) is None:
        misplaced = NAV_PATTERN.search(content)
        if misplaced is None:
            violations.append(
                Violation(
                    display_path,
                    1,
                    'no navigation line. Every session starts with "You are here: ..." so a '
                    "child can see where they are in the sequence.",
                )
            )
        else:
            violations.append(
                Violation(
                    display_path,
                    content.count("\n", 0, misplaced.start()) + 1,
                    'the navigation line sits below the first section. "You are here: ..." '
                    "orients the child before the work starts, so it belongs above the first "
                    "## heading, not after it.",
                )
            )

    strip_match = PARENT_STRIP_PATTERN.search(content)
    if strip_match is None:
        violations.append(
            Violation(
                display_path,
                1,
                'no parent metadata strip. Every session carries a "**For parents:**" strip '
                "with status, time, and involvement -- near the top, or grouped at the bottom; "
                "the specification allows either.",
            )
        )
    else:
        label_line = content.count("\n", 0, strip_match.start()) + 1
        strip = parent_strip_body(scan.content_lines, headings, label_line)
        missing = [name for name, pattern in PARENT_STRIP_FIELDS if pattern.search(strip) is None]
        if missing:
            violations.append(
                Violation(
                    display_path,
                    label_line,
                    'the "**For parents:**" strip has no bullet for these fields: '
                    + ", ".join(missing)
                    + ". A label with no fields under it tells a parent nothing. Give "
                    "one bullet for each of Status, Estimated time, and Parent "
                    "involvement.",
                )
            )

    section_headings = [heading for heading in headings if heading.level == 2]
    titles = [heading.title for heading in section_headings]

    for section in MANDATORY_SECTIONS:
        if section not in titles:
            violations.append(
                Violation(display_path, 1, f'missing mandatory section "## {section}".')
            )

    exempt = bool(AUDIENCE_ADULT_PATTERN.search(scan.marker_text)) or bool(
        NO_SOURCE_CHECK_PATTERN.search(scan.marker_text)
    )
    if SOURCE_CHECK_SECTION not in titles and not exempt:
        violations.append(
            Violation(
                display_path,
                1,
                'missing "## Source Check". A session with a research step must carry it. If '
                "this session has no research step, say so in the file with "
                "<!-- no-source-check: reason --> rather than leaving it silent.",
            )
        )

    present = [t for t in titles if t in ORDERED_SECTIONS]
    expected = [s for s in ORDERED_SECTIONS if s in titles]
    if present != expected:
        violations.append(
            Violation(
                display_path,
                section_headings[0].line_number if section_headings else 1,
                "scaffold sections are out of order. Found "
                f"{' > '.join(present)}; expected {' > '.join(expected)}. Other sections may sit "
                "between them, but these may not be reordered.",
            )
        )

    for index, heading in enumerate(section_headings):
        if heading.title not in ORDERED_SECTIONS:
            continue
        if not renders_as_content(section_body(text, section_headings, index)):
            violations.append(
                Violation(
                    display_path,
                    heading.line_number,
                    f'section "## {heading.title}" is empty.',
                )
            )

    for number in scan.worksheet_fences:
        violations.append(
            Violation(
                display_path,
                number,
                "fenced block used as a worksheet fill-in. Worksheet forms are Markdown tables "
                "(a two-column Prompt | Your answer form, or a narrow criteria-by-option grid). "
                "An empty table cell prints as a box, becomes an editable cell in Google Docs, "
                "and reflows on a phone; a fenced underscore block does none of those.",
            )
        )

    return violations


@dataclass(frozen=True)
class SkippedEntry:
    """One directory entry the walk saw, did not check, and will not fail on.

    A skip is a decision, not an omission. It is recorded so that the walk can
    prove every entry it saw received exactly one disposition; a file that is
    simply not Markdown is the only thing that lands here.
    """

    display_path: str
    reason: str


@dataclass
class WalkTally:
    """How many directory entries the walk saw, and what became of each.

    The four dispositions are exhaustive and mutually exclusive by
    construction. ``balances`` is the reconciliation: if it is ever false, an
    entry was seen and then lost, which is the shape of every silent gate hole
    this checker has had.
    """

    seen: int = 0
    checked: int = 0
    refused: int = 0
    descended: int = 0
    skipped: int = 0

    def balances(self) -> bool:
        """Return whether every entry seen received exactly one disposition."""
        return self.seen == self.checked + self.refused + self.descended + self.skipped


@dataclass
class RootTally:
    """How many scan roots the run was given, and what became of each.

    ``WalkTally`` proves that nothing *below* a root went missing. It says
    nothing about the roots themselves, and the roots are where the last two
    holes were: the default scan root never passed the guard, and a directory
    argument that contributed nothing was simply dropped. The three
    dispositions here are exhaustive and mutually exclusive by construction,
    exactly as the four below a root are, and ``balances`` is the same
    reconciliation one level up.
    """

    requested: int = 0
    walked: int = 0
    checked: int = 0
    refused: int = 0

    def balances(self) -> bool:
        """Return whether every root requested received exactly one disposition."""
        return self.requested == self.walked + self.checked + self.refused


#: Said of a root that was named and then contributed nothing. A run reports
#: on what it opened; a path it was given and never opened is a path it
#: passed over in silence, and with a second argument supplying a target the
#: run-wide guard never fires.
ZERO_TARGET_MESSAGE = (
    "matched no session file, so this run checked nothing from it. A path that "
    "is named and then yields neither a target nor a refusal is a path this run "
    "passed over in silence. Check the path, or check DEFAULT_SCAN_ROOT if this "
    "was the default scan."
)


@dataclass(frozen=True)
class ScanTargets:
    """The session files to read, the refusals that must fail the run, and the
    entries deliberately passed over."""

    paths: tuple[Path, ...]
    refusals: tuple[Violation, ...]
    skipped: tuple[SkippedEntry, ...] = ()


def display_name(path: Path, root: Path, fallback: str) -> str:
    """Return the repo-relative name of a path, or ``fallback`` when it is outside."""
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return fallback


def guard_path(path: Path, root: Path, label: str) -> Violation | None:
    """Return a refusal for a path that is a link, or that resolves outside ``root``.

    ``root`` is already resolved. All three halves matter. ``Path.resolve()``
    follows symbolic links *and* Windows junctions, so the containment test is
    what enforces the boundary; the ``is_symlink()`` test refuses a link even
    when it points back inside the tree, which is what
    ``check-prohibited-placeholders.py`` already does for its own inputs; and
    ``is_junction()`` catches the Windows reparse point that ``is_symlink()``
    reports as an ordinary directory. The junction test is not decoration: the
    walk descends into directories, and a junction pointing at one of its own
    ancestors would otherwise make it descend forever.
    """
    if path.is_symlink() or path.is_junction():
        return Violation(
            label,
            1,
            "symbolic link or junction, not a real file. A session file must be a real "
            "file in the repository, because a link can point at content outside the "
            "allowlisted tree, and a linked directory is a subtree this run would "
            "otherwise never open. Refusing to read it.",
        )
    try:
        path.resolve().relative_to(root)
    except ValueError:
        return Violation(
            label, 1, "resolves outside the repository root. Refusing to read it."
        )
    return None


def walk_session_directory(
    directory: Path,
    root: Path,
    paths: list[Path],
    refusals: list[Violation],
    skipped: list[SkippedEntry],
    tally: WalkTally,
) -> None:
    """Enumerate one directory tree, dispositioning every entry it holds.

    This exists instead of ``Path.glob`` / ``Path.rglob`` because a pattern
    answers only "what matched". Three things a pattern passes over in silence
    have each been a hole in this gate:

    * a **symbolic link to a directory**, which ``**`` does not descend into,
      so the whole linked subtree is never read;
    * an **uppercase ``.MD``**, which a lowercase pattern does not match on the
      case-sensitive filesystem CI runs on, though it matches on the
      developer's case-insensitive one; and
    * a **directory the process cannot read**, whose ``PermissionError``
      ``glob`` swallows, so an unreadable subtree reads as an empty one.

    None of the three can hide from an enumeration that must account for every
    entry it saw. Directories are descended into, Markdown files are checked,
    links and escapes are refused, and anything else is skipped for a reason
    that is written down. ``tally`` counts the four so the caller can prove
    they add up.
    """
    try:
        entries = sorted(directory.iterdir(), key=lambda entry: entry.name)
    except FileNotFoundError:
        # Not there at all. The zero-target guard in collect_targets reports
        # that this run checked nothing, which is the accurate thing to say
        # and the message that names the setting to fix.
        return
    except OSError as error:
        # A directory that cannot be listed is not an empty directory, and
        # this is exactly where glob() would have returned nothing instead.
        refusals.append(
            Violation(
                display_name(directory, root, directory.as_posix()),
                1,
                f"could not be read ({error.strerror}), so this run does not know what "
                "is inside it. An unreadable directory is not an empty one; refusing "
                "to report a clean corpus for a subtree that was never listed.",
            )
        )
        return

    for entry in entries:
        tally.seen += 1
        label = display_name(entry, root, entry.as_posix())

        refusal = guard_path(entry, root, label)
        if refusal is not None:
            refusals.append(refusal)
            tally.refused += 1
            continue

        if entry.is_dir():
            tally.descended += 1
            walk_session_directory(entry, root, paths, refusals, skipped, tally)
            continue

        if entry.is_file() and entry.suffix.lower() == MARKDOWN_SUFFIX:
            paths.append(entry)
            tally.checked += 1
            continue

        skipped.append(SkippedEntry(label, "not a Markdown file"))
        tally.skipped += 1


def collect_directory_root(
    requested: str,
    directory: Path,
    root: Path,
    paths: list[Path],
    refusals: list[Violation],
    skipped: list[SkippedEntry],
    tally: WalkTally,
    roots: RootTally,
) -> None:
    """Walk one requested directory, and refuse it when it contributes nothing.

    The walk accounts for every entry it *sees*. A directory that holds no
    entry at all is seen by nobody, so the walk has nothing to account for and
    the run-wide zero-target guard is the only thing left -- and that guard
    fires only when the *whole run* opened nothing. One real file from another
    argument silences it, and the mistyped directory beside it disappears. So
    the accounting is done per root: a root that adds neither a target nor a
    refusal is itself the refusal.
    """
    before_paths = len(paths)
    before_refusals = len(refusals)
    walk_session_directory(directory, root, paths, refusals, skipped, tally)
    if len(paths) == before_paths and len(refusals) == before_refusals:
        refusals.append(
            Violation(display_name(directory, root, requested), 1, ZERO_TARGET_MESSAGE)
        )
        roots.refused += 1
        return
    roots.walked += 1


def collect_targets(path_arguments: Sequence[str], root: Path) -> ScanTargets:
    """Turn command-line arguments into session Markdown paths, refusing escapes.

    Every path the checker reads passes through here: the default walk, the
    walk of a directory argument, and an explicit file argument alike.
    Validating only the explicit arguments would leave the one path CI
    actually uses -- the default walk -- unguarded.
    """
    root = root.resolve()
    paths: list[Path] = []
    refusals: list[Violation] = []
    skipped: list[SkippedEntry] = []
    tally = WalkTally()
    roots = RootTally()

    if not path_arguments:
        # The default scan root is a requested root like any other, and it is
        # the one CI uses. Guarding the arguments and not this was the last
        # unguarded path into the walk: a symlinked ``framework/sessions``
        # was followed, so the run reported on whatever the link pointed at
        # and said nothing about the directory it was asked for.
        roots.requested += 1
        default_root = root / DEFAULT_SCAN_ROOT
        refusal = guard_path(default_root, root, DEFAULT_SCAN_ROOT)
        if refusal is not None:
            refusals.append(refusal)
            roots.refused += 1
        else:
            collect_directory_root(
                DEFAULT_SCAN_ROOT,
                default_root,
                root,
                paths,
                refusals,
                skipped,
                tally,
                roots,
            )
    else:
        for argument in path_arguments:
            roots.requested += 1
            candidate = Path(argument)
            if not candidate.is_absolute():
                candidate = root / candidate
            refusal = guard_path(candidate, root, display_name(candidate, root, argument))
            if refusal is not None:
                refusals.append(refusal)
                roots.refused += 1
                continue
            candidate = candidate.resolve()
            if candidate.is_dir():
                collect_directory_root(
                    argument, candidate, root, paths, refusals, skipped, tally, roots
                )
            elif candidate.is_file() and candidate.suffix.lower() == MARKDOWN_SUFFIX:
                paths.append(candidate)
                roots.checked += 1
            else:
                roots.refused += 1
                # The argument survived the guard but names nothing this checker
                # can read: a path that does not exist, or a file that is not
                # Markdown.
                refusals.append(
                    Violation(
                        display_name(candidate, root, argument),
                        1,
                        "not a Markdown file or a directory, so there is nothing to "
                        "check. Check the path: a typo here would otherwise pass "
                        "silently, because a run that checks nothing reports no "
                        "problems.",
                    )
                )

    if not roots.balances():
        # The same reconciliation as the walk's, one level up. Every root the
        # run was given is walked, checked, or refused; a future edit that
        # adds a fourth, silent outcome for a root is what this catches, and a
        # silent outcome for a root is exactly the shape of the last two holes.
        refusals.append(
            Violation(
                DEFAULT_SCAN_ROOT if not path_arguments else " ".join(path_arguments),
                1,
                f"the run was given {roots.requested} scan root(s) but accounted for "
                f"{roots.walked + roots.checked + roots.refused} of them. A root that "
                "is neither walked, checked, nor refused has gone missing, and this "
                "run cannot say what it was asked to read.",
            )
        )

    if not tally.balances():
        # The reconciliation. Every entry the walk saw is checked, refused,
        # descended into, or skipped for a reason; the four are exhaustive by
        # construction, so they can only fail to add up if a future edit
        # introduces a fifth, silent outcome. That is the shape of every hole
        # this gate has had, so it fails the run rather than reporting one.
        refusals.append(
            Violation(
                DEFAULT_SCAN_ROOT if not path_arguments else " ".join(path_arguments),
                1,
                f"the walk saw {tally.seen} directory entr(ies) but accounted for "
                f"{tally.checked + tally.refused + tally.descended + tally.skipped} "
                "of them. An entry that is neither checked, refused, descended into, "
                "nor skipped for a stated reason has gone missing, and this run "
                "cannot say what is in the corpus.",
            )
        )

    if not paths and not refusals:
        # One guard for every shape of the same mistake: the run was asked for
        # something and opened nothing. An empty directory, a directory holding
        # no Markdown, and a scan root that has moved all land here, so none of
        # them can report a clean corpus that was never read.
        requested = " ".join(path_arguments) if path_arguments else DEFAULT_SCAN_ROOT
        refusals.append(
            Violation(
                requested,
                1,
                "matched no session file, so this run checked nothing. A run that "
                "opens no file has no evidence that anything is well-formed. Check "
                "the path, or check DEFAULT_SCAN_ROOT if this was the default scan.",
            )
        )

    return ScanTargets(tuple(paths), tuple(refusals), tuple(skipped))


def resolve_paths(path_arguments: Sequence[str], root: Path) -> list[Path]:
    """Return the session Markdown paths the checker will read."""
    return list(collect_targets(path_arguments, root).paths)


def check_targets(targets: ScanTargets, root: Path) -> list[Violation]:
    """Check every collected session file and return all violations."""
    violations: list[Violation] = list(targets.refusals)
    resolved_root = root.resolve()
    for path in targets.paths:
        # guard_path has already proved this path resolves inside the root.
        display_path = path.resolve().relative_to(resolved_root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            # An unreadable file is not a well-formed one. Letting the exception
            # escape ends the run in a traceback, which reads as the gate being
            # broken rather than as one bad file; and a UnicodeDecodeError is a
            # ValueError, so catching only OSError would still miss it. Only
            # OSError carries ``strerror``, hence the getattr.
            detail = getattr(error, "strerror", None) or str(error) or "I/O error"
            violations.append(
                Violation(
                    display_path,
                    1,
                    f"could not be read ({type(error).__name__}: {detail}), so this run "
                    "cannot say whether it is well-formed. Refusing to report it as "
                    "clean.",
                )
            )
            continue
        violations.extend(check_text(text, display_path, path.name))
    return violations


def scan_files(path_arguments: Sequence[str], root: Path = REPO_ROOT) -> list[Violation]:
    """Check every named session file and return all violations."""
    return check_targets(collect_targets(path_arguments, root), root)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Check curriculum sessions for their mandatory structure. "
            "With no paths, checks every session."
        )
    )
    parser.add_argument("paths", nargs="*", help="Session files or directories to check.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None, root: Path = REPO_ROOT) -> int:
    """Run the session-structure check."""
    args = parse_args(argv)
    # One traversal feeds both the verdict and the count. Counting from a
    # second walk lets the report name a number the verdict never looked at.
    targets = collect_targets(args.paths, root)
    violations = check_targets(targets, root)

    for violation in violations:
        print(violation.format_message())

    checked = len(targets.paths)
    # A skip that is recorded but never printed is still an entry the reader
    # does not know about, so the count of skips rides along with the verdict.
    passed_over = (
        f" {len(targets.skipped)} entr(ies) skipped as not Markdown."
        if targets.skipped
        else ""
    )
    if violations:
        print(
            f"\nSession structure: {checked} file(s) checked, "
            f"{len(violations)} problem(s).{passed_over}"
        )
        return 1

    print(f"Session structure: {checked} file(s) checked, all well-formed.{passed_over}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
